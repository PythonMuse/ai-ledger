"""
Generate article visuals for Article 30 — AI Routines for Accountants

Produces the following PNGs saved to visuals/:
  30_hero.png            — Evolution: Prompt → Skill → Routine → Evidence
  30_folder_structure.png — tax-guidance/ folder tree as styled boxes
  30_routine_pattern.png — Flow: Source → KB → Routine → Proposed Update → Human Review → Commit
  30_yaml_anatomy.png    — Annotated YAML routine block with accounting-language callouts
  30_review_package.png  — Anatomy of the proposed-change review package
  30_six_examples.png    — 2×3 card grid of 6 use cases
  30_evolution.png       — Staircase: Prompts → Skills → Routines → Controls → Evidence
  30_carousel_01.png     — Carousel Slide 1: Hook
  30_carousel_02.png     — Carousel Slide 2: The evolution (Prompt → Skill → Routine → Evidence)
  30_carousel_03.png     — Carousel Slide 3: The routine pattern (condensed, vertical)
  30_carousel_04.png     — Carousel Slide 4: The governance point
  30_carousel_05.png     — Carousel Slide 5: Six use cases teaser
  30_carousel_06.png     — Carousel Slide 6: Why this matters for accounting
  30_carousel_07.png     — Carousel Slide 7: CTA / template

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
    patch = FancyBboxPatch((x, y), w, h,
                           boxstyle=f"round,pad=0,rounding_size={radius}",
                           facecolor=facecolor, edgecolor=ec,
                           linewidth=1.5, alpha=alpha,
                           transform=ax.transData, clip_on=False)
    ax.add_patch(patch)
    return patch


# ─────────────────────────────────────────────────────────────
# 30_hero.png — Prompt → Skill → Routine → Evidence evolution
# ─────────────────────────────────────────────────────────────
def make_hero():
    fig = plt.figure(figsize=(13, 6.5), facecolor=WHITE)
    add_header_bar(fig, "AI Routines for Accountants  |  Article 30  |  PythonMuse LLC")
    add_footer(fig)

    ax = fig.add_axes([0.03, 0.10, 0.94, 0.82])
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5)
    ax.axis("off")
    ax.set_facecolor(WHITE)

    ax.text(6.0, 4.7, "The shift from asking to doing — on a schedule",
            ha="center", va="center", fontsize=13,
            color=DEEP_NAVY, style="italic")

    stages = [
        (MIDNIGHT_TEAL, BRIGHT_TEAL,   "PROMPT",   "Open chat.\nAsk a question.\nGet an answer.\nMove on.",             "Where\nmost of us\nstart"),
        (OCEAN_TEAL,    GOLDEN_YELLOW, "SKILL",    "Reusable instructions.\nStored guidance.\nConsistent answers.\nEvery time.",    "Where the\nwork gets\nrepeatable"),
        (SEA_GREEN,     WHITE,         "ROUTINE",  "Scheduled check.\nCompare source.\nPropose update.\nWait for review.", "Where AI\nstarts working\nbefore you ask"),
        (BRIGHT_TEAL,   DEEP_NAVY,     "EVIDENCE", "Who changed it.\nWhen it changed.\nWhy it changed.\nAudit-ready.",    "Where\naccountants\nfeel at home"),
    ]

    card_w = 2.5
    gap = 0.35
    start_x = 0.3

    for i, (bg, text_col, title, body, footnote) in enumerate(stages):
        x = start_x + i * (card_w + gap)

        card(ax, x, 0.4, card_w, 3.9, facecolor=bg, radius=0.1)

        ax.text(x + card_w / 2, 4.0, title,
                ha="center", va="center", fontsize=16,
                color=text_col, fontweight="bold")

        for j, line in enumerate(body.split("\n")):
            ax.text(x + card_w / 2, 3.3 - j * 0.5, line,
                    ha="center", va="center", fontsize=11,
                    color=WHITE if bg != BRIGHT_TEAL else DEEP_NAVY)

        ax.text(x + card_w / 2, 0.75, footnote,
                ha="center", va="center", fontsize=9.5,
                color=WARM_GLOW if bg != BRIGHT_TEAL else OCEAN_TEAL,
                style="italic", linespacing=1.4)

        if i < len(stages) - 1:
            arrow_x = x + card_w + 0.05
            ax.annotate("", xy=(arrow_x + 0.25, 2.35), xytext=(arrow_x, 2.35),
                        arrowprops=dict(arrowstyle="->", color=OCEAN_TEAL, lw=2.5))

    save(fig, "30_hero.png")


# ─────────────────────────────────────────────────────────────
# 30_folder_structure.png — tax-guidance/ tree
# ─────────────────────────────────────────────────────────────
def make_folder_structure():
    fig = plt.figure(figsize=(11, 7), facecolor=WHITE)
    add_header_bar(fig, "From Scattered Files to a Structured Knowledge Base  |  Article 30  |  PythonMuse LLC")
    add_footer(fig)

    ax = fig.add_axes([0.03, 0.10, 0.94, 0.82])
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.set_facecolor(WHITE)

    ax.text(5.5, 5.7, "One prompt converts scattered guidance into a version-controlled knowledge base",
            ha="center", va="center", fontsize=12,
            color=DEEP_NAVY, style="italic")

    tree = [
        (0,   DEEP_NAVY,     GOLDEN_YELLOW, "tax-guidance/",               "Root folder — the whole knowledge base lives here"),
        (1,   MIDNIGHT_TEAL, BRIGHT_TEAL,   "  sources/",                  "Official guidance, as-fetched"),
        (2,   OCEAN_TEAL,    WHITE,         "    rosa-source-summary.md",   "Plain-English summary of the official source"),
        (1,   MIDNIGHT_TEAL, BRIGHT_TEAL,   "  company-guidance/",         "Your team's interpretation"),
        (2,   OCEAN_TEAL,    WHITE,         "    company-application.md",   "How the rule applies to your company"),
        (1,   MIDNIGHT_TEAL, BRIGHT_TEAL,   "  skills/",                   "AI skill files for this topic"),
        (2,   OCEAN_TEAL,    WHITE,         "    review-skill.md",          "Instructions for AI-assisted reviews"),
        (1,   MIDNIGHT_TEAL, BRIGHT_TEAL,   "  routines/",                 "Scheduled monitoring configuration"),
        (2,   OCEAN_TEAL,    WHITE,         "    monitor-guidance.yaml",    "Routine: fetch, compare, propose"),
        (1,   MIDNIGHT_TEAL, BRIGHT_TEAL,   "  evidence/",                 "Audit trail — proposed and approved changes"),
        (2,   OCEAN_TEAL,    WHITE,         "    change-review-log.md",     "Who reviewed what, and when"),
        (1,   SEA_GREEN,     WHITE,         "  README.md",                  "Setup instructions for the team"),
    ]

    row_h = 0.42
    start_y = 5.15

    for i, (indent, bg, text_col, name, desc) in enumerate(tree):
        y = start_y - i * row_h
        card(ax, 0.2, y - 0.19, 10.6, row_h - 0.04, facecolor=bg, radius=0.05)
        ax.text(0.5 + indent * 0.25, y + 0.02, name,
                ha="left", va="center", fontsize=11,
                color=text_col, fontfamily="monospace", fontweight="bold" if indent <= 1 else "normal")
        ax.text(5.8, y + 0.02, desc,
                ha="left", va="center", fontsize=10.5,
                color=WARM_GLOW if bg == DEEP_NAVY else (GOLDEN_YELLOW if bg == MIDNIGHT_TEAL else WHITE),
                style="italic")

    save(fig, "30_folder_structure.png")


# ─────────────────────────────────────────────────────────────
# 30_routine_pattern.png — Source → KB → Routine → … → Commit
# ─────────────────────────────────────────────────────────────
def make_routine_pattern():
    fig = plt.figure(figsize=(13, 6.2), facecolor=WHITE)
    add_header_bar(fig, "The Routine Pattern  |  Article 30  |  PythonMuse LLC")
    add_footer(fig)

    ax = fig.add_axes([0.03, 0.11, 0.94, 0.81])
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4.5)
    ax.axis("off")
    ax.set_facecolor(WHITE)

    ax.text(6.0, 4.2, "Source  →  Local Knowledge Base  →  Routine  →  Proposed Update  →  Human Review  →  Commit",
            ha="center", va="center", fontsize=11.5,
            color=DEEP_NAVY, fontweight="bold")

    steps = [
        (OCEAN_TEAL,    "SOURCE",           "Official website,\nregulation, or policy",         "Where does\nthe truth live?"),
        (MIDNIGHT_TEAL, "LOCAL KB",         "Your structured\nmarkdown files",                  "Where did we\ndocument it?"),
        (SEA_GREEN,     "ROUTINE",          "Scheduled check:\nfetch and compare",              "How often\ndo we verify?"),
        (GOLDEN_YELLOW, "PROPOSED\nUPDATE", "Proposed change\nfile — not live yet",             "What did\nAI find?"),
        (BRIGHT_TEAL,   "HUMAN\nREVIEW",   "Tax manager or\nprocess owner reviews",            "Is this\nchange right?"),
        (SOFT_SAGE,     "COMMIT",           "Approved change\nenters version control",          "Evidence\npreserved."),
    ]

    box_w = 1.85
    box_h = 2.9
    gap = 0.1
    start_x = 0.2
    y_box = 0.4

    for i, (color, title, body, question) in enumerate(steps):
        x = start_x + i * (box_w + gap)

        card(ax, x, y_box, box_w, box_h, facecolor=color, radius=0.08)

        title_color = DEEP_NAVY if color in (GOLDEN_YELLOW, BRIGHT_TEAL, SOFT_SAGE) else WHITE
        body_color  = DEEP_NAVY if color in (GOLDEN_YELLOW, BRIGHT_TEAL, SOFT_SAGE) else WHITE
        q_color     = MIDNIGHT_TEAL if color in (GOLDEN_YELLOW, BRIGHT_TEAL, SOFT_SAGE) else WARM_GLOW

        ax.text(x + box_w / 2, y_box + box_h - 0.35, title,
                ha="center", va="center", fontsize=12.5,
                color=title_color, fontweight="bold", linespacing=1.3)

        for j, line in enumerate(body.split("\n")):
            ax.text(x + box_w / 2, y_box + box_h - 0.95 - j * 0.42, line,
                    ha="center", va="center", fontsize=10, color=body_color)

        for j, line in enumerate(question.split("\n")):
            ax.text(x + box_w / 2, y_box + 0.55 - j * 0.32, line,
                    ha="center", va="center", fontsize=9.5,
                    color=q_color, style="italic")

        if i < len(steps) - 1:
            ax_x = x + box_w + 0.01
            ax.annotate("", xy=(ax_x + 0.08, y_box + box_h / 2),
                        xytext=(ax_x, y_box + box_h / 2),
                        arrowprops=dict(arrowstyle="->", color=DEEP_NAVY, lw=2.0))

    save(fig, "30_routine_pattern.png")


# ─────────────────────────────────────────────────────────────
# 30_yaml_anatomy.png — Annotated YAML routine block
# ─────────────────────────────────────────────────────────────
def make_yaml_anatomy():
    fig = plt.figure(figsize=(13, 8), facecolor=WHITE)
    add_header_bar(fig, "Reading a Routine File Like an Accountant  |  Article 30  |  PythonMuse LLC")
    add_footer(fig)

    ax = fig.add_axes([0.03, 0.09, 0.94, 0.83])
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.5)
    ax.axis("off")
    ax.set_facecolor(WHITE)

    ax.text(6.0, 6.2, "The YAML is not the AI brain — it is the checklist taped to the monitor",
            ha="center", va="center", fontsize=13,
            color=DEEP_NAVY, fontweight="bold", style="italic")

    card(ax, 0.15, 0.4, 5.2, 5.5, facecolor=MIDNIGHT_TEAL, radius=0.08)
    ax.text(2.75, 5.68, "monitor-guidance.yaml", ha="center", va="center",
            fontsize=11, color=GOLDEN_YELLOW, fontfamily="monospace", fontweight="bold")

    yaml_lines = [
        (BRIGHT_TEAL,   "routine_name: monitor_rosa_guidance"),
        (WHITE,         "owner: tax_department"),
        (GOLDEN_YELLOW, "frequency: weekly"),
        ("",            ""),
        (BRIGHT_TEAL,   "source_url: official ROSA guidance"),
        (WHITE,         "local_reference: sources/rosa-summary.md"),
        (WHITE,         "affected_skill: skills/review-skill.md"),
        ("",            ""),
        (SOFT_SAGE,     "steps:"),
        (WHITE,         "  - fetch_current_source"),
        (WHITE,         "  - compare_to_local_markdown"),
        (WHITE,         "  - identify_meaningful_changes"),
        (WHITE,         "  - draft_recommended_updates"),
        (WHITE,         "  - create_review_package"),
        ("",            ""),
        (GOLDEN_YELLOW, "approval_required: true"),
        ("",            ""),
        (ALERT_ORANGE,  "do_not:"),
        (WHITE,         "  - overwrite_approved_guidance"),
        (WHITE,         "  - update_skills_without_human_review"),
        (WHITE,         "  - make_final_tax_conclusions"),
    ]

    for i, (color, line) in enumerate(yaml_lines):
        if color:
            ax.text(0.42, 5.38 - i * 0.24, line, ha="left", va="center",
                    fontsize=9.5, color=color, fontfamily="monospace")

    # Evenly spaced from top to bottom of the plot area — previous fractional
    # scaling pushed the lower entries off the axes and into the footer bar.
    annotations = [
        (5.2,  BRIGHT_TEAL,   "WHO & HOW OFTEN",  "What is this routine?\nWho owns it? When does it run?"),
        (4.075, BRIGHT_TEAL,   "WHAT TO WATCH",     "Source of truth and the\nlocal file we compare against"),
        (2.95, SOFT_SAGE,     "THE STEPS",         "Ordered checklist — same\nlogic as a month-end close"),
        (1.825, GOLDEN_YELLOW, "HUMAN GATE",        "Nothing changes until\na human approves it"),
        (0.7,  ALERT_ORANGE,  "HARD LIMITS",       "Explicit do-nots —\nthe AI's red lines"),
    ]

    for y, color, label, question in annotations:
        ax.annotate("", xy=(5.55, y), xytext=(6.1, y),
                    arrowprops=dict(arrowstyle="<-", color=color, lw=1.5))

        card(ax, 6.2, y - 0.35, 5.6, 0.78, facecolor=WHITE, edgecolor=color, radius=0.05)
        ax.text(6.42, y + 0.18, label, ha="left", va="center",
                fontsize=12, color=color, fontweight="bold")
        ax.text(6.42, y - 0.1, question, ha="left", va="center",
                fontsize=10.5, color=DEEP_NAVY, linespacing=1.4)

    save(fig, "30_yaml_anatomy.png")


# ─────────────────────────────────────────────────────────────
# 30_review_package.png — Anatomy of the proposed-change file
# ─────────────────────────────────────────────────────────────
def make_review_package():
    fig = plt.figure(figsize=(13, 9), facecolor=WHITE)
    add_header_bar(fig, "The Proposed Change Package  |  Article 30  |  PythonMuse LLC")
    add_footer(fig)

    ax = fig.add_axes([0.03, 0.09, 0.94, 0.83])
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7.5)
    ax.axis("off")
    ax.set_facecolor(WHITE)

    ax.text(6.0, 7.15, "AI identifies and recommends. Human reviews and approves. Then the change is committed.",
            ha="center", va="center", fontsize=12,
            color=DEEP_NAVY, style="italic")

    card(ax, 0.2, 0.4, 5.1, 6.6, facecolor=LIGHT_GRAY, edgecolor=OCEAN_TEAL, radius=0.08)
    ax.text(2.75, 6.7, "2026-05-21-proposed-update.md", ha="center", va="center",
            fontsize=10.5, color=OCEAN_TEAL, fontfamily="monospace", fontweight="bold")

    sections = [
        (BRIGHT_TEAL,   "## Date checked",          "May 21, 2026"),
        (BRIGHT_TEAL,   "## Source reviewed",        "Official ROSA guidance page"),
        (GOLDEN_YELLOW, "## Summary of detected change", "Updated language re: documentation requirements"),
        (GOLDEN_YELLOW, "## Potential impact",       "May affect documentation checklist"),
        (WARM_GLOW,     "## Files potentially impacted", "company-application.md\nskills/review-skill.md"),
        (SOFT_SAGE,     "## Recommended update",     "Add new supplier declaration step"),
        (ALERT_ORANGE,  "## Human review required",  "Yes."),
        (ALERT_RED,     "## Decision",               "[ ] Approved  [ ] Rejected  [ ] Needs research"),
    ]

    y_pos = 6.35
    for header_color, header, content in sections:
        ax.text(0.5, y_pos, header, ha="left", va="center",
                fontsize=10, color=header_color, fontfamily="monospace", fontweight="bold")
        for j, line in enumerate(content.split("\n")):
            ax.text(0.5, y_pos - 0.34 - j * 0.28, line, ha="left", va="center",
                    fontsize=9.5, color=DEEP_NAVY, fontfamily="monospace")
        y_pos -= 0.7 + content.count("\n") * 0.28

    callouts = [
        (6.5, BRIGHT_TEAL,   "WHAT CHANGED",    "AI reports exactly what it found\nand where it looked"),
        (4.7,  GOLDEN_YELLOW, "IMPACT ANALYSIS", "Which files and processes\nare potentially affected"),
        (2.9,  SOFT_SAGE,     "RECOMMENDATION",  "AI proposes — it does not\ndecide or implement"),
        (1.1,  ALERT_RED,     "DECISION GATE",   "Reviewer checks a box.\nNothing changes without it."),
    ]

    for y_frac, color, label, note in callouts:
        ax.annotate("", xy=(5.55, y_frac), xytext=(6.1, y_frac),
                    arrowprops=dict(arrowstyle="<-", color=color, lw=1.5))
        card(ax, 6.2, y_frac - 0.35, 5.6, 0.78, facecolor=WHITE, edgecolor=color, radius=0.05)
        ax.text(6.42, y_frac + 0.18, label, ha="left", va="center",
                fontsize=12, color=color, fontweight="bold")
        ax.text(6.42, y_frac - 0.1, note, ha="left", va="center",
                fontsize=10.5, color=DEEP_NAVY, linespacing=1.4)

    save(fig, "30_review_package.png")


# ─────────────────────────────────────────────────────────────
# 30_six_examples.png — 2×3 grid of use cases
# ─────────────────────────────────────────────────────────────
def make_six_examples():
    fig = plt.figure(figsize=(13, 8.5), facecolor=WHITE)
    add_header_bar(fig, "Where AI Routines Can Help Your Team  |  Article 30  |  PythonMuse LLC")
    add_footer(fig)

    ax = fig.add_axes([0.03, 0.09, 0.94, 0.83])
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis("off")
    ax.set_facecolor(WHITE)

    ax.text(6.0, 6.75, "The pattern is the same. The topic changes.",
            ha="center", va="center", fontsize=12,
            color=DEEP_NAVY, style="italic")

    examples = [
        (BRIGHT_TEAL,   "Sales Tax\nNexus",
         "Monthly",
         "Check state tax websites for threshold\nor filing requirement updates.\nCompare to internal guidance.\nFlag changes for tax manager."),

        (GOLDEN_YELLOW, "Payroll Tax\nGuidance",
         "Quarterly",
         "Check official payroll guidance\nfor selected jurisdictions.\nFlag rate, threshold, or filing changes.\nPrepare update for review."),

        (SEA_GREEN,     "Lease Accounting\nPolicy",
         "Quarterly",
         "Check standard setter or firm\nguidance pages.\nFlag new interpretations or\ndisclosure considerations."),

        (OCEAN_TEAL,    "Bank Rec\nException Rules",
         "Monthly",
         "After month-end, review recurring\nreconciling items.\nCompare to current reconciliation skill.\nRecommend new exception rules."),

        (SOFT_SAGE,     "Client Billing\nExceptions",
         "Triggered",
         "When billing completion email arrives,\ncheck exceptions against billing matrix.\nFlag unusual manual adjustments\nfor review."),

        (WARM_GLOW,     "Internal Policy\nMonitoring",
         "Monthly",
         "Check whether approved policy files\nhave changed.\nIdentify affected skills or scripts.\nCreate change impact summary."),
    ]

    card_w = 3.6
    card_h = 2.85
    col_gap = 0.3
    row_gap = 0.35
    cols = 3
    start_x = 0.3
    start_y = 0.4

    for i, (color, title, freq, body) in enumerate(examples):
        col = i % cols
        row = i // cols
        x = start_x + col * (card_w + col_gap)
        y = start_y + (1 - row) * (card_h + row_gap)

        card(ax, x, y, card_w, card_h, facecolor=color, radius=0.1)

        title_dark = color in (GOLDEN_YELLOW, SOFT_SAGE, WARM_GLOW)
        text_col = DEEP_NAVY if title_dark else WHITE
        body_col  = DEEP_NAVY if title_dark else WHITE
        freq_col  = MIDNIGHT_TEAL if title_dark else WARM_GLOW

        ax.text(x + card_w / 2, y + card_h - 0.32, title,
                ha="center", va="center", fontsize=12.5,
                color=text_col, fontweight="bold", linespacing=1.3)

        card(ax, x + card_w / 2 - 0.7, y + card_h - 0.9, 1.4, 0.3,
             facecolor=WHITE, edgecolor=color, alpha=0.25, radius=0.04)
        ax.text(x + card_w / 2, y + card_h - 0.75, freq,
                ha="center", va="center", fontsize=9.5,
                color=freq_col, fontweight="bold")

        for j, line in enumerate(body.split("\n")):
            ax.text(x + card_w / 2, y + card_h - 1.25 - j * 0.4, line,
                    ha="center", va="center", fontsize=9.5, color=body_col)

    save(fig, "30_six_examples.png")


# ─────────────────────────────────────────────────────────────
# 30_evolution.png — Staircase: Prompts → … → Evidence
# ─────────────────────────────────────────────────────────────
def make_evolution():
    fig = plt.figure(figsize=(12, 7), facecolor=WHITE)
    add_header_bar(fig, "The Bridge  |  Article 30  |  PythonMuse LLC")
    add_footer(fig)

    ax = fig.add_axes([0.03, 0.10, 0.94, 0.82])
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5.5)
    ax.axis("off")
    ax.set_facecolor(WHITE)

    ax.text(6.0, 5.2, "The future of AI in accounting is not just better prompts. It is better systems.",
            ha="center", va="center", fontsize=12,
            color=DEEP_NAVY, fontweight="bold", style="italic")

    stairs = [
        (OCEAN_TEAL,    "PROMPTS",   "Where most of us start"),
        (SEA_GREEN,     "SKILLS",    "Make instructions reusable"),
        (BRIGHT_TEAL,   "ROUTINES",  "Make work repeatable"),
        (GOLDEN_YELLOW, "CONTROLS",  "Make it safe"),
        (SOFT_SAGE,     "EVIDENCE",  "Make it audit-friendly"),
    ]

    step_w = 1.9
    step_h = 0.7
    x_start = 0.8

    for i, (color, title, subtitle) in enumerate(stairs):
        x = x_start + i * 0.55
        y_base = 0.4 + i * (step_h + 0.08)
        stair_w = step_w + (len(stairs) - 1 - i) * 0.0

        full_w = x_start + len(stairs) * 0.55 + step_w - x
        card(ax, x, y_base, full_w, step_h, facecolor=color, radius=0.06)

        title_dark = color in (GOLDEN_YELLOW, SOFT_SAGE)
        ax.text(x + 0.25, y_base + step_h / 2 + 0.1, title,
                ha="left", va="center", fontsize=12,
                color=DEEP_NAVY if title_dark else WHITE,
                fontweight="bold")
        ax.text(x + 0.25, y_base + step_h / 2 - 0.18, subtitle,
                ha="left", va="center", fontsize=9,
                color=MIDNIGHT_TEAL if title_dark else WARM_GLOW,
                style="italic")

    ax.text(6.0, 0.15,
            "Not AI replacing the accountant.  AI helping the accountant build systems that are structured, reviewable, and audit-ready.",
            ha="center", va="center", fontsize=9.5,
            color=DEEP_NAVY, style="italic")

    save(fig, "30_evolution.png")


# ─────────────────────────────────────────────────────────────
# Social Carousel — 7 square slides (1080×1080 equiv.)
# ─────────────────────────────────────────────────────────────
CAROUSEL_SIZE = (7.5, 7.5)


def carousel_base(title_text, subtitle_text=None, bg_color=WHITE):
    """Create a square carousel slide with header, footer, and optional subtitle."""
    fig = plt.figure(figsize=CAROUSEL_SIZE, facecolor=bg_color)

    bar_top = fig.add_axes([0.0, 0.88, 1.0, 0.12], facecolor=DEEP_NAVY)
    bar_top.set_axis_off()

    bar_bot = fig.add_axes([0.0, 0.0, 1.0, 0.09], facecolor=DEEP_NAVY)
    bar_bot.set_axis_off()
    fig.text(0.5, 0.055, FOOTER_TEXT, ha="center", va="center",
             fontsize=10, color=WHITE, fontweight="bold")
    fig.text(0.5, 0.018, FOOTER_URL, ha="center", va="center",
             fontsize=9, color=BRIGHT_TEAL)

    fig.text(0.5, 0.944, title_text, ha="center", va="center",
             fontsize=13, color=GOLDEN_YELLOW, fontweight="bold")
    if subtitle_text:
        fig.text(0.5, 0.91, subtitle_text, ha="center", va="center",
                 fontsize=10, color=WARM_GLOW)

    ax = fig.add_axes([0.06, 0.11, 0.88, 0.76])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis("off")
    ax.set_facecolor(bg_color)
    return fig, ax


def make_carousel_01():
    """Hook slide."""
    fig, ax = carousel_base("Article 30  |  PythonMuse")
    ax.text(5, 7.0, "Most accountants think", ha="center", va="center",
            fontsize=18, color=DEEP_NAVY, fontweight="bold")
    ax.text(5, 6.2, "of AI as a prompt.", ha="center", va="center",
            fontsize=18, color=DEEP_NAVY, fontweight="bold")
    ax.text(5, 5.2, "Until it isn't.", ha="center", va="center",
            fontsize=20, color=ALERT_RED, fontweight="bold", style="italic")

    ax.plot([1, 9], [4.4, 4.4], color=OCEAN_TEAL, lw=1.5, alpha=0.4)

    steps = ["Open chat.", "Ask question.", "Get answer.", "Copy, review, adjust, move on."]
    for i, s in enumerate(steps):
        ax.text(5, 3.75 - i * 0.62, s, ha="center", va="center",
                fontsize=11, color=OCEAN_TEAL)

    ax.plot([1, 9], [1.05, 1.05], color=GOLDEN_YELLOW, lw=2)
    ax.text(5, 0.6, "The real shift starts when AI becomes part of a routine.",
            ha="center", va="center", fontsize=10.5, color=DEEP_NAVY, style="italic")
    save(fig, "30_carousel_01.png")


def make_carousel_02():
    """The evolution: Prompt -> Skill -> Routine -> Evidence."""
    fig, ax = carousel_base("The Shift", "From asking to doing — on a schedule")

    stages = [
        (MIDNIGHT_TEAL, BRIGHT_TEAL,   "PROMPT",   "Open chat. Ask. Get an answer. Move on."),
        (OCEAN_TEAL,    GOLDEN_YELLOW, "SKILL",    "Reusable instructions. Consistent answers."),
        (SEA_GREEN,     WHITE,         "ROUTINE",  "Scheduled check. Compare. Propose. Wait for review."),
        (BRIGHT_TEAL,   DEEP_NAVY,     "EVIDENCE", "Who, when, why — audit-ready."),
    ]

    row_h = 1.55
    gap = 0.2
    start_y = 7.3

    for i, (bg, text_col, title, body) in enumerate(stages):
        y = start_y - i * (row_h + gap)
        card(ax, 0.6, y - row_h, 8.8, row_h, facecolor=bg, radius=0.08)
        ax.text(5, y - 0.4, title, ha="center", va="center",
                fontsize=14, color=text_col, fontweight="bold")
        ax.text(5, y - 1.05, body, ha="center", va="center",
                fontsize=9.5, color=WHITE if bg != BRIGHT_TEAL else DEEP_NAVY)

    save(fig, "30_carousel_02.png")


def make_carousel_03():
    """The routine pattern, condensed and stacked vertically for a square frame."""
    fig, ax = carousel_base("The Routine Pattern")

    steps = [
        (OCEAN_TEAL,    "SOURCE",         "Official website, regulation, or policy"),
        (MIDNIGHT_TEAL, "LOCAL KB",       "Your structured markdown files"),
        (SEA_GREEN,     "ROUTINE",        "Scheduled check: fetch and compare"),
        (GOLDEN_YELLOW, "PROPOSED UPDATE","Proposed change file — not live yet"),
        (BRIGHT_TEAL,   "HUMAN REVIEW",   "Tax manager or process owner reviews"),
        (SOFT_SAGE,     "COMMIT",         "Approved change enters version control"),
    ]

    row_h = 1.02
    gap = 0.14
    start_y = 7.55

    for i, (color, title, body) in enumerate(steps):
        y = start_y - i * (row_h + gap)
        card(ax, 0.4, y - row_h, 9.2, row_h, facecolor=color, radius=0.07)
        title_dark = color in (GOLDEN_YELLOW, BRIGHT_TEAL, SOFT_SAGE)
        text_col = DEEP_NAVY if title_dark else WHITE
        ax.text(0.75, y - row_h / 2 + 0.15, title, ha="left", va="center",
                fontsize=11, color=text_col, fontweight="bold")
        ax.text(0.75, y - row_h / 2 - 0.28, body, ha="left", va="center",
                fontsize=8.5, color=text_col)
        if i < len(steps) - 1:
            ax.annotate("", xy=(5, y - row_h - 0.02), xytext=(5, y - row_h - gap + 0.02),
                        arrowprops=dict(arrowstyle="->", color=DEEP_NAVY, lw=1.3))

    save(fig, "30_carousel_03.png")


def make_carousel_04():
    """The governance point: AI proposes, humans decide."""
    fig, ax = carousel_base("The Governance Point")

    ax.text(5, 7.1, "AI proposes.", ha="center", va="center",
            fontsize=22, color=BRIGHT_TEAL, fontweight="bold")
    ax.text(5, 6.2, "Humans decide.", ha="center", va="center",
            fontsize=22, color=DEEP_NAVY, fontweight="bold")

    ax.plot([1, 9], [5.5, 5.5], color=OCEAN_TEAL, lw=1, alpha=0.4)

    flow = ["AI identifies.", "AI recommends.", "Human reviews.", "Human approves.", "Then the change can be committed."]
    for i, s in enumerate(flow):
        ax.text(5, 4.85 - i * 0.72, s, ha="center", va="center",
                fontsize=12, color=OCEAN_TEAL if i < 4 else SEA_GREEN,
                fontweight="bold" if i == 4 else "normal")

    card(ax, 0.7, 0.2, 8.6, 0.75, facecolor=WARM_GLOW, edgecolor=GOLDEN_YELLOW, radius=0.05)
    ax.text(5, 0.57, 'Not "trust me." Show me the evidence.',
            ha="center", va="center", fontsize=11, color=DEEP_NAVY, fontweight="bold", style="italic")
    save(fig, "30_carousel_04.png")


def make_carousel_05():
    """Six use cases, teaser list."""
    fig, ax = carousel_base("Where Routines Can Help")

    examples = [
        (BRIGHT_TEAL,   "Sales Tax Nexus Monitoring"),
        (GOLDEN_YELLOW, "Payroll Tax Guidance"),
        (SEA_GREEN,     "Lease Accounting Policy Updates"),
        (OCEAN_TEAL,    "Bank Reconciliation Exception Rules"),
        (SOFT_SAGE,     "Client Billing Exceptions"),
        (WARM_GLOW,     "Internal Policy Monitoring"),
    ]

    row_h = 0.92
    gap = 0.16
    start_y = 7.35

    for i, (color, label) in enumerate(examples):
        y = start_y - i * (row_h + gap)
        card(ax, 0.5, y - row_h, 9.0, row_h, facecolor=color, radius=0.08)
        title_dark = color in (GOLDEN_YELLOW, SOFT_SAGE, WARM_GLOW)
        ax.text(5, y - row_h / 2, f"{i + 1}.  {label}", ha="center", va="center",
                fontsize=11.5, color=DEEP_NAVY if title_dark else WHITE, fontweight="bold")

    ax.text(5, 0.35, "The pattern is the same. The topic changes.",
            ha="center", va="center", fontsize=10.5, color=DEEP_NAVY, style="italic")
    save(fig, "30_carousel_05.png")


def make_carousel_06():
    """Why this matters for accounting."""
    fig, ax = carousel_base("This Isn't New to Accounting")

    ax.text(5, 7.1, "Accounting teams already", ha="center", va="center",
            fontsize=15, color=DEEP_NAVY, fontweight="bold")
    ax.text(5, 6.4, "live in routines.", ha="center", va="center",
            fontsize=15, color=DEEP_NAVY, fontweight="bold")
    ax.text(5, 5.75, "We just usually call them:", ha="center", va="center",
            fontsize=11, color=OCEAN_TEAL, style="italic")

    terms = ["checklists", "month-end procedures", "recurring tasks",
             "review controls", "SOPs", "audit evidence"]
    for i, t in enumerate(terms):
        col = i % 3
        row = i // 3
        x = 1.6 + col * 2.9
        y = 4.5 - row * 1.15
        card(ax, x - 1.3, y - 0.45, 2.6, 0.9, facecolor=WHITE, edgecolor=BRIGHT_TEAL, radius=0.08)
        ax.text(x, y, t, ha="center", va="center", fontsize=8.5, color=DEEP_NAVY, fontweight="bold")

    card(ax, 0.6, 0.2, 8.8, 0.85, facecolor=MIDNIGHT_TEAL, radius=0.06)
    ax.text(5, 0.62, "AI routines are not foreign to accounting.\nThey are a new way to structure recurring work.",
            ha="center", va="center", fontsize=10, color=WHITE, linespacing=1.5)
    save(fig, "30_carousel_06.png")


def make_carousel_07():
    """CTA / template slide."""
    fig, ax = carousel_base("Try It  |  pythonmuse.com")

    ax.text(5, 7.1, "The Tax Guidance Template", ha="center", va="center",
            fontsize=16, color=DEEP_NAVY, fontweight="bold")

    ax.plot([1, 9], [6.4, 6.4], color=OCEAN_TEAL, lw=1, alpha=0.4)

    files = ["sources/", "company-guidance/", "skills/", "routines/", "evidence/"]
    for i, f in enumerate(files):
        ax.text(5, 5.7 - i * 0.62, f, ha="center", va="center",
                fontsize=11.5, color=BRIGHT_TEAL, fontfamily="monospace")

    card(ax, 0.7, 1.55, 8.6, 0.85, facecolor=GOLDEN_YELLOW, radius=0.06)
    ax.text(5, 1.97, "Clone the repo. Fill in your\nown guidance topic.",
            ha="center", va="center", fontsize=10.5, color=DEEP_NAVY, fontweight="bold", linespacing=1.4)

    ax.text(5, 0.7, "That is the exercise.", ha="center", va="center",
            fontsize=10, color=OCEAN_TEAL, style="italic")
    save(fig, "30_carousel_07.png")


if __name__ == "__main__":
    print("Generating Article 30 visuals...")
    make_hero()
    make_folder_structure()
    make_routine_pattern()
    make_yaml_anatomy()
    make_review_package()
    make_six_examples()
    make_evolution()
    make_carousel_01()
    make_carousel_02()
    make_carousel_03()
    make_carousel_04()
    make_carousel_05()
    make_carousel_06()
    make_carousel_07()
    print("Done.")
