"""Score a decision model's predictions against known outcomes.

Companion demo for Article 43, "Does This Decision Actually Need a Large
Language Model?" (PythonMuse LLC).

It is model-agnostic. It never calls an AI provider and needs no API key. It
reads two CSV files:

  * labels       item_id, known_outcome  (the answer you already know)
  * predictions  item_id, model_choice, probability
                 (from any provider, or typed in by hand; leave probability
                 blank when the model gave no probability, for example a
                 language-model fallback)

and reports:

  1. accuracy by confidence band (auto-route / confirm / escalate /
     no probability)
  2. a confusion table: known outcome (rows) vs. the model's choice (columns)
  3. high-confidence errors: wrong answers that would have been auto-routed.
     These are the ones that matter most.

Run from the article folder:

    python score_predictions.py
    python score_predictions.py --auto 0.95 --confirm 0.70
    python score_predictions.py --labels my_labels.csv --predictions my_preds.csv

The default band cut-offs (0.90 and 0.60) are ILLUSTRATIVE ONLY. They exist so
the demo has something to show. Set your own from your own labeled results and
the cost of a wrong answer; never copy them from an article.

Standard library only. All sample data is synthetic.
"""

import argparse
import csv
import sys
from pathlib import Path

HERE = Path(__file__).parent
DEFAULT_LABELS = HERE / "data" / "collection_notes.csv"
DEFAULT_PREDICTIONS = HERE / "data" / "sample_predictions.csv"

# The allowed answers are defined BEFORE the model is tested.
ALLOWED_CHOICES = [
    "cash_flow",
    "pricing_dispute",
    "purchase_order",
    "quantity_dispute",
    "other",
]

AUTO, CONFIRM, ESCALATE, NO_PROB = "auto-route", "confirm", "escalate", "no probability"
BANDS = [AUTO, CONFIRM, ESCALATE, NO_PROB]

# Illustrative cut-offs only. See the module docstring.
DEFAULT_AUTO_AT = 0.90
DEFAULT_CONFIRM_AT = 0.60


class ScoringError(ValueError):
    """Raised when the input files can't be scored as given."""


def read_rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def band_for(probability, auto_at=DEFAULT_AUTO_AT, confirm_at=DEFAULT_CONFIRM_AT):
    """Which band a probability falls in. Lower bounds are inclusive.

    None (no probability) gets its own band: a person reviews it, because
    there is nothing to set a threshold against.
    """
    if probability is None:
        return NO_PROB
    if probability >= auto_at:
        return AUTO
    if probability >= confirm_at:
        return CONFIRM
    return ESCALATE


def parse_probability(raw, item_id):
    raw = (raw or "").strip()
    if raw == "":
        return None
    try:
        value = float(raw)
    except ValueError as exc:
        raise ScoringError(f"{item_id}: probability {raw!r} is not a number") from exc
    if not 0.0 <= value <= 1.0:
        raise ScoringError(f"{item_id}: probability {value} is outside 0 to 1")
    return value


def score(labels, predictions, auto_at=DEFAULT_AUTO_AT,
          confirm_at=DEFAULT_CONFIRM_AT, allowed=ALLOWED_CHOICES):
    """Score prediction rows against label rows. Returns a results dict."""
    if not confirm_at < auto_at:
        raise ScoringError("the confirm cut-off must be below the auto-route cut-off")

    known = {}
    for row in labels:
        item, outcome = row["item_id"].strip(), row["known_outcome"].strip()
        if outcome not in allowed:
            raise ScoringError(f"{item}: known outcome {outcome!r} is not an allowed choice")
        if item in known:
            raise ScoringError(f"{item}: appears twice in the labels")
        known[item] = outcome

    seen = set()
    items = []
    for row in predictions:
        item = row["item_id"].strip()
        if item not in known:
            raise ScoringError(f"{item}: has a prediction but no known outcome")
        if item in seen:
            raise ScoringError(f"{item}: appears twice in the predictions")
        seen.add(item)
        choice = row["model_choice"].strip()
        if choice not in allowed:
            # A bounded answer space only helps if we enforce it.
            raise ScoringError(f"{item}: model choice {choice!r} is not an allowed choice")
        probability = parse_probability(row.get("probability"), item)
        items.append({
            "item_id": item,
            "known": known[item],
            "choice": choice,
            "probability": probability,
            "band": band_for(probability, auto_at, confirm_at),
            "correct": choice == known[item],
        })

    missing = sorted(set(known) - seen)
    if missing:
        raise ScoringError(f"no prediction for: {', '.join(missing)}")

    by_band = {}
    for band in BANDS:
        rows = [i for i in items if i["band"] == band]
        right = sum(i["correct"] for i in rows)
        by_band[band] = {
            "items": len(rows),
            "correct": right,
            "accuracy": (right / len(rows)) if rows else None,
        }

    confusion = {k: {c: 0 for c in allowed} for k in allowed}
    for i in items:
        confusion[i["known"]][i["choice"]] += 1

    correct = sum(i["correct"] for i in items)
    return {
        "auto_at": auto_at,
        "confirm_at": confirm_at,
        "total": len(items),
        "correct": correct,
        "accuracy": correct / len(items) if items else None,
        "by_band": by_band,
        "confusion": confusion,
        "high_confidence_errors": [i for i in items
                                   if i["band"] == AUTO and not i["correct"]],
        "items": items,
    }


def pct(value):
    return "  n/a" if value is None else f"{value:6.1%}"


def report(results, allowed=ALLOWED_CHOICES, out=sys.stdout):
    w = out.write
    w(f"Scored {results['total']} items: {results['correct']} correct "
      f"({pct(results['accuracy']).strip()} overall)\n")
    w(f"Bands (illustrative): auto-route >= {results['auto_at']:.2f}, "
      f"confirm >= {results['confirm_at']:.2f}, escalate below that\n\n")

    w("1. Accuracy by confidence band\n")
    w(f"   {'Band':<16}{'Items':>6}{'Correct':>9}{'Accuracy':>10}\n")
    for band in BANDS:
        b = results["by_band"][band]
        w(f"   {band:<16}{b['items']:>6}{b['correct']:>9}{pct(b['accuracy']):>10}\n")

    w("\n2. Confusion table (rows: known outcome, columns: model's choice)\n")
    names = {"cash_flow": "cash", "pricing_dispute": "pricing",
             "purchase_order": "PO", "quantity_dispute": "quantity"}
    short = {c: names.get(c, c[:9]) for c in allowed}
    w("   " + f"{'':<18}" + "".join(f"{short[c]:>10}" for c in allowed) + "\n")
    for k in allowed:
        w("   " + f"{k:<18}" + "".join(f"{results['confusion'][k][c]:>10}"
                                       for c in allowed) + "\n")

    w("\n3. High-confidence errors (would have been auto-routed)\n")
    errors = results["high_confidence_errors"]
    if not errors:
        w("   None in this sample. That does not prove there are none.\n")
    for i in errors:
        w(f"   {i['item_id']}: model said {i['choice']} at {i['probability']:.0%}, "
          f"known outcome {i['known']}\n")
    return out


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--labels", default=DEFAULT_LABELS)
    p.add_argument("--predictions", default=DEFAULT_PREDICTIONS)
    p.add_argument("--auto", type=float, default=DEFAULT_AUTO_AT,
                   help="auto-route at or above this probability (illustrative)")
    p.add_argument("--confirm", type=float, default=DEFAULT_CONFIRM_AT,
                   help="confirm at or above this probability (illustrative)")
    args = p.parse_args(argv)
    try:
        results = score(read_rows(args.labels), read_rows(args.predictions),
                        auto_at=args.auto, confirm_at=args.confirm)
    except ScoringError as exc:
        print(f"Cannot score: {exc}", file=sys.stderr)
        return 1
    report(results)
    return 0


if __name__ == "__main__":
    sys.exit(main())
