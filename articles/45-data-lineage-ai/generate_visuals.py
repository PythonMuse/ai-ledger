"""Generate branded visuals for Article 45 -- When AI Leaves the Sandbox: Why
Data Lineage Becomes an Accounting Problem.

Run from anywhere:
    python generate_visuals.py

Article visuals (./visuals/) are built at true slide size (13.333 x 7.5 in)
with scripts/slide_kit.py, so the point size set here is the point size when
the image is dropped on a PowerPoint slide: 24pt body, 26pt+ headings, nothing
under 22pt. Each drawing function is written once and used twice: framed
(header bar + footer) for the article, and header-less (./visuals/slides/) as
an optional slide variant. Three square social cards are exported at exactly
1080 x 1080 px; they are a separate format and not size-checked.

Rules: .claude/skills/pythonmuse-slide-visuals/SKILL.md. save_slide() raises
if any text is under 22pt or runs off the edge. On top of that, every label
placed inside a box is registered with fit() and checked against that box
before saving, because save_slide() cannot see text spilling out of a card.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from slide_kit import (  # noqa: E402
    FRAME_CONTENT_BOTTOM, FRAME_CONTENT_TOP, SLIDE_TARGET_PT,
    blank_slide, framed_slide, save_slide)

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
        # Require a visible inside margin left and right, not just "inside".
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


def arrow(ax, start, end, color=SEA_GREEN):
    ax.annotate("", xy=end, xytext=start,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=6,
                                mutation_scale=40, shrinkA=0, shrinkB=0),
                zorder=5)


def label(ax, x, y, s, bounds, size=BODY_PT, color=DEEP_NAVY, weight="normal",
          ha="center", va="center", **kw):
    t = ax.text(x, y, s, fontsize=size, color=color, fontweight=weight,
                ha=ha, va=va, zorder=4, **kw)
    return fit(t, *bounds)


def band(ax, text, y, h, fill=GOLDEN_YELLOW, color=DEEP_NAVY, size=HEAD_PT):
    box(ax, 0.03, y, 0.94, h, fill)
    label(ax, 0.5, y + h / 2, text, (0.03, 0.97, y, y + h), size=size,
          color=color, weight="bold")


def split_area(top, bottom, band_frac=0.16, gap=0.03):
    """(band_y, band_h, content_y, content_h) with a takeaway band at the
    bottom of the content area."""
    band_h = (top - bottom) * band_frac
    cy = bottom + band_h + gap
    return bottom, band_h, cy, top - cy


def make_pair(draw, name, title, subtitle):
    """Article version (framed) and slide version (header-less)."""
    fig, ax = framed_slide(title, subtitle, FOOTER)
    draw(ax, FRAME_CONTENT_TOP, FRAME_CONTENT_BOTTOM)
    save(fig, OUT / f"45_{name}.png")
    fig, ax = blank_slide()
    draw(ax, SLIDE_TOP, SLIDE_BOTTOM)
    save(fig, SLIDES_OUT / f"45_{name}_slide.png")


# ---------------------------------------------------------------------------
# 1. Hero: one CFO question, four versions of the truth
# ---------------------------------------------------------------------------
SYSTEMS = [
    ("ERP", "Adjustments\nafter close"),
    ("Warehouse", "Refreshed\nbefore them"),
    ("CRM", "Today's\nnames"),
    ("Spreadsheet", "Adjustments\nnot approved"),
]


def draw_hero(ax, top, bottom):
    by, bh, cy, ch = split_area(top, bottom)
    q_h = ch * 0.22
    q_y = cy + ch - q_h
    box(ax, 0.03, q_y, 0.94, q_h, DEEP_NAVY)
    label(ax, 0.5, q_y + q_h / 2,
          "“Why did gross margin fall last month?”",
          (0.03, 0.97, q_y, q_y + q_h), size=HEAD_PT, color=WHITE,
          weight="bold")
    gap = 0.02
    w = (0.94 - 3 * gap) / 4
    card_h = ch * 0.56
    for i, (name, note) in enumerate(SYSTEMS):
        x = 0.03 + i * (w + gap)
        box(ax, x, cy, w, card_h, TEAL_TINT)
        bounds = (x, x + w, cy, cy + card_h)
        label(ax, x + w / 2, cy + card_h * 0.76, name, bounds, size=26,
              color=OCEAN_TEAL, weight="bold")
        label(ax, x + w / 2, cy + card_h * 0.34, note, bounds,
              linespacing=1.2)
        arrow(ax, (x + w / 2, q_y - 0.008), (x + w / 2, cy + card_h + 0.012))
    band(ax, "Four systems. Four versions. One very patient CFO.", by, bh,
         size=26)


# ---------------------------------------------------------------------------
# 2. You already do lineage: tick-and-tie vs. a data pipeline
# ---------------------------------------------------------------------------
LANES = [
    ("WHAT YOU ALREADY TRACE",
     ["Invoice", "Journal\nentry", "General\nledger", "Financial\nstatements"],
     LIGHT_GRAY, DEEP_NAVY),
    ("WHAT DATA LINEAGE TRACES",
     ["ERP", "Extract", "Warehouse", "Dashboard"],
     DEEP_NAVY, WHITE),
]


def draw_you_already_do_lineage(ax, top, bottom):
    by, bh, cy, ch = split_area(top, bottom)
    lane_gap = 0.03
    lane_h = (ch - lane_gap) / 2
    head_h = 0.075
    agap = 0.05
    w = (0.94 - 3 * agap) / 4
    for k, (title, chips, fill, col) in enumerate(LANES):
        ly = cy + ch - (k + 1) * lane_h - k * lane_gap
        chip_h = lane_h - head_h
        label(ax, 0.03, ly + chip_h + head_h / 2, title,
              (0.0, 0.97, ly + chip_h, ly + lane_h), size=26,
              color=OCEAN_TEAL, weight="bold", ha="left")
        for i, c in enumerate(chips):
            x = 0.03 + i * (w + agap)
            box(ax, x, ly, w, chip_h, fill)
            label(ax, x + w / 2, ly + chip_h / 2, c, (x, x + w, ly, ly + chip_h),
                  color=col, weight="bold", linespacing=1.1)
            if i < 3:
                arrow(ax, (x + w + 0.008, ly + chip_h / 2),
                      (x + w + agap - 0.008, ly + chip_h / 2))
    band(ax, "Same tick-and-tie. More systems.", by, bh)


# ---------------------------------------------------------------------------
# 3. A fixed path vs. an agent's path
# ---------------------------------------------------------------------------
FIXED_RUNS = [("Run 1:", "same route"), ("Run 2:", "same route"),
              ("Run 3:", "same route")]
AGENT_RUNS = [("Run 1:", "ERP + CRM"), ("Run 2:", "Warehouse + sheet"),
              ("Run 3:", "something new")]


def draw_fixed_vs_agent_path(ax, top, bottom):
    by, bh, cy, ch = split_area(top, bottom)
    panels = [
        (0.03, 0.44, TEAL_TINT, OCEAN_TEAL, DEEP_NAVY, OCEAN_TEAL,
         "Approved report", "ERP → Warehouse → Report", FIXED_RUNS),
        (0.50, 0.47, DEEP_NAVY, WARM_GLOW, WHITE, BRIGHT_TEAL,
         "AI agent", "Picks a route per question", AGENT_RUNS),
    ]
    for x, w, fill, head_col, body_col, lead_col, head, sub, runs in panels:
        box(ax, x, cy, w, ch, fill)
        bounds = (x, x + w, cy, cy + ch)
        label(ax, x + 0.025, cy + ch - 0.065, head, bounds, size=HEAD_PT,
              color=head_col, weight="bold", ha="left")
        label(ax, x + 0.025, cy + ch - 0.145, sub, bounds, color=body_col,
              style="italic", ha="left")
        step = (ch - 0.23) / 3
        for k, (lead, rest) in enumerate(runs):
            y = cy + ch - 0.25 - k * step
            label(ax, x + 0.025, y, lead, bounds, color=lead_col,
                  weight="bold", ha="left")
            label(ax, x + 0.135, y, rest, bounds, color=body_col, ha="left")
    band(ax, "Flexible is useful. It is also harder to trace.", by, bh)


# ---------------------------------------------------------------------------
# 4. The environment ladder: four places lineage shows up
# ---------------------------------------------------------------------------
STEPS = [
    ("Spreadsheet", "You trace it\nyourself", TEAL_TINT, OCEAN_TEAL, DEEP_NAVY),
    ("Local\nworkflow", "Scripts, git,\nrun records", BRIGHT_TEAL,
     DEEP_NAVY, DEEP_NAVY),
    ("Warehouse\nand BI", "Platform\nlineage views", OCEAN_TEAL,
     WHITE, WHITE),
    ("Enterprise\nagent", "Lineage plus\nrun records", DEEP_NAVY,
     WARM_GLOW, WHITE),
]


def draw_environment_ladder(ax, top, bottom):
    by, bh, cy, ch = split_area(top, bottom)
    gap = 0.014
    w = (0.94 - 3 * gap) / 4
    heights = [0.46, 0.64, 0.82, 1.0]
    for i, (name, body, fill, head_col, body_col) in enumerate(STEPS):
        x = 0.03 + i * (w + gap)
        h = ch * heights[i]
        box(ax, x, cy, w, h, fill)
        bounds = (x, x + w, cy, cy + h)
        n_lines = name.count("\n") + 1
        name_y = cy + h - 0.02 - n_lines * 0.032
        label(ax, x + 0.016, name_y, name, bounds, size=BODY_PT, color=head_col,
              weight="bold", ha="left", linespacing=1.05)
        body_y = name_y - n_lines * 0.032 - 0.075
        label(ax, x + 0.016, body_y, body, bounds, color=body_col, ha="left",
              linespacing=1.15)
    # Upper-left: the direction of travel.
    t = ax.text(0.03, cy + ch - 0.04, "Harder to trace  →", fontsize=26,
                fontweight="bold", color=OCEAN_TEAL, ha="left", va="center",
                zorder=4)
    fit(t, 0.0, 0.03 + w + gap + w, cy + ch * 0.66, cy + ch)
    band(ax, "Same questions. Different tooling.", by, bh)


# ---------------------------------------------------------------------------
# 5. Lineage vs. execution record
# ---------------------------------------------------------------------------
def draw_lineage_vs_execution(ax, top, bottom):
    by, bh, cy, ch = split_area(top, bottom)
    cards = [
        (0.03, TEAL_TINT, OCEAN_TEAL, DEEP_NAVY, "DATA LINEAGE",
         "Where did the data\ncome from?", "Source, changes, output"),
        (0.51, DEEP_NAVY, WARM_GLOW, WHITE, "EXECUTION RECORD",
         "What did the agent\ndo on this run?", "Tools, queries, results"),
    ]
    w = 0.46
    for x, fill, head_col, body_col, head, q, detail in cards:
        box(ax, x, cy, w, ch, fill)
        bounds = (x, x + w, cy, cy + ch)
        label(ax, x + 0.03, cy + ch - 0.07, head, bounds, size=26,
              color=head_col, weight="bold", ha="left")
        label(ax, x + 0.03, cy + ch * 0.50, q, bounds, size=32,
              color=body_col, weight="bold", ha="left", linespacing=1.15)
        label(ax, x + 0.03, cy + 0.07, detail, bounds, color=body_col,
              ha="left")
    band(ax, "You need both. Neither proves the answer.", by, bh)


# ---------------------------------------------------------------------------
# 6. Five controls
# ---------------------------------------------------------------------------
CONTROLS = [
    "Name the authoritative source",
    "Document material transformations",
    "Define the business terms",
    "Keep evidence of each run",
    "Test what happens on conflict",
]


def draw_five_controls(ax, top, bottom):
    gap = 0.018
    h = (top - bottom - 4 * gap) / 5
    for k, c in enumerate(CONTROLS):
        y = top - (k + 1) * h - k * gap
        box(ax, 0.03, y, 0.94, h, LIGHT_GRAY if k % 2 else TEAL_TINT)
        bw = 0.07
        box(ax, 0.045, y + h * 0.12, bw, h * 0.76, DEEP_NAVY, zorder=3,
            rounding=0.012)
        label(ax, 0.045 + bw / 2, y + h / 2, str(k + 1),
              (0.045, 0.045 + bw, y, y + h), size=HEAD_PT,
              color=GOLDEN_YELLOW, weight="bold")
        label(ax, 0.145, y + h / 2, c, (0.03, 0.97, y, y + h), size=HEAD_PT,
              color=DEEP_NAVY, weight="bold", ha="left")


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


def make_social_square():
    fig, ax = blank_axes((13, 13))
    social_header(fig, "Before you connect" + NL + "the agent",
                  "Five controls. Then let it work.")
    top, h, gap = 0.680, 0.085, 0.015
    for k, c in enumerate(CONTROLS):
        y = top - (k + 1) * h - k * gap
        box(ax, 0.06, y, 0.88, h, LIGHT_GRAY if k % 2 else TEAL_TINT)
        ax.add_patch(FancyBboxPatch((0.09, y + h * 0.22), 0.050, h * 0.56,
                                    boxstyle="round,pad=0,rounding_size=0.008",
                                    facecolor=DEEP_NAVY, edgecolor="none",
                                    zorder=3))
        ax.text(0.115, y + h / 2, str(k + 1), fontsize=30, fontweight="bold",
                color=GOLDEN_YELLOW, ha="center", va="center", zorder=4)
        label(ax, 0.17, y + h / 2, c, (0.06, 0.94, y, y + h), size=31,
              color=DEEP_NAVY, weight="bold", ha="left")
    ax.text(0.5, 0.122, "Follow the data before" + NL + "trusting the answer.",
            fontsize=28, style="italic", color=OCEAN_TEAL, ha="center",
            va="center", linespacing=1.3)
    social_footer(fig, y=0.030)
    save_square(fig, "45_social_square.png")


def quote_card(name, lines, sub, quote_pt=60):
    fig, ax = blank_axes((13, 13))
    box(ax, 0.05, 0.110, 0.90, 0.840, DEEP_NAVY, rounding=0.03)
    ax.text(0.130, 0.835, "“", fontsize=170, color=GOLDEN_YELLOW,
            ha="center", va="center", fontweight="bold", zorder=4)
    label(ax, 0.5, 0.560, lines, (0.05, 0.95, 0.30, 0.80), size=quote_pt,
          color=WHITE, weight="bold", linespacing=1.2)
    label(ax, 0.5, 0.215, sub, (0.05, 0.95, 0.12, 0.31), size=30,
          color=WARM_GLOW, style="italic", linespacing=1.3)
    social_footer(fig, y=0.060)
    save_square(fig, name)


def make_social_quote_access():
    quote_card("45_social_quote_access.png",
               "Access is not" + NL + "understanding.",
               "Giving an agent your data is not" + NL
               + "giving it your business context.", quote_pt=70)


def make_social_quote_mcp():
    quote_card("45_social_quote_mcp.png",
               "An MCP connection" + NL + "is not a data" + NL
               + "governance" + NL + "strategy.",
               "Four systems. Four versions." + NL
               + "One very patient CFO.", quote_pt=62)


if __name__ == "__main__":
    make_pair(draw_hero, "hero", "One Question, Four Versions of the Truth",
              "Every system is right. They just disagree.")
    make_pair(draw_you_already_do_lineage, "you_already_do_lineage",
              "You Already Do Data Lineage",
              "Auditors have traced sources for decades.")
    make_pair(draw_fixed_vs_agent_path, "fixed_vs_agent_path",
              "A Fixed Path vs. an Agent's Path",
              "The route used to be approved once.")
    make_pair(draw_environment_ladder, "environment_ladder",
              "Where Data Lineage Shows Up",
              "Four places you might meet it.")
    make_pair(draw_lineage_vs_execution, "lineage_vs_execution",
              "Two Records, Two Questions",
              "Lineage and the execution record are not the same.")
    make_pair(draw_five_controls, "five_controls",
              "Five Controls Before You Connect",
              "Start with one accounting question.")
    make_social_square()
    make_social_quote_access()
    make_social_quote_mcp()
    print("Generated 6 article visuals, 6 slide variants, and 3 social cards "
          "for Article 45.")
