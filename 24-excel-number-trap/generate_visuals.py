"""
Generate article visuals for Article 24 — AI Didn't Break Your Numbers. Excel Did.
Series: Top 10 AI Traps in Accounting — Trap #1

Produces the following PNGs saved to visuals/:
  24_hero.png           — Hero / Cover: split-screen Excel vs Python
  24_carousel_01.png    — Carousel Slide 1: Hook
  24_carousel_02.png    — Carousel Slide 2: The Illusion
  24_carousel_03.png    — Carousel Slide 3: Reality
  24_carousel_04.png    — Carousel Slide 4: Why It Breaks
  24_carousel_05.png    — Carousel Slide 5: The Fix
  24_carousel_06.png    — Carousel Slide 6: The Lesson
  24_carousel_07.png    — Carousel Slide 7: Close / CTA
  24_youtube.png        — YouTube Thumbnail

Branding: white background, Deep Navy text, Bright Teal / Golden Yellow accents.
Per SKILL.md — Matplotlib Visuals (Article Charts).
DPI: 180. Font sizes follow SKILL.md minimums.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
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
LIGHT_GRAY    = "#F5F5F5"

FOOTER       = "PythonMuse  |  Build in the Open"
FOOTER_URL   = "pythonmuse.com  |  github.com/PythonMuse/pythonmuse-workflow-kit"
SERIES_BADGE = "Top 10 AI Traps in Accounting"

MONO_FONT = {"fontfamily": "monospace"}


def save(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  saved -> {path}")


def add_footer(fig):
    """Deep Navy footer bar with white brand text."""
    bar = fig.add_axes([0.0, 0.0, 1.0, 0.07], facecolor=DEEP_NAVY)
    bar.set_axis_off()
    fig.text(0.5, 0.038, FOOTER,
             ha="center", va="center",
             fontsize=11, color=WHITE, fontweight="bold")
    fig.text(0.5, 0.013, FOOTER_URL,
             ha="center", va="center",
             fontsize=9, color=BRIGHT_TEAL)


def add_header_bar(fig, label, trap_num="Trap #1"):
    """Deep Navy header bar across top of figure."""
    bar = fig.add_axes([0.0, 0.93, 1.0, 0.07], facecolor=DEEP_NAVY)
    bar.set_axis_off()
    fig.text(0.5, 0.965, f"{label}  |  {trap_num}",
             ha="center", va="center",
             fontsize=12, color=GOLDEN_YELLOW, fontweight="bold")


# ════════════════════════════════════════════════════════════════
# VISUAL 1 — Hero / Cover
# ════════════════════════════════════════════════════════════════
def make_hero():
    fig = plt.figure(figsize=(14, 8), facecolor=WHITE)

    add_header_bar(fig, SERIES_BADGE, "Trap #1: Parentheses Are Not Negatives")
    add_footer(fig)

    # Two side-by-side content panels
    ax_left  = fig.add_axes([0.03, 0.10, 0.44, 0.80])
    ax_right = fig.add_axes([0.53, 0.10, 0.44, 0.80])

    # Left panel — light green tint (success)
    ax_left.set_facecolor("#EBF7EB")
    ax_left.set_xticks([])
    ax_left.set_yticks([])
    for spine in ax_left.spines.values():
        spine.set_color(SOFT_SAGE)
        spine.set_linewidth(2.5)

    # Right panel — light red tint (error)
    ax_right.set_facecolor("#FDEDED")
    ax_right.set_xticks([])
    ax_right.set_yticks([])
    for spine in ax_right.spines.values():
        spine.set_color(ALERT_RED)
        spine.set_linewidth(2.5)

    # ── LEFT: Excel view ──────────────────────────────────────
    ax_left.text(0.5, 0.90, "Excel says:",
                 ha="center", va="center",
                 fontsize=26, color=OCEAN_TEAL, fontweight="bold")
    ax_left.text(0.5, 0.66, "($1,234.56)",
                 ha="center", va="center",
                 fontsize=54, color=DEEP_NAVY, fontweight="bold",
                 **MONO_FONT)
    for x, label in [(0.18, "Clean"), (0.50, "Formatted"), (0.82, "Trusted")]:
        ax_left.text(x, 0.44, "\u2714", ha="center", fontsize=34, color=SOFT_SAGE)
        ax_left.text(x, 0.32, label, ha="center", fontsize=19,
                     color=OCEAN_TEAL, fontweight="bold")
    ax_left.text(0.5, 0.12, "Looks like a number",
                 ha="center", va="center",
                 fontsize=19, color=OCEAN_TEAL, style="italic")

    # ── RIGHT: Python view ────────────────────────────────────
    ax_right.text(0.5, 0.90, "Python sees:",
                  ha="center", va="center",
                  fontsize=26, color=ALERT_RED, fontweight="bold")
    ax_right.text(0.5, 0.66, '"($1,234.56)"',
                  ha="center", va="center",
                  fontsize=46, color=ALERT_RED, fontweight="bold",
                  **MONO_FONT)
    ax_right.text(0.5, 0.44, "\u2718", ha="center", fontsize=46, color=ALERT_RED)
    ax_right.text(0.5, 0.32, "It's a string",
                  ha="center", fontsize=22, color=ALERT_RED, fontweight="bold")
    ax_right.text(0.5, 0.12, "Not a number. Not negative. Just text.",
                  ha="center", va="center",
                  fontsize=18, color=ALERT_RED, style="italic")

    # ── Arrow between panels ──────────────────────────────────
    fig.add_artist(
        mpatches.FancyArrowPatch(
            (0.488, 0.50), (0.512, 0.50),
            transform=fig.transFigure,
            arrowstyle="->",
            mutation_scale=30,
            color=DEEP_NAVY,
            linewidth=3,
        )
    )

    # ── Subtitle ──────────────────────────────────────────────
    fig.text(0.5, 0.065,
             "AI didn't break your numbers.  Excel's number format did.",
             ha="center", va="center",
             fontsize=15, color=DEEP_NAVY, style="italic")

    save(fig, "24_hero.png")


# ════════════════════════════════════════════════════════════════
# Carousel helper — white background, 9x9 square
# ════════════════════════════════════════════════════════════════
def carousel_fig():
    fig = plt.figure(figsize=(9, 9), facecolor=WHITE)
    ax = fig.add_axes([0.05, 0.09, 0.90, 0.82])
    ax.set_facecolor(WHITE)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    return fig, ax


# ════════════════════════════════════════════════════════════════
# VISUAL 2 — Carousel Slide 1: Hook
# ════════════════════════════════════════════════════════════════
def make_carousel_01():
    fig, ax = carousel_fig()
    add_header_bar(fig, SERIES_BADGE)
    add_footer(fig)

    ax.text(0.5, 0.68,
            "AI didn't break\nyour numbers.",
            ha="center", va="center",
            fontsize=42, fontweight="bold", color=DEEP_NAVY,
            linespacing=1.4)

    ax.axhline(y=0.46, xmin=0.15, xmax=0.85, color=BRIGHT_TEAL, linewidth=3)

    ax.text(0.5, 0.30,
            "Excel lied to you first.",
            ha="center", va="center",
            fontsize=32, fontweight="bold", color=OCEAN_TEAL)

    save(fig, "24_carousel_01.png")


# ════════════════════════════════════════════════════════════════
# VISUAL 3 — Carousel Slide 2: The Illusion
# ════════════════════════════════════════════════════════════════
def make_carousel_02():
    fig, ax = carousel_fig()
    add_header_bar(fig, SERIES_BADGE)
    add_footer(fig)

    ax.text(0.5, 0.88, "The Illusion",
            ha="center", va="center",
            fontsize=26, color=OCEAN_TEAL, fontweight="bold")

    box = FancyBboxPatch((0.08, 0.55), 0.84, 0.25,
                         boxstyle="round,pad=0.02",
                         facecolor=LIGHT_GRAY, edgecolor=BRIGHT_TEAL, linewidth=2.5,
                         transform=ax.transAxes, clip_on=False)
    ax.add_patch(box)
    ax.text(0.5, 0.675, "($1,234.56)",
            ha="center", va="center",
            fontsize=48, color=DEEP_NAVY, fontweight="bold",
            **MONO_FONT)

    ax.text(0.5, 0.44, "Looks like a negative number\u2026",
            ha="center", va="center",
            fontsize=20, color=OCEAN_TEAL, style="italic")

    ax.axhline(y=0.33, xmin=0.15, xmax=0.85, color=BRIGHT_TEAL, linewidth=2)

    ax.text(0.5, 0.20,
            "Excel shows meaning.\nPython requires truth.",
            ha="center", va="center",
            fontsize=18, color=DEEP_NAVY, linespacing=1.5)

    save(fig, "24_carousel_02.png")


# ════════════════════════════════════════════════════════════════
# VISUAL 4 — Carousel Slide 3: Reality
# ════════════════════════════════════════════════════════════════
def make_carousel_03():
    fig, ax = carousel_fig()
    add_header_bar(fig, SERIES_BADGE)
    add_footer(fig)

    ax.text(0.5, 0.88, "The Reality",
            ha="center", va="center",
            fontsize=26, color=ALERT_RED, fontweight="bold")

    box = FancyBboxPatch((0.04, 0.55), 0.92, 0.25,
                         boxstyle="round,pad=0.02",
                         facecolor="#FDEDED", edgecolor=ALERT_RED, linewidth=2.5,
                         transform=ax.transAxes, clip_on=False)
    ax.add_patch(box)
    ax.text(0.5, 0.675, '"($1,234.56)"',
            ha="center", va="center",
            fontsize=42, color=ALERT_RED, fontweight="bold",
            **MONO_FONT)

    ax.text(0.5, 0.44, "\u2026but it's actually text.",
            ha="center", va="center",
            fontsize=20, color=ALERT_RED, style="italic")

    ax.axhline(y=0.33, xmin=0.15, xmax=0.85, color=BRIGHT_TEAL, linewidth=2)

    ax.text(0.5, 0.20,
            "Python does not assume.\nIt converts \u2014 or it fails.",
            ha="center", va="center",
            fontsize=18, color=DEEP_NAVY, linespacing=1.5)

    save(fig, "24_carousel_03.png")


# ════════════════════════════════════════════════════════════════
# VISUAL 5 — Carousel Slide 4: Why It Breaks
# ════════════════════════════════════════════════════════════════
def make_carousel_04():
    fig, ax = carousel_fig()
    add_header_bar(fig, SERIES_BADGE)
    add_footer(fig)

    ax.text(0.5, 0.88, "Why It Breaks",
            ha="center", va="center",
            fontsize=26, color=DEEP_NAVY, fontweight="bold")

    items = [
        ("$",    "not numeric \u2014 it's a symbol"),
        (",",    "formatting only \u2014 not structure"),
        ("( )",  "just characters \u2014 not math"),
    ]
    y_positions = [0.69, 0.52, 0.35]
    for (symbol, desc), y in zip(items, y_positions):
        pill = FancyBboxPatch((0.05, y - 0.07), 0.18, 0.14,
                              boxstyle="round,pad=0.01",
                              facecolor=DEEP_NAVY, edgecolor=DEEP_NAVY,
                              transform=ax.transAxes, clip_on=False)
        ax.add_patch(pill)
        ax.text(0.14, y, symbol,
                ha="center", va="center",
                fontsize=28, color=GOLDEN_YELLOW, fontweight="bold",
                **MONO_FONT)
        ax.text(0.29, y, "\u2192",
                ha="center", va="center",
                fontsize=24, color=BRIGHT_TEAL)
        ax.text(0.64, y, desc,
                ha="center", va="center",
                fontsize=17, color=DEEP_NAVY)

    ax.axhline(y=0.21, xmin=0.10, xmax=0.90, color=BRIGHT_TEAL, linewidth=2)
    ax.text(0.5, 0.12,
            "Python does not assume. It converts.",
            ha="center", va="center",
            fontsize=16, color=OCEAN_TEAL, style="italic")

    save(fig, "24_carousel_04.png")


# ════════════════════════════════════════════════════════════════
# VISUAL 6 — Carousel Slide 5: The Fix
# ════════════════════════════════════════════════════════════════
def make_carousel_05():
    fig, ax = carousel_fig()
    add_header_bar(fig, SERIES_BADGE)
    add_footer(fig)

    ax.text(0.5, 0.88, "The Fix",
            ha="center", va="center",
            fontsize=26, color=DEEP_NAVY, fontweight="bold")

    # Code block — dark background per SKILL.md (code blocks stay dark)
    code_box = FancyBboxPatch(
        (0.03, 0.44), 0.94, 0.36,
        boxstyle="round,pad=0.02",
        facecolor=MIDNIGHT_TEAL, edgecolor=OCEAN_TEAL, linewidth=2,
        transform=ax.transAxes, clip_on=False,
    )
    ax.add_patch(code_box)

    rendered = [
        (".replace(r'[$,]', '', regex=True)",             BRIGHT_TEAL, 0.74),
        ("  # remove $ and commas",                        WHITE,       0.67),
        (".replace(r'\\((.*?)\\)', r'-\\1', regex=True)", BRIGHT_TEAL, 0.60),
        ("  # (123)  \u2192  -123",                        WHITE,       0.53),
        (".astype(float)",                                 BRIGHT_TEAL, 0.47),
    ]
    for line, color, y in rendered:
        ax.text(0.07, y, line,
                ha="left", va="center",
                fontsize=13, color=color,
                **MONO_FONT)

    ax.text(0.5, 0.34,
            "Teach Python accounting language.",
            ha="center", va="center",
            fontsize=18, color=DEEP_NAVY, fontweight="bold")

    ax.text(0.5, 0.20,
            "Full reusable Skill \u2192 PythonMuse Workflow Kit",
            ha="center", va="center",
            fontsize=14, color=OCEAN_TEAL, style="italic")

    save(fig, "24_carousel_05.png")


# ════════════════════════════════════════════════════════════════
# VISUAL 7 — Carousel Slide 6: The Lesson
# ════════════════════════════════════════════════════════════════
def make_carousel_06():
    fig, ax = carousel_fig()
    add_header_bar(fig, SERIES_BADGE)
    add_footer(fig)

    ax.text(0.5, 0.88, "The Lesson",
            ha="center", va="center",
            fontsize=26, color=DEEP_NAVY, fontweight="bold")

    # Light box
    box1 = FancyBboxPatch((0.05, 0.58), 0.90, 0.21,
                          boxstyle="round,pad=0.02",
                          facecolor=LIGHT_GRAY, edgecolor=BRIGHT_TEAL, linewidth=2.5,
                          transform=ax.transAxes, clip_on=False)
    ax.add_patch(box1)
    ax.text(0.5, 0.685, "Excel shows meaning.",
            ha="center", va="center",
            fontsize=28, color=DEEP_NAVY, fontweight="bold")

    # Dark box
    box2 = FancyBboxPatch((0.05, 0.33), 0.90, 0.21,
                          boxstyle="round,pad=0.02",
                          facecolor=DEEP_NAVY, edgecolor=DEEP_NAVY, linewidth=2,
                          transform=ax.transAxes, clip_on=False)
    ax.add_patch(box2)
    ax.text(0.5, 0.44, "Python requires truth.",
            ha="center", va="center",
            fontsize=28, color=GOLDEN_YELLOW, fontweight="bold")

    ax.text(0.5, 0.18,
            "We don't have an AI problem.\nWe have a data discipline gap.",
            ha="center", va="center",
            fontsize=16, color=OCEAN_TEAL, style="italic", linespacing=1.5)

    save(fig, "24_carousel_06.png")


# ════════════════════════════════════════════════════════════════
# VISUAL 8 — Carousel Slide 7: Close / CTA
# ════════════════════════════════════════════════════════════════
def make_carousel_07():
    fig, ax = carousel_fig()
    add_header_bar(fig, SERIES_BADGE)
    add_footer(fig)

    # Checkmark pill
    pill = FancyBboxPatch((0.25, 0.72), 0.50, 0.15,
                          boxstyle="round,pad=0.02",
                          facecolor=SOFT_SAGE, edgecolor=SOFT_SAGE,
                          transform=ax.transAxes, clip_on=False)
    ax.add_patch(pill)
    ax.text(0.5, 0.795, "Trap #1  \u2714",
            ha="center", va="center",
            fontsize=24, color=WHITE, fontweight="bold")

    ax.text(0.5, 0.56,
            "9 more your Excel\ndidn't warn you about\u2026",
            ha="center", va="center",
            fontsize=28, color=DEEP_NAVY, fontweight="bold", linespacing=1.4)

    ax.axhline(y=0.40, xmin=0.15, xmax=0.85, color=BRIGHT_TEAL, linewidth=2.5)

    # CTA box
    cta = FancyBboxPatch((0.12, 0.25), 0.76, 0.13,
                         boxstyle="round,pad=0.02",
                         facecolor=GOLDEN_YELLOW, edgecolor=GOLDEN_YELLOW,
                         transform=ax.transAxes, clip_on=False)
    ax.add_patch(cta)
    ax.text(0.5, 0.315, "Follow  \u00b7  Save  \u00b7  Share",
            ha="center", va="center",
            fontsize=22, color=DEEP_NAVY, fontweight="bold")

    ax.text(0.5, 0.13, "pythonmuse.com",
            ha="center", va="center",
            fontsize=18, color=OCEAN_TEAL, fontweight="bold")

    save(fig, "24_carousel_07.png")


# ════════════════════════════════════════════════════════════════
# VISUAL 9 — YouTube Thumbnail  (16:9)
# ════════════════════════════════════════════════════════════════
def make_youtube():
    fig = plt.figure(figsize=(12.8, 7.2), facecolor=WHITE)

    # Header bar
    hdr = fig.add_axes([0.0, 0.90, 1.0, 0.10], facecolor=DEEP_NAVY)
    hdr.set_axis_off()
    fig.text(0.5, 0.945, "Top 10 AI Traps in Accounting  |  Trap #1",
             ha="center", va="center",
             fontsize=15, color=GOLDEN_YELLOW, fontweight="bold")

    # Content area
    ax = fig.add_axes([0.0, 0.09, 1.0, 0.81])
    ax.set_facecolor(WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Left box — wrong format
    wrong = FancyBboxPatch((0.04, 0.22), 0.36, 0.62,
                           boxstyle="round,pad=0.02",
                           facecolor="#FDEDED", edgecolor=ALERT_RED, linewidth=3,
                           transform=ax.transAxes, clip_on=False)
    ax.add_patch(wrong)
    ax.text(0.22, 0.72, "(1,234)",
            ha="center", va="center",
            fontsize=60, color=DEEP_NAVY, fontweight="bold",
            **MONO_FONT)
    ax.text(0.22, 0.38, "WRONG",
            ha="center", va="center",
            fontsize=32, color=ALERT_RED, fontweight="bold")

    # Arrow
    ax.annotate("",
                xy=(0.59, 0.56), xytext=(0.43, 0.56),
                arrowprops=dict(
                    arrowstyle="->",
                    color=DEEP_NAVY,
                    lw=4,
                    mutation_scale=38,
                ))

    # Right box — fixed
    fixed = FancyBboxPatch((0.60, 0.22), 0.36, 0.62,
                           boxstyle="round,pad=0.02",
                           facecolor="#EBF7EB", edgecolor=SOFT_SAGE, linewidth=3,
                           transform=ax.transAxes, clip_on=False)
    ax.add_patch(fixed)
    ax.text(0.78, 0.72, "-1234",
            ha="center", va="center",
            fontsize=60, color=OCEAN_TEAL, fontweight="bold",
            **MONO_FONT)
    ax.text(0.78, 0.38, "FIXED",
            ha="center", va="center",
            fontsize=32, color=OCEAN_TEAL, fontweight="bold")

    # Title
    ax.text(0.5, 0.10,
            "The Number Format Trap",
            ha="center", va="center",
            fontsize=38, color=DEEP_NAVY, fontweight="bold")

    # Footer bar
    ftr = fig.add_axes([0.0, 0.0, 1.0, 0.10], facecolor=DEEP_NAVY)
    ftr.set_axis_off()
    fig.text(0.5, 0.054, FOOTER,
             ha="center", va="center",
             fontsize=12, color=WHITE, fontweight="bold")
    fig.text(0.5, 0.018, FOOTER_URL,
             ha="center", va="center",
             fontsize=10, color=BRIGHT_TEAL)

    save(fig, "24_youtube.png")


# ════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("Generating Article 24 visuals (white background, updated branding)...")
    make_hero()
    make_carousel_01()
    make_carousel_02()
    make_carousel_03()
    make_carousel_04()
    make_carousel_05()
    make_carousel_06()
    make_carousel_07()
    make_youtube()
    print(f"\nAll visuals saved to: {OUT_DIR}")
