"""
Generate article visuals for Article 20c — How Finance Teams Should Structure AI Repositories

Produces the following PNG saved to visuals/:
  20c_hero.png — the finance-close/ folder skeleton, styled like a VS Code file explorer

Branding: white background, Deep Navy text, Bright Teal / Golden Yellow accents.
Per SKILL.md — Matplotlib Visuals (Article Charts).
DPI: 180. Font sizes follow SKILL.md minimums.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(SCRIPT_DIR, "visuals")
os.makedirs(OUT_DIR, exist_ok=True)

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
LIGHT_GRAY    = "#F5F5F5"

FOOTER_TEXT = "PythonMuse LLC  |  pythonmuse.com"
FOOTER_URL  = "github.com/PythonMuse/ai-ledger"


def save(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=180, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  saved -> {path}")


def add_footer(fig, y_bar=0.0, bar_h=0.065):
    bar = fig.add_axes([0.0, y_bar, 1.0, bar_h])
    bar.set_xlim(0, 1); bar.set_ylim(0, 1)
    bar.set_axis_off()
    bar.add_patch(FancyBboxPatch((0, 0), 1, 1, boxstyle="square,pad=0",
                                 facecolor=DEEP_NAVY, edgecolor="none",
                                 transform=bar.transAxes))
    bar.text(0.5, 0.55, FOOTER_TEXT,
             ha="center", va="center", fontsize=10, color=WHITE, fontweight="bold",
             transform=bar.transAxes)
    bar.text(0.5, 0.18, FOOTER_URL,
             ha="center", va="center", fontsize=9, color=BRIGHT_TEAL,
             transform=bar.transAxes)


def add_header_bar(fig, label, y_bar=0.935, bar_h=0.065):
    bar = fig.add_axes([0.0, y_bar, 1.0, bar_h])
    bar.set_xlim(0, 1); bar.set_ylim(0, 1)
    bar.set_axis_off()
    bar.add_patch(FancyBboxPatch((0, 0), 1, 1, boxstyle="square,pad=0",
                                 facecolor=DEEP_NAVY, edgecolor="none",
                                 transform=bar.transAxes))
    bar.text(0.5, 0.5, label,
             ha="center", va="center", fontsize=12, color=GOLDEN_YELLOW, fontweight="bold",
             transform=bar.transAxes)


def card(ax, x, y, w, h, facecolor, edgecolor=None, alpha=1.0, radius=0.03):
    ec = edgecolor or facecolor
    patch = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={radius}",
                            facecolor=facecolor, edgecolor=ec, linewidth=1.5, alpha=alpha)
    ax.add_patch(patch)
    return patch


# ─────────────────────────────────────────────────────────────
# 20c_hero.png — Finance repo skeleton, VS Code explorer style
# ─────────────────────────────────────────────────────────────
def make_hero():
    fig = plt.figure(figsize=(13, 7), facecolor=WHITE)
    add_header_bar(fig, "How Finance Teams Should Structure AI Repositories  |  Article 20c  |  PythonMuse LLC")
    add_footer(fig)

    ax = fig.add_axes([0.20, 0.10, 0.60, 0.80])
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 7.2)
    ax.axis("off")
    ax.set_facecolor(WHITE)

    # Explorer sidebar panel
    card(ax, 0.2, 0.3, 7.6, 6.6, facecolor=MIDNIGHT_TEAL, radius=0.05)
    ax.text(0.6, 6.55, "EXPLORER", ha="left", va="center",
            fontsize=10.5, color=WARM_GLOW, fontweight="bold", alpha=0.85)

    rows = [
        (0, "finance-close/",  BRIGHT_TEAL, True),
        (1, "data/",           BRIGHT_TEAL, True),
        (2, "raw/",            GOLDEN_YELLOW, False),
        (2, "processed/",      GOLDEN_YELLOW, False),
        (1, "scripts/",        BRIGHT_TEAL, True),
        (1, "prompts/",        BRIGHT_TEAL, True),
        (1, "outputs/",        BRIGHT_TEAL, True),
        (1, "evidence/",       BRIGHT_TEAL, True),
        (1, "skills/",         BRIGHT_TEAL, True),
        (1, "agents/",         BRIGHT_TEAL, True),
        (1, "docs/",           BRIGHT_TEAL, True),
        (1, ".gitignore",      WHITE, False),
        (1, "README.md",       WHITE, False),
    ]

    top_y = 6.05
    row_h = 0.445
    for i, (depth, label, color, is_dir) in enumerate(rows):
        y_pos = top_y - i * row_h
        x_pos = 0.65 + depth * 0.55
        weight = "bold" if is_dir else "normal"
        ax.text(x_pos, y_pos, label, ha="left", va="center",
                fontsize=11.5, color=color, fontweight=weight, fontfamily="monospace",
                alpha=1.0)

    save(fig, "20c_hero.png")


if __name__ == "__main__":
    print("Generating Article 20c visuals...")
    make_hero()
    print("Done.")
