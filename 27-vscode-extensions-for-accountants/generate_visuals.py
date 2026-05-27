"""
Generate article visuals for Article 27 — Visual Studio Code Extensions for Accountants

Produces the following PNGs saved to visuals/:
  27_hero.png               — Hero / Cover card
  27_governance_funnel.png  — Five questions before installing (decision funnel)
  27_starter_stack.png      — Recommended starter extensions for accountants
  27_csv_before_after.png   — CSV file: plain text vs. Rainbow CSV colors
  27_name_impersonation.png — Extension name impersonation warning table
  27_carousel_01.png        — Social: Hook slide
  27_carousel_02.png        — Social: Extensions vs Libraries teaser
  27_carousel_03.png        — Social: Governance funnel summary
  27_carousel_04.png        — Social: Starter stack CTA

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
    ax.text(0.5, 0.935, "Visual Studio Code", transform=ax.transAxes,
            ha="center", va="center", fontsize=32, fontweight="bold",
            color=GOLDEN_YELLOW)
    ax.text(0.5, 0.855, "Extensions for Accountants", transform=ax.transAxes,
            ha="center", va="center", fontsize=30, fontweight="bold",
            color=GOLDEN_YELLOW)
    ax.text(0.5, 0.77, "Customize your workspace intentionally — not accidentally",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=13, color=BRIGHT_TEAL)

    # Center quote box
    ax.add_patch(FancyBboxPatch((0.07, 0.48), 0.86, 0.19,
                                boxstyle="round,pad=0.02", linewidth=2,
                                edgecolor=BRIGHT_TEAL, facecolor=LIGHT_GRAY))
    ax.text(0.5, 0.595, '"Just because you CAN install it',
            transform=ax.transAxes, ha="center", va="center",
            fontsize=15, fontstyle="italic", color=DEEP_NAVY)
    ax.text(0.5, 0.53, "doesn't mean you SHOULD.\"",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=15, fontstyle="italic", color=DEEP_NAVY)

    # Three concept cards
    cards = [
        ("Security", "Extensions can\nread your files", BRIGHT_TEAL),
        ("Governance", "Minimalism\nis a control", GOLDEN_YELLOW),
        ("Clarity", "Extensions ≠\nPython libraries", SOFT_SAGE),
    ]
    card_y = 0.16
    card_h = 0.25
    card_w = 0.24
    starts = [0.06, 0.38, 0.70]

    for (title, body, color), x in zip(cards, starts):
        ax.add_patch(FancyBboxPatch((x, card_y), card_w, card_h,
                                    boxstyle="round,pad=0.015", linewidth=0,
                                    facecolor=DEEP_NAVY))
        ax.text(x + card_w / 2, card_y + card_h * 0.73, title,
                transform=ax.transAxes, ha="center", va="center",
                fontsize=13, fontweight="bold", color=color)
        ax.text(x + card_w / 2, card_y + card_h * 0.35, body,
                transform=ax.transAxes, ha="center", va="center",
                fontsize=10, color=WHITE, linespacing=1.5)

    add_footer(fig, y=0.01)
    save(fig, "27_hero.png")


# ─────────────────────────────────────────────────────────────
# 2. Governance Funnel
# ─────────────────────────────────────────────────────────────
def make_governance_funnel():
    fig, ax = plt.subplots(figsize=(10, 13))
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    add_header_bar(ax, "Five Questions Before Installing",
                   subtitle="Apply this checklist before every extension install")

    questions = [
        ("1", "Who built it?", "Microsoft, GitHub, and established orgs are lower risk.\nBrand-new publishers with vague descriptions are not."),
        ("2", "How many people use it?", "Low install counts + unknown publisher + broad permissions\n= not yet ready for a finance workflow."),
        ("3", "Is it open source?", "Open source means community review is possible.\nTransparency improves trust."),
        ("4", "What does it actually do?", "Read the description. Does it send data externally?\nDoes it execute commands? Does it need API keys?"),
        ("5", "Is it actively maintained?", "Abandoned extensions accumulate unpatched vulnerabilities.\nAvoid projects with no recent activity."),
    ]

    funnel_widths = [0.88, 0.80, 0.72, 0.64, 0.56]
    y_positions = [0.760, 0.623, 0.485, 0.348, 0.210]
    box_h = 0.100
    accent_colors = [BRIGHT_TEAL, SEA_GREEN, OCEAN_TEAL, GOLDEN_YELLOW, SOFT_SAGE]

    for i, (num, question, detail) in enumerate(questions):
        w = funnel_widths[i]
        x = (1 - w) / 2
        y = y_positions[i]

        ax.add_patch(FancyBboxPatch((x, y), w, box_h,
                                    boxstyle="round,pad=0.01", linewidth=1.5,
                                    edgecolor=accent_colors[i], facecolor=LIGHT_GRAY))
        ax.add_patch(FancyBboxPatch((x, y), 0.055, box_h,
                                    boxstyle="round,pad=0.01", linewidth=0,
                                    facecolor=accent_colors[i]))
        ax.text(x + 0.028, y + box_h / 2, num,
                transform=ax.transAxes, ha="center", va="center",
                fontsize=16, fontweight="bold", color=WHITE)
        ax.text(x + 0.075, y + box_h * 0.72, question,
                transform=ax.transAxes, ha="left", va="center",
                fontsize=12, fontweight="bold", color=DEEP_NAVY)
        ax.text(x + 0.075, y + box_h * 0.28, detail,
                transform=ax.transAxes, ha="left", va="center",
                fontsize=9, color=OCEAN_TEAL, linespacing=1.4)

        if i < len(questions) - 1:
            next_y = y_positions[i + 1]
            ax.annotate("", xy=(0.5, next_y + box_h + 0.005),
                        xytext=(0.5, y - 0.005),
                        xycoords="axes fraction", textcoords="axes fraction",
                        arrowprops=dict(arrowstyle="->", color=DEEP_NAVY,
                                        lw=1.5, alpha=0.4))

    # Bottom conclusion bar
    ax.add_patch(FancyBboxPatch((0.10, 0.06), 0.80, 0.09,
                                boxstyle="round,pad=0.01", linewidth=0,
                                facecolor=DEEP_NAVY))
    ax.text(0.5, 0.113, "Minimalism is a control.",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=14, fontweight="bold", color=GOLDEN_YELLOW)
    ax.text(0.5, 0.075, "Install only what you truly need.",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=11, color=BRIGHT_TEAL)

    add_footer(fig, y=0.018)
    save(fig, "27_governance_funnel.png")


# ─────────────────────────────────────────────────────────────
# 3. Starter Stack
# ─────────────────────────────────────────────────────────────
def make_starter_stack():
    fig, ax = plt.subplots(figsize=(13, 9))
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    add_header_bar(ax, "Accountant Starter Stack",
                   subtitle="Five extensions. No more needed to start building real workflows.")

    extensions = [
        ("Python", "Microsoft",
         "Python language support, IntelliSense, linting, and debugging",
         BRIGHT_TEAL),
        ("GitHub Copilot", "GitHub",
         "AI co-pilot for writing and explaining code — if your organization approves it",
         GOLDEN_YELLOW),
        ("Markdown All in One", "Yu Zhang",
         "Preview and edit documentation, process notes, and CLAUDE.md files",
         SOFT_SAGE),
        ("Rainbow CSV", "mechatroner",
         "Color-code columns in CSV files so you can read them at a glance",
         SEA_GREEN),
        ("GitLens", "GitKraken",
         "Visual Git history, blame annotations, and change tracking",
         WARM_GLOW),
    ]

    row_start = 0.80
    row_gap = 0.125
    bar_h = 0.10

    for i, (name, publisher, desc, color) in enumerate(extensions):
        y = row_start - i * row_gap

        # Row background
        bg = LIGHT_GRAY if i % 2 == 0 else WHITE
        ax.add_patch(FancyBboxPatch((0.02, y - bar_h * 0.6), 0.96, bar_h,
                                    boxstyle="round,pad=0.008", linewidth=0,
                                    facecolor=bg))

        # Color accent left bar
        ax.add_patch(FancyBboxPatch((0.02, y - bar_h * 0.6), 0.008, bar_h,
                                    boxstyle="square,pad=0", linewidth=0,
                                    facecolor=color))

        ax.text(0.04, y, name, transform=ax.transAxes,
                ha="left", va="center", fontsize=13, fontweight="bold",
                color=DEEP_NAVY)
        ax.text(0.04, y - 0.030, f"by {publisher}", transform=ax.transAxes,
                ha="left", va="center", fontsize=9, color=OCEAN_TEAL)
        ax.text(0.38, y - 0.008, desc, transform=ax.transAxes,
                ha="left", va="center", fontsize=10.5, color=DEEP_NAVY)

    ax.text(0.5, 0.085,
            "You are building governed finance workflows — not competing in a gaming tournament.",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=11, fontstyle="italic", color=OCEAN_TEAL)

    add_footer(fig, y=0.015)
    save(fig, "27_starter_stack.png")


# ─────────────────────────────────────────────────────────────
# 4. CSV Before / After (Rainbow CSV demo)
# ─────────────────────────────────────────────────────────────
def make_csv_before_after():
    fig, ax = plt.subplots(figsize=(14, 7))
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    add_header_bar(ax, "The Same File. Two Very Different Reads.",
                   subtitle="One extension transforms how you read accounting data")

    panel_top    = 0.83
    panel_bottom = 0.10
    panel_h      = panel_top - panel_bottom

    # Left panel
    ax.add_patch(FancyBboxPatch((0.02, panel_bottom), 0.45, panel_h,
                                boxstyle="round,pad=0.01", linewidth=2,
                                edgecolor=ALERT_RED, facecolor=LIGHT_GRAY))
    ax.text(0.245, panel_top - 0.04, "Without Rainbow CSV",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=12, fontweight="bold", color=ALERT_RED)

    # Right panel
    ax.add_patch(FancyBboxPatch((0.53, panel_bottom), 0.45, panel_h,
                                boxstyle="round,pad=0.01", linewidth=2,
                                edgecolor=SEA_GREEN, facecolor=LIGHT_GRAY))
    ax.text(0.755, panel_top - 0.04, "With Rainbow CSV",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=12, fontweight="bold", color=SEA_GREEN)

    headers   = ["Account", "Description",   "Debit",  "Credit", "Period"]
    rows_data = [
        ["1001",  "Cash Operating",  "50,000", "—",      "2024-12"],
        ["2010",  "Accts Recv.",      "18,500", "—",      "2024-12"],
        ["3010",  "Revenue",          "—",      "68,500", "2024-12"],
        ["4020",  "Accts Payable",    "—",      "12,000", "2024-12"],
    ]
    col_colors = [DEEP_NAVY, OCEAN_TEAL, SEA_GREEN, ALERT_RED, "#7B5EA7"]
    col_x      = [0.545, 0.617, 0.750, 0.820, 0.885]

    row_y0  = 0.715
    row_gap = 0.115
    MONO    = {"fontfamily": "monospace"}

    # Before panel — all one color
    bef_x = 0.038
    ax.text(bef_x, row_y0, "Account,Description,Debit,Credit,Period",
            transform=ax.transAxes, ha="left", va="center",
            fontsize=8.5, fontweight="bold", color=DEEP_NAVY, **MONO)
    before_rows = [
        "1001,Cash Operating,50000,,2024-12",
        "2010,Accts Receivable,18500,,2024-12",
        "3010,Revenue,,68500,2024-12",
        "4020,Accts Payable,,12000,2024-12",
    ]
    for i, row_str in enumerate(before_rows):
        ax.text(bef_x, row_y0 - row_gap * (i + 1), row_str,
                transform=ax.transAxes, ha="left", va="center",
                fontsize=8.5, color="#555555", **MONO)

    ax.text(0.245, panel_bottom + 0.035, "Which column is the amount?",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=10, color=ALERT_RED, fontstyle="italic")

    # After panel — each column a distinct color
    for j, (header, color) in enumerate(zip(headers, col_colors)):
        ax.text(col_x[j], row_y0, header,
                transform=ax.transAxes, ha="left", va="center",
                fontsize=8.5, fontweight="bold", color=color, **MONO)
    for i, row in enumerate(rows_data):
        y = row_y0 - row_gap * (i + 1)
        for j, (val, color) in enumerate(zip(row, col_colors)):
            ax.text(col_x[j], y, val,
                    transform=ax.transAxes, ha="left", va="center",
                    fontsize=8.5, color=color, **MONO)

    ax.text(0.755, panel_bottom + 0.035, "Every column is instantly distinct.",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=10, color=SEA_GREEN, fontstyle="italic")

    add_footer(fig, y=0.015)
    save(fig, "27_csv_before_after.png")


# ─────────────────────────────────────────────────────────────
# 5. Name Impersonation Warning
# ─────────────────────────────────────────────────────────────
def make_name_impersonation():
    fig, ax = plt.subplots(figsize=(13, 9))
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    add_header_bar(ax, "The Name Is Not the Publisher",
                   subtitle="Always verify the publisher account — not just the extension title")

    entries = [
        ("claude-ai-assistant",      "dev-tools-pro-2024",    False, "Not affiliated with Anthropic"),
        ("github-copilot-enhancer",  "aiextensions-hub",      False, "Not affiliated with GitHub"),
        ("ms-python-official",       "python-tools-ltd",      False, "Not affiliated with Microsoft"),
        ("Python",                   "ms-python  (Microsoft)", True,  "Official — verified publisher"),
    ]

    col_x_name   = 0.04
    col_x_pub    = 0.38
    col_x_status = 0.73
    row_start    = 0.80
    row_gap      = 0.130
    box_h        = 0.100

    # Column headers
    for x, label in [
        (col_x_name,   "Extension Title"),
        (col_x_pub,    "Publisher Account"),
        (col_x_status, "Status"),
    ]:
        ax.text(x, row_start + 0.025, label,
                transform=ax.transAxes, ha="left", va="center",
                fontsize=11, fontweight="bold", color=DEEP_NAVY)

    ax.plot([0.02, 0.98], [row_start - 0.005, row_start - 0.005],
            transform=ax.transAxes, color=DEEP_NAVY, linewidth=1, alpha=0.25)

    for i, (name, publisher, verified, note) in enumerate(entries):
        y      = row_start - row_gap * (i + 1) + 0.04
        bg     = LIGHT_GRAY if i % 2 == 0 else WHITE
        accent = SEA_GREEN if verified else ALERT_RED

        ax.add_patch(FancyBboxPatch((0.02, y - box_h * 0.55), 0.96, box_h,
                                    boxstyle="round,pad=0.005", linewidth=0,
                                    facecolor=bg))
        ax.add_patch(FancyBboxPatch((0.02, y - box_h * 0.55), 0.006, box_h,
                                    boxstyle="square,pad=0", linewidth=0,
                                    facecolor=accent))

        ax.text(col_x_name, y, name,
                transform=ax.transAxes, ha="left", va="center",
                fontsize=11, color=DEEP_NAVY, fontfamily="monospace")
        ax.text(col_x_pub, y, publisher,
                transform=ax.transAxes, ha="left", va="center",
                fontsize=10, color=OCEAN_TEAL)

        status_icon  = "✓  Verified" if verified else "⚠  Unverified"
        status_color = SEA_GREEN     if verified else ALERT_RED
        ax.text(col_x_status, y + 0.013, status_icon,
                transform=ax.transAxes, ha="left", va="center",
                fontsize=11, fontweight="bold", color=status_color)
        ax.text(col_x_status, y - 0.020, note,
                transform=ax.transAxes, ha="left", va="center",
                fontsize=8.5, color=OCEAN_TEAL, fontstyle="italic")

    # Bottom callout
    ax.add_patch(FancyBboxPatch((0.04, 0.06), 0.92, 0.075,
                                boxstyle="round,pad=0.01", linewidth=0,
                                facecolor=DEEP_NAVY))
    ax.text(0.5, 0.100,
            "Look for the verification badge and the official publisher name — not just the title.",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=11, fontweight="bold", color=GOLDEN_YELLOW)

    add_footer(fig, y=0.015)
    save(fig, "27_name_impersonation.png")


# ─────────────────────────────────────────────────────────────
# 6–9. Social carousel slides (square, 10x10)
# ─────────────────────────────────────────────────────────────
def make_carousel_01():
    fig, ax = plt.subplots(figsize=(10, 10))
    fig.patch.set_facecolor(DEEP_NAVY)
    ax.set_facecolor(DEEP_NAVY)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0.5, 0.82, "There is a moment every accountant", transform=ax.transAxes,
            ha="center", va="center", fontsize=17, color=WHITE)
    ax.text(0.5, 0.73, "has after opening VS Code:", transform=ax.transAxes,
            ha="center", va="center", fontsize=17, color=WHITE)

    ax.add_patch(FancyBboxPatch((0.06, 0.42), 0.88, 0.24,
                                boxstyle="round,pad=0.02", linewidth=0,
                                facecolor=OCEAN_TEAL))
    ax.text(0.5, 0.565, "Install one tool. Then another.",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=16, color=WHITE)
    ax.text(0.5, 0.49, "Then a CSV helper. Then a mega pack.",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=16, color=GOLDEN_YELLOW, fontweight="bold")

    ax.text(0.5, 0.30, "Suddenly your workspace looks like a", transform=ax.transAxes,
            ha="center", va="center", fontsize=14, color=BRIGHT_TEAL)
    ax.text(0.5, 0.22, "NASCAR jacket.", transform=ax.transAxes,
            ha="center", va="center", fontsize=20, fontweight="bold",
            color=GOLDEN_YELLOW)

    ax.text(0.5, 0.10, "Here is how to install intentionally.",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=13, color=WHITE, alpha=0.85)
    ax.text(0.5, 0.035, FOOTER, transform=ax.transAxes,
            ha="center", va="center", fontsize=9, color=OCEAN_TEAL)
    save(fig, "27_carousel_01.png")


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
    ax.text(0.5, 0.938, "Extensions ≠ Libraries",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=22, fontweight="bold", color=GOLDEN_YELLOW)

    rows = [
        ("VS Code Extension", "Python Library"),
        ("Extends VS Code", "Extends Python"),
        ("Installed in VS Code", "Installed with pip"),
        ("Helps YOU work", "Helps your SCRIPT work"),
        ("Like a desk tool", "Like a skill you teach"),
    ]

    headers = rows[0]
    data = rows[1:]

    y0 = 0.78
    gap = 0.115

    for j, header in enumerate(headers):
        x = 0.28 if j == 0 else 0.72
        col_color = BRIGHT_TEAL if j == 0 else GOLDEN_YELLOW
        ax.add_patch(FancyBboxPatch((0.03 + j * 0.47, y0 - 0.04), 0.44, 0.075,
                                    boxstyle="round,pad=0.01", linewidth=0,
                                    facecolor=DEEP_NAVY))
        ax.text(x, y0, header, transform=ax.transAxes,
                ha="center", va="center", fontsize=13, fontweight="bold",
                color=col_color)

    for i, (left, right) in enumerate(data):
        y = y0 - gap * (i + 1)
        bg = LIGHT_GRAY if i % 2 == 0 else WHITE
        ax.add_patch(FancyBboxPatch((0.03, y - 0.04), 0.44, 0.075,
                                    boxstyle="round,pad=0.01", linewidth=0,
                                    facecolor=bg))
        ax.add_patch(FancyBboxPatch((0.53, y - 0.04), 0.44, 0.075,
                                    boxstyle="round,pad=0.01", linewidth=0,
                                    facecolor=bg))
        ax.text(0.28, y, left, transform=ax.transAxes,
                ha="center", va="center", fontsize=11.5, color=DEEP_NAVY)
        ax.text(0.72, y, right, transform=ax.transAxes,
                ha="center", va="center", fontsize=11.5, color=SEA_GREEN,
                fontweight="bold")

    ax.text(0.5, 0.065, "Full breakdown → Article 28: Python Libraries for Accountants",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=10.5, color=OCEAN_TEAL, fontstyle="italic")
    ax.text(0.5, 0.025, FOOTER, transform=ax.transAxes,
            ha="center", va="center", fontsize=9, color=OCEAN_TEAL)
    save(fig, "27_carousel_02.png")


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
    ax.text(0.5, 0.938, "Before You Install — Ask These 5",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=20, fontweight="bold", color=GOLDEN_YELLOW)

    questions = [
        "Who built it?",
        "How many people use it?",
        "Is it open source?",
        "What does it actually do?",
        "Is it actively maintained?",
    ]
    colors = [BRIGHT_TEAL, SEA_GREEN, OCEAN_TEAL, GOLDEN_YELLOW, SOFT_SAGE]
    y0 = 0.76
    gap = 0.12

    for i, (q, c) in enumerate(zip(questions, colors)):
        y = y0 - i * gap
        ax.add_patch(FancyBboxPatch((0.05, y - 0.04), 0.90, 0.08,
                                    boxstyle="round,pad=0.01", linewidth=0,
                                    facecolor=LIGHT_GRAY))
        ax.add_patch(FancyBboxPatch((0.05, y - 0.04), 0.055, 0.08,
                                    boxstyle="round,pad=0.01", linewidth=0,
                                    facecolor=c))
        ax.text(0.082, y, str(i + 1), transform=ax.transAxes,
                ha="center", va="center", fontsize=14, fontweight="bold",
                color=WHITE)
        ax.text(0.13, y, q, transform=ax.transAxes,
                ha="left", va="center", fontsize=13, color=DEEP_NAVY)

    ax.add_patch(FancyBboxPatch((0.08, 0.065), 0.84, 0.075,
                                boxstyle="round,pad=0.01", linewidth=0,
                                facecolor=DEEP_NAVY))
    ax.text(0.5, 0.103, "Minimalism is a control.",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=14, fontweight="bold", color=GOLDEN_YELLOW)

    ax.text(0.5, 0.022, FOOTER, transform=ax.transAxes,
            ha="center", va="center", fontsize=9, color=OCEAN_TEAL)
    save(fig, "27_carousel_03.png")


def make_carousel_04():
    fig, ax = plt.subplots(figsize=(10, 10))
    fig.patch.set_facecolor(DEEP_NAVY)
    ax.set_facecolor(DEEP_NAVY)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0.5, 0.85, "Accountant Starter Stack",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=22, fontweight="bold", color=BRIGHT_TEAL)
    ax.text(0.5, 0.775, "Five extensions. That is enough to start.",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=14, color=WHITE)

    stack = [
        ("Python", BRIGHT_TEAL),
        ("GitHub Copilot", GOLDEN_YELLOW),
        ("Markdown All in One", SOFT_SAGE),
        ("Rainbow CSV", SEA_GREEN),
        ("GitLens", WARM_GLOW),
    ]
    y0 = 0.67
    gap = 0.105
    for i, (name, color) in enumerate(stack):
        y = y0 - i * gap
        ax.add_patch(FancyBboxPatch((0.08, y - 0.035), 0.84, 0.075,
                                    boxstyle="round,pad=0.01", linewidth=0,
                                    facecolor=MIDNIGHT_TEAL))
        ax.add_patch(FancyBboxPatch((0.08, y - 0.035), 0.010, 0.075,
                                    boxstyle="square,pad=0", linewidth=0,
                                    facecolor=color))
        ax.text(0.15, y, name, transform=ax.transAxes,
                ha="left", va="center", fontsize=13, color=WHITE,
                fontweight="bold")

    ax.text(0.5, 0.115, "Full article at:",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=11, color=WHITE, alpha=0.7)
    ax.text(0.5, 0.06, "github.com/PythonMuse/ai-ledger",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=12, color=BRIGHT_TEAL)
    ax.text(0.5, 0.018, FOOTER, transform=ax.transAxes,
            ha="center", va="center", fontsize=9, color=OCEAN_TEAL)
    save(fig, "27_carousel_04.png")


# ─────────────────────────────────────────────────────────────
# Run all
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating Article 27 visuals...")
    make_hero()
    make_governance_funnel()
    make_starter_stack()
    make_csv_before_after()
    make_name_impersonation()
    make_carousel_01()
    make_carousel_02()
    make_carousel_03()
    make_carousel_04()
    print("Done.")
