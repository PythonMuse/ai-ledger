"""
Generate Article 22 visuals -- The Workings Layer: Fitting AI Into the Files You Can't Change.

Visual 01: Hero / front image -- title card
Visual 02: Folder Hierarchy Diagram -- CLAUDE.md + workings/ safe zone with annotations

Footer on every visual: PythonMuse LLC  |  github.com/PythonMuse
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import os

# ── Output directory ───────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR    = os.path.join(SCRIPT_DIR, "visuals")
os.makedirs(OUT_DIR, exist_ok=True)

# ── Brand colors (SKILL.md standard block) ────────────────────────────────────
DEEP_NAVY     = "#002639"
MIDNIGHT_TEAL = "#003144"
BRIGHT_TEAL   = "#3ABFB9"
GOLDEN_YELLOW = "#FFD75E"
WARM_GLOW     = "#F5D384"
OCEAN_TEAL    = "#005F6F"
SOFT_SAGE     = "#91BE8E"
SEA_GREEN     = "#2BA19A"
WHITE         = "#FFFFFF"
LIGHT_GRAY    = "#F5F5F5"
ALERT_RED     = "#E05252"
ALERT_ORANGE  = "#E07D3B"

FOOTER_TEXT = "PythonMuse LLC   |   github.com/PythonMuse"


def rbox(ax, x, y, w, h, fc, ec=DEEP_NAVY, lw=1.5, r=0.10, zorder=2):
    patch = FancyBboxPatch((x, y), w, h,
                           boxstyle=f"round,pad=0,rounding_size={r}",
                           facecolor=fc, edgecolor=ec, linewidth=lw, zorder=zorder)
    ax.add_patch(patch)


def add_footer(ax, xmax, ymin):
    bar = FancyBboxPatch((0, ymin), xmax, 0.50,
                         boxstyle="square,pad=0",
                         facecolor=DEEP_NAVY, edgecolor="none", zorder=10)
    ax.add_patch(bar)
    ax.text(xmax / 2, ymin + 0.25, FOOTER_TEXT,
            ha="center", va="center",
            fontsize=12, color=WHITE, zorder=11)


# ──────────────────────────────────────────────────────────────────────────────
# Visual 01: Hero / front image
# ──────────────────────────────────────────────────────────────────────────────
def make_hero():
    W, H = 14, 7
    fig, ax = plt.subplots(figsize=(W, H))
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")

    # ── Top accent bar ────────────────────────────────────────────────────────
    ax.add_patch(FancyBboxPatch((0, H - 1.0), W, 1.0,
                                boxstyle="square,pad=0",
                                facecolor=DEEP_NAVY, edgecolor="none", zorder=1))
    ax.text(W / 2, H - 0.5, "PythonMuse LLC  |  AI in Accounting",
            ha="center", va="center", fontsize=14, color=BRIGHT_TEAL, zorder=2)

    # ── Title ─────────────────────────────────────────────────────────────────
    ax.text(W / 2, 5.05, "The Workings Layer Method",
            ha="center", va="center",
            fontsize=28, fontweight="bold", color=DEEP_NAVY, zorder=3)

    # ── Subtitle ──────────────────────────────────────────────────────────────
    ax.text(W / 2, 4.20, "Fit AI into the files you can't change",
            ha="center", va="center",
            fontsize=16, style="italic", color=OCEAN_TEAL, zorder=3)

    # ── Divider ───────────────────────────────────────────────────────────────
    ax.plot([2.0, W - 2.0], [3.70, 3.70], color=BRIGHT_TEAL, linewidth=2.5)

    # ── Rule chips (two-line labels so text fits comfortably) ─────────────────
    chip_labels = [
        "Don't touch\nlegacy files",
        "Define scope\nwith CLAUDE.md",
        "Work inside\nworkings/",
    ]
    chip_colors = [GOLDEN_YELLOW, BRIGHT_TEAL, SOFT_SAGE]
    chip_w, chip_h = 3.7, 0.80
    chip_y = 2.45
    starts_x = [0.95, 5.15, 9.35]

    for label, color, sx in zip(chip_labels, chip_colors, starts_x):
        ax.add_patch(FancyBboxPatch((sx, chip_y), chip_w, chip_h,
                                    boxstyle="round,pad=0.1",
                                    facecolor=color, edgecolor="none", zorder=4))
        ax.text(sx + chip_w / 2, chip_y + chip_h / 2, label,
                ha="center", va="center",
                fontsize=12, fontweight="bold", color=DEEP_NAVY,
                linespacing=1.35, zorder=5)

    # ── Tagline box ───────────────────────────────────────────────────────────
    ax.add_patch(FancyBboxPatch((2.5, 1.10), 9.0, 0.70,
                                boxstyle="round,pad=0.1",
                                facecolor=DEEP_NAVY, edgecolor="none", zorder=4))
    ax.text(W / 2, 1.45, "Layer on top. Break nothing.",
            ha="center", va="center",
            fontsize=15, style="italic", color=WHITE, zorder=5)

    # ── Footer ────────────────────────────────────────────────────────────────
    add_footer(ax, W, 0)

    fig.savefig(os.path.join(OUT_DIR, "22_visual_front.png"),
                dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print("Saved: 22_visual_front.png")


# ──────────────────────────────────────────────────────────────────────────────
# Visual 02: Folder Hierarchy Diagram
# ──────────────────────────────────────────────────────────────────────────────
def make_folder_hierarchy():
    fig, ax = plt.subplots(figsize=(14, 9))
    fig.patch.set_facecolor(LIGHT_GRAY)
    ax.set_facecolor(LIGHT_GRAY)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis("off")

    # ── Title ─────────────────────────────────────────────────────────────────
    ax.text(7, 8.45, "The Workings Layer Method",
            ha="center", va="center",
            fontsize=22, fontweight="bold", color=DEEP_NAVY, zorder=3)
    ax.text(7, 7.95, "Define scope with CLAUDE.md. Keep all new work inside workings/.",
            ha="center", va="center",
            fontsize=12, color=OCEAN_TEAL, style="italic", zorder=3)

    # ── Left column: legacy structure (untouched) ─────────────────────────────
    left_x = 0.6
    ax.text(left_x + 2.2, 7.35, "Legacy File Structure",
            ha="center", va="center",
            fontsize=14, fontweight="bold", color=DEEP_NAVY, zorder=3)

    legacy_items = [
        ("Budget/", MIDNIGHT_TEAL, 0),
        ("2024/", MIDNIGHT_TEAL, 1),
        ("2025/", MIDNIGHT_TEAL, 1),
        ("2026/", OCEAN_TEAL, 1),
        ("Revenue/", MIDNIGHT_TEAL, 2),
        ("Expenses/", MIDNIGHT_TEAL, 2),
        ("FY26_Budget_FINAL_v3.xlsx", MIDNIGHT_TEAL, 2),
    ]

    item_h = 0.50
    item_w = 4.0
    y_start = 6.65

    for i, (label, color, indent) in enumerate(legacy_items):
        y = y_start - i * 0.58
        x = left_x + indent * 0.35
        w = item_w - indent * 0.35
        rbox(ax, x, y - item_h / 2, w, item_h, fc=color, ec=BRIGHT_TEAL, lw=1.0, r=0.08, zorder=2)
        prefix = "    " * indent + ("" if indent == 0 else "")
        ax.text(x + 0.18, y, f"{'  ' * indent}{label}",
                ha="left", va="center",
                fontsize=11, color=WHITE, zorder=3)

    # "Do not touch" label
    rbox(ax, left_x, 1.85, item_w, 0.50, fc=ALERT_RED, ec=DEEP_NAVY, lw=1.5, r=0.10, zorder=4)
    ax.text(left_x + item_w / 2, 2.10, "Do not touch legacy files",
            ha="center", va="center",
            fontsize=12, fontweight="bold", color=WHITE, zorder=5)

    # ── Right column: workings layer ──────────────────────────────────────────
    right_x = 7.8
    ax.text(right_x + 2.5, 7.35, "Workings Layer",
            ha="center", va="center",
            fontsize=14, fontweight="bold", color=DEEP_NAVY, zorder=3)

    # CLAUDE.md card
    rbox(ax, right_x, 6.15, 5.0, 0.90, fc=GOLDEN_YELLOW, ec=DEEP_NAVY, lw=2, r=0.12, zorder=3)
    ax.text(right_x + 2.5, 6.78, "CLAUDE.md",
            ha="center", va="center",
            fontsize=14, fontweight="bold", color=DEEP_NAVY, zorder=4)
    ax.text(right_x + 2.5, 6.38, "AI Brain -- defines scope and rules",
            ha="center", va="center",
            fontsize=11, color=DEEP_NAVY, zorder=4)

    # 2026/ folder
    rbox(ax, right_x, 5.40, 5.0, 0.55, fc=MIDNIGHT_TEAL, ec=BRIGHT_TEAL, lw=1.5, r=0.08, zorder=2)
    ax.text(right_x + 0.18, 5.675, "2026/",
            ha="left", va="center",
            fontsize=12, color=WHITE, zorder=3)

    # workings/ safe zone background
    rbox(ax, right_x + 0.3, 2.05, 4.5, 3.15, fc=OCEAN_TEAL, ec=BRIGHT_TEAL, lw=2, r=0.15, zorder=2)
    ax.text(right_x + 2.55, 5.00, "workings/   <-- Safe Zone",
            ha="center", va="center",
            fontsize=12, fontweight="bold", color=GOLDEN_YELLOW, zorder=4)

    sub_items = [
        ("data/", "Raw inputs -- read only here", MIDNIGHT_TEAL),
        ("scripts/", "Processing logic", MIDNIGHT_TEAL),
        ("outputs/", "Generated results", SEA_GREEN),
    ]
    sy = 4.45
    for label, desc, color in sub_items:
        rbox(ax, right_x + 0.5, sy - 0.28, 4.1, 0.55, fc=color, ec=DEEP_NAVY, lw=1.0, r=0.08, zorder=3)
        ax.text(right_x + 0.72, sy, label,
                ha="left", va="center",
                fontsize=11, fontweight="bold", color=WHITE, zorder=4)
        ax.text(right_x + 1.9, sy, f"  {desc}",
                ha="left", va="center",
                fontsize=10, color=WHITE, alpha=0.85, zorder=4)
        sy -= 0.72

    # Output card at bottom right
    rbox(ax, right_x, 1.50, 5.0, 0.65, fc=SOFT_SAGE, ec=DEEP_NAVY, lw=1.5, r=0.10, zorder=3)
    ax.text(right_x + 2.5, 1.83, "Final output -> back to original folder",
            ha="center", va="center",
            fontsize=11, color=DEEP_NAVY, fontweight="bold", zorder=4)

    # ── Center divider and arrow ───────────────────────────────────────────────
    ax.plot([6.7, 6.7], [1.5, 7.5], color=BRIGHT_TEAL, lw=1.5, linestyle="--", alpha=0.5, zorder=1)
    ax.annotate("", xy=(7.6, 4.0), xytext=(6.7, 4.0),
                arrowprops=dict(arrowstyle="->", color=BRIGHT_TEAL, lw=2.0))

    # Footer
    add_footer(ax, 14, 0.0)

    fig.savefig(os.path.join(OUT_DIR, "22_folder_hierarchy.png"),
                dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print("Saved: 22_folder_hierarchy.png")


# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    make_hero()
    make_folder_hierarchy()
    print("All visuals generated.")
