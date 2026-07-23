"""
Generate article visuals for Article 20d — GitHub vs. The Shared Drive

Produces the following PNGs saved to visuals/:
  20d_hero.png            — split-screen: cluttered shared drive vs. a clean Git history panel
  20d_diff_comparison.png — same formula change: invisible in Excel vs. an explicit diff in Git

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
# 20d_hero.png — Shared drive chaos vs. Git history clarity
# ─────────────────────────────────────────────────────────────
def make_hero():
    fig = plt.figure(figsize=(13, 7), facecolor=WHITE)
    add_header_bar(fig, "GitHub vs. The Shared Drive  |  Article 20d  |  PythonMuse LLC")
    add_footer(fig)

    ax = fig.add_axes([0.03, 0.10, 0.94, 0.82])
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5.5)
    ax.axis("off")
    ax.set_facecolor(WHITE)

    # ── LEFT: Shared Drive ────────────────────────────────────
    card(ax, 0.1, 0.3, 5.2, 4.8, facecolor=LIGHT_GRAY, edgecolor=ALERT_RED, radius=0.1)
    card(ax, 0.1, 4.5, 5.2, 0.6, facecolor=ALERT_RED, radius=0.08)
    ax.text(2.7, 4.8, "THE SHARED DRIVE", ha="center", va="center",
            fontsize=12, color=WHITE, fontweight="bold")

    left_lines = [
        "Susan overwrites the file.",
        "Author: maybe recorded.",
        "Reason: hopefully an email.",
        "What changed: re-read the",
        "  whole file to spot it.",
        "Undo: only if someone kept",
        "  a copy.",
    ]
    for i, line in enumerate(left_lines):
        y_pos = 4.05 - i * 0.5
        ax.text(0.45, y_pos, line, ha="left", va="center",
                fontsize=10, color=DEEP_NAVY, fontfamily="monospace")

    ax.text(2.7, 0.62, '"We\'ll get back to you."',
            ha="center", va="center", fontsize=9.5,
            color=ALERT_RED, style="italic")

    # ── VS divider ────────────────────────────────────────────
    ax.text(6.0, 2.75, "VS", ha="center", va="center",
            fontsize=22, color=DEEP_NAVY, fontweight="bold", alpha=0.25)

    # ── RIGHT: Git / GitHub ───────────────────────────────────
    card(ax, 6.7, 0.3, 5.1, 4.8, facecolor=LIGHT_GRAY, edgecolor=BRIGHT_TEAL, radius=0.1)
    card(ax, 6.7, 4.5, 5.1, 0.6, facecolor=BRIGHT_TEAL, radius=0.08)
    ax.text(9.25, 4.8, "GIT / GITHUB", ha="center", va="center",
            fontsize=12, color=DEEP_NAVY, fontweight="bold")

    right_lines = [
        "Susan saves a commit.",
        "Author: always recorded.",
        "Reason: a commit message,",
        "  tied to the change forever.",
        "What changed: exact",
        "  line-by-line diff.",
        "Undo: always. One click.",
    ]
    for i, line in enumerate(right_lines):
        y_pos = 4.05 - i * 0.5
        ax.text(6.95, y_pos, line, ha="left", va="center",
                fontsize=10, color=OCEAN_TEAL, fontweight="bold", fontfamily="monospace")

    ax.text(9.25, 0.62, '"Here\'s the exact commit."',
            ha="center", va="center", fontsize=9.5,
            color=SEA_GREEN, style="italic")

    save(fig, "20d_hero.png")


# ─────────────────────────────────────────────────────────────
# 20d_diff_comparison.png — Excel formula change (invisible) vs. Git diff (explicit)
# ─────────────────────────────────────────────────────────────
def make_diff_comparison():
    fig = plt.figure(figsize=(13, 7), facecolor=WHITE)
    add_header_bar(fig, "Same Change, Two Tools  |  Article 20d  |  PythonMuse LLC")
    add_footer(fig)

    ax = fig.add_axes([0.03, 0.10, 0.94, 0.82])
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.4)
    ax.axis("off")
    ax.set_facecolor(WHITE)

    # ── LEFT: Excel ───────────────────────────────────────────
    card(ax, 0.1, 0.3, 5.2, 5.5, facecolor=LIGHT_GRAY, edgecolor=ALERT_RED, radius=0.08)
    card(ax, 0.1, 5.1, 5.2, 0.7, facecolor=ALERT_RED, radius=0.06)
    ax.text(2.7, 5.45, "EXCEL", ha="center", va="center",
            fontsize=12, color=WHITE, fontweight="bold")

    # formula bar
    card(ax, 0.35, 4.35, 4.7, 0.55, facecolor=WHITE, edgecolor=DEEP_NAVY, radius=0.03)
    ax.text(0.55, 4.62, "fx   =SUM(B2:B12)", ha="left", va="center",
            fontsize=11, color=DEEP_NAVY, fontfamily="monospace")

    # mock grid
    grid_top = 4.1
    for r in range(4):
        y0 = grid_top - r * 0.62
        fill = WHITE if r % 2 == 0 else LIGHT_GRAY
        card(ax, 0.35, y0 - 0.55, 4.7, 0.55, facecolor=fill, edgecolor="#DDDDDD", radius=0.0)
        label = "184,205" if r == 1 else f"row {r+1} data"
        color = DEEP_NAVY
        weight = "bold" if r == 1 else "normal"
        ax.text(0.6, y0 - 0.28, label, ha="left", va="center",
                fontsize=10.5, color=color, fontweight=weight, fontfamily="monospace")

    ax.text(2.7, 0.68, "Nothing on the sheet says this changed.",
            ha="center", va="center", fontsize=10.5,
            color=ALERT_RED, style="italic")

    # ── VS divider ────────────────────────────────────────────
    ax.text(6.0, 3.2, "VS", ha="center", va="center",
            fontsize=22, color=DEEP_NAVY, fontweight="bold", alpha=0.25)

    # ── RIGHT: Git diff ───────────────────────────────────────
    card(ax, 6.7, 0.3, 5.1, 5.5, facecolor=MIDNIGHT_TEAL, edgecolor=BRIGHT_TEAL, radius=0.08)
    card(ax, 6.7, 5.1, 5.1, 0.7, facecolor=BRIGHT_TEAL, radius=0.06)
    ax.text(9.25, 5.45, "GIT DIFF", ha="center", va="center",
            fontsize=12, color=DEEP_NAVY, fontweight="bold")

    diff_lines = [
        (" ", "def variance_total(df):", WHITE),
        ("-", "    return df['B'][1:10].sum()", ALERT_RED),
        ("+", "    return df['B'][1:12].sum()", SOFT_SAGE),
        (" ", "", WHITE),
        (" ", "# 2 lines changed, 1 file", WARM_GLOW),
    ]
    for i, (marker, text, color) in enumerate(diff_lines):
        y_pos = 4.55 - i * 0.55
        bg = None
        if marker == "-":
            bg = "#5A2A2A"
        elif marker == "+":
            bg = "#2A4A3A"
        if bg:
            card(ax, 6.85, y_pos - 0.24, 4.8, 0.44, facecolor=bg, radius=0.0)
        ax.text(6.95, y_pos, f"{marker} {text}", ha="left", va="center",
                fontsize=10.5, color=color, fontfamily="monospace")

    ax.text(9.25, 0.68, "The change is explicit — line by line.",
            ha="center", va="center", fontsize=10.5,
            color=SOFT_SAGE, style="italic")

    save(fig, "20d_diff_comparison.png")


if __name__ == "__main__":
    print("Generating Article 20d visuals...")
    make_hero()
    make_diff_comparison()
    print("Done.")
