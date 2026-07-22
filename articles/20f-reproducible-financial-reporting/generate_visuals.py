"""
Generate article visuals for Article 20f — Reproducible Financial Reporting

Produces the following PNG saved to visuals/:
  20f_hero.png — the v2026-04-close tag as a sealed audit folder, fed by the repo's inputs

Branding: white background, Deep Navy text, Bright Teal / Golden Yellow accents.
Per SKILL.md — Matplotlib Visuals (Article Charts).
DPI: 180. Font sizes follow SKILL.md minimums.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
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
# 20f_hero.png — The tag as a sealed, reproducible snapshot
# ─────────────────────────────────────────────────────────────
def make_hero():
    fig = plt.figure(figsize=(13, 7), facecolor=WHITE)
    add_header_bar(fig, "Reproducible Financial Reporting  |  Article 20f  |  PythonMuse LLC")
    add_footer(fig)

    ax = fig.add_axes([0.03, 0.10, 0.94, 0.82])
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.5)
    ax.axis("off")
    ax.set_facecolor(WHITE)

    inputs = ["data/raw/", "scripts/", "prompts/", "outputs/", "commit history"]
    n = len(inputs)
    total_w = 10.6
    gap = 0.3
    box_w = (total_w - gap * (n - 1)) / n
    y_top = 5.6
    for i, label in enumerate(inputs):
        x0 = 0.7 + i * (box_w + gap)
        card(ax, x0, y_top, box_w, 0.75, facecolor=LIGHT_GRAY, edgecolor=OCEAN_TEAL, radius=0.06)
        ax.text(x0 + box_w / 2, y_top + 0.375, label, ha="center", va="center",
                fontsize=10, color=DEEP_NAVY, fontweight="bold", fontfamily="monospace")
        cx = x0 + box_w / 2
        ax.annotate("", xy=(6.0, 3.9), xytext=(cx, y_top - 0.05),
                    arrowprops=dict(arrowstyle="->", color=OCEAN_TEAL, lw=1.2, alpha=0.7))

    # The seal
    seal = Circle((6.0, 3.0), 1.35, facecolor=DEEP_NAVY, edgecolor=GOLDEN_YELLOW, linewidth=4, zorder=3)
    ax.add_patch(seal)
    ax.text(6.0, 3.25, "v2026-04-close", ha="center", va="center",
            fontsize=13, color=GOLDEN_YELLOW, fontweight="bold", zorder=4)
    ax.text(6.0, 2.75, "sealed & frozen", ha="center", va="center",
            fontsize=9.5, color=WHITE, style="italic", zorder=4)

    ax.text(6.0, 1.0, "Rerun the workflow. Get the same numbers.",
            ha="center", va="center", fontsize=13, color=OCEAN_TEAL,
            fontweight="bold", style="italic")

    save(fig, "20f_hero.png")


if __name__ == "__main__":
    print("Generating Article 20f visuals...")
    make_hero()
    print("Done.")
