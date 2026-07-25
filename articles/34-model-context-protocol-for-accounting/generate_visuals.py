"""Generate branded visuals for Article 34 — Model Context Protocol for Accounting.

Run from the article folder:
    python generate_visuals.py
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.path import Path
import matplotlib.patches as mpatches

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


def add_header_bar(fig, title, subtitle, height=0.14):
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


def rounded_box(ax, xy, w, h, color, text_color=WHITE, text="", fontsize=12,
                 sub="", subsize=10, sub_color=None, bold=True):
    box = FancyBboxPatch(
        xy, w, h, boxstyle="round,pad=0.02,rounding_size=0.03",
        facecolor=color, edgecolor="none", zorder=2,
    )
    ax.add_patch(box)
    cx, cy = xy[0] + w / 2, xy[1] + h / 2
    if sub:
        ax.text(cx, cy + h * 0.14, text, fontsize=fontsize, fontweight="bold" if bold else "normal",
                 color=text_color, ha="center", va="center", zorder=3)
        ax.text(cx, cy - h * 0.22, sub, fontsize=subsize, color=sub_color or text_color,
                 ha="center", va="center", zorder=3, alpha=1.0, linespacing=1.4)
    else:
        ax.text(cx, cy, text, fontsize=fontsize, fontweight="bold" if bold else "normal",
                 color=text_color, ha="center", va="center", zorder=3)


def arrow(ax, x1, y, x2, color=OCEAN_TEAL):
    ax.annotate("", xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=2.4,
                                shrinkA=2, shrinkB=2, mutation_scale=18),
                zorder=1)


# ---------------------------------------------------------------------------
# 1. Hero: evolution infographic — ERP Menus -> Reports -> APIs -> MCP -> Agents
# ---------------------------------------------------------------------------
def make_hero():
    fig, ax = plt.subplots(figsize=(14, 5.2), facecolor=WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    add_header_bar(fig, "From ERP Menus to AI Agents",
                    "The evolving interface between accountants and financial systems")

    stages = [
        ("ERP Menus", "Learn where every\nreport lives", OCEAN_TEAL),
        ("Reports", "Export, filter,\ncombine files", SEA_GREEN),
        ("APIs", "System-to-system\ndata requests", BRIGHT_TEAL),
        ("MCP", "A governed tool\nlayer for AI clients", GOLDEN_YELLOW),
        ("AI Agents", "Describe the outcome,\nreview the result", SOFT_SAGE),
    ]

    n = len(stages)
    box_w, box_h = 0.15, 0.34
    gap = (1 - n * box_w) / (n + 1)
    y = 0.30

    xs = []
    for i, (title, sub, color) in enumerate(stages):
        x = gap + i * (box_w + gap)
        xs.append(x)
        text_color = OCEAN_TEAL if color in (GOLDEN_YELLOW, WARM_GLOW, SOFT_SAGE) else WHITE
        rounded_box(ax, (x, y), box_w, box_h, color, text_color=text_color,
                    text=title, fontsize=13.5, sub=sub, subsize=10.5, sub_color=text_color)

    for i in range(n - 1):
        x1 = xs[i] + box_w
        x2 = xs[i + 1]
        arrow(ax, x1 + 0.005, y + box_h / 2, x2 - 0.005)

    fig.text(0.5, 0.10, "Each stage still exists today — MCP adds a governed layer, it does not erase the ones before it.",
              fontsize=11, color=OCEAN_TEAL, ha="center", va="center", style="italic", alpha=1.0)

    fig.savefig("visuals/34_hero.png", dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


# ---------------------------------------------------------------------------
# 2. Architecture: layered stack diagram
# ---------------------------------------------------------------------------
def make_architecture():
    fig, ax = plt.subplots(figsize=(9, 8.6), facecolor=WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    add_header_bar(fig, "A Governed MCP Architecture",
                    "Who talks to what, and in which order")

    layers = [
        ("Accountant", "Defines the question, reviews the answer", OCEAN_TEAL, WHITE),
        ("AI assistant or governed agent", "Interprets intent, selects approved tools", SEA_GREEN, WHITE),
        ("MCP server", "Exposes a defined, permissioned set of tools", GOLDEN_YELLOW, OCEAN_TEAL),
        ("ERP APIs, reports, databases,\nand business logic", "Where the real calculations and records live", BRIGHT_TEAL, WHITE),
        ("Financial and operational systems", "QuickBooks Online · Sage Intacct · NetSuite · Dynamics 365", DEEP_NAVY, WHITE),
    ]

    n = len(layers)
    box_h = 0.13
    gap = 0.045
    top = 0.86
    x0, w = 0.08, 0.84

    centers = []
    for i, (title, sub, color, text_color) in enumerate(layers):
        y = top - i * (box_h + gap) - box_h
        centers.append(y + box_h / 2)
        rounded_box(ax, (x0, y), w, box_h, color, text_color=text_color,
                    text=title, fontsize=13, sub=sub, subsize=10, sub_color=text_color)

    for i in range(n - 1):
        y1 = centers[i] - box_h / 2
        y2 = centers[i + 1] + box_h / 2
        ax.annotate("", xy=(0.5, y2 + 0.008), xytext=(0.5, y1 - 0.008),
                    arrowprops=dict(arrowstyle="-|>", color=OCEAN_TEAL, lw=2.2,
                                    mutation_scale=16), zorder=1)

    fig.savefig("visuals/34_architecture.png", dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


# ---------------------------------------------------------------------------
# 3. Maturity stages: Retrieve -> ... -> Execute
# ---------------------------------------------------------------------------
def make_maturity_stages():
    fig, ax = plt.subplots(figsize=(13, 4.6), facecolor=WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    add_header_bar(fig, "The Safest Progression",
                    "Resist the temptation to skip straight to “Execute”")

    stages = [
        ("Retrieve", SEA_GREEN),
        ("Analyze", BRIGHT_TEAL),
        ("Recommend", GOLDEN_YELLOW),
        ("Prepare", WARM_GLOW),
        ("Approve", ALERT_ORANGE),
        ("Execute", ALERT_RED),
    ]
    n = len(stages)
    box_w, box_h = 0.135, 0.30
    gap = (1 - n * box_w) / (n + 1)
    y = 0.33

    xs = []
    for i, (title, color) in enumerate(stages):
        x = gap + i * (box_w + gap)
        xs.append(x)
        text_color = OCEAN_TEAL if color in (GOLDEN_YELLOW, WARM_GLOW) else WHITE
        rounded_box(ax, (x, y), box_w, box_h, color, text_color=text_color, text=title, fontsize=13)

    for i in range(n - 1):
        arrow(ax, xs[i] + box_w + 0.004, y + box_h / 2, xs[i + 1] - 0.004)

    fig.text(0.5, 0.11,
              "Most accounting workflows should live comfortably in the first three stages for a long time.",
              fontsize=11, color=OCEAN_TEAL, ha="center", va="center", style="italic", alpha=1.0)

    fig.savefig("visuals/34_maturity_stages.png", dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


# ---------------------------------------------------------------------------
# 4. Social square: condensed evolution graphic for LinkedIn / X
# ---------------------------------------------------------------------------
def make_social_square():
    fig, ax = plt.subplots(figsize=(8, 8), facecolor=WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    header_h = 0.20
    bar = FancyBboxPatch((0, 1 - header_h), 1, header_h, boxstyle="square,pad=0",
                          facecolor=DEEP_NAVY, edgecolor="none", zorder=0)
    ax.add_patch(bar)
    fig.text(0.06, 1 - header_h / 2 + 0.03, "From ERP Menus\nto AI Agents", fontsize=22, fontweight="bold",
              color=WHITE, va="center", ha="left", linespacing=1.3)
    fig.text(0.06, 1 - header_h - 0.035, "What MCP could mean for accounting",
              fontsize=12, color=OCEAN_TEAL, va="top", ha="left", style="italic")

    stages = [
        ("ERP Menus", OCEAN_TEAL),
        ("Reports", SEA_GREEN),
        ("APIs", BRIGHT_TEAL),
        ("MCP", GOLDEN_YELLOW),
        ("AI Agents", SOFT_SAGE),
    ]
    n = len(stages)
    box_h = 0.095
    gap = 0.035
    top = 1 - header_h - 0.12
    x0, w = 0.08, 0.84

    ys = []
    for i, (title, color) in enumerate(stages):
        y = top - i * (box_h + gap) - box_h
        ys.append(y + box_h / 2)
        text_color = OCEAN_TEAL if color in (GOLDEN_YELLOW, WARM_GLOW) else WHITE
        rounded_box(ax, (x0, y), w, box_h, color, text_color=text_color, text=title, fontsize=15)

    for i in range(n - 1):
        y1 = ys[i] - box_h / 2
        y2 = ys[i + 1] + box_h / 2
        ax.annotate("", xy=(0.5, y2 + 0.006), xytext=(0.5, y1 - 0.006),
                    arrowprops=dict(arrowstyle="-|>", color=OCEAN_TEAL, lw=2.4,
                                    mutation_scale=16), zorder=1)

    fig.text(0.5, 0.045, "PythonMuse LLC · pythonmuse.com", fontsize=10,
              color=OCEAN_TEAL, ha="center", va="center", alpha=0.85)

    fig.savefig("visuals/34_social_square.png", dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


if __name__ == "__main__":
    make_hero()
    make_architecture()
    make_maturity_stages()
    make_social_square()
    print("Generated: 34_hero.png, 34_architecture.png, 34_maturity_stages.png, 34_social_square.png")
