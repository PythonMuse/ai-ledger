"""Generate branded visuals for Article 35 -- Don't Just Prompt AI. ONBOARD It.

Run from the article folder:
    python generate_visuals.py
"""

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

plt.rcParams["font.family"] = "sans-serif"


def add_header_bar(fig, title, subtitle, height=0.13):
    bar = FancyBboxPatch(
        (0, 1 - height), 1, height,
        boxstyle="square,pad=0", transform=fig.transFigure,
        facecolor=DEEP_NAVY, edgecolor="none", zorder=0,
    )
    fig.patches.append(bar)
    fig.text(0.03, 1 - height / 2 + 0.018, title, fontsize=22, fontweight="bold",
              color=WHITE, va="center", ha="left")
    fig.text(0.03, 1 - height / 2 - 0.032, subtitle, fontsize=12,
              color=WARM_GLOW, va="center", ha="left", alpha=1.0)
    fig.text(0.97, 1 - height / 2, "PythonMuse LLC", fontsize=9,
              color=WHITE, va="center", ha="right", alpha=0.70)


# FancyBboxPatch inflates each box by `pad` on every side. Keep this small so
# that the gaps computed in each layout below survive and the connector arrows
# stay visible -- a larger pad silently eats them.
BOX_PAD = 0.004


def rounded_box(ax, xy, w, h, color, text_color=WHITE, text="", fontsize=12,
                 sub="", subsize=10, sub_color=None, bold=True, title_offset=0.16,
                 sub_offset=0.22, linespacing=1.4, edge=None, lw=0, ha="center",
                 text_x=None):
    box = FancyBboxPatch(
        xy, w, h, boxstyle=f"round,pad={BOX_PAD},rounding_size=0.03",
        facecolor=color, edgecolor=edge or "none", linewidth=lw, zorder=2,
    )
    ax.add_patch(box)
    cx, cy = xy[0] + w / 2, xy[1] + h / 2
    tx = text_x if text_x is not None else cx
    if sub:
        ax.text(tx, cy + h * title_offset, text, fontsize=fontsize,
                 fontweight="bold" if bold else "normal",
                 color=text_color, ha=ha, va="center", zorder=3)
        ax.text(tx, cy - h * sub_offset, sub, fontsize=subsize, color=sub_color or text_color,
                 ha=ha, va="center", zorder=3, alpha=1.0, linespacing=linespacing)
    else:
        ax.text(tx, cy, text, fontsize=fontsize, fontweight="bold" if bold else "normal",
                 color=text_color, ha=ha, va="center", zorder=3, linespacing=linespacing)


def arrow_v(ax, x, y1, y2, color=OCEAN_TEAL, lw=2.2):
    ax.annotate("", xy=(x, y2), xytext=(x, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                mutation_scale=16), zorder=1)


# The seven ONBOARD steps, shared between the hero and the social variant.
ONBOARD_STEPS = [
    ("O", "Organize", "Create the workspace and define AI's role", DEEP_NAVY),
    ("N", "Name", "Define the assignment, scope, and deliverable", MIDNIGHT_TEAL),
    ("B", "Brief", "Transfer the business and accounting context", OCEAN_TEAL),
    ("O", "Obtain", "Require an approved plan before execution", SEA_GREEN),
    ("A", "Allow", "Run only a controlled, approved test", BRIGHT_TEAL),
    ("R", "Review", "Validate calculations, evidence, and exceptions", GOLDEN_YELLOW),
    ("D", "Document", "Update instructions with what was learned", WARM_GLOW),
]


# ---------------------------------------------------------------------------
# 1. Hero -- the ONBOARD checklist as a vertical stepper
# ---------------------------------------------------------------------------
def make_hero():
    fig, ax = plt.subplots(figsize=(10, 12.2), facecolor=WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_position([0, 0, 1, 1])

    add_header_bar(fig, "The ONBOARD Checklist",
                    "A supervised, seven-step method for onboarding AI into a real workflow",
                    height=0.095)

    n = len(ONBOARD_STEPS)
    box_w = 0.80
    x0 = 0.10
    top = 0.885
    bottom = 0.075
    box_h = 0.093
    gap = ((top - bottom) - n * box_h) / (n - 1)

    centers = []
    for i, (letter, word, desc, color) in enumerate(ONBOARD_STEPS):
        y = top - i * (box_h + gap) - box_h
        centers.append(y + box_h / 2)
        text_color = OCEAN_TEAL if color in (GOLDEN_YELLOW, WARM_GLOW) else WHITE
        rounded_box(ax, (x0, y), box_w, box_h, color, text_color=text_color,
                    text=f"{letter}  —  {word}", fontsize=17,
                    sub=desc, subsize=12, sub_color=text_color,
                    title_offset=0.20, sub_offset=0.24)

    for i in range(n - 1):
        arrow_v(ax, x0 + box_w / 2, centers[i] - box_h / 2 - 0.004,
                centers[i + 1] + box_h / 2 + 0.004)

    fig.text(0.5, 0.035,
              "Not a one-prompt formula. A supervised process for turning accounting knowledge into a repeatable workflow.",
              fontsize=11, color=OCEAN_TEAL, ha="center", va="center", style="italic", alpha=1.0)

    fig.savefig("visuals/35_hero.png", dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


# ---------------------------------------------------------------------------
# 2. The onboarding workspace -- folder-structure tree
# ---------------------------------------------------------------------------
def make_workspace():
    fig, ax = plt.subplots(figsize=(12, 10.6), facecolor=WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_position([0, 0, 1, 1])

    add_header_bar(fig, "The Onboarding Workspace",
                    "monthly-variance-review/ -- one folder, one shared understanding of where everything lives",
                    height=0.10)

    rows = [
        (0, MIDNIGHT_TEAL, GOLDEN_YELLOW, "AGENTS.md",
         "AI's role, allowed and prohibited actions, stop conditions"),
        (0, MIDNIGHT_TEAL, GOLDEN_YELLOW, "plan.md",
         "The assignment: scope, exclusions, and deliverable"),
        (0, MIDNIGHT_TEAL, GOLDEN_YELLOW, "status_update.md",
         "Where the work stands right now"),
        (0, MIDNIGHT_TEAL, GOLDEN_YELLOW, "backlog.md",
         "Recommended controls awaiting human review"),
        (0, OCEAN_TEAL, WHITE, "data/",
         "Raw and processed data, kept strictly apart"),
        (1, "#F5F5F5", DEEP_NAVY, "raw/",
         "Source files -- never modified"),
        (1, "#F5F5F5", DEEP_NAVY, "processed/",
         "Transformed data -- created only after approval"),
        (0, OCEAN_TEAL, WHITE, "scripts/",
         "Reviewed, reusable processing logic"),
        (0, OCEAN_TEAL, WHITE, "prompts/",
         "The prompts that ran this workflow"),
        (0, OCEAN_TEAL, WHITE, "outputs/",
         "Draft reports awaiting review"),
        (0, OCEAN_TEAL, WHITE, "evidence/",
         "Tie-outs and validation proof"),
        (0, OCEAN_TEAL, WHITE, "skills/",
         "Reusable accounting logic, referenced by name"),
        (0, SEA_GREEN, WHITE, "docs/",
         "Definitions, mappings, and known exceptions"),
    ]

    n = len(rows)
    x0, w = 0.06, 0.90
    top = 0.865
    bottom = 0.045
    row_h = 0.052
    gap = ((top - bottom) - n * row_h) / (n - 1)

    for i, (indent, bg, text_col, name, desc) in enumerate(rows):
        y = top - i * (row_h + gap) - row_h
        rounded_box(ax, (x0, y), w, row_h, bg, text_color=text_col,
                    text=name, fontsize=12.5, ha="left",
                    text_x=x0 + 0.03 + indent * 0.03, bold=(indent == 0))
        desc_color = OCEAN_TEAL if bg == "#F5F5F5" else (WARM_GLOW if bg in (MIDNIGHT_TEAL, OCEAN_TEAL) else WHITE)
        ax.text(x0 + 0.42, y + row_h / 2, desc, fontsize=10.5, color=desc_color,
                 ha="left", va="center", style="italic", zorder=3)

    fig.text(0.5, 0.02,
              "data/raw/ is read-only by convention. A neat folder structure is not a security control -- it is just a neat folder structure.",
              fontsize=10, color=OCEAN_TEAL, ha="center", va="center", style="italic", alpha=1.0)

    fig.savefig("visuals/35_workspace_structure.png", dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


# ---------------------------------------------------------------------------
# 3. Social square -- condensed ONBOARD stepper for LinkedIn
# ---------------------------------------------------------------------------
def make_social_square():
    fig, ax = plt.subplots(figsize=(8, 8), facecolor=WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_position([0, 0, 1, 1])

    header_h = 0.155
    add_header_bar(fig, "Don't Just Prompt AI.",
                    "ONBOARD it. -- a 7-step method for your first AI workflow", height=header_h)

    n = len(ONBOARD_STEPS)
    box_w = 0.90
    x0 = 0.05
    top = 1 - header_h - 0.025
    bottom = 0.05
    box_h = 0.082
    gap = ((top - bottom) - n * box_h) / (n - 1)

    for i, (letter, word, desc, color) in enumerate(ONBOARD_STEPS):
        y = top - i * (box_h + gap) - box_h
        text_color = OCEAN_TEAL if color in (GOLDEN_YELLOW, WARM_GLOW) else WHITE
        rounded_box(ax, (x0, y), box_w, box_h, color, text_color=text_color,
                    text=f"{letter} — {word}", fontsize=13.5, ha="left",
                    text_x=x0 + 0.035,
                    sub=desc, subsize=10, sub_color=text_color,
                    title_offset=0.20, sub_offset=0.26)

    fig.text(0.5, 0.015, "PythonMuse LLC · pythonmuse.com", fontsize=9.5,
              color=OCEAN_TEAL, ha="center", va="center", alpha=0.85)

    fig.savefig("visuals/35_social_square.png", dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


if __name__ == "__main__":
    make_hero()
    make_workspace()
    make_social_square()
    print("Generated 3 visuals for Article 35.")
