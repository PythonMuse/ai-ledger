"""Build the Article 43 workbooks -- "Does This Decision Actually Need a Large
Language Model?"

Run from anywhere:
    python generate_worksheet.py

Writes, into ./templates/:
    decision_model_pilot_worksheet.xlsx  pilot worksheet, pre-filled with 20
                                         synthetic AR collection notes, live
                                         formulas for Correct, Band, and a summary
    decision_model_pilot_worksheet.csv   the same pre-filled rows, as values
    cost_per_acceptable_decision.xlsx    four scenarios side by side, every
                                         calculated cell a visible formula

The pilot rows are read from ./data/collection_notes.csv and
./data/sample_predictions.csv, so the worksheet, the CSV, and the
score_predictions.py demo always agree.

Styling follows docs/PythonMuse_BrandSample.xlsx: Deep Navy header row with
white bold text, thin Ocean Teal borders, #EDF5F5 alternating rows, Midnight
Teal total row with Golden Yellow text, rotating brand tab colors.
All content is synthetic. Prices are illustrative, not any provider's.
"""

import csv
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

DEEP_NAVY = "002639"
MIDNIGHT_TEAL = "003144"
BRIGHT_TEAL = "3ABFB9"
GOLDEN_YELLOW = "FFD75E"
OCEAN_TEAL = "005F6F"
SOFT_SAGE = "91BE8E"
ALT_ROW = "EDF5F5"
WHITE = "FFFFFF"

HERE = Path(__file__).parent
DATA = HERE / "data"
TEMPLATES = HERE / "templates"
FOOTER = "PythonMuse LLC  |  www.pythonmuse.com"

ALLOWED = "cash_flow, pricing_dispute, purchase_order, quantity_dispute, other"
AUTO_AT, CONFIRM_AT = 0.90, 0.60      # illustrative only

thin = Side(style="thin", color=OCEAN_TEAL)
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
HEADER_FILL = PatternFill("solid", fgColor=DEEP_NAVY)
ALT_FILL = PatternFill("solid", fgColor=ALT_ROW)
TOTAL_FILL = PatternFill("solid", fgColor=MIDNIGHT_TEAL)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="top")


# ---------------------------------------------------------------------------
# Cost per acceptable decision: inputs, and a Python mirror of the formulas
# ---------------------------------------------------------------------------
INPUT_ROWS = [
    ("volume", "Items per month", "#,##0"),
    ("in_tokens", "Input tokens per item", "#,##0"),
    ("out_tokens", "Output tokens per item", "#,##0"),
    ("in_price", "Input price per million tokens ($, illustrative)", "$#,##0.00"),
    ("out_price", "Output price per million tokens ($, illustrative)", "$#,##0.00"),
    ("auto", "Share auto-routed (no person)", "0%"),
    ("confirm", "Share a person confirms", "0%"),
    ("escalate", "Share escalated to a person", "0%"),
    ("min_confirm", "Minutes per confirmation", "0.0"),
    ("min_escalate", "Minutes per escalation", "0.0"),
    ("rate", "Reviewer cost per hour ($)", "$#,##0"),
    ("auto_error", "Error rate on auto-routed items", "0.0%"),
    ("error_cost", "Cost of one uncaught error ($)", "$#,##0"),
]

SCENARIOS = [
    {"name": "Decision model + bands", "volume": 10000, "in_tokens": 500,
     "out_tokens": 0, "in_price": 0.10, "out_price": 0.0, "auto": 0.70,
     "confirm": 0.20, "escalate": 0.10, "min_confirm": 1.0, "min_escalate": 6.0,
     "rate": 60, "auto_error": 0.01, "error_cost": 50},
    {"name": "Cheapest model, loose bands", "volume": 10000, "in_tokens": 500,
     "out_tokens": 0, "in_price": 0.05, "out_price": 0.0, "auto": 0.50,
     "confirm": 0.0, "escalate": 0.50, "min_confirm": 1.0, "min_escalate": 6.0,
     "rate": 60, "auto_error": 0.02, "error_cost": 50},
    {"name": "LLM paragraph, every item read", "volume": 10000, "in_tokens": 500,
     "out_tokens": 300, "in_price": 2.00, "out_price": 10.00, "auto": 0.0,
     "confirm": 1.0, "escalate": 0.0, "min_confirm": 1.5, "min_escalate": 6.0,
     "rate": 60, "auto_error": 0.0, "error_cost": 50},
    {"name": "All manual", "volume": 10000, "in_tokens": 0, "out_tokens": 0,
     "in_price": 0.0, "out_price": 0.0, "auto": 0.0, "confirm": 1.0,
     "escalate": 0.0, "min_confirm": 3.0, "min_escalate": 6.0, "rate": 60,
     "auto_error": 0.0, "error_cost": 50},
]


def cost_per_acceptable_decision(s):
    """Python mirror of the workbook formulas (tested in test_score_predictions.py)."""
    model = s["volume"] * (s["in_tokens"] * s["in_price"]
                           + s["out_tokens"] * s["out_price"]) / 1_000_000
    review = s["volume"] * (s["confirm"] * s["min_confirm"]
                            + s["escalate"] * s["min_escalate"]) * s["rate"] / 60
    uncaught = s["volume"] * s["auto"] * s["auto_error"]
    error_cost = uncaught * s["error_cost"]
    total = model + review + error_cost
    acceptable = s["volume"] - uncaught
    return {"model_cost": model, "review_cost": review, "uncaught": uncaught,
            "error_cost": error_cost, "total_cost": total,
            "acceptable": acceptable, "per_decision": total / acceptable}


# ---------------------------------------------------------------------------
# Shared styling helpers
# ---------------------------------------------------------------------------
def title_block(ws, title, subtitle):
    ws["A1"] = title
    ws["A1"].font = Font(name="Calibri", size=16, bold=True, color=DEEP_NAVY)
    ws["A2"] = subtitle
    ws["A2"].font = Font(name="Calibri", size=12, bold=True, color=BRIGHT_TEAL)
    ws.sheet_view.showGridLines = False


def header_row(ws, row, names_widths):
    for c, (name, width) in enumerate(names_widths, start=1):
        cell = ws.cell(row=row, column=c, value=name)
        cell.font = Font(name="Calibri", size=11, bold=True, color=WHITE)
        cell.fill = HEADER_FILL
        cell.border = BORDER
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        if width:
            ws.column_dimensions[get_column_letter(c)].width = width
    ws.row_dimensions[row].height = 32


def body_cell(ws, r, c, value, alt, bold=False, fmt=None, align=WRAP):
    cell = ws.cell(row=r, column=c, value=value)
    cell.font = Font(name="Calibri", size=11, color=DEEP_NAVY, bold=bold)
    cell.border = BORDER
    cell.alignment = align
    if alt:
        cell.fill = ALT_FILL
    if fmt:
        cell.number_format = fmt
    return cell


def footer(ws, row):
    ws.cell(row=row, column=1, value=FOOTER).font = Font(
        name="Calibri", size=10, italic=True, color=OCEAN_TEAL)


def landscape(ws):
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True


# ---------------------------------------------------------------------------
# Pilot worksheet
# ---------------------------------------------------------------------------
PILOT_COLUMNS = [
    ("Item ID", 10), ("Collection note (synthetic)", 46), ("Allowed choices", 26),
    ("Known outcome", 17), ("Model's choice", 17), ("Probability", 12),
    ("Correct (Y/N)", 10), ("Band", 15), ("Severity if wrong", 16),
    ("Could a simpler method solve it?", 28), ("Notes", 30),
]
FIRST = 5        # first data row (header on row 4)

PILOT_INSTRUCTIONS = [
    "How to run a bounded-decision pilot",
    "",
    "1. Pick ONE historical task where the possible answers are already known (old collection notes with final reason codes, AP exceptions that went to known teams).",
    "2. Write the allowed choices down BEFORE you test anything. Add an 'other' or 'cannot tell' option so the model is never forced into a wrong box.",
    "3. Use synthetic or approved data only. Nothing confidential goes into an unapproved tool.",
    "4. For each item: record the known outcome, the model's choice, and its probability (leave probability blank if the tool gave none).",
    "5. Correct and Band fill in automatically. Band cut-offs live on the 'Settings' tab. They start as placeholders: set them from your own results.",
    "6. For every wrong answer, record how bad it would have been: annoying (wrong queue, a person catches it), costly (delay, rework), or control failure (cleared with no review).",
    "7. Ask, for every row: could a written rule, an LLM, or a person have done this better? Some items never needed a model.",
    "8. Do not let the model take action during the pilot. You are measuring, not automating.",
    "",
    "The 'AR Pilot Example' tab is filled in with 20 synthetic notes. Item AR-011 contains a planted instruction and is the one high-confidence error. It is there on purpose.",
    "The 'Summary' tab counts accuracy by band from the example. The 'Your Pilot' tab is blank and ready to use.",
    "",
    "Companion to the PythonMuse LLC article 'Does This Decision Actually Need a Large Language Model?' Synthetic example data only.",
    "Educational purposes only; not professional advice.",
]


def load_pilot_rows():
    with open(DATA / "collection_notes.csv", newline="", encoding="utf-8") as f:
        notes = {r["item_id"]: r for r in csv.DictReader(f)}
    with open(DATA / "sample_predictions.csv", newline="", encoding="utf-8") as f:
        preds = list(csv.DictReader(f))
    rows = []
    for p in preds:
        n = notes[p["item_id"]]
        prob = float(p["probability"]) if p["probability"].strip() else None
        rows.append({"item_id": p["item_id"], "note": n["note"],
                     "known": n["known_outcome"], "choice": p["model_choice"],
                     "probability": prob, "severity": p["error_severity"],
                     "alternative": n["simpler_alternative"]})
    return rows


def band_value(prob):
    if prob is None:
        return "no probability"
    if prob >= AUTO_AT:
        return "auto-route"
    return "confirm" if prob >= CONFIRM_AT else "escalate"


def pilot_table(ws, rows, blank_rows=0):
    header_row(ws, FIRST - 1, PILOT_COLUMNS)
    all_rows = rows + [None] * blank_rows
    last = FIRST + len(all_rows) - 1
    for i, item in enumerate(all_rows):
        r = FIRST + i
        alt = i % 2 == 1
        vals = ([item["item_id"], item["note"], ALLOWED, item["known"], item["choice"],
                 item["probability"]] if item else
                [None, None, ALLOWED, None, None, None])
        for c, v in enumerate(vals, start=1):
            body_cell(ws, r, c, v, alt, fmt="0%" if c == 6 else None,
                      align=CENTER if c in (1, 6) else WRAP)
        body_cell(ws, r, 7, f'=IF(E{r}="","",IF(D{r}=E{r},"Y","N"))', alt,
                  bold=True, align=CENTER)
        body_cell(ws, r, 8,
                  f'=IF(E{r}="","",IF(F{r}="","no probability",'
                  f'IF(F{r}>=Settings!$B$5,"auto-route",'
                  f'IF(F{r}>=Settings!$B$6,"confirm","escalate"))))', alt)
        body_cell(ws, r, 9, item["severity"] if item else None, alt)
        body_cell(ws, r, 10, item["alternative"] if item else None, alt)
        body_cell(ws, r, 11, None, alt)
        ws.row_dimensions[r].height = 48 if item else 30

    for col, formula in (("D", "known"), ("E", "choice")):
        dv = DataValidation(type="list",
                            formula1='"cash_flow,pricing_dispute,purchase_order,quantity_dispute,other"',
                            allow_blank=True)
        dv.add(f"{col}{FIRST}:{col}{last}")
        ws.add_data_validation(dv)
    dv_sev = DataValidation(type="list", formula1='"annoying,costly,control failure"',
                            allow_blank=True)
    dv_sev.add(f"I{FIRST}:I{last}")
    ws.add_data_validation(dv_sev)

    ws.freeze_panes = ws.cell(row=FIRST, column=3)
    ws.auto_filter.ref = f"A{FIRST - 1}:{get_column_letter(len(PILOT_COLUMNS))}{last}"
    footer(ws, last + 2)
    landscape(ws)
    return last


def build_pilot(out_dir):
    rows = load_pilot_rows()
    wb = Workbook()

    ws = wb.active
    ws.title = "Instructions"
    ws.sheet_properties.tabColor = BRIGHT_TEAL
    title_block(ws, "Decision Model Pilot Worksheet",
                "Test one bounded decision against answers you already know")
    ws.column_dimensions["A"].width = 130
    for i, line in enumerate(PILOT_INSTRUCTIONS, start=4):
        cell = ws.cell(row=i, column=1, value=line)
        heading = i == 4
        cell.font = Font(name="Calibri", size=12 if heading else 11, bold=heading,
                         color=OCEAN_TEAL if heading else DEEP_NAVY)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    footer(ws, 4 + len(PILOT_INSTRUCTIONS) + 1)

    st = wb.create_sheet("Settings")
    st.sheet_properties.tabColor = SOFT_SAGE
    title_block(st, "Band Cut-offs", "Placeholders. Set them from your own labeled results.")
    header_row(st, 4, [("Setting", 40), ("Value", 12), ("Why", 70)])
    for i, (name, val, why) in enumerate([
        ("Auto-route at or above", AUTO_AT,
         "Illustrative. Raise it until the auto-route band holds no errors you can't live with."),
        ("Confirm at or above (escalate below)", CONFIRM_AT,
         "Illustrative. Below this, a person or a stronger method takes the item."),
    ]):
        r = 5 + i
        body_cell(st, r, 1, name, i % 2 == 1)
        body_cell(st, r, 2, val, i % 2 == 1, bold=True, fmt="0%", align=CENTER)
        body_cell(st, r, 3, why, i % 2 == 1)
    footer(st, 8)

    ex = wb.create_sheet("AR Pilot Example")
    ex.sheet_properties.tabColor = GOLDEN_YELLOW
    title_block(ex, "Example: AR Collection-Note Reason Codes",
                "20 synthetic notes. Allowed choices defined first; the model's answers checked against known outcomes.")
    last = pilot_table(ex, rows)

    sm = wb.create_sheet("Summary")
    sm.sheet_properties.tabColor = OCEAN_TEAL
    title_block(sm, "Summary: Accuracy by Band", "Live formulas over the 'AR Pilot Example' tab")
    header_row(sm, 4, [("Band", 22), ("Items", 10), ("Correct", 10), ("Accuracy", 12)])
    src = "'AR Pilot Example'"
    rng_band = f"{src}!$H${FIRST}:$H${last}"
    rng_ok = f"{src}!$G${FIRST}:$G${last}"
    for i, band in enumerate(["auto-route", "confirm", "escalate", "no probability"]):
        r = 5 + i
        body_cell(sm, r, 1, band, i % 2 == 1)
        body_cell(sm, r, 2, f'=COUNTIF({rng_band},A{r})', i % 2 == 1, align=CENTER)
        body_cell(sm, r, 3, f'=COUNTIFS({rng_band},A{r},{rng_ok},"Y")', i % 2 == 1,
                  align=CENTER)
        body_cell(sm, r, 4, f'=IF(B{r}=0,"",C{r}/B{r})', i % 2 == 1, fmt="0.0%",
                  align=CENTER)
    for c, v in enumerate(["Total", "=SUM(B5:B8)", "=SUM(C5:C8)",
                           '=IF(B9=0,"",C9/B9)'], start=1):
        cell = sm.cell(row=9, column=c, value=v)
        cell.font = Font(name="Calibri", size=11, bold=True, color=GOLDEN_YELLOW)
        cell.fill = TOTAL_FILL
        cell.border = BORDER
        cell.alignment = CENTER if c > 1 else WRAP
        if c == 4:
            cell.number_format = "0.0%"
    sm.cell(row=11, column=1,
            value="Look hardest at any 'N' in the auto-route band: nobody would have reviewed it.").font = Font(
        name="Calibri", size=11, italic=True, color=OCEAN_TEAL)
    footer(sm, 13)

    yours = wb.create_sheet("Your Pilot")
    yours.sheet_properties.tabColor = BRIGHT_TEAL
    title_block(yours, "Your Pilot: [name the decision]",
                "Define the allowed choices first. One row per historical item.")
    pilot_table(yours, [], blank_rows=25)

    wb.save(out_dir / "decision_model_pilot_worksheet.xlsx")

    with open(out_dir / "decision_model_pilot_worksheet.csv", "w", newline="",
              encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([name for name, _ in PILOT_COLUMNS])
        for item in rows:
            w.writerow([item["item_id"], item["note"], ALLOWED, item["known"],
                        item["choice"],
                        "" if item["probability"] is None else f"{item['probability']:.2f}",
                        "Y" if item["known"] == item["choice"] else "N",
                        band_value(item["probability"]), item["severity"],
                        item["alternative"], ""])


# ---------------------------------------------------------------------------
# Cost per acceptable decision workbook
# ---------------------------------------------------------------------------
CALC_ROWS = [
    ("Model cost ($)", "={c}5*({c}6*{c}8+{c}7*{c}9)/1000000", "$#,##0.00"),
    ("Review cost ($)", "={c}5*({c}11*{c}13+{c}12*{c}14)*{c}15/60", "$#,##0.00"),
    ("Uncaught errors (items)", "={c}5*{c}10*{c}16", "#,##0"),
    ("Cost of uncaught errors ($)", "={c}22*{c}17", "$#,##0.00"),
    ("Total cost ($)", "={c}20+{c}21+{c}23", "$#,##0.00"),
    ("Acceptable decisions (items)", "={c}5-{c}22", "#,##0"),
    ("Shares add to 100%?", '=IF(ROUND({c}10+{c}11+{c}12,6)=1,"OK","Fix shares")', None),
]

COST_NOTES = [
    "How to read this",
    "",
    "Cost per acceptable decision = (model cost + review cost + cost of uncaught errors) / decisions that ended up right.",
    "An item a person confirms or escalates is assumed to end up right; only auto-routed errors slip through.",
    "Every number in the yellow-headed input block is a placeholder. Replace it with your own volumes, minutes, rates, and error costs.",
    "Prices are illustrative, not any provider's list price. See the article's technical appendix for dated provider prices.",
    "Notice which line moves the answer. In this example it is almost never the model price.",
    "",
    "Educational purposes only; not professional advice. Synthetic numbers.",
]


def build_cost(out_dir):
    wb = Workbook()
    ws = wb.active
    ws.title = "Compare"
    ws.sheet_properties.tabColor = GOLDEN_YELLOW
    title_block(ws, "Cost per Acceptable Decision",
                "The cheapest model is not automatically the cheapest process")
    header_row(ws, 4, [("Inputs", 48)] + [(s["name"], 22) for s in SCENARIOS])
    for i, (key, label, fmt) in enumerate(INPUT_ROWS):
        r = 5 + i
        body_cell(ws, r, 1, label, i % 2 == 1)
        for j, s in enumerate(SCENARIOS):
            body_cell(ws, r, 2 + j, s[key], i % 2 == 1, fmt=fmt, align=CENTER)

    header_row(ws, 19, [("Calculated (formulas)", None)] + [(s["name"], None) for s in SCENARIOS])
    for i, (label, formula, fmt) in enumerate(CALC_ROWS):
        r = 20 + i
        target = 27 if label.startswith("Shares") else r
        body_cell(ws, target, 1, label, i % 2 == 1)
        for j in range(len(SCENARIOS)):
            col = get_column_letter(2 + j)
            body_cell(ws, target, 2 + j, formula.format(c=col), i % 2 == 1, fmt=fmt,
                      align=CENTER)

    # The answer row, styled as the total row.
    for c in range(1, 2 + len(SCENARIOS)):
        col = get_column_letter(c)
        value = "Cost per acceptable decision ($)" if c == 1 else f"={col}24/{col}25"
        cell = ws.cell(row=26, column=c, value=value)
        cell.font = Font(name="Calibri", size=12, bold=True, color=GOLDEN_YELLOW)
        cell.fill = TOTAL_FILL
        cell.border = BORDER
        cell.alignment = CENTER if c > 1 else WRAP
        if c > 1:
            cell.number_format = "$#,##0.00"

    for i, line in enumerate(COST_NOTES, start=29):
        cell = ws.cell(row=i, column=1, value=line)
        heading = i == 29
        cell.font = Font(name="Calibri", size=12 if heading else 11, bold=heading,
                         color=OCEAN_TEAL if heading else DEEP_NAVY)
    footer(ws, 29 + len(COST_NOTES) + 1)
    ws.freeze_panes = "B5"
    landscape(ws)
    wb.save(out_dir / "cost_per_acceptable_decision.xlsx")


def build(out_dir=TEMPLATES):
    out_dir = Path(out_dir)
    out_dir.mkdir(exist_ok=True)
    build_pilot(out_dir)
    build_cost(out_dir)


if __name__ == "__main__":
    build()
    for s in SCENARIOS:
        r = cost_per_acceptable_decision(s)
        print(f"{s['name']:<34} total ${r['total_cost']:>10,.2f}  "
              f"per acceptable decision ${r['per_decision']:.2f}")
    print("Wrote templates/decision_model_pilot_worksheet.xlsx and .csv, "
          "and templates/cost_per_acceptable_decision.xlsx")
