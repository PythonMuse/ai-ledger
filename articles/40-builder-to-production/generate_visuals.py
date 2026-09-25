"""Generate branded visuals for Article 40 -- You Built an AI Workflow. What
Happens If You Win the Lottery?

Run from the article folder:
    python generate_visuals.py

Produces five article visuals plus two social cards in ./visuals/.
"""

import os

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

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

# Font sizes in this file are set directly at the slide-readable level the
# house SKILL.md benchmarks describe (focal card text ~28-36pt, header titles
# in the 40s, footer branding ~18-20pt on these large canvases) rather than
# tuned small and scaled up afterwards. Every position below is a fraction of
# the figure (0-1), so if a layout ever feels cramped, grow the canvas inches
# in blank_axes() first -- do not shrink the text.

FOOTER = "PythonMuse LLC  |  www.pythonmuse.com"

# FancyBboxPatch inflates each box by `pad` on every side. Keep it small so the
# gaps computed below survive and the connector arrows stay visible.
BOX_PAD = 0.004

# Anything at or lighter than Bright Teal takes dark text.
LIGHT_FILLS = (BRIGHT_TEAL, GOLDEN_YELLOW, WARM_GLOW, SOFT_SAGE, LIGHT_GRAY, WHITE)


def text_colors(fill):
    """Return (title_color, secondary_color) for text sitting on `fill`."""
    if fill in (BRIGHT_TEAL, SOFT_SAGE):
        return DEEP_NAVY, DEEP_NAVY
    if fill in LIGHT_FILLS:
        return DEEP_NAVY, OCEAN_TEAL
    return WHITE, WARM_GLOW


def blank_axes(figsize):
    fig, ax = plt.subplots(figsize=figsize, facecolor=WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_position([0, 0, 1, 1])
    return fig, ax


def add_header_bar(fig, title, subtitle, height, title_size, subtitle_size,
                   title_y=0.36, subtitle_y=0.74):
    """Deep Navy bar across the top. title_y / subtitle_y are fractions of the
    bar's height measured down from the top edge of the figure."""
    bar = FancyBboxPatch(
        (0, 1 - height), 1, height,
        boxstyle="square,pad=0", transform=fig.transFigure,
        facecolor=DEEP_NAVY, edgecolor="none", zorder=0,
    )
    fig.patches.append(bar)
    fig.text(0.03, 1 - height * title_y, title, fontsize=title_size,
             fontweight="bold", color=WHITE, va="center", ha="left")
    fig.text(0.03, 1 - height * subtitle_y, subtitle, fontsize=subtitle_size,
             color=WARM_GLOW, va="center", ha="left")


def box(ax, xy, w, h, fill, edge=None, lw=0, zorder=2, rounding=0.02):
    ax.add_patch(FancyBboxPatch(
        xy, w, h, boxstyle=f"round,pad={BOX_PAD},rounding_size={rounding}",
        facecolor=fill, edgecolor=edge or "none", linewidth=lw, zorder=zorder,
    ))


def arrow(ax, start, end, color=OCEAN_TEAL, width=3.2, scale=26, style="-|>",
          ls="solid", zorder=1, rad=0.0):
    ax.annotate("", xy=end, xytext=start,
                arrowprops=dict(arrowstyle=style, color=color, lw=width,
                                mutation_scale=scale, linestyle=ls,
                                shrinkA=0, shrinkB=0,
                                connectionstyle=f"arc3,rad={rad}"),
                zorder=zorder)


def footer(fig, y=0.012, size=19):
    fig.text(0.5, y, FOOTER, fontsize=size, color=OCEAN_TEAL,
             ha="center", va="center", alpha=0.80)


def save(fig, name):
    os.makedirs("visuals", exist_ok=True)
    fig.savefig(f"visuals/{name}", dpi=180, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)


# ---------------------------------------------------------------------------
# 1. Hero -- how an experiment drifts into a business process
# ---------------------------------------------------------------------------
DRIFT = [
    ("Experiment", "A 10:30 p.m.\nidea", LIGHT_GRAY),
    ("Helpful\nTool", "Saves you\n20 minutes", SOFT_SAGE),
    ("Habit", "You run it\nevery month", BRIGHT_TEAL),
    ("Dependency", "Someone else\nuses the output", OCEAN_TEAL),
    ("Business\nProcess", "Part of the\nclose", DEEP_NAVY),
]


def make_hero():
    fig, ax = blank_axes((24, 14))
    add_header_bar(fig, "The Experiment That Accidentally Became a Process",
                   "Nobody announced it. It just kept being useful.",
                   height=0.165, title_size=50, subtitle_size=30)

    n = len(DRIFT)
    gap = 0.036
    w = (0.94 - gap * (n - 1)) / n
    h = 0.265
    base, rise = 0.215, 0.083

    centers = []
    for i, (label, caption, fill) in enumerate(DRIFT):
        x = 0.03 + i * (w + gap)
        y = base + i * rise
        edge = OCEAN_TEAL if fill == LIGHT_GRAY else None
        box(ax, (x, y), w, h, fill, edge=edge, lw=2.5)
        title_col, sub_col = text_colors(fill)
        ax.text(x + w / 2, y + h * 0.69, label, fontsize=34, fontweight="bold",
                color=title_col, ha="center", va="center", linespacing=1.05,
                zorder=4)
        ax.text(x + w / 2, y + h * 0.25, caption, fontsize=25,
                color=sub_col, ha="center", va="center", linespacing=1.2,
                zorder=4)
        centers.append((x, y, w, h))

    for i in range(n - 1):
        x, y, w_, h_ = centers[i]
        nx, ny, _, nh = centers[i + 1]
        arrow(ax, (x + w_ + 0.006, y + h_ * 0.5),
              (nx - 0.006, ny + nh * 0.5), color=OCEAN_TEAL, width=4, scale=32)

    # Rising "dependency" axis under the staircase.
    arrow(ax, (0.04, 0.180), (0.96, 0.180), color=SEA_GREEN, width=3,
          scale=30)
    ax.text(0.04, 0.150, "Organizational dependency grows — whether or not anyone decided it should",
            fontsize=25, color=OCEAN_TEAL, style="italic", ha="left",
            va="center")

    box(ax, (0.03, 0.035), 0.94, 0.090, GOLDEN_YELLOW)
    ax.text(0.5, 0.080,
            "You may have removed the manual dependency without removing the person dependency.",
            fontsize=29, fontweight="bold", color=DEEP_NAVY, ha="center",
            va="center", zorder=4)
    footer(fig, y=0.010)
    save(fig, "40_hero.png")


# ---------------------------------------------------------------------------
# 2. Graduation path -- documentation and control rise with dependency
# ---------------------------------------------------------------------------
GRADUATION = [  # bottom (Experiment) to top (Managed Asset)
    ("Experiment", "Room to play. Notes to yourself are plenty.", LIGHT_GRAY),
    ("Personal Tool", "A short README: what it does and why.", SOFT_SAGE),
    ("Team Tool", "Human Instructions and validation steps.", BRIGHT_TEAL),
    ("Production Workflow", "Owner, backup, tested, version-controlled.", OCEAN_TEAL),
    ("Managed Asset", "Monitored, change-controlled, reviewed.", DEEP_NAVY),
]


def make_graduation_path():
    fig, ax = blank_axes((24, 17))
    add_header_bar(fig, "Do Not Stop the Builders. Create a Graduation Path.",
                   "Documentation and control grow as the organization's dependency grows.",
                   height=0.140, title_size=48, subtitle_size=29)

    left = 0.085
    chip_w = 0.262
    card_x = left + chip_w + 0.015
    meter_x = 0.800
    card_w = meter_x - 0.020 - card_x
    row_h, gap = 0.100, 0.022
    bottom = 0.215

    # Column labels.
    top_row_top = bottom + len(GRADUATION) * row_h + (len(GRADUATION) - 1) * gap
    ax.text(left, top_row_top + 0.030, "STAGE", fontsize=24, fontweight="bold",
            color=SEA_GREEN, ha="left", va="center")
    ax.text(card_x, top_row_top + 0.030, "WHAT TO LEAVE BEHIND",
            fontsize=24, fontweight="bold", color=SEA_GREEN, ha="left",
            va="center")
    ax.text(meter_x + 0.085, top_row_top + 0.030, "CONTROL",
            fontsize=24, fontweight="bold", color=SEA_GREEN, ha="center",
            va="center")

    sq, sq_gap = 0.026, 0.009
    for i, (stage, need, fill) in enumerate(GRADUATION):
        y = bottom + i * (row_h + gap)
        edge = OCEAN_TEAL if fill == LIGHT_GRAY else None
        box(ax, (left, y), chip_w, row_h, fill, edge=edge, lw=2.5)
        title_col, _ = text_colors(fill)
        ax.text(left + chip_w / 2, y + row_h / 2, stage, fontsize=32,
                fontweight="bold", color=title_col, ha="center", va="center",
                zorder=4)

        box(ax, (card_x, y), card_w, row_h, LIGHT_GRAY, edge=OCEAN_TEAL, lw=1.8)
        ax.text(card_x + 0.020, y + row_h / 2, need, fontsize=30,
                color=DEEP_NAVY, ha="left", va="center", zorder=4)

        # Control meter: i + 1 filled squares out of five.
        for k in range(5):
            filled = k <= i
            ax.add_patch(FancyBboxPatch(
                (meter_x + k * (sq + sq_gap), y + row_h / 2 - 0.022), sq, 0.044,
                boxstyle="round,pad=0.002,rounding_size=0.006",
                facecolor=SEA_GREEN if filled else WHITE,
                edgecolor=SEA_GREEN, linewidth=2, zorder=3))

    # Upward "graduate" arrow on the left.
    arrow(ax, (0.045, bottom), (0.045, top_row_top), color=SEA_GREEN,
          width=4, scale=34)
    ax.text(0.024, (bottom + top_row_top) / 2, "GRADUATE AS DEPENDENCY GROWS",
            rotation=90, fontsize=22, fontweight="bold", color=OCEAN_TEAL,
            ha="center", va="center")

    box(ax, (0.03, 0.050), 0.94, 0.115, GOLDEN_YELLOW)
    ax.text(0.5, 0.123, "Would the business care if this disappeared tomorrow?",
            fontsize=34, fontweight="bold", color=DEEP_NAVY, ha="center",
            va="center", zorder=4)
    ax.text(0.5, 0.076, "If yes, it is time to start thinking about how to inherit it.",
            fontsize=26, color=OCEAN_TEAL, ha="center", va="center", zorder=4)
    footer(fig, y=0.014)
    save(fig, "40_graduation_path.png")


# ---------------------------------------------------------------------------
# 3. Four breadcrumbs -- the minimum survivability standard
# ---------------------------------------------------------------------------
BREADCRUMBS = [
    ("1", "README", "What is this, and\nwhy does it exist?",
     "README.md", MIDNIGHT_TEAL),
    ("2", "BUSINESS-LOGIC COMMENTS", "Why does the code\ndo that?",
     "# BUSINESS RULE: intercompany\n# is reconciled separately", OCEAN_TEAL),
    ("3", "HUMAN INSTRUCTIONS", "How do I run it,\nand how do I check it?",
     "HUMAN_INSTRUCTIONS.md", OCEAN_TEAL),
    ("4", "OUTPUT TRAIL", "Where did this\nfile come from?",
     "A Control tab in the output", MIDNIGHT_TEAL),
]


def make_four_breadcrumbs():
    fig, ax = blank_axes((24, 18))
    add_header_bar(fig, "The Minimum Survivability Standard",
                   "Four breadcrumbs, so someone else can follow the trail.",
                   height=0.135, title_size=50, subtitle_size=30)

    col_w, row_h = 0.458, 0.314
    gx, gy = 0.024, 0.020
    top = 0.834

    for idx, (num, title, question, example, fill) in enumerate(BREADCRUMBS):
        r, c = divmod(idx, 2)
        x = 0.03 + c * (col_w + gx)
        y = top - (r + 1) * row_h - r * gy
        box(ax, (x, y), col_w, row_h, fill)

        badge = 0.062
        box(ax, (x + 0.022, y + row_h - 0.022 - badge * 24 / 18), badge,
            badge * 24 / 18, WARM_GLOW, rounding=0.012)
        ax.text(x + 0.022 + badge / 2, y + row_h - 0.022 - badge * 24 / 18 / 2,
                num, fontsize=36, fontweight="bold", color=DEEP_NAVY,
                ha="center", va="center", zorder=4)
        ax.text(x + 0.022 + badge + 0.022, y + row_h - 0.022 - badge * 24 / 18 / 2,
                title, fontsize=29, fontweight="bold", color=WARM_GLOW,
                ha="left", va="center", zorder=4)

        ax.text(x + 0.030, y + row_h * 0.505, question, fontsize=36,
                color=WHITE, ha="left", va="center", linespacing=1.2,
                zorder=4)

        # Example "tag" at the bottom of each card, in code-block styling.
        # One tag height for every card, so a two-line example never
        # pushes up into the question above it.
        tag_h = 0.080
        box(ax, (x + 0.030, y + 0.022), col_w - 0.060, tag_h, WHITE,
            rounding=0.01, zorder=3)
        ax.text(x + 0.045, y + 0.022 + tag_h / 2, example, fontsize=24,
                family="monospace", color=DEEP_NAVY, ha="left", va="center",
                linespacing=1.15, zorder=4)

    box(ax, (0.03, 0.040), 0.94, 0.090, GOLDEN_YELLOW)
    ax.text(0.5, 0.085,
            "Build freely. Leave enough breadcrumbs for someone else to follow.",
            fontsize=33, fontweight="bold", color=DEEP_NAVY, ha="center",
            va="center", zorder=4)
    footer(fig, y=0.012)
    save(fig, "40_four_breadcrumbs.png")


# ---------------------------------------------------------------------------
# 4. The Unavailable Tomorrow Test -- six steps without the builder
# ---------------------------------------------------------------------------
TOMORROW_STEPS = [
    ("FIND THE WORKFLOW", "Where does it live — somewhere the team can reach?"),
    ("PREPARE THE INPUTS", "Which files, what format, named how, placed where?"),
    ("RUN IT", "Which dates and variables change first? How does it start?"),
    ("FIND THE OUTPUT", "Where does it land? Where does the reviewed copy go?"),
    ("VALIDATE IT", "What must tie? Which exceptions need a human?"),
    ("REPRODUCE IT NEXT MONTH", "Could they do it again without calling anyone?"),
]


def make_unavailable_tomorrow():
    fig, ax = blank_axes((22, 22))
    add_header_bar(fig, "The Unavailable Tomorrow Test",
                   "The builder won the lottery. Could another accountant do all six?",
                   height=0.112, title_size=52, subtitle_size=30)

    top = 0.860
    card_h, gap = 0.098, 0.018
    x, w = 0.03, 0.94
    fills = [MIDNIGHT_TEAL, OCEAN_TEAL, SEA_GREEN] * 2

    for i, (label, detail) in enumerate(TOMORROW_STEPS):
        y = top - i * (card_h + gap) - card_h
        box(ax, (x, y), w, card_h, LIGHT_GRAY, edge=OCEAN_TEAL, lw=1.8)
        bw, bh = 0.070, 0.070
        box(ax, (x + 0.020, y + card_h / 2 - bh / 2), bw, bh, fills[i],
            rounding=0.012, zorder=3)
        ax.text(x + 0.020 + bw / 2, y + card_h / 2, str(i + 1), fontsize=38,
                fontweight="bold", color=WHITE, ha="center", va="center",
                zorder=4)
        tx = x + 0.020 + bw + 0.028
        ax.text(tx, y + card_h * 0.70, label, fontsize=31, fontweight="bold",
                color=DEEP_NAVY, ha="left", va="center", zorder=4)
        ax.text(tx, y + card_h * 0.29, detail, fontsize=28, color=OCEAN_TEAL,
                ha="left", va="center", zorder=4)
        if i < len(TOMORROW_STEPS) - 1:
            arrow(ax, (x + 0.020 + bw / 2, y - 0.001),
                  (x + 0.020 + bw / 2, y - gap + 0.001), color=SEA_GREEN,
                  width=3, scale=22, zorder=5)

    rows_bottom = top - len(TOMORROW_STEPS) * (card_h + gap) + gap
    banner_h = 0.105
    banner_y = rows_bottom - 0.030 - banner_h
    box(ax, (0.03, banner_y), 0.94, banner_h, GOLDEN_YELLOW)
    ax.text(0.5, banner_y + banner_h * 0.66,
            "If any step needs the builder, the process still depends on the builder.",
            fontsize=29, fontweight="bold", color=DEEP_NAVY, ha="center",
            va="center", zorder=4)
    ax.text(0.5, banner_y + banner_h * 0.28,
            "\"It ran without an error\" is not step five.",
            fontsize=27, color=OCEAN_TEAL, style="italic", ha="center",
            va="center", zorder=4)
    footer(fig, y=0.010)
    save(fig, "40_unavailable_tomorrow.png")


# ---------------------------------------------------------------------------
# 5. Lifecycle -- Build to Retire, with the change loop inset
# ---------------------------------------------------------------------------
LIFECYCLE = [
    ("Build", "It works for me"),
    ("Prove", "Tested on real cases"),
    ("Approve", "The owner signs off"),
    ("Launch", "Team location,\nno personal logins"),
    ("Adopt", "Operators trained"),
    ("Monitor", "Still tying out?"),
    ("Improve", "Through the\nchange loop"),
    ("Retire", "Switched off\non purpose"),
]

CHANGE_LOOP = ["Issue", "Diagnose", "Change", "Retest", "Reapprove", "Release"]


def make_lifecycle():
    import math

    fig, ax = blank_axes((24, 20))
    add_header_bar(fig, "What Happens After the Agent Is Built?",
                   "Building is one stage. Changes need their own loop, or January's workflow is not September's.",
                   height=0.120, title_size=50, subtitle_size=27)

    cx, cy = 0.5, 0.455
    rx, ry = 0.385, 0.315
    bw, bh = 0.185, 0.118
    fills = [LIGHT_GRAY, SOFT_SAGE, BRIGHT_TEAL, SEA_GREEN,
             OCEAN_TEAL, MIDNIGHT_TEAL, DEEP_NAVY, LIGHT_GRAY]

    pos = []
    for i, (stage, note) in enumerate(LIFECYCLE):
        ang = math.radians(112.5 - 45 * i)
        px, py = cx + rx * math.cos(ang), cy + ry * math.sin(ang)
        pos.append((px, py))
        fill = fills[i]
        edge = OCEAN_TEAL if fill == LIGHT_GRAY else None
        box(ax, (px - bw / 2, py - bh / 2), bw, bh, fill, edge=edge, lw=2.5,
            zorder=3)
        title_col, sub_col = text_colors(fill)
        if fill in (BRIGHT_TEAL, SOFT_SAGE):
            sub_col = DEEP_NAVY
        ax.text(px, py + bh * 0.22, stage, fontsize=34, fontweight="bold",
                color=title_col, ha="center", va="center", zorder=4)
        ax.text(px, py - bh * 0.24, note, fontsize=22, color=sub_col,
                ha="center", va="center", linespacing=1.1, zorder=4)

    # Arrows between consecutive stages (Retire is an end, not a restart).
    for i in range(len(pos) - 1):
        (x1, y1), (x2, y2) = pos[i], pos[i + 1]
        dx, dy = x2 - x1, y2 - y1
        d = math.hypot(dx, dy)
        # Trim each end so the arrow runs gap-to-gap, not box-centre to centre.
        def trim(px, py, sx, sy):
            tx = (bw / 2 + 0.010) / abs(sx) if sx else 1e9
            ty = (bh / 2 + 0.010) / abs(sy) if sy else 1e9
            t = min(tx, ty)
            return px + sx * t, py + sy * t
        ux, uy = dx / d, dy / d
        s = trim(x1, y1, ux, uy)
        e = trim(x2, y2, -ux, -uy)
        arrow(ax, s, e, color=OCEAN_TEAL, width=4, scale=30, rad=-0.12)

    # Change-loop inset in the middle of the ring.
    iw, ih = 0.44, 0.300
    ix, iy = cx - iw / 2, cy - ih / 2
    box(ax, (ix, iy), iw, ih, WHITE, edge=GOLDEN_YELLOW, lw=5, zorder=2)
    ax.text(cx, iy + ih - 0.034, "THE CHANGE LOOP", fontsize=30,
            fontweight="bold", color=OCEAN_TEAL, ha="center", va="center",
            zorder=4)
    chip_w, chip_h = 0.120, 0.058
    cgap = 0.020
    row_y = [iy + ih - 0.110, iy + ih - 0.110 - chip_h - 0.042]
    for k, name in enumerate(CHANGE_LOOP):
        r, c = divmod(k, 3)
        # Second row runs right-to-left so the loop reads as a U-turn.
        col = c if r == 0 else 2 - c
        chip_x = cx - (3 * chip_w + 2 * cgap) / 2 + col * (chip_w + cgap)
        box(ax, (chip_x, row_y[r] - chip_h / 2), chip_w, chip_h,
            GOLDEN_YELLOW if name == "Reapprove" else MIDNIGHT_TEAL,
            rounding=0.012, zorder=3)
        ax.text(chip_x + chip_w / 2, row_y[r], name, fontsize=24,
                fontweight="bold",
                color=DEEP_NAVY if name == "Reapprove" else WHITE,
                ha="center", va="center", zorder=4)
        if c < 2:
            step = chip_w + cgap
            if r == 0:
                arrow(ax, (chip_x + chip_w + 0.003, row_y[r]),
                      (chip_x + step - 0.003, row_y[r]), color=SEA_GREEN,
                      width=3, scale=20, zorder=5)
            else:
                arrow(ax, (chip_x - 0.003, row_y[r]),
                      (chip_x - cgap + 0.003, row_y[r]), color=SEA_GREEN,
                      width=3, scale=20, zorder=5)
    # U-turn from Retest-row end (Change) down to Retest.
    right_x = cx + (3 * chip_w + 2 * cgap) / 2
    arrow(ax, (right_x - chip_w / 2, row_y[0] - chip_h / 2 - 0.003),
          (right_x - chip_w / 2, row_y[1] + chip_h / 2 + 0.003),
          color=SEA_GREEN, width=3, scale=20, zorder=5)
    ax.text(cx, iy + 0.036, "Prompt, mapping, source file, model, config.",
            fontsize=22, color=DEEP_NAVY, style="italic", ha="center",
            va="center", zorder=4)

    ax.text(0.5, 0.040,
            "Know which version you are actually relying on.",
            fontsize=32, fontweight="bold", color=DEEP_NAVY, ha="center",
            va="center")
    footer(fig, y=0.010)
    save(fig, "40_lifecycle.png")


# ---------------------------------------------------------------------------
# 6. Social square -- the Unavailable Tomorrow Test at a glance
# ---------------------------------------------------------------------------
def make_social_square():
    fig, ax = blank_axes((13, 13))
    header_h = 0.235
    fig.patches.append(FancyBboxPatch(
        (0, 1 - header_h), 1, header_h, boxstyle="square,pad=0",
        transform=fig.transFigure, facecolor=DEEP_NAVY, edgecolor="none",
        zorder=0))
    fig.text(0.05, 0.965, "You Built It.\nCould Anyone Else Run It?",
             fontsize=46, fontweight="bold", color=WHITE, va="top", ha="left",
             linespacing=1.1)
    fig.text(0.05, 0.800, "The lottery test for employee-built workflows",
             fontsize=26, color=WARM_GLOW, va="center", ha="left")

    steps = ["Find it", "Prepare the inputs", "Run it", "Find the output",
             "Validate it", "Reproduce it next month"]
    top, h, gap = 0.735, 0.068, 0.014
    for i, s in enumerate(steps):
        y = top - i * (h + gap) - h
        fill = [MIDNIGHT_TEAL, OCEAN_TEAL, SEA_GREEN][i % 3]
        box(ax, (0.06, y), 0.88, h, fill, rounding=0.015)
        ax.text(0.10, y + h / 2, f"{i + 1}", fontsize=30, fontweight="bold",
                color=WARM_GLOW, ha="center", va="center", zorder=4)
        ax.text(0.15, y + h / 2, s, fontsize=31, fontweight="bold",
                color=WHITE, ha="left", va="center", zorder=4)

    box(ax, (0.06, 0.080), 0.88, 0.120, GOLDEN_YELLOW)
    ax.text(0.5, 0.140, "If not, leave some breadcrumbs.",
            fontsize=36, fontweight="bold", color=DEEP_NAVY, ha="center",
            va="center", zorder=4)
    footer(fig, y=0.030, size=20)
    save(fig, "40_social_square.png")


# ---------------------------------------------------------------------------
# 7. Social quote card
# ---------------------------------------------------------------------------
def make_social_quote():
    fig, ax = blank_axes((16, 9))
    box(ax, (0.03, 0.10), 0.94, 0.85, DEEP_NAVY, rounding=0.03)
    ax.text(0.085, 0.80, "“", fontsize=150, color=GOLDEN_YELLOW,
            ha="center", va="center", fontweight="bold", zorder=4)
    ax.text(0.5, 0.56,
            "You may have removed the\nmanual dependency without\nremoving the person dependency.",
            fontsize=48, fontweight="bold", color=WHITE, ha="center",
            va="center", linespacing=1.25, zorder=4)
    ax.text(0.5, 0.215,
            "You Built an AI Workflow. What Happens If You Win the Lottery?",
            fontsize=24, color=WARM_GLOW, style="italic", ha="center",
            va="center", zorder=4)
    footer(fig, y=0.050, size=20)
    save(fig, "40_social_lottery_quote.png")


if __name__ == "__main__":
    make_hero()
    make_graduation_path()
    make_four_breadcrumbs()
    make_unavailable_tomorrow()
    make_lifecycle()
    make_social_square()
    make_social_quote()
    print("Generated 7 visuals for Article 40.")
