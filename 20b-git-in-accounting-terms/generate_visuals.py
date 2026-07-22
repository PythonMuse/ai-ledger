"""
Generate article visuals for Article 20b — Git Explained Using Accounting Terms

Produces the following PNG saved to visuals/:
  20b_hero.png — the Rosetta Stone: accounting term next to its Git equivalent

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
# 20b_hero.png — The Rosetta Stone: Accounting term <-> Git term
# ─────────────────────────────────────────────────────────────
def make_hero():
    fig = plt.figure(figsize=(13, 7), facecolor=WHITE)
    add_header_bar(fig, "Git Explained Using Accounting Terms  |  Article 20b  |  PythonMuse LLC")
    add_footer(fig)

    ax = fig.add_axes([0.03, 0.10, 0.94, 0.82])
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.5)
    ax.axis("off")
    ax.set_facecolor(WHITE)

    rows = [
        ("A workpaper folder",              "Repository"),
        ("A journal entry",                 "Commit"),
        ("The JE explanation / memo",        "Commit message"),
        ("The audit trail",                 "Git log / history"),
        ("A scenario / draft budget",        "Branch"),
        ("The review-and-approval workflow", "Pull request"),
        ("A correcting entry",              "Revert"),
    ]

    # Column headers
    card(ax, 0.2, 5.75, 5.4, 0.55, facecolor=DEEP_NAVY, radius=0.06)
    card(ax, 6.4, 5.75, 5.4, 0.55, facecolor=BRIGHT_TEAL, radius=0.06)
    ax.text(2.9, 6.02, "What Accountants Call It", ha="center", va="center",
            fontsize=12.5, color=WHITE, fontweight="bold")
    ax.text(9.1, 6.02, "Git Concept", ha="center", va="center",
            fontsize=12.5, color=DEEP_NAVY, fontweight="bold")

    row_h = 0.72
    top_y = 5.55
    for i, (acct, git) in enumerate(rows):
        y_pos = top_y - i * row_h
        fill = LIGHT_GRAY if i % 2 == 0 else WHITE
        card(ax, 0.2, y_pos - row_h + 0.08, 5.4, row_h - 0.08, facecolor=fill, edgecolor=LIGHT_GRAY, radius=0.03)
        card(ax, 6.4, y_pos - row_h + 0.08, 5.4, row_h - 0.08, facecolor=fill, edgecolor=LIGHT_GRAY, radius=0.03)
        ax.text(0.5, y_pos - row_h / 2 + 0.04, acct, ha="left", va="center",
                fontsize=11, color=DEEP_NAVY)
        ax.text(6.7, y_pos - row_h / 2 + 0.04, git, ha="left", va="center",
                fontsize=11, color=OCEAN_TEAL, fontweight="bold")
        ax.text(6.0, y_pos - row_h / 2 + 0.04, "=", ha="center", va="center",
                fontsize=13, color=OCEAN_TEAL, fontweight="bold")

    save(fig, "20b_hero.png")


if __name__ == "__main__":
    print("Generating Article 20b visuals...")
    make_hero()
    print("Done.")
