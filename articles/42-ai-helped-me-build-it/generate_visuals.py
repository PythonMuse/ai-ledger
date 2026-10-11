"""Generate branded visuals for Article 42 -- AI Helped Me Build It. AI Does
Not Have to Run It.

Run from anywhere:
    python generate_visuals.py

Article visuals (./visuals/) are built at true slide size (13.333 x 7.5 in)
with scripts/slide_kit.py, so the point size set here is the point size when
the image is dropped on a PowerPoint slide: 24pt body, 32pt+ headings, nothing
under 22pt. Each drawing function is written once and used twice: framed (header
bar + footer) for the article, and header-less (./visuals/slides/) as an
optional slide variant. Two extra slide-only visuals cover the control
questions and the rule of thumb. Three square social cards are exported at
exactly 1080 x 1080 px; they are a separate format and not size-checked.

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


def card(ax, x, y, w, h, fill, head, lines, head_col, body_col,
         head_size=HEAD_PT, head_off=0.085, first_off=0.200, step=0.140,
         bold_last=False):
    """Heading near the top of a filled card, body lines beneath it. Offsets
    are measured down from the card's top edge, in figure fractions."""
    box(ax, x, y, w, h, fill)
    pad = 0.025
    ax.text(x + pad, y + h - head_off, head, fontsize=head_size,
            fontweight="bold", color=head_col, ha="left", va="center",
            zorder=4)
    for i, line in enumerate(lines):
        last = bold_last and i == len(lines) - 1
        ax.text(x + pad, y + h - first_off - i * step, line,
                fontsize=BODY_PT, fontweight="bold" if last else "normal",
                color=body_col, ha="left", va="center", zorder=4)


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
# 1. Hero: build time vs. run time
# ---------------------------------------------------------------------------
def draw_hero(ax, top, bottom):
    by, bh, cy, ch = split_area(top, bottom)
    lx, rx, w = 0.03, 0.60, 0.37
    card(ax, lx, cy, w, ch, LIGHT_GRAY, "BUILD TIME",
         ["AI explains the steps", "Drafts the script", "Tests on mock data"],
         OCEAN_TEAL, DEEP_NAVY)
    card(ax, rx, cy, w, ch, DEEP_NAVY, "RUN TIME",
         ["Same approved rules", "Data stays put", "You review exceptions"],
         WARM_GLOW, WHITE)
    mid = (lx + w + rx) / 2
    ay = cy + ch * 0.42
    arrow(ax, (lx + w + 0.015, ay), (rx - 0.015, ay))
    ax.text(mid, ay + 0.105, "Tested.\nApproved.", fontsize=BODY_PT,
            fontweight="bold", color=DEEP_NAVY, ha="center", va="center",
            linespacing=1.2)
    band(ax, "Then the model goes home.", by, bh, size=36)


def make_hero():
    fig, ax = framed_slide(
        "Build Time vs. Run Time",
        "AI helps build it once. The approved script runs it.", FOOTER)
    draw_hero(ax, FRAME_CONTENT_TOP, FRAME_CONTENT_BOTTOM)
    save_slide(fig, str(OUT / "42_hero.png"))


def make_hero_slide():
    fig, ax = blank_slide()
    draw_hero(ax, SLIDE_TOP, SLIDE_BOTTOM)
    save_slide(fig, str(SLIDES_OUT / "42_hero_slide.png"))


# ---------------------------------------------------------------------------
# 2. Asking the chatbot every month vs. building it once
# ---------------------------------------------------------------------------
def draw_chatbot_vs_build(ax, top, bottom):
    by, bh, cy, ch = split_area(top, bottom)
    w = 0.455
    card(ax, 0.03, cy, w, ch, LIGHT_GRAY, "ASK THE CHATBOT",
         ["Data goes to the model", "The approach may shift",
          "Evidence: a transcript"], OCEAN_TEAL, DEEP_NAVY)
    card(ax, 0.515, cy, w, ch, DEEP_NAVY, "BUILD IT ONCE",
         ["Mock data at build time", "Same rules every run",
          "Evidence: run log, report"], WARM_GLOW, WHITE)
    band(ax, "Same task. Different evidence.", by, bh)


def make_chatbot_vs_build():
    fig, ax = framed_slide(
        "Ask the Chatbot, or Build It Once",
        "Same task. Very different evidence for the reviewer.", FOOTER)
    draw_chatbot_vs_build(ax, FRAME_CONTENT_TOP, FRAME_CONTENT_BOTTOM)
    save_slide(fig, str(OUT / "42_chatbot_vs_build.png"))


def make_chatbot_vs_build_slide():
    fig, ax = blank_slide()
    draw_chatbot_vs_build(ax, SLIDE_TOP, SLIDE_BOTTOM)
    save_slide(fig, str(SLIDES_OUT / "42_chatbot_vs_build_slide.png"))


# ---------------------------------------------------------------------------
# 3. Four kinds of work
# ---------------------------------------------------------------------------
KINDS = [
    ("RULES", "Can we write the rule?", "Excel, SQL, Python",
     DEEP_NAVY, WARM_GLOW, WHITE),
    ("PATTERNS", "History holds a pattern?", "Machine learning",
     OCEAN_TEAL, WARM_GLOW, WHITE),
    ("LANGUAGE", "Must it read text?", "An LLM, validated",
     BRIGHT_TEAL, DEEP_NAVY, DEEP_NAVY),
    ("JUDGMENT", "Needs accountability?", "A qualified person",
     GOLDEN_YELLOW, DEEP_NAVY, DEEP_NAVY),
]


def draw_four_kinds(ax, top, bottom):
    by, bh, cy, ch = split_area(top, bottom, band_frac=0.16)
    gap = 0.03
    w, h = 0.455, (ch - gap) / 2
    for idx, (name, question, tool, fill, head_col, body_col) in enumerate(KINDS):
        r, c = divmod(idx, 2)
        x = 0.03 + c * 0.485
        y = cy + ch - (r + 1) * h - r * gap
        card(ax, x, y, w, h, fill, name, [question, tool], head_col,
             body_col, head_off=0.068, first_off=0.150, step=0.075,
             bold_last=True)
    band(ax, "AI helps build all four. Judgment stays human.", by, bh,
         size=30)


def make_four_kinds():
    fig, ax = framed_slide(
        "Four Kinds of Work in Every Process",
        "Classify each step, not the whole process.", FOOTER)
    draw_four_kinds(ax, FRAME_CONTENT_TOP, FRAME_CONTENT_BOTTOM)
    save_slide(fig, str(OUT / "42_four_kinds_of_work.png"))


def make_four_kinds_slide():
    fig, ax = blank_slide()
    draw_four_kinds(ax, SLIDE_TOP, SLIDE_BOTTOM)
    save_slide(fig, str(SLIDES_OUT / "42_four_kinds_slide.png"))


# ---------------------------------------------------------------------------
# 4. Decision tree: the four "choose an approach" questions
#    (the two control questions are their own slide)
# ---------------------------------------------------------------------------
TREE = [
    ("Necessary and understood?", "If not: redesign first.", LIGHT_GRAY,
     OCEAN_TEAL, DEEP_NAVY),
    ("Can we write the rule?", "Deterministic automation.", DEEP_NAVY,
     WARM_GLOW, WHITE),
    ("Language to interpret?", "Consider an LLM. Validate it.", OCEAN_TEAL,
     WARM_GLOW, WHITE),
    ("Pattern, but no rule?", "Consider machine learning.", BRIGHT_TEAL,
     DEEP_NAVY, DEEP_NAVY),
]


def draw_decision_tree(ax, top, bottom):
    by, bh, cy, ch = split_area(top, bottom)
    gap = 0.02
    n = len(TREE)
    h = (ch - gap * (n - 1)) / n
    for i, (q, a, fill, qcol, acol) in enumerate(TREE):
        y = cy + ch - (i + 1) * h - i * gap
        box(ax, 0.03, y, 0.94, h, fill)
        ax.text(0.060, y + h / 2, f"{i + 1}.  {q}", fontsize=BODY_PT,
                color=qcol, ha="left", va="center", zorder=4)
        ax.text(0.510, y + h / 2, a, fontsize=BODY_PT, fontweight="bold",
                color=acol, ha="left", va="center", zorder=4)
    band(ax, "Every option: a person stays accountable.", by, bh, size=30)


def make_decision_tree():
    fig, ax = framed_slide(
        "A Decision Tree for Each Step",
        "Ask it of every step, not the whole process.", FOOTER)
    draw_decision_tree(ax, FRAME_CONTENT_TOP, FRAME_CONTENT_BOTTOM)
    save_slide(fig, str(OUT / "42_decision_tree.png"))


def make_decision_tree_slide():
    fig, ax = blank_slide()
    draw_decision_tree(ax, SLIDE_TOP, SLIDE_BOTTOM)
    save_slide(fig, str(SLIDES_OUT / "42_decision_tree_slide.png"))


# ---------------------------------------------------------------------------
# 5. Variance workflow: script, LLM, accountant
# ---------------------------------------------------------------------------
LANES = [
    ("SCRIPT", ["Calculates the", "27 percent"], DEEP_NAVY, WARM_GLOW, WHITE),
    ("LLM", ["Suggests", "questions", "(if permitted)"], BRIGHT_TEAL,
     DEEP_NAVY, DEEP_NAVY),
    ("ACCOUNTANT", ["Finds, supports,", "and owns the", "explanation"],
     GOLDEN_YELLOW, DEEP_NAVY, DEEP_NAVY),
]


def draw_swimlane(ax, top, bottom):
    by, bh, cy, ch = split_area(top, bottom)
    w, gap = 0.292, 0.032
    for i, (name, lines, fill, head_col, body_col) in enumerate(LANES):
        x = 0.03 + i * (w + gap)
        card(ax, x, cy, w, ch, fill, name, lines, head_col, body_col,
             head_size=30, step=0.115)
        if i < len(LANES) - 1:
            arrow(ax, (x + w + 0.002, cy + ch / 2),
                  (x + w + gap - 0.002, cy + ch / 2))
    band(ax, "Python calculates. AI suggests. You decide.", by, bh, size=30)


def make_variance_swimlane():
    fig, ax = framed_slide(
        "Variance Analysis, Step by Step",
        "Three kinds of work, three owners.", FOOTER)
    draw_swimlane(ax, FRAME_CONTENT_TOP, FRAME_CONTENT_BOTTOM)
    save_slide(fig, str(OUT / "42_variance_swimlane.png"))


def make_swimlane_slide():
    fig, ax = blank_slide()
    draw_swimlane(ax, SLIDE_TOP, SLIDE_BOTTOM)
    save_slide(fig, str(SLIDES_OUT / "42_variance_swimlane_slide.png"))


# ---------------------------------------------------------------------------
# 6. Control, or polite request?
# ---------------------------------------------------------------------------
def draw_control_or_request(ax, top, bottom):
    by, bh, cy, ch = split_area(top, bottom)
    w = 0.455
    panel_h = 0.185
    for x, fill, head, head_col, sub, sub_col, code, code_fill, foot, foot_col in [
        (0.03, LIGHT_GRAY, "POLITE REQUEST", OCEAN_TEAL,
         "Written in the agent file", DEEP_NAVY,
         "Do not touch the\npayroll folder.", MIDNIGHT_TEAL,
         "The model is asked.", DEEP_NAVY),
        (0.515, DEEP_NAVY, "CONTROL", WARM_GLOW,
         "Claude Code settings.json", WHITE,
         "deny:\nRead(./payroll/**)", MIDNIGHT_TEAL,
         "The harness blocks it.", WHITE),
    ]:
        box(ax, x, cy, w, ch, fill)
        ax.text(x + 0.025, cy + ch - 0.075, head, fontsize=HEAD_PT,
                fontweight="bold", color=head_col, ha="left", va="center",
                zorder=4)
        ax.text(x + 0.025, cy + ch - 0.155, sub, fontsize=BODY_PT,
                color=sub_col, ha="left", va="center", zorder=4)
        py = cy + ch - 0.215 - panel_h
        box(ax, x + 0.025, py, w - 0.050, panel_h, code_fill, zorder=3)
        ax.text(x + 0.050, py + panel_h / 2, code, fontsize=BODY_PT,
                family="monospace", color=WHITE, ha="left", va="center",
                linespacing=1.4, zorder=4)
        ax.text(x + 0.025, cy + 0.060, foot, fontsize=28, fontweight="bold",
                color=foot_col, ha="left", va="center", zorder=4)
    band(ax, "Know which is which.", by, bh)


def make_control_or_request():
    fig, ax = framed_slide(
        "Control, or Polite Request?",
        "A sentence asks. A harness setting enforces.", FOOTER)
    draw_control_or_request(ax, FRAME_CONTENT_TOP, FRAME_CONTENT_BOTTOM)
    save_slide(fig, str(OUT / "42_control_or_request.png"))


def make_control_or_request_slide():
    fig, ax = blank_slide()
    draw_control_or_request(ax, SLIDE_TOP, SLIDE_BOTTOM)
    save_slide(fig, str(SLIDES_OUT / "42_control_or_request_slide.png"))


# ---------------------------------------------------------------------------
# Slide-only extras
# ---------------------------------------------------------------------------
def make_control_questions_slide():
    """Questions 5 and 6 of the per-step tree: they apply to every option."""
    fig, ax = blank_slide()
    ax.text(0.03, 0.915, "Then, for every option:", fontsize=HEAD_PT,
            fontweight="bold", color=DEEP_NAVY, ha="left", va="center")
    card(ax, 0.03, 0.470, 0.94, 0.360, DEEP_NAVY,
         "5.  Judgment, approval, or limits?",
         ["A qualified person stays responsible,",
          "whatever technology prepared the work."],
         WARM_GLOW, WHITE)
    card(ax, 0.03, 0.070, 0.94, 0.360, OCEAN_TEAL,
         "6.  What evidence shows it worked?",
         ["Define validation, logging, exceptions,",
          "and sign-off before you build."],
         WARM_GLOW, WHITE)
    save_slide(fig, str(SLIDES_OUT / "42_control_questions_slide.png"))


def make_rule_of_thumb_slide():
    """One-slide takeaway: the framework in four rows."""
    fig, ax = blank_slide()
    rows = [
        ("Rule is known?", "Encode the rule.", DEEP_NAVY, WARM_GLOW, WHITE),
        ("Language to read?", "LLM, then validate it.", OCEAN_TEAL, WARM_GLOW,
         WHITE),
        ("Pattern, no rule?", "Machine learning may fit.", BRIGHT_TEAL,
         DEEP_NAVY, DEEP_NAVY),
        ("Needs accountability?", "Keep a person responsible.", GOLDEN_YELLOW,
         DEEP_NAVY, DEEP_NAVY),
    ]
    h, gap, top = 0.190, 0.030, 0.940
    for i, (q, a, fill, qcol, acol) in enumerate(rows):
        y = top - i * (h + gap) - h
        box(ax, 0.03, y, 0.94, h, fill)
        ax.text(0.060, y + h / 2, q, fontsize=BODY_PT, color=qcol,
                ha="left", va="center", zorder=4)
        ax.text(0.400, y + h / 2, a, fontsize=28, fontweight="bold",
                color=acol, ha="left", va="center", zorder=4)
    save_slide(fig, str(SLIDES_OUT / "42_rule_of_thumb_slide.png"))


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


def social_box(ax, xy, w, h, fill, edge=None, lw=0, zorder=2, rounding=0.02):
    ax.add_patch(FancyBboxPatch(
        xy, w, h, boxstyle=f"round,pad={BOX_PAD},rounding_size={rounding}",
        facecolor=fill, edgecolor=edge or "none", linewidth=lw, zorder=zorder))


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
    fig, ax = blank_axes((13, 13))
    social_header(fig, "AI helped build it.\nAI does not have to run it.",
                  "Build time vs. run time, for accounting workflows")
    rows = [
        ("BUILD TIME", "AI explains, drafts, and tests\nwith mock data. Once.", LIGHT_GRAY),
        ("RUN TIME", "The approved script runs.\nEvery month. Same rules.", DEEP_NAVY),
    ]
    top, h, gap = 0.650, 0.205, 0.035
    for i, (label, text, fill) in enumerate(rows):
        y = top - i * (h + gap) - h
        edge = OCEAN_TEAL if fill == LIGHT_GRAY else None
        social_box(ax, (0.06, y), 0.88, h, fill, edge=edge, lw=2.5, rounding=0.02)
        dark = fill == LIGHT_GRAY
        ax.text(0.10, y + h - 0.050, label, fontsize=30, fontweight="bold",
                color=OCEAN_TEAL if dark else WARM_GLOW, ha="left",
                va="center", zorder=4)
        ax.text(0.10, y + 0.075, text, fontsize=33,
                color=DEEP_NAVY if dark else WHITE, ha="left", va="center",
                linespacing=1.2, zorder=4)
    social_box(ax, (0.06, 0.085), 0.88, 0.090, GOLDEN_YELLOW)
    ax.text(0.5, 0.130, "Then the model goes home.", fontsize=36,
            fontweight="bold", color=DEEP_NAVY, ha="center", va="center",
            zorder=4)
    social_footer(fig, y=0.040)
    save_square(fig, "42_social_square.png")


def make_social_rule_of_thumb():
    fig, ax = blank_axes((13, 13))
    social_header(fig, "The Rule of Thumb",
                  "Which method belongs in each step?", header_h=0.220,
                  title_size=60)
    rules = [
        ("Rule is known?", "Encode the rule.", DEEP_NAVY),
        ("Language to interpret?", "Consider an LLM. Validate it.", SEA_GREEN),
        ("Pattern you can't write?", "Machine learning may fit.", OCEAN_TEAL),
        ("Needs accountability?", "Keep a person responsible.", GOLDEN_YELLOW),
    ]
    top, h, gap = 0.745, 0.142, 0.022
    for i, (q, a, fill) in enumerate(rules):
        y = top - i * (h + gap) - h
        social_box(ax, (0.06, y), 0.88, h, fill, rounding=0.02)
        dark = fill == GOLDEN_YELLOW
        ax.text(0.095, y + h * 0.68, q, fontsize=29, fontweight="bold",
                color=DEEP_NAVY if dark else WARM_GLOW, ha="left",
                va="center", zorder=4)
        ax.text(0.095, y + h * 0.30, a, fontsize=33, fontweight="bold",
                color=DEEP_NAVY if dark else WHITE, ha="left", va="center",
                zorder=4)
    social_footer(fig, y=0.040)
    save_square(fig, "42_social_rule_of_thumb.png")


def make_social_wrong_rule():
    fig, ax = blank_axes((13, 13))
    social_box(ax, (0.05, 0.110), 0.90, 0.840, DEEP_NAVY, rounding=0.03)
    ax.text(0.130, 0.835, "“", fontsize=170, color=GOLDEN_YELLOW,
            ha="center", va="center", fontweight="bold", zorder=4)
    ax.text(0.5, 0.590,
            "A script can apply\nthe wrong rule\nperfectly.",
            fontsize=58, fontweight="bold", color=WHITE, ha="center",
            va="center", linespacing=1.2, zorder=4)
    ax.text(0.5, 0.370, "Every month. Forever.", fontsize=44,
            fontweight="bold", color=GOLDEN_YELLOW, ha="center",
            va="center", zorder=4)
    ax.text(0.5, 0.230,
            "Deterministic does not mean correct.\nTest it with data built to break it.",
            fontsize=28, color=WARM_GLOW, style="italic", ha="center",
            va="center", linespacing=1.3, zorder=4)
    social_footer(fig, y=0.060)
    save_square(fig, "42_social_wrong_rule.png")


if __name__ == "__main__":
    # Article visuals (framed, slide size).
    make_hero()
    make_chatbot_vs_build()
    make_four_kinds()
    make_decision_tree()
    make_variance_swimlane()
    make_control_or_request()
    # Optional header-less slide variants, plus two slide-only extras.
    make_hero_slide()
    make_chatbot_vs_build_slide()
    make_four_kinds_slide()
    make_decision_tree_slide()
    make_swimlane_slide()
    make_control_or_request_slide()
    make_control_questions_slide()
    make_rule_of_thumb_slide()
    # Social cards.
    make_social_square()
    make_social_rule_of_thumb()
    make_social_wrong_rule()
    print("Generated 6 article visuals, 8 slide variants, and 3 social cards "
          "for Article 42.")
