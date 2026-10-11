"""Generate branded visuals for Article 41 -- If the Data Can't Leave, Bring
the Model In.

Run from the article folder:
    python generate_visuals.py

Produces, in ./visuals/:
  - four article visuals (41_hero, 41_division_of_labor, 41_cross_client,
    41_scorecard)
  - two social cards (41_social_*)
and, in ./visuals/slides/, header-less slide versions of the same ideas plus
two slide-only extras (what we measure, takeaway).

SIZE RULE (see .claude/skills/pythonmuse-slide-visuals/SKILL.md): the article
visuals are built at true slide size, 13.333 x 7.5 in (16:9), so the point sizes
below are the point sizes seen when the PNG is dropped onto a PowerPoint slide.
Body text is 24pt, nothing is under 22pt, and scripts/slide_kit.py refuses to
save an image that breaks that. Every visual shares one drawing function
between its article version and its slide version.
"""

import os
import sys

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "scripts"))
from slide_kit import (  # noqa: E402
    FRAME_CONTENT_BOTTOM, FRAME_CONTENT_TOP, SLIDE_H_IN, SLIDE_TARGET_PT,
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

LIGHT_TEAL        = "#EDF5F5"   # row backgrounds
LIGHT_TEAL_SOLID  = "#A8E0DD"   # palette "Light Teal"
PINK_TINT         = "#F6D5D5"   # failing cell

plt.rcParams["font.family"] = "sans-serif"

FOOTER = "PythonMuse LLC  |  www.pythonmuse.com"
BODY = SLIDE_TARGET_PT          # 24pt

# FancyBboxPatch inflates each box by `pad` on every side. Keep it small so the
# computed gaps survive and connector arrows stay visible.
BOX_PAD = 0.004


def inch(v):
    """Inches of slide height -> fraction of figure height."""
    return v / SLIDE_H_IN


def box(ax, xy, w, h, fill, edge=None, lw=0, zorder=2, rounding=0.012):
    ax.add_patch(FancyBboxPatch(
        xy, w, h, boxstyle=f"round,pad={BOX_PAD},rounding_size={rounding}",
        facecolor=fill, edgecolor=edge or "none", linewidth=lw, zorder=zorder))


def arrow(ax, start, end, color=OCEAN_TEAL, width=4.5, scale=30, zorder=5):
    ax.annotate("", xy=end, xytext=start,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=width,
                                mutation_scale=scale, shrinkA=0, shrinkB=0),
                zorder=zorder)


def takeaway_bar(ax, text, y, h, size=28):
    box(ax, (0.04, y), 0.92, h, GOLDEN_YELLOW)
    ax.text(0.5, y + h / 2, text, fontsize=size, fontweight="bold",
            color=DEEP_NAVY, ha="center", va="center", linespacing=1.25,
            zorder=4)


# ===========================================================================
# 1. Hero -- where does the model run?   (shared drawing)
# ===========================================================================
SPECTRUM = [
    ("Consumer app", "Free or personal chat tools", LIGHT_TEAL_SOLID, DEEP_NAVY),
    ("Enterprise plan", "ChatGPT, Gemini, Copilot", SOFT_SAGE, DEEP_NAVY),
    ("Your cloud account", "Azure OpenAI, Amazon Bedrock", BRIGHT_TEAL, DEEP_NAVY),
    ("Company hardware", "Approved workstation or server", OCEAN_TEAL, WHITE),
    ("Air-gapped", "No network connection", DEEP_NAVY, WHITE),
]


def draw_hero(ax, top, bottom, arrow_label=False):
    bar_h = 0.13
    takeaway_bar(ax, "Match where it runs to what your data allows.", bottom, bar_h)
    rows_bottom = bottom + bar_h + 0.045
    n, gap = len(SPECTRUM), 0.009
    row_h = ((top - rows_bottom) - gap * (n - 1)) / n
    x0 = 0.115 if arrow_label else 0.085
    chip_w = 0.34
    for i, (label, caption, fill, col) in enumerate(SPECTRUM):
        y = top - (i + 1) * row_h - i * gap
        box(ax, (x0, y), 0.97 - x0, row_h, LIGHT_TEAL)
        box(ax, (x0, y), chip_w, row_h, fill, zorder=3)
        ax.text(x0 + chip_w / 2, y + row_h / 2, label, fontsize=BODY,
                fontweight="bold", color=col, ha="center", va="center", zorder=4)
        ax.text(x0 + chip_w + 0.03, y + row_h / 2, caption, fontsize=BODY,
                color=DEEP_NAVY, ha="left", va="center", zorder=4)
    ax_x = x0 - 0.03
    arrow(ax, (ax_x, top - 0.012), (ax_x, rows_bottom + 0.012),
          color=SEA_GREEN, width=5, scale=34, zorder=2)
    if arrow_label:  # only the slide has the height to spare for the label
        ax.text(ax_x - 0.038, (top + rows_bottom) / 2, "CONTROL + RESPONSIBILITY",
                fontsize=BODY, fontweight="bold", color=OCEAN_TEAL, rotation=90,
                ha="center", va="center")


def make_hero():
    fig, ax = framed_slide("Where Does the Model Need to Run?",
                           "Going down the list: more control, more responsibility.",
                           FOOTER)
    draw_hero(ax, FRAME_CONTENT_TOP, FRAME_CONTENT_BOTTOM)
    save_slide(fig, "visuals/41_hero.png")


def make_hero_slide():
    fig, ax = blank_slide()
    draw_hero(ax, 0.93, 0.04, arrow_label=True)
    save_slide(fig, "visuals/slides/41_hero_slide.png")


# ===========================================================================
# 2. Division of labor -- retrieve, calculate, judge
# ===========================================================================
ROLES = [
    ("AI CO-PILOT", "Retrieves\nand cites",
     ["Finds the inputs", "Cites sources", "Admits gaps"], BRIGHT_TEAL, DEEP_NAVY),
    ("EXCEL / PYTHON", "Calculates",
     ["Runs the models", "Waterfall math", "Repeatable"], OCEAN_TEAL, WHITE),
    ("SPECIALIST", "Judges",
     ["Sets the pass bar", "Reviews evidence", "Owns the call"], DEEP_NAVY, WHITE),
]


def draw_division(ax, top, bottom):
    bar_h = 0.115
    takeaway_bar(ax, "Excel stays. It finally gets a co-pilot.", bottom, bar_h)
    yb = bottom + bar_h + 0.04
    h = top - yb
    n, gap = len(ROLES), 0.035
    w = (0.92 - gap * (n - 1)) / n
    for i, (who, verb, bullets, fill, col) in enumerate(ROLES):
        x = 0.04 + i * (w + gap)
        box(ax, (x, yb), w, h, fill, rounding=0.015)
        ax.text(x + w / 2, yb + h - inch(0.40), who, fontsize=BODY,
                fontweight="bold", color=col, ha="center", va="center", zorder=4)
        ax.text(x + w / 2, yb + h - inch(1.25), verb, fontsize=32,
                fontweight="bold", color=col, ha="center", va="center",
                linespacing=1.05, zorder=4)
        inset_top, inset_bot = yb + h - inch(1.95), yb + inch(0.20)
        inset_h = inset_top - inset_bot
        box(ax, (x + 0.018, inset_bot), w - 0.036, inset_h, WHITE, zorder=3)
        for j, b in enumerate(bullets):
            by = inset_top - (j + 0.5) * inset_h / len(bullets)
            ax.text(x + 0.034, by, b, fontsize=BODY, color=DEEP_NAVY,
                    ha="left", va="center", zorder=4)
        if i < n - 1:
            arrow(ax, (x + w + 0.006, yb + h / 2),
                  (x + w + gap - 0.006, yb + h / 2), color=SEA_GREEN)


def make_division_of_labor():
    fig, ax = framed_slide("Let Excel Keep Doing the Math",
                           "A cleaner split of responsibilities for valuation work.",
                           FOOTER)
    draw_division(ax, FRAME_CONTENT_TOP, FRAME_CONTENT_BOTTOM)
    save_slide(fig, "visuals/41_division_of_labor.png")


def make_division_slide():
    fig, ax = blank_slide()
    draw_division(ax, 0.955, 0.04)
    save_slide(fig, "visuals/slides/41_division_slide.png")


# ===========================================================================
# 3. Cross-client retrieval -- the check happens before the model
# ===========================================================================
def draw_cross_client(ax, top, bottom):
    bar_h = 0.13
    takeaway_bar(ax, "A polite prompt is not an access control.", bottom, bar_h)
    rows_bottom = bottom + bar_h + 0.05
    row_gap = 0.04
    rh = ((top - rows_bottom) - row_gap) / 2
    bw, gap, x0 = 0.245, 0.040, 0.125
    rows = [
        (top - rh, "✗", ALERT_RED, [
            ("Analyst asks\nfor similar deals", LIGHT_TEAL_SOLID, DEEP_NAVY),
            ("Model searches\nevery client", MIDNIGHT_TEAL, WHITE),
            ("A different\nclient's deal", ALERT_RED, WHITE)]),
        (top - 2 * rh - row_gap, "✓", SEA_GREEN, [
            ("Analyst asks\nfor similar deals", LIGHT_TEAL_SOLID, DEEP_NAVY),
            ("Filter checks\npermissions", BRIGHT_TEAL, DEEP_NAVY),
            ("Model sees only\nthis client", SOFT_SAGE, DEEP_NAVY)]),
    ]
    for y, mark, chip, steps in rows:
        box(ax, (0.04, y), 0.065, rh, chip)
        ax.text(0.0725, y + rh / 2, mark, fontsize=40, fontweight="bold",
                color=WHITE, ha="center", va="center", zorder=4)
        for i, (label, fill, col) in enumerate(steps):
            x = x0 + i * (bw + gap)
            box(ax, (x, y), bw, rh, fill, rounding=0.015)
            ax.text(x + bw / 2, y + rh / 2, label, fontsize=BODY,
                    fontweight="bold", color=col, ha="center", va="center",
                    linespacing=1.2, zorder=4)
            if i < 2:
                arrow(ax, (x + bw + 0.004, y + rh / 2),
                      (x + bw + gap - 0.004, y + rh / 2), color=chip)


def make_cross_client():
    fig, ax = framed_slide("A Prompt Is Not an Access Control",
                           "The permission check must happen before the model.",
                           FOOTER)
    draw_cross_client(ax, FRAME_CONTENT_TOP, FRAME_CONTENT_BOTTOM)
    save_slide(fig, "visuals/41_cross_client.png")


def make_cross_client_slide():
    fig, ax = blank_slide()
    draw_cross_client(ax, 0.93, 0.06)
    save_slide(fig, "visuals/slides/41_cross_client_slide.png")


# ===========================================================================
# 4. Benchmark scorecard -- pass bar set first, one invented citation fails
# ===========================================================================
SCORE_HEADS = ["", "Pass bar", "Small", "Large"]
SCORE_ROWS = [
    # (measure, bar, small, large, (small_ok, large_ok))
    ("Right answers", "95%+", "80%", "100%", (False, True)),
    ("Correct citations", "95%+", "84.2%", "94.7%", (False, False)),
    ("Invented answers", "Zero", "1", "1", (False, False)),
]


def draw_scorecard(ax, top, bottom):
    bar_h = 0.115
    takeaway_bar(ax, "One invented citation is still a fail.", bottom, bar_h)
    note_y = bottom + bar_h + 0.045
    table_bottom = note_y + 0.035
    g, g_result = 0.008, 0.014
    u = ((top - table_bottom) - (3 * g + g_result)) / 5
    xs = [0.04, 0.415, 0.585, 0.755]
    ws = [0.365, 0.160, 0.160, 0.205]

    cur = top
    for x, w, t in zip(xs, ws, SCORE_HEADS):
        if t:
            box(ax, (x, cur - u), w, u, DEEP_NAVY)
            ax.text(x + w / 2, cur - u / 2, t, fontsize=BODY, fontweight="bold",
                    color=WHITE, ha="center", va="center", zorder=4)
    cur -= u + g
    for q, bar, small, large, oks in SCORE_ROWS:
        y = cur - u
        for c, (x, w, v) in enumerate(zip(xs, ws, [q, bar, small, large])):
            fill, weight = LIGHT_TEAL, "bold" if c == 0 else "normal"
            if c in (2, 3):
                fill, weight = (SOFT_SAGE if oks[c - 2] else PINK_TINT), "bold"
            box(ax, (x, y), w, u, fill)
            ax.text(x + (0.014 if c == 0 else w / 2), y + u / 2, v, fontsize=BODY,
                    fontweight=weight, color=DEEP_NAVY,
                    ha="left" if c == 0 else "center", va="center", zorder=4)
        cur = y - g
    y = cur + g - g_result - u
    box(ax, (xs[0], y), xs[1] + ws[1] - xs[0], u, MIDNIGHT_TEAL)
    ax.text(xs[0] + 0.014, y + u / 2, "Meets the pass bar?", fontsize=BODY,
            fontweight="bold", color=WHITE, ha="left", va="center", zorder=4)
    for x, w in ((xs[2], ws[2]), (xs[3], ws[3])):
        box(ax, (x, y), w, u, ALERT_RED)
        ax.text(x + w / 2, y + u / 2, "No", fontsize=28, fontweight="bold",
                color=WHITE, ha="center", va="center", zorder=4)
    ax.text(0.04, note_y,
            "Local models. Example results from the test kit, not real output.",
            fontsize=22, color=OCEAN_TEAL, style="italic", ha="left", va="center")


def make_scorecard():
    fig, ax = framed_slide("Your Work. Your Data. Your Pass Bar.",
                           "Same finished engagements. Every model. One pass bar.",
                           FOOTER)
    draw_scorecard(ax, FRAME_CONTENT_TOP, FRAME_CONTENT_BOTTOM)
    save_slide(fig, "visuals/41_scorecard.png")


def make_result_slide():
    fig, ax = blank_slide()
    draw_scorecard(ax, 0.945, 0.04)
    save_slide(fig, "visuals/slides/41_result_slide.png")


# ===========================================================================
# Slide-only extras (no article counterpart)
# ===========================================================================
MEASURES = [
    "Did it get the answer right?",
    "Did it cite the correct source?",
    "Did it invent anything?",
    "How often did an analyst correct it?",
    "How much time did it save?",
    "What did it cost to run?",
]


def make_measure_slide():
    fig, ax = blank_slide()
    top, row_h, gap = 0.955, 0.105, 0.012
    chips = [OCEAN_TEAL, SEA_GREEN]
    for i, q in enumerate(MEASURES):
        y = top - (i + 1) * row_h - i * gap
        box(ax, (0.04, y), 0.92, row_h, LIGHT_TEAL)
        box(ax, (0.04, y), 0.07, row_h, chips[i % 2], zorder=3)
        ax.text(0.075, y + row_h / 2, str(i + 1), fontsize=30, fontweight="bold",
                color=WHITE, ha="center", va="center", zorder=4)
        ax.text(0.135, y + row_h / 2, q, fontsize=26, color=DEEP_NAVY,
                ha="left", va="center", zorder=4)
    takeaway_bar(ax, "Your work. Your data. Your acceptance criteria.", 0.04, 0.15)
    save_slide(fig, "visuals/slides/41_measure_slide.png")


TAKEAWAYS = [
    "Start with the work, not the model",
    "Test on work you already finished",
    "AI retrieves. Excel calculates.",
    "Local does not mean secure.",
]


def make_takeaway_slide():
    fig, ax = blank_slide()
    fills = [MIDNIGHT_TEAL, OCEAN_TEAL, SEA_GREEN, DEEP_NAVY]
    top, row_h, gap = 0.955, 0.150, 0.020
    for i, t in enumerate(TAKEAWAYS):
        y = top - (i + 1) * row_h - i * gap
        box(ax, (0.04, y), 0.92, row_h, fills[i], rounding=0.015)
        ax.text(0.095, y + row_h / 2, str(i + 1), fontsize=36, fontweight="bold",
                color=GOLDEN_YELLOW, ha="center", va="center", zorder=4)
        ax.text(0.15, y + row_h / 2, t, fontsize=30, fontweight="bold",
                color=WHITE, ha="left", va="center", zorder=4)
    takeaway_bar(ax, "If the data can't leave, bring the model in.", 0.05, 0.15)
    save_slide(fig, "visuals/slides/41_takeaway_slide.png")


# ===========================================================================
# Social cards (not slides; separate formats, kept as built)
# ===========================================================================
def blank_axes(figsize):
    fig, ax = plt.subplots(figsize=figsize, facecolor=WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_position([0, 0, 1, 1])
    return fig, ax


def social_footer(fig, y, size):
    fig.text(0.5, y, FOOTER, fontsize=size, color=OCEAN_TEAL,
             ha="center", va="center", alpha=0.80)


def social_save(fig, name):
    os.makedirs("visuals", exist_ok=True)
    fig.savefig(f"visuals/{name}", dpi=180, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)


def make_social_prompt_quote():
    fig, ax = blank_axes((16, 9))
    box(ax, (0.03, 0.10), 0.94, 0.85, DEEP_NAVY, rounding=0.03)
    ax.text(0.085, 0.80, "“", fontsize=150, color=GOLDEN_YELLOW,
            ha="center", va="center", fontweight="bold", zorder=4)
    ax.text(0.5, 0.58, "A prompt is not\nan access control.",
            fontsize=60, fontweight="bold", color=WHITE, ha="center",
            va="center", linespacing=1.2, zorder=4)
    ax.text(0.5, 0.235, "If the Data Can't Leave, Bring the Model In",
            fontsize=26, color=WARM_GLOW, style="italic", ha="center",
            va="center", zorder=4)
    social_footer(fig, 0.050, 20)
    social_save(fig, "41_social_prompt_quote.png")


def make_social_square():
    fig, ax = blank_axes((13, 13))
    header_h = 0.235
    fig.patches.append(FancyBboxPatch(
        (0, 1 - header_h), 1, header_h, boxstyle="square,pad=0",
        transform=fig.transFigure, facecolor=DEEP_NAVY, edgecolor="none",
        zorder=0))
    fig.text(0.05, 0.955, "Local Does Not\nMean Secure.", fontsize=50,
             fontweight="bold", color=WHITE, va="top", ha="left",
             linespacing=1.1)
    fig.text(0.05, 0.800, "No cybersecurity fairy dust included.",
             fontsize=26, color=WARM_GLOW, va="center", ha="left")

    items = ["Authentication and permissions", "Least-privilege access",
             "Logging and monitoring", "Model-version controls",
             "An ethical wall in retrieval", "Human review"]
    top, h, gap = 0.735, 0.068, 0.014
    for i, s in enumerate(items):
        y = top - i * (h + gap) - h
        fill = [MIDNIGHT_TEAL, OCEAN_TEAL, SEA_GREEN][i % 3]
        box(ax, (0.06, y), 0.88, h, fill, rounding=0.015)
        ax.text(0.10, y + h / 2, "✓", fontsize=30, fontweight="bold",
                color=WARM_GLOW, ha="center", va="center", zorder=4)
        ax.text(0.15, y + h / 2, s, fontsize=30, fontweight="bold",
                color=WHITE, ha="left", va="center", zorder=4)

    box(ax, (0.06, 0.080), 0.88, 0.120, GOLDEN_YELLOW)
    ax.text(0.5, 0.140, "More control. More responsibility.", fontsize=34,
            fontweight="bold", color=DEEP_NAVY, ha="center", va="center",
            zorder=4)
    social_footer(fig, 0.030, 20)
    social_save(fig, "41_social_square.png")


if __name__ == "__main__":
    make_hero()
    make_division_of_labor()
    make_cross_client()
    make_scorecard()
    print("Generated 4 slide-scale article visuals for Article 41.")
    make_hero_slide()
    make_division_slide()
    make_cross_client_slide()
    make_result_slide()
    make_measure_slide()
    make_takeaway_slide()
    print("Generated 6 header-less slide visuals in visuals/slides/.")
    make_social_prompt_quote()
    make_social_square()
    print("Generated 2 social cards.")
