"""Generate branded visuals for Article 43 -- Does This Decision Actually Need
a Large Language Model?

Run from anywhere:
    python generate_visuals.py

Article visuals (./visuals/) are built at true slide size (13.333 x 7.5 in)
with scripts/slide_kit.py, so the point size set here is the point size when
the image is dropped on a PowerPoint slide: 24pt body, 32pt+ headings, nothing
under 22pt. Each drawing function is written once and used twice: framed (header
bar + footer) for the article, and header-less (./visuals/slides/) as an
optional slide variant. Three square social cards are exported at exactly
1080 x 1080 px; they are a separate format and not size-checked.

Rules: .claude/skills/pythonmuse-slide-visuals/SKILL.md. save_slide() raises
if any text is under 22pt or runs off the edge.
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

plt.rcParams["font.family"] = "sans-serif"

FOOTER = "PythonMuse LLC  |  www.pythonmuse.com"
OUT = Path(__file__).parent / "visuals"
SLIDES_OUT = OUT / "slides"

HEAD_PT = 32      # headings and focal words
BODY_PT = SLIDE_TARGET_PT
BOX_PAD = 0.002

# Slide variants use (almost) the whole canvas.
SLIDE_TOP, SLIDE_BOTTOM = 0.94, 0.06


# ---------------------------------------------------------------------------
# Shared drawing helpers (all coordinates are 0-1 figure fractions)
# ---------------------------------------------------------------------------
def box(ax, x, y, w, h, fill, zorder=2):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle=f"round,pad={BOX_PAD},rounding_size=0.02",
        facecolor=fill, edgecolor="none", zorder=zorder))


def arrow(ax, start, end, color=SEA_GREEN):
    ax.annotate("", xy=end, xytext=start,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=6,
                                mutation_scale=40, shrinkA=0, shrinkB=0),
                zorder=5)


def band(ax, text, y, h, size=HEAD_PT):
    box(ax, 0.03, y, 0.94, h, GOLDEN_YELLOW)
    ax.text(0.5, y + h / 2, text, fontsize=size, fontweight="bold",
            color=DEEP_NAVY, ha="center", va="center", zorder=4)


def split_area(top, bottom, band_frac=0.17, gap=0.03):
    """Return (band_y, band_h, content_y, content_h) for a content area with a
    gold takeaway band at its bottom."""
    band_h = (top - bottom) * band_frac
    cy = bottom + band_h + gap
    return bottom, band_h, cy, top - cy


# ---------------------------------------------------------------------------
# 1. Hero: the paragraph vs. the decision
# ---------------------------------------------------------------------------
def draw_hero(ax, top, bottom):
    by, bh, cy, ch = split_area(top, bottom)
    w = 0.455
    # Left: the paragraph nobody needed.
    box(ax, 0.03, cy, w, ch, LIGHT_GRAY)
    ax.text(0.055, cy + ch - 0.075, "THE PARAGRAPH", fontsize=HEAD_PT,
            fontweight="bold", color=OCEAN_TEAL, ha="left", va="center",
            zorder=4)
    ax.text(0.055, cy + ch * 0.42,
            "“Based on my review of\nthe correspondence, it\n"
            "appears the delay is\nprimarily related to…”",
            fontsize=BODY_PT, style="italic", color=DEEP_NAVY, ha="left",
            va="center", linespacing=1.35, zorder=4)
    # Right: the decision the workflow needed.
    rx = 0.515
    box(ax, rx, cy, w, ch, DEEP_NAVY)
    ax.text(rx + 0.025, cy + ch - 0.075, "THE DECISION", fontsize=HEAD_PT,
            fontweight="bold", color=WARM_GLOW, ha="left", va="center",
            zorder=4)
    ax.text(rx + w / 2, cy + ch * 0.50, "Missing PO", fontsize=40,
            fontweight="bold", color=WHITE, ha="center", va="center",
            zorder=4)
    ax.text(rx + w / 2, cy + ch * 0.24, "91%", fontsize=54,
            fontweight="bold", color=GOLDEN_YELLOW, ha="center",
            va="center", zorder=4)
    band(ax, "Accounting has enough paragraphs already.", by, bh, size=30)


def make_hero():
    fig, ax = framed_slide(
        "A Decision, Not a Conversation",
        "Sometimes the workflow only needs the label.", FOOTER)
    draw_hero(ax, FRAME_CONTENT_TOP, FRAME_CONTENT_BOTTOM)
    save_slide(fig, str(OUT / "43_hero.png"))


def make_hero_slide():
    fig, ax = blank_slide()
    draw_hero(ax, SLIDE_TOP, SLIDE_BOTTOM)
    save_slide(fig, str(SLIDES_OUT / "43_hero_slide.png"))


# ---------------------------------------------------------------------------
# 2. Start with the shape of the answer
# ---------------------------------------------------------------------------
SHAPES = [
    ("A known rule or match?", "Deterministic automation", DEEP_NAVY,
     WARM_GLOW, WHITE),
    ("Pick from a known list?", "Decision model", OCEAN_TEAL, WARM_GLOW,
     WHITE),
    ("Must it write or interpret?", "Large language model", BRIGHT_TEAL,
     DEEP_NAVY, DEEP_NAVY),
    ("Needs accountability?", "A qualified person", GOLDEN_YELLOW,
     DEEP_NAVY, DEEP_NAVY),
]


def draw_shape_of_answer(ax, top, bottom):
    by, bh, cy, ch = split_area(top, bottom)
    gap = 0.02
    n = len(SHAPES)
    h = (ch - gap * (n - 1)) / n
    for i, (q, a, fill, qcol, acol) in enumerate(SHAPES):
        y = cy + ch - (i + 1) * h - i * gap
        box(ax, 0.03, y, 0.94, h, fill)
        ax.text(0.060, y + h / 2, q, fontsize=BODY_PT, color=qcol,
                ha="left", va="center", zorder=4)
        ax.text(0.470, y + h / 2, a, fontsize=28, fontweight="bold",
                color=acol, ha="left", va="center", zorder=4)
    band(ax, "Match the method to the work.", by, bh)


def make_shape_of_answer():
    fig, ax = framed_slide(
        "Start With the Shape of the Answer",
        "Look at the output the step needs. Then pick the method.", FOOTER)
    draw_shape_of_answer(ax, FRAME_CONTENT_TOP, FRAME_CONTENT_BOTTOM)
    save_slide(fig, str(OUT / "43_shape_of_answer.png"))


def make_shape_of_answer_slide():
    fig, ax = blank_slide()
    draw_shape_of_answer(ax, SLIDE_TOP, SLIDE_BOTTOM)
    save_slide(fig, str(SLIDES_OUT / "43_shape_of_answer_slide.png"))


# ---------------------------------------------------------------------------
# 3. Confidence bands: a probability needs a plan
# ---------------------------------------------------------------------------
BANDS = [
    ("Incorrect PO   96%", "AUTO-ROUTE", "to the PO queue", DEEP_NAVY,
     WARM_GLOW, WHITE),
    ("Pricing dispute   78%", "CONFIRM", "a person clicks yes", OCEAN_TEAL,
     WARM_GLOW, WHITE),
    ("PO 47%  Pricing 42%  Other 11%", "ESCALATE", "a person decides",
     GOLDEN_YELLOW, DEEP_NAVY, DEEP_NAVY),
]


def draw_confidence_bands(ax, top, bottom):
    by, bh, cy, ch = split_area(top, bottom)
    gap = 0.03
    n = len(BANDS)
    h = (ch - gap * (n - 1)) / n
    lw, rx = 0.50, 0.60
    for i, (result, name, action, fill, head_col, body_col) in enumerate(BANDS):
        y = cy + ch - (i + 1) * h - i * gap
        box(ax, 0.03, y, lw, h, LIGHT_GRAY)
        ax.text(0.055, y + h / 2, result, fontsize=BODY_PT, fontweight="bold",
                family="monospace", color=DEEP_NAVY, ha="left", va="center",
                zorder=4)
        arrow(ax, (0.03 + lw + 0.008, y + h / 2), (rx - 0.008, y + h / 2))
        box(ax, rx, y, 0.97 - rx, h, fill)
        ax.text(rx + 0.025, y + h * 0.68, name, fontsize=28, fontweight="bold",
                color=head_col, ha="left", va="center", zorder=4)
        ax.text(rx + 0.025, y + h * 0.30, action, fontsize=BODY_PT,
                color=body_col, ha="left", va="center", zorder=4)
    band(ax, "Set the thresholds from your own data.", by, bh, size=30)


def make_confidence_bands():
    fig, ax = framed_slide(
        "A Probability Needs a Plan",
        "Decide what each confidence level is allowed to do.", FOOTER)
    draw_confidence_bands(ax, FRAME_CONTENT_TOP, FRAME_CONTENT_BOTTOM)
    save_slide(fig, str(OUT / "43_confidence_bands.png"))


def make_confidence_bands_slide():
    fig, ax = blank_slide()
    draw_confidence_bands(ax, SLIDE_TOP, SLIDE_BOTTOM)
    save_slide(fig, str(SLIDES_OUT / "43_confidence_bands_slide.png"))


# ---------------------------------------------------------------------------
# 4. Layered workflow: an AP funnel
# ---------------------------------------------------------------------------
LAYERS = [
    ("RULES", "clear most invoices", 0.94, DEEP_NAVY, WARM_GLOW, WHITE),
    ("DECISION MODEL", "routes the exceptions", 0.80, OCEAN_TEAL, WARM_GLOW,
     WHITE),
    ("LLM", "reads the long threads", 0.66, BRIGHT_TEAL, DEEP_NAVY,
     DEEP_NAVY),
    ("A PERSON", "approves", 0.52, GOLDEN_YELLOW, DEEP_NAVY, DEEP_NAVY),
]


def draw_layered_workflow(ax, top, bottom):
    by, bh, cy, ch = split_area(top, bottom)
    gap = 0.02
    n = len(LAYERS)
    h = (ch - gap * (n - 1)) / n
    for i, (name, what, w, fill, head_col, body_col) in enumerate(LAYERS):
        y = cy + ch - (i + 1) * h - i * gap
        x = 0.5 - w / 2
        box(ax, x, y, w, h, fill)
        ax.text(x + 0.03, y + h / 2, name, fontsize=28, fontweight="bold",
                color=head_col, ha="left", va="center", zorder=4)
        ax.text(x + w - 0.03, y + h / 2, what, fontsize=BODY_PT,
                color=body_col, ha="right", va="center", zorder=4)
    band(ax, "Not an “LLM workflow.” A controlled one.", by, bh,
         size=30)


def make_layered_workflow():
    fig, ax = framed_slide(
        "One Workflow, Several Methods",
        "Accounts payable: each layer does what it is built for.", FOOTER)
    draw_layered_workflow(ax, FRAME_CONTENT_TOP, FRAME_CONTENT_BOTTOM)
    save_slide(fig, str(OUT / "43_layered_workflow.png"))


def make_layered_workflow_slide():
    fig, ax = blank_slide()
    draw_layered_workflow(ax, SLIDE_TOP, SLIDE_BOTTOM)
    save_slide(fig, str(SLIDES_OUT / "43_layered_workflow_slide.png"))


# ---------------------------------------------------------------------------
# Social cards (1080 x 1080): a separate format, not size-checked
# ---------------------------------------------------------------------------
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


def social_box(ax, xy, w, h, fill, rounding=0.02, zorder=2):
    ax.add_patch(FancyBboxPatch(
        xy, w, h, boxstyle=f"round,pad={BOX_PAD},rounding_size={rounding}",
        facecolor=fill, edgecolor="none", zorder=zorder))


def save_square(fig, name, inches=13):
    """Exact 1080 x 1080 px, so no tight bbox (it would trim)."""
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
    """Square hero: the paragraph vs. the decision."""
    fig, ax = blank_axes((13, 13))
    social_header(fig, "Does this decision\nneed an LLM?",
                  "Sometimes the workflow only needs the label.")
    social_box(ax, (0.06, 0.445), 0.88, 0.215, LIGHT_GRAY)
    ax.text(0.10, 0.615, "THE PARAGRAPH", fontsize=28, fontweight="bold",
            color=OCEAN_TEAL, ha="left", va="center", zorder=4)
    ax.text(0.10, 0.515,
            "“Based on my review of the correspondence,\n"
            "it appears the delay is primarily related to…”",
            fontsize=27, style="italic", color=DEEP_NAVY, ha="left",
            va="center", linespacing=1.3, zorder=4)
    social_box(ax, (0.06, 0.205), 0.88, 0.205, DEEP_NAVY)
    ax.text(0.10, 0.365, "THE DECISION", fontsize=28, fontweight="bold",
            color=WARM_GLOW, ha="left", va="center", zorder=4)
    ax.text(0.10, 0.268, "Missing PO", fontsize=52, fontweight="bold",
            color=WHITE, ha="left", va="center", zorder=4)
    ax.text(0.90, 0.268, "91%", fontsize=60, fontweight="bold",
            color=GOLDEN_YELLOW, ha="right", va="center", zorder=4)
    social_box(ax, (0.06, 0.085), 0.88, 0.090, GOLDEN_YELLOW)
    ax.text(0.5, 0.130, "A decision, not a conversation.", fontsize=36,
            fontweight="bold", color=DEEP_NAVY, ha="center", va="center",
            zorder=4)
    social_footer(fig, y=0.040)
    save_square(fig, "43_social_square.png")


def make_social_paragraphs():
    """Quote card."""
    fig, ax = blank_axes((13, 13))
    social_box(ax, (0.05, 0.110), 0.90, 0.840, DEEP_NAVY, rounding=0.03)
    ax.text(0.130, 0.835, "“", fontsize=170, color=GOLDEN_YELLOW,
            ha="center", va="center", fontweight="bold", zorder=4)
    ax.text(0.5, 0.590, "Accounting has\nenough paragraphs\nalready.",
            fontsize=62, fontweight="bold", color=WHITE, ha="center",
            va="center", linespacing=1.2, zorder=4)
    ax.text(0.5, 0.345, "Missing PO — 91%", fontsize=44,
            fontweight="bold", family="monospace", color=GOLDEN_YELLOW,
            ha="center", va="center", zorder=4)
    ax.text(0.5, 0.215,
            "When the next step only needs a label,\nthe essay is optional.",
            fontsize=28, color=WARM_GLOW, style="italic", ha="center",
            va="center", linespacing=1.3, zorder=4)
    social_footer(fig, y=0.060)
    save_square(fig, "43_social_paragraphs.png")


def make_social_cost_per_decision():
    """The four synthetic scenarios from templates/cost_per_acceptable_decision.xlsx."""
    fig, ax = blank_axes((13, 13))
    social_header(fig, "Cost per\nacceptable decision",
                  "The cheapest model is not the cheapest process.")
    rows = [
        ("Decision model + bands", "$1.16", DEEP_NAVY, WARM_GLOW, WHITE),
        ("LLM, every item read", "$1.50", OCEAN_TEAL, WARM_GLOW, WHITE),
        ("All manual", "$3.00", SEA_GREEN, WHITE, WHITE),
        ("Cheapest model,\nhalf to a person", "$3.54", GOLDEN_YELLOW,
         DEEP_NAVY, DEEP_NAVY),
    ]
    top, h, gap = 0.660, 0.118, 0.020
    for i, (label, value, fill, lcol, vcol) in enumerate(rows):
        y = top - i * (h + gap) - h
        social_box(ax, (0.06, y), 0.88, h, fill)
        ax.text(0.095, y + h / 2, label, fontsize=31, fontweight="bold",
                color=lcol, ha="left", va="center", linespacing=1.1,
                zorder=4)
        ax.text(0.905, y + h / 2, value, fontsize=44, fontweight="bold",
                color=vcol, ha="right", va="center", zorder=4)
    ax.text(0.5, 0.0835,
            "Synthetic example, 10,000 notes. Review time, not model price,\n"
            "moves the answer.",
            fontsize=22, color=OCEAN_TEAL, style="italic", ha="center",
            va="center", linespacing=1.3)
    social_footer(fig, y=0.030)
    save_square(fig, "43_social_cost_per_decision.png")


if __name__ == "__main__":
    # Article visuals (framed, slide size).
    make_hero()
    make_shape_of_answer()
    make_confidence_bands()
    make_layered_workflow()
    # Optional header-less slide variants.
    make_hero_slide()
    make_shape_of_answer_slide()
    make_confidence_bands_slide()
    make_layered_workflow_slide()
    # Social cards.
    make_social_square()
    make_social_paragraphs()
    make_social_cost_per_decision()
    print("Generated 4 article visuals, 4 slide variants, and 3 social cards "
          "for Article 43.")
