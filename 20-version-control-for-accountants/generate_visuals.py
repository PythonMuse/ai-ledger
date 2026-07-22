"""
Generate article visuals for the Article 20 series hub — Version Control for Accountants in the AI Era

Produces the following PNG saved to visuals/:
  20_series_hero.png — the 6-part roadmap, chaos (20a) to reproducibility (20f)

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
# 20_series_hero.png — 6-part roadmap, chaos to reproducibility
# ─────────────────────────────────────────────────────────────
def make_hero():
    fig = plt.figure(figsize=(13, 7), facecolor=WHITE)
    add_header_bar(fig, "Version Control for Accountants in the AI Era  |  6-Part Series  |  PythonMuse LLC")
    add_footer(fig)

    ax = fig.add_axes([0.03, 0.12, 0.94, 0.78])
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.0)
    ax.axis("off")
    ax.set_facecolor(WHITE)

    parts = [
        ("20a", "The FINAL_v2.xlsx\nDisaster",         ALERT_RED,     WHITE),
        ("20b", "Git in\nAccounting Terms",             ALERT_ORANGE,  WHITE),
        ("20c", "Structuring\nAI Repositories",          GOLDEN_YELLOW, DEEP_NAVY),
        ("20d", "GitHub vs.\nThe Shared Drive",          SOFT_SAGE,     DEEP_NAVY),
        ("20e", "Pull Requests\nAre Controls",           SEA_GREEN,     WHITE),
        ("20f", "Reproducible\nFinancial Reporting",     BRIGHT_TEAL,   DEEP_NAVY),
    ]

    n = len(parts)
    gap = 0.25
    box_w = (12 - gap * (n - 1)) / n
    y0, h = 2.7, 2.2

    for i, (part, title, color, text_color) in enumerate(parts):
        x0 = i * (box_w + gap)
        card(ax, x0, y0, box_w, h, facecolor=color, radius=0.06)
        ax.text(x0 + box_w / 2, y0 + h - 0.42, part, ha="center", va="center",
                fontsize=13, color=text_color, fontweight="bold")
        ax.text(x0 + box_w / 2, y0 + h / 2 - 0.25, title, ha="center", va="center",
                fontsize=9.5, color=text_color, fontweight="bold", linespacing=1.4)
        if i < n - 1:
            ax.annotate("", xy=(x0 + box_w + gap - 0.03, y0 + h / 2),
                        xytext=(x0 + box_w + 0.03, y0 + h / 2),
                        arrowprops=dict(arrowstyle="->", color=DEEP_NAVY, lw=1.6, alpha=0.55))

    ax.text(6.0, 5.5, "We already had a version control problem. AI just exposed it.",
            ha="center", va="center", fontsize=14, color=DEEP_NAVY, fontweight="bold")
    ax.text(6.0, 1.2, "Read top to bottom — each article builds on the one before it.",
            ha="center", va="center", fontsize=10.5, color=OCEAN_TEAL, style="italic")

    save(fig, "20_series_hero.png")


if __name__ == "__main__":
    print("Generating Article 20 series hub visuals...")
    make_hero()
    print("Done.")
