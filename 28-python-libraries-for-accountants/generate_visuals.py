"""
Generate article visuals for Article 28 — Python Libraries for Accountants

Produces the following PNGs saved to visuals/:
  28_hero.png                    — Hero / Cover card
  28_extensions_vs_libraries.png — Full side-by-side comparison table
  28_key_libraries.png           — Key libraries for accounting and finance
  28_carousel_01.png             — Social: Hook slide
  28_carousel_02.png             — Social: Extensions vs Libraries
  28_carousel_03.png             — Social: Key libraries for accountants
  28_carousel_04.png             — Social: CTA / minimalism close

Branding: white background, Deep Navy text, Bright Teal / Golden Yellow accents.
DPI: 180.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import os

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

FOOTER     = "PythonMuse LLC  |  pythonmuse.com"
FOOTER_URL = "github.com/PythonMuse/ai-ledger"
MONO       = {"fontfamily": "monospace"}


def save(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  saved -> {path}")


def add_footer(fig, y=0.02):
    fig.text(0.5, y, FOOTER, ha="center", va="bottom",
             fontsize=9, color=OCEAN_TEAL)
    fig.text(0.5, y - 0.025, FOOTER_URL, ha="center", va="bottom",
             fontsize=8, color=OCEAN_TEAL, alpha=0.7)


def add_header_bar(ax, title, subtitle=None, bar_color=DEEP_NAVY,
                   title_color=GOLDEN_YELLOW, sub_color=BRIGHT_TEAL):
    ax.add_patch(FancyBboxPatch((0, 0.88), 1, 0.12, transform=ax.transAxes,
                                boxstyle="square,pad=0", linewidth=0,
                                facecolor=bar_color, clip_on=False))
    y_title = 0.955 if subtitle else 0.938
    ax.text(0.5, y_title, title, transform=ax.transAxes,
            ha="center", va="center", fontsize=17, fontweight="bold",
            color=title_color)
    if subtitle:
        ax.text(0.5, 0.905, subtitle, transform=ax.transAxes,
                ha="center", va="center", fontsize=11, color=sub_color)


# ─────────────────────────────────────────────────────────────
# 1. Hero
# ─────────────────────────────────────────────────────────────
def make_hero():
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Header bar
    ax.add_patch(FancyBboxPatch((0, 0.72), 1, 0.28, transform=ax.transAxes,
                                boxstyle="square,pad=0", linewidth=0,
                                facecolor=DEEP_NAVY, clip_on=False))
    ax.text(0.5, 0.935, "Python Libraries", transform=ax.transAxes,
            ha="center", va="center", fontsize=36, fontweight="bold",
            color=GOLDEN_YELLOW)
    ax.text(0.5, 0.855, "for Accountants", transform=ax.transAxes,
            ha="center", va="center", fontsize=34, fontweight="bold",
            color=GOLDEN_YELLOW)
    ax.text(0.5, 0.77, "Skills you teach your code",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=14, color=BRIGHT_TEAL)

    # Central analogy box
    ax.add_patch(FancyBboxPatch((0.06, 0.47), 0.88, 0.20,
                                boxstyle="round,pad=0.02", linewidth=2,
                                edgecolor=BRIGHT_TEAL, facecolor=LIGHT_GRAY))
    ax.text(0.5, 0.595, "Extensions = tools you add to your desk",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=14, color=OCEAN_TEAL, fontstyle="italic")
    ax.text(0.5, 0.53, "Libraries = skills you teach your assistant",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=14, fontweight="bold", color=DEEP_NAVY, fontstyle="italic")

    # Library name cards
    libs = [
        ("pandas", "tabular data", BRIGHT_TEAL),
        ("openpyxl", "Excel files", GOLDEN_YELLOW),
        ("matplotlib", "charts", SOFT_SAGE),
        ("pathlib", "file paths", SEA_GREEN),
    ]
    card_y = 0.16
    card_h = 0.24
    card_w = 0.20
    starts = [0.04, 0.27, 0.50, 0.73]

    for (lib, use, color), x in zip(libs, starts):
        ax.add_patch(FancyBboxPatch((x, card_y), card_w, card_h,
                                    boxstyle="round,pad=0.015", linewidth=0,
                                    facecolor=DEEP_NAVY))
        ax.text(x + card_w / 2, card_y + card_h * 0.72, lib,
                transform=ax.transAxes, ha="center", va="center",
                fontsize=12, fontweight="bold", color=color, **MONO)
        ax.text(x + card_w / 2, card_y + card_h * 0.32, use,
                transform=ax.transAxes, ha="center", va="center",
                fontsize=10, color=WHITE)

    add_footer(fig, y=0.01)
    save(fig, "28_hero.png")


# ─────────────────────────────────────────────────────────────
# 2. Extensions vs Libraries Full Comparison
# ─────────────────────────────────────────────────────────────
def make_comparison():
    fig, ax = plt.subplots(figsize=(14, 9))
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    add_header_bar(ax, "Extensions vs Libraries",
                   subtitle="The distinction that clears up most confusion for accountants")

    rows = [
        ("What it extends",   "Your editor (VS Code)",       "Python the language"),
        ("Installed into",    "VS Code",                     "Python environment"),
        ("Helps",             "You work more effectively",   "Your script do more"),
        ("Focus",             "UI, tooling, editing",        "Data, logic, processing"),
        ("Analogy",           "Tool on your desk",           "Skill you teach your assistant"),
        ("Examples",          "GitHub Copilot, Rainbow CSV", "pandas, openpyxl, matplotlib"),
        ("How to install",    "VS Code Marketplace",         "pip install in terminal"),
    ]

    col_label = 0.04
    col_ext   = 0.40
    col_lib   = 0.73
    row_start = 0.82
    row_gap   = 0.097

    # Column headers
    ax.add_patch(FancyBboxPatch((0.33, row_start - 0.01), 0.29, 0.055,
                                boxstyle="round,pad=0.01", linewidth=0,
                                facecolor=DEEP_NAVY))
    ax.add_patch(FancyBboxPatch((0.66, row_start - 0.01), 0.30, 0.055,
                                boxstyle="round,pad=0.01", linewidth=0,
                                facecolor=DEEP_NAVY))
    ax.text(col_ext + 0.10, row_start + 0.017, "VS Code Extension",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=13, fontweight="bold", color=BRIGHT_TEAL)
    ax.text(col_lib + 0.10, row_start + 0.017, "Python Library",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=13, fontweight="bold", color=GOLDEN_YELLOW)

    for i, (label, ext_val, lib_val) in enumerate(rows):
        y = row_start - row_gap * (i + 1)
        bg = LIGHT_GRAY if i % 2 == 0 else WHITE

        ax.add_patch(FancyBboxPatch((0.33, y - 0.032), 0.29, 0.065,
                                    boxstyle="round,pad=0.005", linewidth=0,
                                    facecolor=bg))
        ax.add_patch(FancyBboxPatch((0.66, y - 0.032), 0.30, 0.065,
                                    boxstyle="round,pad=0.005", linewidth=0,
                                    facecolor=bg))

        ax.text(col_label, y, label, transform=ax.transAxes,
                ha="left", va="center", fontsize=11, fontweight="bold",
                color=DEEP_NAVY)
        ax.text(col_ext + 0.10, y, ext_val, transform=ax.transAxes,
                ha="center", va="center", fontsize=10.5, color=OCEAN_TEAL)
        ax.text(col_lib + 0.10, y, lib_val, transform=ax.transAxes,
                ha="center", va="center", fontsize=10.5, color=SEA_GREEN,
                fontweight="bold")

    # Summary bar
    ax.add_patch(FancyBboxPatch((0.04, 0.01), 0.92, 0.055,
                                boxstyle="round,pad=0.01", linewidth=0,
                                facecolor=DEEP_NAVY))
    ax.text(0.5, 0.038,
            "Extensions help YOU work.    |    Libraries help PYTHON work.",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=13, fontweight="bold", color=GOLDEN_YELLOW)

    add_footer(fig, y=-0.02)
    save(fig, "28_extensions_vs_libraries.png")


# ─────────────────────────────────────────────────────────────
# 3. Key Libraries for Accounting
# ─────────────────────────────────────────────────────────────
def make_key_libraries():
    fig, ax = plt.subplots(figsize=(13, 11))
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    add_header_bar(ax, "Key Python Libraries for Accounting and Finance",
                   subtitle="Start here — these cover most accounting automation workflows")

    libraries = [
        (
            "pandas",
            "Tabular data — rows, columns, filters, sums",
            ["Read ERP exports (CSV)", "Filter by date / account / department",
             "Calculate totals and variances", "Merge data sources for reconciliation"],
            BRIGHT_TEAL,
        ),
        (
            "openpyxl",
            "Read and write Excel .xlsx files",
            ["Open Excel workbooks without Excel", "Write results to formatted sheets",
             "Automate month-end Excel updates"],
            GOLDEN_YELLOW,
        ),
        (
            "matplotlib",
            "Charts and graphs — programmatic output",
            ["Budget vs. actual variance charts", "Consistent management report visuals",
             "Reproducible charts from any dataset"],
            SOFT_SAGE,
        ),
        (
            "pathlib",
            "File paths and folder navigation (built in)",
            ["Process every file in a folder", "Build consistent naming logic",
             "Organize output by period or entity"],
            SEA_GREEN,
        ),
        (
            "datetime",
            "Dates, periods, and date math (built in)",
            ["Calculate days outstanding for AR aging", "Convert ERP date formats",
             "Generate period labels for reports"],
            WARM_GLOW,
        ),
    ]

    row_start = 0.815
    row_gap = 0.138
    row_h = 0.115

    for i, (name, tagline, uses, color) in enumerate(libraries):
        y = row_start - i * row_gap
        bg = LIGHT_GRAY if i % 2 == 0 else WHITE

        ax.add_patch(FancyBboxPatch((0.02, y - row_h * 0.55), 0.96, row_h,
                                    boxstyle="round,pad=0.008", linewidth=0,
                                    facecolor=bg))
        ax.add_patch(FancyBboxPatch((0.02, y - row_h * 0.55), 0.007, row_h,
                                    boxstyle="square,pad=0", linewidth=0,
                                    facecolor=color))

        # Library name + tagline (left column)
        ax.text(0.045, y + 0.012, name, transform=ax.transAxes,
                ha="left", va="center", fontsize=14, fontweight="bold",
                color=DEEP_NAVY, **MONO)
        ax.text(0.045, y - 0.020, tagline, transform=ax.transAxes,
                ha="left", va="center", fontsize=9.5, color=OCEAN_TEAL,
                fontstyle="italic")

        # Use cases (right column)
        for j, use in enumerate(uses[:3]):
            ax.text(0.41, y + 0.010 - j * 0.027, f"• {use}",
                    transform=ax.transAxes, ha="left", va="center",
                    fontsize=9.5, color=DEEP_NAVY)

    ax.text(0.5, 0.055,
            "pandas + openpyxl + matplotlib covers most accounting automation tasks.",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=11, color=OCEAN_TEAL, fontstyle="italic")

    add_footer(fig, y=0.012)
    save(fig, "28_key_libraries.png")


# ─────────────────────────────────────────────────────────────
# 4. Social carousel slides (square, 10x10)
# ─────────────────────────────────────────────────────────────
def make_carousel_01():
    fig, ax = plt.subplots(figsize=(10, 10))
    fig.patch.set_facecolor(DEEP_NAVY)
    ax.set_facecolor(DEEP_NAVY)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0.5, 0.83, "Someone told you to", transform=ax.transAxes,
            ha="center", va="center", fontsize=18, color=WHITE)
    ax.text(0.5, 0.74, '"just import pandas."', transform=ax.transAxes,
            ha="center", va="center", fontsize=22, fontweight="bold",
            color=GOLDEN_YELLOW)

    ax.add_patch(FancyBboxPatch((0.06, 0.47), 0.88, 0.20,
                                boxstyle="round,pad=0.02", linewidth=0,
                                facecolor=OCEAN_TEAL))
    ax.text(0.5, 0.595, "Wait — is that different from", transform=ax.transAxes,
            ha="center", va="center", fontsize=15, color=WHITE)
    ax.text(0.5, 0.52, "a VS Code extension?", transform=ax.transAxes,
            ha="center", va="center", fontsize=15, color=BRIGHT_TEAL,
            fontweight="bold")

    ax.text(0.5, 0.35, "Yes. Completely different.", transform=ax.transAxes,
            ha="center", va="center", fontsize=18, fontweight="bold",
            color=GOLDEN_YELLOW)
    ax.text(0.5, 0.25, "Here is the distinction that changes everything.",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=13, color=WHITE)

    ax.text(0.5, 0.09, "Article 28 | PythonMuse LLC", transform=ax.transAxes,
            ha="center", va="center", fontsize=11, color=BRIGHT_TEAL)
    ax.text(0.5, 0.035, FOOTER, transform=ax.transAxes,
            ha="center", va="center", fontsize=9, color=OCEAN_TEAL)
    save(fig, "28_carousel_01.png")


def make_carousel_02():
    fig, ax = plt.subplots(figsize=(10, 10))
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.add_patch(FancyBboxPatch((0, 0.86), 1, 0.14,
                                boxstyle="square,pad=0", linewidth=0,
                                facecolor=DEEP_NAVY, clip_on=False))
    ax.text(0.5, 0.938, "The Analogy That Lands",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=22, fontweight="bold", color=GOLDEN_YELLOW)

    # Extension card
    ax.add_patch(FancyBboxPatch((0.04, 0.55), 0.43, 0.26,
                                boxstyle="round,pad=0.02", linewidth=2,
                                edgecolor=BRIGHT_TEAL, facecolor=LIGHT_GRAY))
    ax.text(0.255, 0.78, "Extension", transform=ax.transAxes,
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=BRIGHT_TEAL)
    ax.text(0.255, 0.695, "Tool on your\noffice desk", transform=ax.transAxes,
            ha="center", va="center", fontsize=13, color=DEEP_NAVY,
            linespacing=1.5)
    ax.text(0.255, 0.595, "Helps YOU work", transform=ax.transAxes,
            ha="center", va="center", fontsize=11, color=OCEAN_TEAL,
            fontstyle="italic")

    # Library card
    ax.add_patch(FancyBboxPatch((0.53, 0.55), 0.43, 0.26,
                                boxstyle="round,pad=0.02", linewidth=2,
                                edgecolor=GOLDEN_YELLOW, facecolor=LIGHT_GRAY))
    ax.text(0.745, 0.78, "Library", transform=ax.transAxes,
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=SEA_GREEN)
    ax.text(0.745, 0.695, "Skill you teach\nyour assistant", transform=ax.transAxes,
            ha="center", va="center", fontsize=13, color=DEEP_NAVY,
            linespacing=1.5)
    ax.text(0.745, 0.595, "Helps PYTHON work", transform=ax.transAxes,
            ha="center", va="center", fontsize=11, color=OCEAN_TEAL,
            fontstyle="italic")

    ax.text(0.5, 0.47, "≠", transform=ax.transAxes,
            ha="center", va="center", fontsize=36, fontweight="bold",
            color=DEEP_NAVY, alpha=0.6)

    ax.add_patch(FancyBboxPatch((0.05, 0.27), 0.90, 0.15,
                                boxstyle="round,pad=0.015", linewidth=0,
                                facecolor=DEEP_NAVY))
    ax.text(0.5, 0.37, "One customizes your environment.",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=12, color=WHITE)
    ax.text(0.5, 0.305, "The other expands what your code can execute.",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=12, color=BRIGHT_TEAL, fontweight="bold")

    ax.text(0.5, 0.155, "Install extensions in VS Code.", transform=ax.transAxes,
            ha="center", va="center", fontsize=11, color=OCEAN_TEAL)
    ax.text(0.5, 0.100, "Install libraries with pip in the terminal.",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=11, color=OCEAN_TEAL)

    ax.text(0.5, 0.025, FOOTER, transform=ax.transAxes,
            ha="center", va="center", fontsize=9, color=OCEAN_TEAL)
    save(fig, "28_carousel_02.png")


def make_carousel_03():
    fig, ax = plt.subplots(figsize=(10, 10))
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.add_patch(FancyBboxPatch((0, 0.86), 1, 0.14,
                                boxstyle="square,pad=0", linewidth=0,
                                facecolor=DEEP_NAVY, clip_on=False))
    ax.text(0.5, 0.938, "The Accounting Library Stack",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=21, fontweight="bold", color=GOLDEN_YELLOW)

    libs = [
        ("pandas",     "Read, filter, sum tabular data",    BRIGHT_TEAL),
        ("openpyxl",   "Read and write Excel .xlsx files",  GOLDEN_YELLOW),
        ("matplotlib", "Charts and graphs from any data",   SOFT_SAGE),
        ("pathlib",    "Navigate folders, process files",   SEA_GREEN),
        ("datetime",   "Date math, aging, period labels",   WARM_GLOW),
    ]
    y0 = 0.77
    gap = 0.118

    for i, (name, desc, color) in enumerate(libs):
        y = y0 - i * gap
        ax.add_patch(FancyBboxPatch((0.04, y - 0.042), 0.92, 0.088,
                                    boxstyle="round,pad=0.01", linewidth=0,
                                    facecolor=LIGHT_GRAY if i % 2 == 0 else WHITE))
        ax.add_patch(FancyBboxPatch((0.04, y - 0.042), 0.007, 0.088,
                                    boxstyle="square,pad=0", linewidth=0,
                                    facecolor=color))
        ax.text(0.07, y + 0.005, name, transform=ax.transAxes,
                ha="left", va="center", fontsize=14, fontweight="bold",
                color=DEEP_NAVY, **MONO)
        ax.text(0.35, y + 0.005, desc, transform=ax.transAxes,
                ha="left", va="center", fontsize=11, color=OCEAN_TEAL)

    ax.text(0.5, 0.065,
            "pandas + openpyxl covers most accounting automation.",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=11, color=OCEAN_TEAL, fontstyle="italic")
    ax.text(0.5, 0.025, FOOTER, transform=ax.transAxes,
            ha="center", va="center", fontsize=9, color=OCEAN_TEAL)
    save(fig, "28_carousel_03.png")


def make_carousel_04():
    fig, ax = plt.subplots(figsize=(10, 10))
    fig.patch.set_facecolor(DEEP_NAVY)
    ax.set_facecolor(DEEP_NAVY)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0.5, 0.83, "Install Only What You Truly Need",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=20, fontweight="bold", color=BRIGHT_TEAL)

    ax.add_patch(FancyBboxPatch((0.06, 0.56), 0.88, 0.20,
                                boxstyle="round,pad=0.02", linewidth=0,
                                facecolor=GOLDEN_YELLOW))
    ax.text(0.5, 0.675, "Minimalism is a control.",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=20, fontweight="bold", color=DEEP_NAVY)
    ax.text(0.5, 0.605, "It applies equally to extensions and libraries.",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=13, color=DEEP_NAVY)

    principles = [
        "Every library becomes a dependency.",
        "Dependencies need maintenance.",
        "Maintenance needs governance.",
        "Governance starts with minimalism.",
    ]
    y0 = 0.50
    for i, p in enumerate(principles):
        ax.text(0.5, y0 - i * 0.075, p, transform=ax.transAxes,
                ha="center", va="center", fontsize=12, color=WHITE,
                alpha=0.90)

    ax.text(0.5, 0.17, "Full article at:",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=11, color=WHITE, alpha=0.7)
    ax.text(0.5, 0.11, "github.com/PythonMuse/ai-ledger",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=12, color=BRIGHT_TEAL)

    ax.text(0.5, 0.035, FOOTER, transform=ax.transAxes,
            ha="center", va="center", fontsize=9, color=OCEAN_TEAL)
    save(fig, "28_carousel_04.png")


# ─────────────────────────────────────────────────────────────
# Run all
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating Article 28 visuals...")
    make_hero()
    make_comparison()
    make_key_libraries()
    make_carousel_01()
    make_carousel_02()
    make_carousel_03()
    make_carousel_04()
    print("Done.")
