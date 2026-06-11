"""
Generate article visuals for Article 32 — From AI Answers to Audit Trails

Produces the following PNGs saved to visuals/:
  32_hero.png          — "Based on what?" — chat answer vs. reviewable output
  32_chat_checklist.png — Chat-only validation checklist (8 items)
  32_folder_structure.png — Harness folder anatomy for monthly variance review
  32_chat_vs_harness.png  — Side-by-side comparison table: chat vs harness
  32_risk_matrix.png      — Risk-based decision: when to use chat vs. harness

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
             ha="center", va="center", fontsize=12, color=WHITE, fontweight="bold",
             transform=bar.transAxes)


def card(ax, x, y, w, h, facecolor, edgecolor=None, alpha=1.0, radius=0.03):
    ec = edgecolor or facecolor
    patch = FancyBboxPatch((x, y), w, h,
                           boxstyle=f"round,pad=0,rounding_size={radius}",
                           facecolor=facecolor, edgecolor=ec,
                           linewidth=1.5, alpha=alpha,
                           transform=ax.transData, clip_on=False)
    ax.add_patch(patch)
    return patch


# ─────────────────────────────────────────────────────────────
# 32_hero.png — "Based on what?" — Chat answer vs. reviewable output
# ─────────────────────────────────────────────────────────────
def make_hero():
    fig = plt.figure(figsize=(13, 7), facecolor=WHITE)
    add_header_bar(fig, "From AI Answers to Audit Trails  |  Article 32  |  PythonMuse LLC")
    add_footer(fig)

    ax = fig.add_axes([0.03, 0.10, 0.94, 0.82])
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5.5)
    ax.axis("off")
    ax.set_facecolor(WHITE)

    # ── LEFT: The AI answer ───────────────────────────────────
    card(ax, 0.1, 0.3, 5.2, 4.8, facecolor=LIGHT_GRAY, edgecolor=ALERT_ORANGE, radius=0.1)
    card(ax, 0.1, 4.5, 5.2, 0.6, facecolor=ALERT_ORANGE, radius=0.08)
    ax.text(2.7, 4.8, "THE AI ANSWER", ha="center", va="center",
            fontsize=12, color=WHITE, fontweight="bold")

    # Paragraph block
    paragraph = [
        "Travel expense increased primarily",
        "due to higher client site visits,",
        "conference attendance, and airfare",
        "cost increases.",
    ]
    for i, line in enumerate(paragraph):
        ax.text(0.45, 3.85 - i * 0.38, line, ha="left", va="center",
                fontsize=9.5, color=DEEP_NAVY)

    # Support audit notes
    notes = [
        ("Confidence level: very high.", DEEP_NAVY, "normal"),
        ("Support provided: none.", ALERT_RED, "bold"),
        ("Assumptions labeled: also none.", ALERT_RED, "bold"),
    ]
    for i, (line, color, weight) in enumerate(notes):
        ax.text(0.45, 2.20 - i * 0.50, line, ha="left", va="center",
                fontsize=9.5, color=color, fontweight=weight)

    ax.text(2.7, 0.62, '"The AI sounded confident."',
            ha="center", va="center", fontsize=9.5,
            color=OCEAN_TEAL, style="italic")

    # ── VS divider ────────────────────────────────────────────
    ax.text(6.0, 2.75, "VS", ha="center", va="center",
            fontsize=22, color=DEEP_NAVY, fontweight="bold", alpha=0.25)

    # ── RIGHT: The reviewable output ──────────────────────────
    card(ax, 6.7, 0.3, 5.1, 4.8, facecolor=LIGHT_GRAY, edgecolor=BRIGHT_TEAL, radius=0.1)
    card(ax, 6.7, 4.5, 5.1, 0.6, facecolor=BRIGHT_TEAL, radius=0.08)
    ax.text(9.25, 4.8, "THE REVIEWABLE OUTPUT", ha="center", va="center",
            fontsize=12, color=DEEP_NAVY, fontweight="bold")

    review_items = [
        (BRIGHT_TEAL,   "Source files documented"),
        (BRIGHT_TEAL,   "Row counts verified"),
        (OCEAN_TEAL,    "Facts separated from assumptions"),
        (OCEAN_TEAL,    "Supported vs. unsupported labeled"),
        (SOFT_SAGE,     "Totals tied to source"),
        (SEA_GREEN,     "Exceptions listed"),
        (OCEAN_TEAL,    "Reviewer checklist included"),
        (BRIGHT_TEAL,   "Can be reproduced next month"),
    ]
    for i, (color, label) in enumerate(review_items):
        y_pos = 4.05 - i * 0.44
        ax.text(6.95, y_pos, f"  {label}", ha="left", va="center",
                fontsize=9.5, color=color)

    ax.text(9.25, 0.62, '"Based on what? Here is the answer."',
            ha="center", va="center", fontsize=9.5,
            color=SEA_GREEN, style="italic")

    save(fig, "32_hero.png")


# ─────────────────────────────────────────────────────────────
# 32_chat_checklist.png — Chat-only validation checklist
# ─────────────────────────────────────────────────────────────
def make_chat_checklist():
    fig = plt.figure(figsize=(12, 8), facecolor=WHITE)
    add_header_bar(fig, "Chat-Only Validation Checklist  |  Article 32  |  PythonMuse LLC")
    add_footer(fig)

    ax = fig.add_axes([0.03, 0.10, 0.94, 0.82])
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.5)
    ax.axis("off")
    ax.set_facecolor(WHITE)

    ax.text(6.0, 6.25, "Before you use a chat-only AI output in accounting work",
            ha="center", va="center", fontsize=12, color=DEEP_NAVY,
            fontweight="bold")

    checklist = [
        (BRIGHT_TEAL,   "Did I provide actual source data?",
         "AI can only work with what you gave it. Pasting a total is not the same as the detail."),
        (BRIGHT_TEAL,   "Did AI separate facts from assumptions?",
         "Ask it to split the response. If it blended both, that is a signal."),
        (GOLDEN_YELLOW, "Did AI show the calculation or logic?",
         "A number without a formula is not support. Ask it to show the math."),
        (GOLDEN_YELLOW, "Do the numbers tie to the source?",
         "Verify totals manually. AI is not a calculator you can skip reviewing."),
        (SOFT_SAGE,     "Did AI make unsupported business explanations?",
         "If it said 'conference attendance' and you gave it no conference data, that is an assumption."),
        (SEA_GREEN,     "Did I independently verify key claims?",
         "You own the conclusion. AI drafts it. You verify it."),
        (OCEAN_TEAL,    "Did I remove sensitive data before pasting?",
         "Never paste employee names, client IDs, or confidential data into a cloud chat tool."),
        (WARM_GLOW,     "Did I save the prompt and response?",
         "If the output supports a business decision, keep a record. Audit trails start here."),
    ]

    for i, (color, question, detail) in enumerate(checklist):
        y = 5.6 - i * 0.68
        card(ax, 0.15, y - 0.28, 11.7, 0.62, facecolor=WHITE, edgecolor=color, radius=0.06)
        card(ax, 0.15, y - 0.28, 0.18, 0.62, facecolor=color, radius=0.06)

        ax.text(0.55, y + 0.04, f"  {question}", ha="left", va="center",
                fontsize=10, color=DEEP_NAVY, fontweight="bold")
        ax.text(0.55, y - 0.18, f"  {detail}", ha="left", va="center",
                fontsize=8.5, color=OCEAN_TEAL, style="italic")

    ax.text(6.0, 0.22,
            "Chat can absolutely help. But the first polished response is not the finished work.",
            ha="center", va="center", fontsize=10,
            color=DEEP_NAVY, style="italic")

    save(fig, "32_chat_checklist.png")


# ─────────────────────────────────────────────────────────────
# 32_folder_structure.png — Harness folder anatomy
# ─────────────────────────────────────────────────────────────
def make_folder_structure():
    fig = plt.figure(figsize=(15, 8.5), facecolor=WHITE)
    add_header_bar(fig, "Monthly Variance Review — Harness Folder Structure  |  Article 32  |  PythonMuse LLC")
    add_footer(fig)

    ax = fig.add_axes([0.03, 0.10, 0.94, 0.82])
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 6.8)
    ax.axis("off")
    ax.set_facecolor(WHITE)

    folders = [
        (BRIGHT_TEAL,   "raw_data/",        "Source files\nuntouched originals",
         ["gl_actuals_april.csv", "budget_april.csv", "prior_month_actuals.csv"]),
        (GOLDEN_YELLOW, "instructions/",    "Reusable accounting\nrules for AI",
         ["variance_review_skill.md"]),
        (SEA_GREEN,     "scripts/",         "Python validation\nand analysis",
         ["validate_variance.py"]),
        (SOFT_SAGE,     "outputs/",         "Final reviewed\nresults",
         ["variance_analysis.xlsx", "variance_explanation.md"]),
        (WARM_GLOW,     "evidence/",        "Audit trail —\ntie-outs & reviewer notes",
         ["tie_out_report.md", "review_questions.md"]),
    ]

    card_w = 2.72
    gap = 0.18
    start_x = 0.22
    card_h = 5.8
    header_h = 0.82

    for i, (color, folder, purpose, files) in enumerate(folders):
        x = start_x + i * (card_w + gap)
        y_bot = 0.55
        y_top = y_bot + card_h

        card(ax, x, y_bot, card_w, card_h, facecolor=WHITE, edgecolor=color, radius=0.09)
        card(ax, x, y_top - header_h, card_w, header_h, facecolor=color, radius=0.09)

        ax.text(x + card_w / 2, y_top - header_h / 2,
                folder, ha="center", va="center",
                fontsize=13, color=DEEP_NAVY, fontweight="bold",
                fontfamily="monospace")

        # GOLDEN_YELLOW and WARM_GLOW are illegible on white — use OCEAN_TEAL instead
        purpose_color = OCEAN_TEAL if color in (GOLDEN_YELLOW, WARM_GLOW) else color
        ax.text(x + card_w / 2, y_top - header_h - 0.58,
                purpose, ha="center", va="center",
                fontsize=11, color=purpose_color, fontweight="bold",
                style="italic", linespacing=1.45)

        for j, fname in enumerate(files):
            fy = y_top - header_h - 1.55 - j * 0.68
            ax.text(x + 0.14, fy, fname, ha="left", va="center",
                    fontsize=11, color=MIDNIGHT_TEAL, fontfamily="monospace")

    ax.text(7.5, 0.26,
            "Structure is a control.  Knowing where the source file is, is a control.  Evidence is a control.",
            ha="center", va="center", fontsize=11.5,
            color=DEEP_NAVY, style="italic")

    save(fig, "32_folder_structure.png")


# ─────────────────────────────────────────────────────────────
# 32_chat_vs_harness.png — Comparison table
# ─────────────────────────────────────────────────────────────
def make_chat_vs_harness():
    fig = plt.figure(figsize=(13, 7.5), facecolor=WHITE)
    add_header_bar(fig, "Chat vs. AI Work Harness  |  Article 32  |  PythonMuse LLC")
    add_footer(fig)

    ax = fig.add_axes([0.03, 0.10, 0.94, 0.82])
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.2)
    ax.axis("off")
    ax.set_facecolor(WHITE)

    # Column headers
    card(ax, 0.1, 5.6, 11.8, 0.52, facecolor=DEEP_NAVY, radius=0.06)
    ax.text(2.5, 5.86, "Validation Question", ha="center", va="center",
            fontsize=10.5, color=GOLDEN_YELLOW, fontweight="bold")
    ax.text(6.5, 5.86, "Chat-Only Approach", ha="center", va="center",
            fontsize=10.5, color=WARM_GLOW, fontweight="bold")
    ax.text(10.2, 5.86, "AI Work Harness", ha="center", va="center",
            fontsize=10.5, color=BRIGHT_TEAL, fontweight="bold")

    rows = [
        ("What data did AI use?",
         "Ask it to list the sources",
         "Source files stored in project folder"),
        ("Did totals tie?",
         "Ask AI to show math, then check manually",
         "Script produces a tie-out report"),
        ("Did AI make assumptions?",
         "Ask it to separate facts from assumptions",
         "Instructions require that format every time"),
        ("Can I rerun next month?",
         "Recreate the prompt manually",
         "Reuse the folder structure and script"),
        ("Can someone review it?",
         "Share the chat transcript",
         "Share files, outputs, scripts, and evidence"),
        ("Can I prove what changed?",
         "Difficult unless manually saved",
         "Version history can show changes"),
    ]

    for i, (question, chat_ans, harness_ans) in enumerate(rows):
        y = 4.75 - i * 0.78
        bg = LIGHT_GRAY if i % 2 == 0 else WHITE
        card(ax, 0.1, y - 0.28, 11.8, 0.72, facecolor=bg, edgecolor=bg, radius=0.04)

        ax.text(0.25, y + 0.08, question, ha="left", va="center",
                fontsize=9.5, color=DEEP_NAVY, fontweight="bold")
        ax.text(4.4, y + 0.08, chat_ans, ha="left", va="center",
                fontsize=9, color=OCEAN_TEAL)
        ax.text(8.15, y + 0.08, harness_ans, ha="left", va="center",
                fontsize=9, color=SEA_GREEN)

        # divider lines
        ax.axvline(4.35, ymin=(y - 0.28) / 6.2, ymax=(y + 0.44) / 6.2,
                   color=OCEAN_TEAL, linewidth=0.7, alpha=0.4)
        ax.axvline(8.1, ymin=(y - 0.28) / 6.2, ymax=(y + 0.44) / 6.2,
                   color=OCEAN_TEAL, linewidth=0.7, alpha=0.4)

    ax.text(6.0, 0.22,
            "Neither approach is perfect.  The right choice depends on the risk of the work.",
            ha="center", va="center", fontsize=10,
            color=DEEP_NAVY, style="italic")

    save(fig, "32_chat_vs_harness.png")


# ─────────────────────────────────────────────────────────────
# 32_risk_matrix.png — Risk-based decision: chat vs. harness
# ─────────────────────────────────────────────────────────────
def make_risk_matrix():
    fig = plt.figure(figsize=(13, 7), facecolor=WHITE)
    add_header_bar(fig, "Match the Tool to the Risk  |  Article 32  |  PythonMuse LLC")
    add_footer(fig)

    ax = fig.add_axes([0.03, 0.10, 0.94, 0.82])
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5.5)
    ax.axis("off")
    ax.set_facecolor(WHITE)

    # ── LEFT: Chat is fine ────────────────────────────────────
    card(ax, 0.1, 0.3, 5.3, 4.8, facecolor=LIGHT_GRAY, edgecolor=BRIGHT_TEAL, radius=0.1)
    card(ax, 0.1, 4.5, 5.3, 0.6, facecolor=BRIGHT_TEAL, radius=0.08)
    ax.text(2.75, 4.8, "CHAT IS FINE", ha="center", va="center",
            fontsize=12, color=DEEP_NAVY, fontweight="bold")
    ax.text(2.75, 4.35, "Lower-risk, exploratory work", ha="center", va="center",
            fontsize=9.5, color=OCEAN_TEAL, style="italic")

    chat_ok = [
        "Brainstorming explanations",
        "Drafting emails and memos",
        "Summarizing non-sensitive articles",
        "Creating first drafts",
        "Explaining unfamiliar concepts",
        "Turning rough notes into clean language",
        "Reviewing language and tone",
    ]
    for i, item in enumerate(chat_ok):
        y_pos = 4.0 - i * 0.47
        ax.text(0.45, y_pos, f"   {item}", ha="left", va="center",
                fontsize=9.5, color=DEEP_NAVY)

    ax.text(2.75, 0.62, "A sticky note works fine for a grocery list.",
            ha="center", va="center", fontsize=9, color=SEA_GREEN, style="italic")

    # ── VS divider ────────────────────────────────────────────
    ax.text(6.0, 2.75, "→", ha="center", va="center",
            fontsize=26, color=DEEP_NAVY, fontweight="bold", alpha=0.20)

    # ── RIGHT: Consider a harness ─────────────────────────────
    card(ax, 6.6, 0.3, 5.2, 4.8, facecolor=LIGHT_GRAY, edgecolor=GOLDEN_YELLOW, radius=0.1)
    card(ax, 6.6, 4.5, 5.2, 0.6, facecolor=GOLDEN_YELLOW, radius=0.08)
    ax.text(9.2, 4.8, "CONSIDER A HARNESS", ha="center", va="center",
            fontsize=12, color=DEEP_NAVY, fontweight="bold")
    ax.text(9.2, 4.35, "Higher-risk, evidence-required work", ha="center", va="center",
            fontsize=9.5, color=OCEAN_TEAL, style="italic")

    harness_items = [
        "Reconciliations",
        "Variance analysis for reporting",
        "Financial reporting support",
        "Forecasting and board packages",
        "Sensitive data analysis",
        "Repeatable month-end workflows",
        '"How did you get this number?"',
    ]
    for i, item in enumerate(harness_items):
        y_pos = 4.0 - i * 0.47
        ax.text(6.75, y_pos, f"   {item}", ha="left", va="center",
                fontsize=9.5, color=DEEP_NAVY)

    ax.text(9.2, 0.62, "Not ideal for lease accounting.",
            ha="center", va="center", fontsize=9, color=OCEAN_TEAL, style="italic")

    save(fig, "32_risk_matrix.png")


# ─────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating Article 32 visuals...")
    make_hero()
    make_chat_checklist()
    make_folder_structure()
    make_chat_vs_harness()
    make_risk_matrix()
    print("Done.")
