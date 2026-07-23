"""
Generate article visuals for Article 20e — Pull Requests Are Internal Controls

Produces the following PNGs saved to visuals/:
  20e_hero.png         — a PR review card annotated with the accounting controls it maps to
  20e_coso_mapping.png — the five COSO components mapped to pull request mechanics

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
# 20e_hero.png — PR review card, annotated with accounting controls
# ─────────────────────────────────────────────────────────────
def make_hero():
    fig = plt.figure(figsize=(13, 7), facecolor=WHITE)
    add_header_bar(fig, "Pull Requests Are Internal Controls  |  Article 20e  |  PythonMuse LLC")
    add_footer(fig)

    ax = fig.add_axes([0.03, 0.10, 0.94, 0.82])
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.6)
    ax.axis("off")
    ax.set_facecolor(WHITE)

    # PR window card
    card(ax, 2.6, 0.35, 6.8, 5.9, facecolor=LIGHT_GRAY, edgecolor=DEEP_NAVY, radius=0.06)
    card(ax, 2.6, 5.65, 6.8, 0.6, facecolor=DEEP_NAVY, radius=0.05)
    ax.text(6.0, 5.95, "Pull Request:  recon/exception-handler-v2",
            ha="center", va="center", fontsize=11.5, color=WHITE, fontweight="bold",
            fontfamily="monospace")

    checklist = [
        "What changed?  →  diff (automatic)",
        "Why?  →  PR description",
        "What produced it?  →  linked prompt",
        "How was it tested?  →  tie-out results",
    ]
    for i, item in enumerate(checklist):
        y_pos = 5.05 - i * 0.62
        ax.text(2.95, y_pos, "✓", ha="left", va="center",
                fontsize=13, color=SEA_GREEN, fontweight="bold")
        ax.text(3.35, y_pos, item, ha="left", va="center",
                fontsize=10.5, color=DEEP_NAVY)

    # Approval stamp
    card(ax, 6.6, 0.65, 2.5, 0.85, facecolor=SOFT_SAGE, radius=0.08)
    ax.text(7.85, 1.075, "APPROVED", ha="center", va="center",
            fontsize=13, color=DEEP_NAVY, fontweight="bold")

    # Left-side control annotations pointing into the PR
    left_labels = [
        ("Preparer", 5.3),
        ("Reviewer", 4.0),
        ("Segregation\nof Duties", 2.6),
        ("Audit Trail", 1.1),
    ]
    for label, y_pos in left_labels:
        ax.text(0.2, y_pos, label, ha="left", va="center",
                fontsize=10, color=OCEAN_TEAL, fontweight="bold", linespacing=1.3)
        ax.annotate("", xy=(2.55, y_pos), xytext=(1.55, y_pos),
                    arrowprops=dict(arrowstyle="->", color=OCEAN_TEAL, lw=1.4))

    save(fig, "20e_hero.png")


# ─────────────────────────────────────────────────────────────
# 20e_coso_mapping.png — COSO components <-> pull request mechanics
# ─────────────────────────────────────────────────────────────
def make_coso_mapping():
    fig = plt.figure(figsize=(13, 8), facecolor=WHITE)
    add_header_bar(fig, "COSO Meets the Pull Request  |  Article 20e  |  PythonMuse LLC")
    add_footer(fig)

    ax = fig.add_axes([0.03, 0.08, 0.94, 0.84])
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7.4)
    ax.axis("off")
    ax.set_facecolor(WHITE)

    rows = [
        ("Control Environment", "Branch protection rules + written PR template"),
        ("Risk Assessment", "\"What does this change affect?\" section of the PR"),
        ("Control Activities", "Required approvals, required test results"),
        ("Information &\nCommunication", "PR comments, linked tickets, linked prompts"),
        ("Monitoring", "Audit report of every merged PR over a period"),
    ]

    # Column headers
    card(ax, 0.2, 6.6, 5.4, 0.6, facecolor=DEEP_NAVY, radius=0.06)
    card(ax, 6.4, 6.6, 5.4, 0.6, facecolor=BRIGHT_TEAL, radius=0.06)
    ax.text(2.9, 6.9, "COSO Component", ha="center", va="center",
            fontsize=12.5, color=WHITE, fontweight="bold")
    ax.text(9.1, 6.9, "Pull Request Mechanic", ha="center", va="center",
            fontsize=12.5, color=DEEP_NAVY, fontweight="bold")

    row_h = 1.18
    top_y = 6.45
    for i, (coso, pr) in enumerate(rows):
        y_pos = top_y - i * row_h
        fill = LIGHT_GRAY if i % 2 == 0 else WHITE
        card(ax, 0.2, y_pos - row_h + 0.1, 5.4, row_h - 0.12, facecolor=fill, edgecolor=LIGHT_GRAY, radius=0.03)
        card(ax, 6.4, y_pos - row_h + 0.1, 5.4, row_h - 0.12, facecolor=fill, edgecolor=LIGHT_GRAY, radius=0.03)
        mid_y = y_pos - row_h / 2 + 0.04
        ax.text(0.5, mid_y, coso, ha="left", va="center",
                fontsize=11.5, color=DEEP_NAVY, fontweight="bold", linespacing=1.3)
        ax.text(6.7, mid_y, pr, ha="left", va="center",
                fontsize=11, color=OCEAN_TEAL, linespacing=1.3, wrap=True)
        ax.text(6.0, mid_y, "→", ha="center", va="center",
                fontsize=15, color=OCEAN_TEAL, fontweight="bold")

    save(fig, "20e_coso_mapping.png")


if __name__ == "__main__":
    print("Generating Article 20e visuals...")
    make_hero()
    make_coso_mapping()
    print("Done.")
