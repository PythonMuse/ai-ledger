"""
Generate article visuals for Article 20a — The FINAL_v2.xlsx Disaster

Produces the following PNG saved to visuals/:
  20a_hero.png — the shared-drive filename cascade, with the tagline that ties the series together

Branding: white background, Deep Navy text, Bright Teal / Golden Yellow accents.
Per SKILL.md — Matplotlib Visuals (Article Charts).
DPI: 180. Font sizes follow SKILL.md minimums.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import os

# ── Output directory ──────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(SCRIPT_DIR, "visuals")
os.makedirs(OUT_DIR, exist_ok=True)

# ── PythonMuse brand colors ───────────────────────────────────
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
# 20a_hero.png — The shared-drive folder, one file highlighted
# ─────────────────────────────────────────────────────────────
def make_hero():
    fig = plt.figure(figsize=(13, 7), facecolor=WHITE)
    add_header_bar(fig, "The FINAL_v2.xlsx Disaster  |  Article 20a  |  PythonMuse LLC")
    add_footer(fig)

    ax = fig.add_axes([0.15, 0.14, 0.70, 0.76])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.5)
    ax.axis("off")
    ax.set_facecolor(WHITE)

    # Folder window
    card(ax, 0.3, 1.0, 9.4, 5.2, facecolor=LIGHT_GRAY, edgecolor=ALERT_RED, radius=0.08)
    card(ax, 0.3, 5.5, 9.4, 0.7, facecolor=ALERT_RED, radius=0.06)
    ax.text(5.0, 5.85, "2026 Budget", ha="center", va="center",
            fontsize=14, color=WHITE, fontweight="bold")

    files = [
        "Budget_FINAL.xlsx",
        "Budget_FINAL_v2.xlsx",
        "Budget_FINAL_v2_REAL.xlsx",
        "Budget_FINAL_v2_REAL_USE_THIS_ONE.xlsx",
    ]
    for i, fname in enumerate(files):
        y_pos = 4.6 - i * 0.85
        is_last = i == len(files) - 1
        color = ALERT_RED if is_last else DEEP_NAVY
        weight = "bold" if is_last else "normal"
        ax.text(0.75, y_pos, fname, ha="left", va="center",
                fontsize=11.5, color=color, fontfamily="monospace", fontweight=weight)
        if is_last:
            ax.annotate("the one everyone\nkeeps using",
                        xy=(8.0, y_pos), xytext=(8.0, y_pos - 1.1),
                        ha="center", va="top", fontsize=9.5, color=ALERT_RED,
                        style="italic",
                        arrowprops=dict(arrowstyle="->", color=ALERT_RED, lw=1.5))

    save(fig, "20a_hero.png")


if __name__ == "__main__":
    print("Generating Article 20a visuals...")
    make_hero()
    print("Done.")
