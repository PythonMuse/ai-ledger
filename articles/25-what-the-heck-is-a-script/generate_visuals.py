"""
Generate article visuals for Article 25 — What the Heck Is a Script?

Produces the following PNGs saved to visuals/:
  25_hero.png               — Hero / Cover card
  25_accounting_vs_script.png — Side-by-side comparison table
  25_excel_vs_python.png    — Same problem, both ways (cleanup)
  25_same_problem_ladder.png — Three paired examples: simple → medium → hard
  25_carousel_01.png        — Social: Hook slide
  25_carousel_02.png        — Social: You already write scripts
  25_carousel_03.png        — Social: Excel formula vs Python
  25_carousel_04.png        — Social: The simplest explanation

Branding: white background, Deep Navy text, Bright Teal / Golden Yellow accents.
DPI: 180.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
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
            ha="center", va="center", fontsize=18, fontweight="bold",
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
    ax.text(0.5, 0.93, "What the Heck", transform=ax.transAxes,
            ha="center", va="center", fontsize=38, fontweight="bold",
            color=GOLDEN_YELLOW)
    ax.text(0.5, 0.84, "Is a Script?", transform=ax.transAxes,
            ha="center", va="center", fontsize=38, fontweight="bold",
            color=GOLDEN_YELLOW)
    ax.text(0.5, 0.76, "The Accountant-Friendly Explanation Nobody Gives You",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=13, color=BRIGHT_TEAL)

    # Center quote box
    ax.add_patch(FancyBboxPatch((0.08, 0.46), 0.84, 0.22,
                                boxstyle="round,pad=0.02", linewidth=2,
                                edgecolor=BRIGHT_TEAL, facecolor=LIGHT_GRAY))
    ax.text(0.5, 0.595, '"It\'s basically an SOP for a computer."',
            transform=ax.transAxes, ha="center", va="center",
            fontsize=16, fontstyle="italic", color=DEEP_NAVY)
    ax.text(0.5, 0.51, "— The answer that makes the whole room nod",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=11, color=OCEAN_TEAL)

    # Three equal-width cards at the bottom
    card_data = [
        ("SOP", "Script", BRIGHT_TEAL),
        ("Checklist", "Algorithm", GOLDEN_YELLOW),
        ("Month-end\nProcess", "Workflow", SOFT_SAGE),
    ]
    card_y = 0.16
    card_h = 0.22
    card_w = 0.24
    starts = [0.06, 0.38, 0.70]

    for (acct, prog, color), x in zip(card_data, starts):
        ax.add_patch(FancyBboxPatch((x, card_y), card_w, card_h,
                                    boxstyle="round,pad=0.015", linewidth=0,
                                    facecolor=DEEP_NAVY))
        ax.text(x + card_w / 2, card_y + card_h * 0.70, acct,
                transform=ax.transAxes, ha="center", va="center",
                fontsize=13, fontweight="bold", color=color)
        ax.text(x + card_w / 2, card_y + card_h * 0.35,
                f"= {prog}", transform=ax.transAxes,
                ha="center", va="center", fontsize=11, color=WHITE)

    ax.text(0.5, 0.09, "You already write scripts.\nYou just called them something else.",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=12, color=DEEP_NAVY, linespacing=1.6)

    add_footer(fig, y=0.01)
    save(fig, "25_hero.png")


# ─────────────────────────────────────────────────────────────
# 2. Accounting World vs Programming World
# ─────────────────────────────────────────────────────────────
def make_comparison():
    fig, ax = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    add_header_bar(ax, "You Already Write Scripts",
                   subtitle="Accountants use different words for the same ideas")

    rows = [
        ("SOP",                  "Script"),
        ("Checklist",            "Algorithm"),
        ("Macro",                "Automation"),
        ("Excel formula",        "Instruction"),
        ("Month-end close",      "Workflow"),
    ]

    col_left  = 0.10
    col_mid   = 0.50
    col_right = 0.90
    row_start = 0.80
    row_gap   = 0.105

    # Column headers
    ax.add_patch(FancyBboxPatch((col_left - 0.02, row_start - 0.015),
                                0.36, 0.065,
                                boxstyle="round,pad=0.01", linewidth=0,
                                facecolor=DEEP_NAVY))
    ax.add_patch(FancyBboxPatch((col_mid - 0.02, row_start - 0.015),
                                0.36, 0.065,
                                boxstyle="round,pad=0.01", linewidth=0,
                                facecolor=DEEP_NAVY))
    ax.text(col_left + 0.16, row_start + 0.020, "Accounting World",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=14, fontweight="bold", color=BRIGHT_TEAL)
    ax.text(col_mid + 0.16, row_start + 0.020, "Programming World",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=14, fontweight="bold", color=GOLDEN_YELLOW)

    for i, (acct, prog) in enumerate(rows):
        y = row_start - row_gap * (i + 1)
        bg = LIGHT_GRAY if i % 2 == 0 else WHITE

        ax.add_patch(FancyBboxPatch((col_left - 0.02, y - 0.03),
                                    0.36, 0.065,
                                    boxstyle="round,pad=0.01", linewidth=0,
                                    facecolor=bg))
        ax.add_patch(FancyBboxPatch((col_mid - 0.02, y - 0.03),
                                    0.36, 0.065,
                                    boxstyle="round,pad=0.01", linewidth=0,
                                    facecolor=bg))

        ax.text(col_left + 0.16, y + 0.005, acct,
                transform=ax.transAxes, ha="center", va="center",
                fontsize=13, color=DEEP_NAVY)
        ax.text(col_mid + 0.16, y + 0.005, prog,
                transform=ax.transAxes, ha="center", va="center",
                fontsize=13, fontweight="bold", color=SEA_GREEN)

        # Arrow between columns
        ax.annotate("", xy=(col_mid - 0.025, y + 0.005),
                    xytext=(col_left + 0.34, y + 0.005),
                    xycoords="axes fraction", textcoords="axes fraction",
                    arrowprops=dict(arrowstyle="->", color=BRIGHT_TEAL, lw=1.5))

    ax.text(0.5, 0.05,
            "If you follow the same steps every month — you already have a script.",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=12, fontstyle="italic", color=OCEAN_TEAL)

    add_footer(fig)
    save(fig, "25_accounting_vs_script.png")


# ─────────────────────────────────────────────────────────────
# 3. Excel vs Python code comparison
# ─────────────────────────────────────────────────────────────
def make_code_comparison():
    """Same problem, both ways: clean '$(1,234.50)' -> -1234.50"""
    fig, ax = plt.subplots(figsize=(14, 7.5))
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    add_header_bar(ax, "Same Problem. Both Ways.",
                   subtitle='Clean an exported amount  "$(1,234.50)"  →  -1234.50')

    # Layout constants — 4% outer margin so borders fully visible, 12% centre gap for "vs"
    L_X, R_X = 0.04, 0.56   # left box x-start, right box x-start
    BOX_W    = 0.40           # each box width  (right edge = 0.96, gap = 0.12)
    BOX_Y, BOX_H = 0.18, 0.66
    L_CX = L_X + BOX_W / 2   # 0.24  — left box centre
    R_CX = R_X + BOX_W / 2   # 0.76  — right box centre

    # Left panel — Excel
    ax.add_patch(FancyBboxPatch((L_X, BOX_Y), BOX_W, BOX_H,
                                boxstyle="round,pad=0.015", linewidth=2,
                                edgecolor=ALERT_RED, facecolor=LIGHT_GRAY))
    ax.text(L_CX, 0.81, "Excel Formula", transform=ax.transAxes,
            ha="center", va="center", fontsize=14, fontweight="bold",
            color=ALERT_RED)

    excel_lines = [
        "=-VALUE(",
        "  SUBSTITUTE(",
        "   SUBSTITUTE(",
        "    SUBSTITUTE(",
        "     SUBSTITUTE(",
        '       A2,"$",""),',
        '     ",",""),',
        '    "(","-"),',
        '   ")","")',
        " )",
    ]
    for j, line in enumerate(excel_lines):
        ax.text(L_X + 0.02, 0.745 - j * 0.05, line,
                transform=ax.transAxes, ha="left", va="center",
                fontsize=11, color=DEEP_NAVY, **MONO)

    ax.text(L_CX, 0.24,
            "Four nested SUBSTITUTEs.\nGood luck explaining it.",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=11, color=ALERT_RED, fontstyle="italic",
            linespacing=1.5)

    # Right panel — Python
    ax.add_patch(FancyBboxPatch((R_X, BOX_Y), BOX_W, BOX_H,
                                boxstyle="round,pad=0.015", linewidth=2,
                                edgecolor=BRIGHT_TEAL, facecolor=LIGHT_GRAY))
    ax.text(R_CX, 0.81, "Python Script", transform=ax.transAxes,
            ha="center", va="center", fontsize=14, fontweight="bold",
            color=SEA_GREEN)

    python_lines = [
        "def clean_amount(amount):",
        '    amount = amount.replace("$","")',
        '    amount = amount.replace(",","")',
        '    amount = amount.replace("(","-")',
        '    amount = amount.replace(")","")',
        "    return float(amount)",
    ]
    for j, line in enumerate(python_lines):
        ax.text(R_X + 0.02, 0.735 - j * 0.055, line,
                transform=ax.transAxes, ha="left", va="center",
                fontsize=10.5, color=DEEP_NAVY, **MONO)

    steps = [
        "Reads like an accounting",
        "cleanup checklist.",
    ]
    for j, step in enumerate(steps):
        ax.text(R_CX, 0.275 - j * 0.045, step,
                transform=ax.transAxes, ha="center", va="center",
                fontsize=11, color=SEA_GREEN, fontstyle="italic")

    # VS divider — centred in the 14% gap, bold and clearly visible
    ax.text(0.5, 0.51, "vs", transform=ax.transAxes,
            ha="center", va="center", fontsize=30, fontweight="bold",
            color=DEEP_NAVY, alpha=0.65)

    # Equivalence proof bar
    ax.add_patch(FancyBboxPatch((0.04, 0.09), 0.92, 0.055,
                                boxstyle="round,pad=0.01", linewidth=0,
                                facecolor=DEEP_NAVY))
    ax.text(0.5, 0.117,
            'Same input  "$(1,234.50)"   →   Same result  -1234.50',
            transform=ax.transAxes, ha="center", va="center",
            fontsize=12, fontweight="bold", color=GOLDEN_YELLOW, **MONO)

    # Footer drawn in axes space just below the dark bar; subplots_adjust collapses dead space
    fig.subplots_adjust(bottom=0.02, top=0.97)
    ax.text(0.5, 0.065, FOOTER, transform=ax.transAxes,
            ha="center", va="center", fontsize=9, color=OCEAN_TEAL)
    ax.text(0.5, 0.040, FOOTER_URL, transform=ax.transAxes,
            ha="center", va="center", fontsize=8, color=OCEAN_TEAL, alpha=0.7)
    save(fig, "25_excel_vs_python.png")


# ─────────────────────────────────────────────────────────────
# 3b. Same-Problem Ladder — simple, medium, hard
# ─────────────────────────────────────────────────────────────
def make_ladder():
    """Three accounting problems solved both ways, side by side."""
    fig, ax = plt.subplots(figsize=(15, 12))
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    add_header_bar(ax, "Same Problem. Both Ways.",
                   subtitle="One accounting task at a time — solved in Excel, then as a script")

    # Column headers (shifted down to avoid overlap)
    ax.add_patch(FancyBboxPatch((0.30, 0.765), 0.26, 0.045,
                                boxstyle="round,pad=0.008", linewidth=0,
                                facecolor=ALERT_RED, alpha=0.85))
    ax.text(0.43, 0.787, "Excel Formula", transform=ax.transAxes,
            ha="center", va="center", fontsize=12, fontweight="bold",
            color=WHITE)

    ax.add_patch(FancyBboxPatch((0.65, 0.765), 0.31, 0.045,
                                boxstyle="round,pad=0.008", linewidth=0,
                                facecolor=SEA_GREEN))
    ax.text(0.805, 0.787, "Python Script", transform=ax.transAxes,
            ha="center", va="center", fontsize=12, fontweight="bold",
            color=WHITE)

    examples = [
        {
            "title": "1.  Invoice Line Total",
            "subtitle": ["Quantity × Price"],
            "excel": ["=B2*C2"],
            "python": [
                "def line_total(quantity, price):",
                "    return quantity * price",
            ],
        },
        {
            "title": "2.  Rate Lookup",
            "subtitle": [
                "Find the rate.",
                "If missing, use zero.",
                "Multiply by quantity.",
            ],
            "excel": [
                "=IFERROR(",
                "  VLOOKUP(A2,",
                "    'Rate Table'!A:D,",
                "    4,FALSE)*B2,",
                "  0)",
            ],
            "python": [
                "def billed_amount(item, qty, rate_table):",
                "    rate = rate_table.get(item, 0)",
                "    return rate * qty",
            ],
        },
        {
            "title": "3.  Clean an Amount",
            "subtitle": ['"$(1,234.50)"', "→  -1234.50"],
            "excel": [
                "=-VALUE(SUBSTITUTE(",
                "  SUBSTITUTE(",
                "   SUBSTITUTE(",
                '    SUBSTITUTE(A2,"$",""),',
                '    ",",""),"(","-"),',
                '  ")",""))',
            ],
            "python": [
                "def clean_amount(amount):",
                '    amount = amount.replace("$", "")',
                '    amount = amount.replace(",", "")',
                '    amount = amount.replace("(", "-")',
                '    amount = amount.replace(")", "")',
                "    return float(amount)",
            ],
        },
    ]

    row_top = 0.73
    row_h = 0.235
    row_gap = 0.015

    for i, ex in enumerate(examples):
        y_top = row_top - i * (row_h + row_gap)
        y_bot = y_top - row_h

        # Row background
        ax.add_patch(FancyBboxPatch((0.02, y_bot), 0.96, row_h,
                                    boxstyle="round,pad=0.005", linewidth=0,
                                    facecolor=LIGHT_GRAY if i % 2 == 0 else WHITE))

        # Title strip (left column, narrow)
        ax.text(0.04, y_top - 0.035, ex["title"],
                transform=ax.transAxes, ha="left", va="top",
                fontsize=12, fontweight="bold", color=DEEP_NAVY)
        for k, line in enumerate(ex["subtitle"]):
            ax.text(0.04, y_top - 0.075 - k * 0.028, line,
                    transform=ax.transAxes, ha="left", va="top",
                    fontsize=9.5, color=OCEAN_TEAL, fontstyle="italic")

        # Excel code box
        ax.add_patch(FancyBboxPatch((0.30, y_bot + 0.015), 0.26, row_h - 0.03,
                                    boxstyle="round,pad=0.008", linewidth=1.2,
                                    edgecolor=ALERT_RED, facecolor=WHITE))
        for j, line in enumerate(ex["excel"]):
            ax.text(0.305, y_top - 0.045 - j * 0.030, line,
                    transform=ax.transAxes, ha="left", va="top",
                    fontsize=9, color=DEEP_NAVY, **MONO)

        # Python code box
        ax.add_patch(FancyBboxPatch((0.65, y_bot + 0.015), 0.31, row_h - 0.03,
                                    boxstyle="round,pad=0.008", linewidth=1.2,
                                    edgecolor=BRIGHT_TEAL, facecolor=WHITE))
        for j, line in enumerate(ex["python"]):
            ax.text(0.655, y_top - 0.045 - j * 0.030, line,
                    transform=ax.transAxes, ha="left", va="top",
                    fontsize=9, color=DEEP_NAVY, **MONO)

        # Arrow between
        ax.annotate("", xy=(0.645, y_top - row_h / 2),
                    xytext=(0.565, y_top - row_h / 2),
                    xycoords="axes fraction", textcoords="axes fraction",
                    arrowprops=dict(arrowstyle="->", color=BRIGHT_TEAL, lw=2))

    ax.text(0.5, -0.04,
            "As complexity grows, the script stays readable — the formula doesn't.",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=12, color=DEEP_NAVY, fontstyle="italic")

    add_footer(fig, y=0.005)
    save(fig, "25_same_problem_ladder.png")


# ─────────────────────────────────────────────────────────────
# 4. Social carousel slides (square, 10x10)
# ─────────────────────────────────────────────────────────────
def make_carousel_01():
    """Hook slide."""
    fig, ax = plt.subplots(figsize=(10, 10))
    fig.patch.set_facecolor(DEEP_NAVY)
    ax.set_facecolor(DEEP_NAVY)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0.5, 0.80, "Someone stopped me", transform=ax.transAxes,
            ha="center", va="center", fontsize=20, color=WHITE)
    ax.text(0.5, 0.68, "mid-presentation and asked:",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=20, color=WHITE)

    ax.add_patch(FancyBboxPatch((0.08, 0.38), 0.84, 0.22,
                                boxstyle="round,pad=0.02", linewidth=0,
                                facecolor=OCEAN_TEAL))
    ax.text(0.5, 0.505, '"Okay… but what the heck',
            transform=ax.transAxes, ha="center", va="center",
            fontsize=22, fontweight="bold", color=GOLDEN_YELLOW)
    ax.text(0.5, 0.425, 'is a script?"',
            transform=ax.transAxes, ha="center", va="center",
            fontsize=22, fontweight="bold", color=GOLDEN_YELLOW)

    ax.text(0.5, 0.24, "Fair question.", transform=ax.transAxes,
            ha="center", va="center", fontsize=18, color=BRIGHT_TEAL,
            fontweight="bold")
    ax.text(0.5, 0.16, "Here is the answer nobody gives accountants.",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=14, color=WHITE)

    ax.text(0.5, 0.05, "PythonMuse LLC  |  pythonmuse.com",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=9, color=OCEAN_TEAL)
    save(fig, "25_carousel_01.png")


def make_carousel_02():
    """You already write scripts."""
    fig, ax = plt.subplots(figsize=(10, 10))
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.add_patch(FancyBboxPatch((0, 0.86), 1, 0.14,
                                boxstyle="square,pad=0", linewidth=0,
                                facecolor=DEEP_NAVY, clip_on=False))
    ax.text(0.5, 0.935, "You Already Write Scripts",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=22, fontweight="bold", color=GOLDEN_YELLOW)

    pairs = [
        ("SOP", "Script"),
        ("Checklist", "Algorithm"),
        ("Macro", "Automation"),
        ("Excel formula", "Instruction"),
        ("Month-end close", "Workflow"),
    ]
    y0 = 0.77
    gap = 0.12
    for i, (left, right) in enumerate(pairs):
        y = y0 - i * gap
        bg = LIGHT_GRAY if i % 2 == 0 else WHITE
        ax.add_patch(FancyBboxPatch((0.04, y - 0.045), 0.92, 0.09,
                                    boxstyle="round,pad=0.01", linewidth=0,
                                    facecolor=bg))
        ax.text(0.27, y, left, transform=ax.transAxes,
                ha="center", va="center", fontsize=14, color=DEEP_NAVY)
        ax.text(0.5,  y, "=", transform=ax.transAxes,
                ha="center", va="center", fontsize=14, color=BRIGHT_TEAL,
                fontweight="bold")
        ax.text(0.73, y, right, transform=ax.transAxes,
                ha="center", va="center", fontsize=14, color=SEA_GREEN,
                fontweight="bold")

    ax.text(0.5, 0.05, "You just called them something else.",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=13, color=OCEAN_TEAL, fontstyle="italic")
    save(fig, "25_carousel_02.png")


def make_carousel_03():
    """Same logic — two worlds. Side-by-side clean_amount."""
    fig, ax = plt.subplots(figsize=(10, 10))
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.add_patch(FancyBboxPatch((0, 0.86), 1, 0.14,
                                boxstyle="square,pad=0", linewidth=0,
                                facecolor=DEEP_NAVY, clip_on=False))
    ax.text(0.5, 0.945, "Same Logic — Two Worlds",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=20, fontweight="bold", color=GOLDEN_YELLOW)
    ax.text(0.5, 0.885, 'Clean  "$(1,234.50)"  →  -1234.50',
            transform=ax.transAxes, ha="center", va="center",
            fontsize=11, color=BRIGHT_TEAL, **MONO)

    # Excel box (top)
    ax.add_patch(FancyBboxPatch((0.05, 0.55), 0.90, 0.27,
                                boxstyle="round,pad=0.015", linewidth=2,
                                edgecolor=ALERT_RED, facecolor=LIGHT_GRAY))
    ax.text(0.5, 0.795, "Excel", transform=ax.transAxes,
            ha="center", va="center", fontsize=13, fontweight="bold",
            color=ALERT_RED)
    excel_lines = [
        "=-VALUE(SUBSTITUTE(",
        "  SUBSTITUTE(SUBSTITUTE(",
        '    SUBSTITUTE(A2,"$",""),',
        '    ",",""),"(","-"),',
        '  ")",""))',
    ]
    for j, line in enumerate(excel_lines):
        ax.text(0.08, 0.745 - j * 0.038, line,
                transform=ax.transAxes, ha="left", va="center",
                fontsize=10.5, color=DEEP_NAVY, **MONO)

    # Python box (bottom)
    ax.add_patch(FancyBboxPatch((0.05, 0.18), 0.90, 0.32,
                                boxstyle="round,pad=0.015", linewidth=2,
                                edgecolor=BRIGHT_TEAL, facecolor=LIGHT_GRAY))
    ax.text(0.5, 0.475, "Python", transform=ax.transAxes,
            ha="center", va="center", fontsize=13, fontweight="bold",
            color=SEA_GREEN)
    python_lines = [
        "def clean_amount(amount):",
        '    amount = amount.replace("$", "")',
        '    amount = amount.replace(",", "")',
        '    amount = amount.replace("(", "-")',
        '    amount = amount.replace(")", "")',
        "    return float(amount)",
    ]
    for j, line in enumerate(python_lines):
        ax.text(0.08, 0.425 - j * 0.036, line,
                transform=ax.transAxes, ha="left", va="center",
                fontsize=10.5, color=DEEP_NAVY, **MONO)

    ax.text(0.5, 0.10,
            "One hides the logic.\nThe other reads like a checklist.",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=12, color=DEEP_NAVY, linespacing=1.5, fontstyle="italic")

    ax.text(0.5, 0.025, "PythonMuse LLC  |  pythonmuse.com",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=9, color=OCEAN_TEAL)
    save(fig, "25_carousel_03.png")


def make_carousel_04():
    """The simplest explanation — CTA."""
    fig, ax = plt.subplots(figsize=(10, 10))
    fig.patch.set_facecolor(DEEP_NAVY)
    ax.set_facecolor(DEEP_NAVY)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0.5, 0.82, "The Simplest Explanation",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=20, color=BRIGHT_TEAL, fontweight="bold")

    ax.add_patch(FancyBboxPatch((0.06, 0.52), 0.88, 0.22,
                                boxstyle="round,pad=0.02", linewidth=0,
                                facecolor=GOLDEN_YELLOW))
    ax.text(0.5, 0.645,
            '"It\'s basically an SOP for a computer."',
            transform=ax.transAxes, ha="center", va="center",
            fontsize=18, fontweight="bold", color=DEEP_NAVY,
            fontstyle="italic")

    ax.text(0.5, 0.40, "A script does not replace accountants.",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=14, color=WHITE)
    ax.text(0.5, 0.32, "It replaces repetitive clicking.",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=14, color=BRIGHT_TEAL, fontweight="bold")

    ax.text(0.5, 0.18, "Full article at:",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=12, color=WHITE, alpha=0.7)
    ax.text(0.5, 0.11, "github.com/PythonMuse/ai-ledger",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=13, color=BRIGHT_TEAL)

    ax.text(0.5, 0.04, "PythonMuse LLC  |  pythonmuse.com",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=9, color=OCEAN_TEAL)
    save(fig, "25_carousel_04.png")


# ─────────────────────────────────────────────────────────────
# Run all
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating Article 25 visuals...")
    make_hero()
    make_comparison()
    make_code_comparison()
    make_ladder()
    make_carousel_01()
    make_carousel_02()
    make_carousel_03()
    make_carousel_04()
    print("Done.")
