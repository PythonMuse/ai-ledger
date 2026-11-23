"""Generate branded visuals for Article 47 -- Your AI Workflow Is Running.
Who Is Watching It? (a PythonMuse Lab).

Run from anywhere:
    python generate_visuals.py

Article visuals (./visuals/) are built at true slide size (13.333 x 7.5 in)
with scripts/slide_kit.py, so the point size set here is the point size when
the image is dropped on a PowerPoint slide: 24pt body, 26pt+ headings, nothing
under 22pt. Each drawing function is written once and used twice: framed
(header bar + footer) for the article, and header-less (./visuals/slides/) as
an optional slide variant. Two square social cards are exported at exactly
1080 x 1080 px; they are a separate format and not size-checked.

Rules: .claude/skills/pythonmuse-slide-visuals/SKILL.md. save_slide() raises
if any text is under 22pt or runs off the edge. On top of that, every label
placed inside a box is registered with fit() and checked against that box
before saving, because save_slide() cannot see text spilling out of a card.

Code licensed under MIT; see LICENSE-CODE.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from slide_kit import (  # noqa: E402
    FRAME_CONTENT_BOTTOM, FRAME_CONTENT_TOP, SLIDE_TARGET_PT, blank_slide,
    framed_slide, save_slide)

DEEP_NAVY     = "#002639"
MIDNIGHT_TEAL = "#003144"
BRIGHT_TEAL   = "#3ABFB9"
GOLDEN_YELLOW = "#FFD75E"
WARM_GLOW     = "#F5D384"
OCEAN_TEAL    = "#005F6F"
SOFT_SAGE     = "#91BE8E"
SEA_GREEN     = "#2BA19A"
WHITE         = "#FFFFFF"
ALERT_RED     = "#E05252"
ALERT_ORANGE  = "#E07D3B"

LIGHT_GRAY = "#F5F5F5"
TEAL_TINT = "#EDF5F5"

plt.rcParams["font.family"] = "sans-serif"

FOOTER = "PythonMuse LLC  |  www.pythonmuse.com"
OUT = Path(__file__).parent / "visuals"
SLIDES_OUT = OUT / "slides"

HEAD_PT = 28      # card headings and focal words
BODY_PT = SLIDE_TARGET_PT
BOX_PAD = 0.002

# Slide variants use (almost) the whole canvas.
SLIDE_TOP, SLIDE_BOTTOM = 0.94, 0.06


# ---------------------------------------------------------------------------
# Containment check: text registered with fit() must stay inside its box.
# ---------------------------------------------------------------------------
_FITS = []


def fit(t, x0, x1, y0, y1):
    """Register text object t as belonging inside the box (figure fractions)."""
    _FITS.append((t, x0, x1, y0, y1))
    return t


def check_fits(fig):
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    inv = fig.transFigure.inverted()
    problems = []
    for t, x0, x1, y0, y1 in _FITS:
        if t.figure is not fig:
            continue
        bb = inv.transform_bbox(t.get_window_extent(r))
        if (bb.x0 < x0 + 0.008 or bb.x1 > x1 - 0.008
                or bb.y0 < y0 + 0.004 or bb.y1 > y1 - 0.004):
            problems.append(f"spills out of its box: '{t.get_text()[:40]}'")
    _FITS.clear()
    if problems:
        plt.close(fig)
        raise ValueError("Layout check failed:\n  - " + "\n  - ".join(problems))


def save(fig, path):
    check_fits(fig)
    save_slide(fig, str(path))


# ---------------------------------------------------------------------------
# Shared drawing helpers (all coordinates are 0-1 figure fractions)
# ---------------------------------------------------------------------------
def box(ax, x, y, w, h, fill, zorder=2, rounding=0.02):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad={BOX_PAD},rounding_size={rounding}",
        facecolor=fill, edgecolor="none", zorder=zorder))


def arrow(ax, start, end, color=SEA_GREEN, lw=6):
    ax.annotate("", xy=end, xytext=start,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                mutation_scale=40, shrinkA=0, shrinkB=0),
                zorder=5)


def label(ax, x, y, s, bounds, size=BODY_PT, color=DEEP_NAVY, weight="normal",
          ha="center", va="center", **kw):
    t = ax.text(x, y, s, fontsize=size, color=color, fontweight=weight,
                ha=ha, va=va, zorder=6, **kw)
    return fit(t, *bounds)


def band(ax, text, y, h, fill=GOLDEN_YELLOW, color=DEEP_NAVY, size=HEAD_PT):
    box(ax, 0.03, y, 0.94, h, fill)
    label(ax, 0.5, y + h / 2, text, (0.03, 0.97, y, y + h), size=size,
          color=color, weight="bold")


def split_area(top, bottom, band_frac=0.17, gap=0.03):
    """(band_y, band_h, content_y, content_h) with a takeaway band at the
    bottom of the content area."""
    band_h = (top - bottom) * band_frac
    cy = bottom + band_h + gap
    return bottom, band_h, cy, top - cy


def make_pair(draw, name, title, subtitle):
    """Article version (framed) and slide version (header-less)."""
    fig, ax = framed_slide(title, subtitle, FOOTER)
    draw(ax, FRAME_CONTENT_TOP, FRAME_CONTENT_BOTTOM)
    save(fig, OUT / f"47_{name}.png")
    fig, ax = blank_slide()
    draw(ax, SLIDE_TOP, SLIDE_BOTTOM)
    save(fig, SLIDES_OUT / f"47_{name}_slide.png")


def card_list(ax, x, y, w, h, fill, head, head_col, items, body_col,
              head_size=HEAD_PT):
    """A card with a heading and a short list, evenly spaced."""
    box(ax, x, y, w, h, fill)
    bounds = (x, x + w, y, y + h)
    label(ax, x + 0.025, y + h - 0.075, head, bounds, size=head_size,
          color=head_col, weight="bold", ha="left")
    area_top, area_bottom = y + h - 0.15, y + 0.03
    n = len(items)
    step = min((area_top - area_bottom - 0.06) / max(n - 1, 1), 0.12)
    mid = (area_top + area_bottom) / 2
    first = mid + step * (n - 1) / 2
    for k, item in enumerate(items):
        label(ax, x + 0.03, first - k * step, "•  " + item, bounds,
              color=body_col, ha="left")


# ---------------------------------------------------------------------------
# 1. Hero: "Completed successfully." and the four questions it can't answer
# ---------------------------------------------------------------------------
QUESTIONS = [
    ("What did it\nprocess?", TEAL_TINT, DEEP_NAVY),
    ("What went\nwrong?", TEAL_TINT, DEEP_NAVY),
    ("Who\nreviewed it?", TEAL_TINT, DEEP_NAVY),
    ("Where's the\nevidence?", GOLDEN_YELLOW, DEEP_NAVY),
]


def draw_hero(ax, top, bottom):
    span = top - bottom
    bh = span * 0.30
    by = top - bh
    box(ax, 0.17, by, 0.66, bh, SOFT_SAGE)
    label(ax, 0.5, by + bh / 2, "✓  Completed successfully.",
          (0.17, 0.83, by, by + bh), size=36, color=DEEP_NAVY, weight="bold")
    gap = 0.02
    w = (0.94 - 3 * gap) / 4
    ch = span * 0.42
    cy = bottom + span * 0.02
    for k, (q, fill, col) in enumerate(QUESTIONS):
        x = 0.03 + k * (w + gap)
        box(ax, x, cy, w, ch, fill)
        label(ax, x + w / 2, cy + ch / 2, q, (x, x + w, cy, cy + ch),
              size=26, color=col, weight="bold", linespacing=1.25)
        # A dotted "question" link from the banner to each card.
        ax.plot([0.5, x + w / 2], [by - 0.01, cy + ch + 0.012],
                color=OCEAN_TEAL, lw=3, ls=(0, (2, 3)), zorder=1)


# ---------------------------------------------------------------------------
# 2. Logs, metrics, traces, each with its accounting twin
# ---------------------------------------------------------------------------
SIGNALS = [
    ("Log", "Records an event", "ERP activity\nhistory", TEAL_TINT,
     OCEAN_TEAL, DEEP_NAVY),
    ("Metric", "Measures a result", "A KPI or\nexception rate", DEEP_NAVY,
     WARM_GLOW, WHITE),
    ("Trace", "Follows one run", "A transaction\nwalk-through", TEAL_TINT,
     OCEAN_TEAL, DEEP_NAVY),
]


def draw_logs_metrics_traces(ax, top, bottom):
    by, bh, cy, ch = split_area(top, bottom, band_frac=0.17)
    gap = 0.02
    w = (0.94 - 2 * gap) / 3
    for k, (name, does, like, fill, head_col, body_col) in enumerate(SIGNALS):
        x = 0.03 + k * (w + gap)
        box(ax, x, cy, w, ch, fill)
        b = (x, x + w, cy, cy + ch)
        label(ax, x + w / 2, cy + ch * 0.85, name, b, size=32, color=head_col,
              weight="bold")
        label(ax, x + w / 2, cy + ch * 0.66, does, b, color=body_col)
        label(ax, x + w / 2, cy + ch * 0.45, "In accounting:", b,
              color=head_col, weight="bold")
        label(ax, x + w / 2, cy + ch * 0.22, like, b, color=body_col,
              linespacing=1.2)
    band(ax, "Recording is not monitoring.", by, bh)


# ---------------------------------------------------------------------------
# 3. Git records the version; telemetry records the run
# ---------------------------------------------------------------------------
def draw_git_vs_telemetry(ax, top, bottom):
    by, bh, cy, ch = split_area(top, bottom, band_frac=0.17)
    w = 0.42
    lx, rx = 0.03, 0.97 - w
    # Left: Git
    box(ax, lx, cy, w, ch, LIGHT_GRAY)
    lb = (lx, lx + w, cy, cy + ch)
    label(ax, lx + 0.025, cy + ch * 0.85, "Git: the version", lb, size=HEAD_PT,
          color=OCEAN_TEAL, weight="bold", ha="left")
    label(ax, lx + 0.03, cy + ch * 0.58, "Was: within \\$1 = matched", lb,
          ha="left")
    label(ax, lx + 0.03, cy + ch * 0.36, "Now: exact match only", lb,
          ha="left", weight="bold")
    label(ax, lx + 0.03, cy + ch * 0.14, "(an approved change?)", lb,
          ha="left", color=OCEAN_TEAL, style="italic")
    # Right: telemetry
    box(ax, rx, cy, w, ch, DEEP_NAVY)
    rb = (rx, rx + w, cy, cy + ch)
    label(ax, rx + 0.025, cy + ch * 0.85, "Telemetry: the run", rb,
          size=HEAD_PT, color=WARM_GLOW, weight="bold", ha="left")
    label(ax, rx + w / 2, cy + ch * 0.47, "12  →  45", rb, size=54,
          color=GOLDEN_YELLOW, weight="bold")
    label(ax, rx + w / 2, cy + ch * 0.18, "unmatched items", rb, color=WHITE)
    mid = cy + ch / 2
    arrow(ax, (lx + w + 0.015, mid), (rx - 0.015, mid), lw=7)
    band(ax, "Git explains the change. Telemetry shows the effect.", by, bh,
         fill=DEEP_NAVY, color=WARM_GLOW, size=26)


# ---------------------------------------------------------------------------
# 4. Three layers of evidence
# ---------------------------------------------------------------------------
LAYERS = [
    ("Change control", "What was supposed to run",
     "Git, approved instructions, access", OCEAN_TEAL, WHITE),
    ("Execution", "What actually ran",
     "Logs, traces, errors, retries", SEA_GREEN, WHITE),
    ("Accounting\ncontrol", "Whether the controls operated",
     "Tie-outs, exceptions, sign-off", GOLDEN_YELLOW, DEEP_NAVY),
]


def draw_three_layers(ax, top, bottom):
    by, bh, cy, ch = split_area(top, bottom, band_frac=0.16)
    gap = 0.02
    rh = (ch - 2 * gap) / 3
    chip_w = 0.27
    for k, (name, what, src, chip_fill, chip_col) in enumerate(LAYERS):
        y = cy + ch - (k + 1) * rh - k * gap
        box(ax, 0.03, y, chip_w, rh, chip_fill)
        label(ax, 0.03 + chip_w / 2, y + rh / 2, name,
              (0.03, 0.03 + chip_w, y, y + rh), size=26, color=chip_col,
              weight="bold", linespacing=1.1)
        rx = 0.03 + chip_w + 0.015
        box(ax, rx, y, 0.97 - rx, rh, TEAL_TINT)
        rb = (rx, 0.97, y, y + rh)
        label(ax, rx + 0.025, y + rh * 0.68, what, rb, size=26,
              weight="bold", ha="left")
        label(ax, rx + 0.025, y + rh * 0.28, src, rb, color=OCEAN_TEAL,
              ha="left")
    band(ax, "You need all three, tied together by a run ID.", by, bh,
         fill=DEEP_NAVY, color=WARM_GLOW, size=26)


# ---------------------------------------------------------------------------
# 5. Anatomy of a monitoring control
# ---------------------------------------------------------------------------
PARTS = [["Owner", "Expectation", "Threshold"],
         ["Review", "Escalation", "Evidence"]]


def draw_monitoring_control(ax, top, bottom):
    by, bh, cy, ch = split_area(top, bottom, band_frac=0.17)
    lw_ = 0.28
    box(ax, 0.03, cy, lw_, ch, LIGHT_GRAY)
    lb = (0.03, 0.03 + lw_, cy, cy + ch)
    label(ax, 0.03 + lw_ / 2, cy + ch * 0.80, "A metric", lb, size=HEAD_PT,
          color=OCEAN_TEAL, weight="bold")
    label(ax, 0.03 + lw_ / 2, cy + ch * 0.50, "100", lb, size=54,
          color=DEEP_NAVY, weight="bold")
    label(ax, 0.03 + lw_ / 2, cy + ch * 0.22, "exceptions today\n(usually 10)",
          lb, linespacing=1.2)
    rx = 0.03 + lw_ + 0.08
    rw = 0.97 - rx
    arrow(ax, (0.03 + lw_ + 0.012, cy + ch / 2), (rx - 0.012, cy + ch / 2),
          lw=7)
    box(ax, rx, cy, rw, ch, DEEP_NAVY)
    rb = (rx, rx + rw, cy, cy + ch)
    label(ax, rx + 0.03, cy + ch * 0.85, "A control adds", rb, size=HEAD_PT,
          color=WARM_GLOW, weight="bold", ha="left")
    col_w = (rw - 0.06) / 2
    # Two columns, three rows: Owner / Review, Expectation / Escalation, ...
    for i, name in enumerate(PARTS[0] + PARTS[1]):
        col = 0 if i < 3 else 1
        row = i % 3
        label(ax, rx + 0.04 + col * col_w, cy + ch * (0.62 - row * 0.22),
              "•  " + name, rb, size=28, color=WHITE, ha="left")
    band(ax, "A metric becomes a control when someone owns it.", by, bh)


# ---------------------------------------------------------------------------
# 6. Where does the monitoring data go?
# ---------------------------------------------------------------------------
def draw_where_data_goes(ax, top, bottom):
    span = top - bottom
    gap = 0.03
    th = span * 0.36
    ty = top - th
    # Top row: workflow -> monitoring service
    ww = 0.30
    box(ax, 0.03, ty, ww, th, LIGHT_GRAY)
    label(ax, 0.03 + ww / 2, ty + th / 2, "Your AI\nworkflow",
          (0.03, 0.03 + ww, ty, ty + th), size=HEAD_PT, weight="bold",
          linespacing=1.15)
    mx = 0.03 + ww + 0.14
    mw = 0.97 - mx
    box(ax, mx, ty, mw, th, GOLDEN_YELLOW)
    mb = (mx, 0.97, ty, ty + th)
    label(ax, mx + mw / 2, ty + th * 0.66, "Monitoring service", mb,
          size=HEAD_PT, weight="bold")
    label(ax, mx + mw / 2, ty + th * 0.30, "Its own access and retention", mb)
    arrow(ax, (0.03 + ww + 0.012, ty + th / 2), (mx - 0.012, ty + th / 2),
          lw=7)
    label(ax, (0.03 + ww + mx) / 2, ty + th / 2 + 0.07, "telemetry",
          (0.03 + ww, mx, ty, ty + th), color=OCEAN_TEAL, style="italic",
          size=22)
    # Bottom row: what to send
    bh = ty - gap - (bottom + span * 0.02)
    by = bottom + span * 0.02
    w = (0.94 - 0.02) / 2
    box(ax, 0.03, by, w, bh, TEAL_TINT)
    b1 = (0.03, 0.03 + w, by, by + bh)
    label(ax, 0.06, by + bh * 0.74, "Usually enough", b1,
          size=HEAD_PT, color=OCEAN_TEAL, weight="bold", ha="left")
    label(ax, 0.06, by + bh * 0.36, "Metadata: counts," + NL + "status, IDs, timing",
          b1, ha="left", linespacing=1.3)
    x2 = 0.03 + w + 0.02
    box(ax, x2, by, w, bh, DEEP_NAVY)
    b2 = (x2, x2 + w, by, by + bh)
    label(ax, x2 + 0.03, by + bh * 0.74, "Off unless needed", b2,
          size=HEAD_PT, color=WARM_GLOW, weight="bold", ha="left")
    label(ax, x2 + 0.03, by + bh * 0.36,
          "Full content: prompts," + NL + "responses, documents", b2, color=WHITE,
          ha="left", linespacing=1.3)


# ---------------------------------------------------------------------------
# Social cards (1080 x 1080): a separate format, not size-checked
# ---------------------------------------------------------------------------
NL = "\n"


def social_footer(fig, y, size=20):
    fig.text(0.5, y, FOOTER, fontsize=size, color=OCEAN_TEAL, ha="center",
             va="center", alpha=0.80)


def blank_axes(figsize):
    fig, ax = plt.subplots(figsize=figsize, facecolor=WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_position([0, 0, 1, 1])
    return fig, ax


def save_square(fig, name, inches=13):
    """Exact 1080 x 1080 px, so no tight bbox (it would trim)."""
    check_fits(fig)
    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / name, dpi=1080 / inches, facecolor=fig.get_facecolor())
    plt.close(fig)


def social_header(fig, title, subtitle, header_h=0.300, title_size=56):
    fig.patches.append(FancyBboxPatch(
        (0, 1 - header_h), 1, header_h, boxstyle="square,pad=0",
        transform=fig.transFigure, facecolor=DEEP_NAVY, edgecolor="none",
        zorder=0))
    fig.text(0.06, 1 - header_h * 0.42, title, fontsize=title_size,
             fontweight="bold", color=WHITE, va="center", ha="left",
             linespacing=1.1)
    fig.text(0.06, 1 - header_h * 0.86, subtitle, fontsize=26,
             color=WARM_GLOW, va="center", ha="left")


def make_social_quote():
    fig, ax = blank_axes((13, 13))
    box(ax, 0.05, 0.110, 0.90, 0.840, DEEP_NAVY, rounding=0.03)
    box(ax, 0.40, 0.855, 0.20, 0.012, GOLDEN_YELLOW, zorder=4,
        rounding=0.004)
    label(ax, 0.5, 0.560, "\"Completed\nsuccessfully\"\nis the workflow's\n"
          "opinion of itself.", (0.05, 0.95, 0.32, 0.80), size=58,
          color=WHITE, weight="bold", linespacing=1.2)
    label(ax, 0.5, 0.215, "Monitoring is how someone\nchecks the claim.",
          (0.05, 0.95, 0.12, 0.31), size=34, color=WARM_GLOW,
          style="italic", linespacing=1.25)
    social_footer(fig, y=0.060)
    save_square(fig, "47_social_quote.png")


SOCIAL_LAYERS = [
    ("Change control", "What was supposed to run", OCEAN_TEAL, WHITE),
    ("Execution", "What actually ran", SEA_GREEN, WHITE),
    ("Accounting control", "Whether the controls operated", GOLDEN_YELLOW,
     DEEP_NAVY),
]


def make_social_layers():
    fig, ax = blank_axes((13, 13))
    social_header(fig, "Who is watching" + NL + "your AI workflow?",
                  "Three layers of evidence")
    top, h, gap = 0.655, 0.150, 0.025
    for k, (name, what, fill, col) in enumerate(SOCIAL_LAYERS):
        y = top - (k + 1) * h - k * gap
        box(ax, 0.06, y, 0.88, h, fill)
        b = (0.06, 0.94, y, y + h)
        label(ax, 0.10, y + h * 0.68, name, b, size=38, color=col,
              weight="bold", ha="left")
        label(ax, 0.10, y + h * 0.30, what, b, size=30, color=col, ha="left")
    ax.text(0.5, 0.090, "A successful run is a claim, not evidence.",
            fontsize=30, style="italic", color=OCEAN_TEAL, ha="center",
            va="center")
    social_footer(fig, y=0.030)
    save_square(fig, "47_social_layers.png")


if __name__ == "__main__":
    make_pair(draw_hero, "hero", "Completed Successfully. Now What?",
              "The workflow's opinion of itself is not evidence.")
    make_pair(draw_logs_metrics_traces, "logs_metrics_traces",
              "Logs, Metrics, and Traces", "Each one has an accounting twin.")
    make_pair(draw_git_vs_telemetry, "git_vs_telemetry",
              "Git Records the Version, Not the Run",
              "Same rule change, two different records.")
    make_pair(draw_three_layers, "three_layers", "Three Layers of Evidence",
              "Intended, executed, and controlled.")
    make_pair(draw_monitoring_control, "monitoring_control",
              "Anatomy of a Monitoring Control",
              "Collecting a number is not the same as acting on it.")
    make_pair(draw_where_data_goes, "where_data_goes",
              "Where Does the Monitoring Data Go?",
              "The monitoring tool is part of the data trail.")
    make_social_quote()
    make_social_layers()
    print("Generated 6 article visuals, 6 slide variants, and 2 social cards "
          "for Article 47.")
