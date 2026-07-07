"""
Generate article visuals for Article 29 — The Magic Loop

Produces the following PNGs saved to visuals/:
  29_hero.png             — /loop command vs the stack it generates
  29_four_layers.png      — The four automation layers (Python/YAML/SQL/Markdown)
  29_yaml_anatomy.png     — Annotated YAML block with accounting-language callouts
  29_old_vs_new.png       — Old world (developer team) vs new world (1 accountant + AI)
  29_review_checklist.png — 5-question review checklist before approving any loop

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
# 29_hero.png — /loop command vs the generated stack
# ─────────────────────────────────────────────────────────────
def make_hero():
    fig = plt.figure(figsize=(13, 6.5), facecolor=WHITE)
    add_header_bar(fig, "The Magic Loop  |  Article 29  |  PythonMuse LLC")
    add_footer(fig)

    ax = fig.add_axes([0.03, 0.10, 0.94, 0.82])
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5)
    ax.axis("off")
    ax.set_facecolor(WHITE)

    # ── LEFT: The command ─────────────────────────────────────
    card(ax, 0.15, 0.2, 4.8, 4.4, facecolor=DEEP_NAVY, radius=0.1)

    ax.text(2.55, 4.3, "You type:", ha="center", va="center",
            fontsize=11, color=BRIGHT_TEAL, style="italic")

    prompt_lines = [
        "/loop monitor inbox",
        "for invoicing email",
        "then refresh dashboard",
        "save to monthly folder",
        "notify finance team",
    ]
    for i, line in enumerate(prompt_lines):
        ax.text(2.55, 3.65 - i * 0.48, line, ha="center", va="center",
                fontsize=12, color=GOLDEN_YELLOW,
                fontfamily="monospace")

    ax.text(2.55, 0.6, "Seconds later...", ha="center", va="center",
            fontsize=10, color=WARM_GLOW, style="italic")

    # Arrow
    ax.annotate("", xy=(5.5, 2.5), xytext=(5.0, 2.5),
                arrowprops=dict(arrowstyle="->", color=BRIGHT_TEAL, lw=2.5))

    # ── RIGHT: The generated stack ────────────────────────────
    card(ax, 5.7, 0.2, 5.9, 4.4, facecolor=LIGHT_GRAY, edgecolor=BRIGHT_TEAL, radius=0.1)

    ax.text(8.65, 4.3, "AI builds for you:", ha="center", va="center",
            fontsize=11, color=DEEP_NAVY, style="italic")

    stack_items = [
        (SEA_GREEN,     ".py   Python scripts"),
        (BRIGHT_TEAL,   ".yaml Workflow config"),
        (OCEAN_TEAL,    ".sql  Data queries"),
        (SOFT_SAGE,     ".md   Documentation"),
        (GOLDEN_YELLOW, "      Triggers + retries"),
        (WARM_GLOW,     "      Logging + audit trail"),
    ]
    for i, (color, label) in enumerate(stack_items):
        y_pos = 3.65 - i * 0.52
        card(ax, 5.9, y_pos - 0.15, 5.4, 0.4, facecolor=WHITE, edgecolor=color, radius=0.04)
        ax.text(6.15, y_pos + 0.04, "▶", ha="center", va="center",
                fontsize=10, color=color)
        ax.text(6.45, y_pos + 0.04, label, ha="left", va="center",
                fontsize=10, color=DEEP_NAVY, fontfamily="monospace")

    # Bottom quote
    ax.text(6.0, 0.55, "Easy to generate ≠ safe to run",
            ha="left", va="center", fontsize=11,
            color=ALERT_RED, fontweight="bold", style="italic")

    save(fig, "29_hero.png")


# ─────────────────────────────────────────────────────────────
# 29_four_layers.png — The four automation layers
# ─────────────────────────────────────────────────────────────
def make_four_layers():
    fig = plt.figure(figsize=(12, 7), facecolor=WHITE)
    add_header_bar(fig, "The Four Layers of an AI-Generated Workflow  |  Article 29  |  PythonMuse LLC")
    add_footer(fig)

    ax = fig.add_axes([0.03, 0.10, 0.94, 0.82])
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5.5)
    ax.axis("off")
    ax.set_facecolor(WHITE)

    layers = [
        (SEA_GREEN,     "PYTHON  .py",  "Logic",          "Calculations, transformations,\nautomation steps",       "The associate running\nthe month-end process"),
        (BRIGHT_TEAL,   "YAML    .yaml","Configuration",  "Workflow structure, triggers,\npermissions, sequence",    "The written SOP the\nassociate follows"),
        (OCEAN_TEAL,    "SQL     .sql", "Data",           "Pulling records from databases\nand data warehouses",      "The query that runs\nagainst your ERP"),
        (SOFT_SAGE,     "MARKDOWN .md", "Instructions",   "Agent guidance, controls,\ndocumentation, policies",     "The policy memo that\ngoverns the process"),
    ]

    col_labels = ["Layer", "File Type", "Handles", "Accounting Analogy"]
    col_x = [0.15, 2.3, 5.1, 9.0]
    col_w = [2.0, 2.5, 3.5, 2.8]

    # Header row
    card(ax, 0.1, 4.85, 11.8, 0.55, facecolor=DEEP_NAVY, radius=0.06)
    for label, x in zip(col_labels, col_x):
        ax.text(x, 5.12, label, ha="left", va="center",
                fontsize=11, color=GOLDEN_YELLOW, fontweight="bold")

    for i, (color, filetype, handle, detail, analogy) in enumerate(layers):
        y = 3.6 - i * 1.05
        card(ax, 0.1, y, 11.8, 0.95, facecolor=WHITE, edgecolor=color, radius=0.06)

        # Color stripe on left
        card(ax, 0.1, y, 0.18, 0.95, facecolor=color, radius=0.06)

        ax.text(col_x[0], y + 0.47, filetype, ha="left", va="center",
                fontsize=10, color=color, fontfamily="monospace", fontweight="bold")

        ax.text(col_x[1], y + 0.47, handle, ha="left", va="center",
                fontsize=11, color=DEEP_NAVY, fontweight="bold")

        ax.text(col_x[2], y + 0.55, detail, ha="left", va="center",
                fontsize=9.5, color=MIDNIGHT_TEAL, linespacing=1.5)

        ax.text(col_x[3], y + 0.55, analogy, ha="left", va="center",
                fontsize=9.5, color=OCEAN_TEAL, style="italic", linespacing=1.5)

    ax.text(6.0, 0.2, "You do not need to write all four.  The AI writes them.  Your job: review before you approve.",
            ha="center", va="center", fontsize=10, color=DEEP_NAVY, style="italic")

    save(fig, "29_four_layers.png")


# ─────────────────────────────────────────────────────────────
# 29_yaml_anatomy.png — Annotated YAML block
# ─────────────────────────────────────────────────────────────
def make_yaml_anatomy():
    fig = plt.figure(figsize=(13, 7.5), facecolor=WHITE)
    add_header_bar(fig, "Reading a Workflow File Like an Accountant  |  Article 29  |  PythonMuse LLC")
    add_footer(fig)

    ax = fig.add_axes([0.03, 0.10, 0.94, 0.82])
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.set_facecolor(WHITE)

    # Title
    ax.text(6.0, 5.7, "YAML = A written procedure manual that computers can read",
            ha="center", va="center", fontsize=12,
            color=DEEP_NAVY, fontweight="bold", style="italic")

    # YAML code block (left side)
    card(ax, 0.15, 0.3, 5.0, 5.1, facecolor=MIDNIGHT_TEAL, radius=0.08)
    ax.text(2.65, 5.18, "invoice-to-dashboard.yaml", ha="center", va="center",
            fontsize=10, color=GOLDEN_YELLOW, fontfamily="monospace", fontweight="bold")

    yaml_lines = [
        (BRIGHT_TEAL,   "trigger:"),
        (WHITE,         "  type: email"),
        (WHITE,         '  subject: "Invoicing complete"'),
        ("", ""),
        (GOLDEN_YELLOW, "steps:"),
        (WHITE,         "  - pull_sales_data"),
        (WHITE,         "  - build_dashboard"),
        (WHITE,         "  - notify_finance"),
        ("", ""),
        (SOFT_SAGE,     "permissions:"),
        (WHITE,         "  allowed_folders:"),
        (WHITE,         "    - data/raw"),
        (WHITE,         "    - outputs/dashboards"),
        ("", ""),
        (WARM_GLOW,     "retry:"),
        (WHITE,         "  attempts: 3"),
        ("", ""),
        (ALERT_ORANGE,  "approval:"),
        (WHITE,         "  required: true"),
        (WHITE,         "  approver_role: finance_manager"),
    ]

    for i, (color, line) in enumerate(yaml_lines):
        if color:
            ax.text(0.45, 4.75 - i * 0.225, line, ha="left", va="center",
                    fontsize=9, color=color, fontfamily="monospace")

    # Annotations (right side)
    annotations = [
        (0.225, BRIGHT_TEAL,   "TRIGGER",   "What starts this process?\nCould it fire accidentally?"),
        (0.785, GOLDEN_YELLOW, "SEQUENCE",  "What order do things happen?\nDoes notification come last?"),
        (1.35,  SOFT_SAGE,     "PERMISSIONS","What can this workflow touch?\nAre raw files protected?"),
        (1.685, WARM_GLOW,     "RETRY RULES","What if something fails?\nCould it create duplicates?"),
        (1.91,  ALERT_ORANGE,  "HUMAN GATE","Does a human review before\nanything gets published?"),
    ]

    for frac, color, label, question in annotations:
        y = 4.75 - frac * 4.5 / 1.0

        ax.annotate("", xy=(5.4, y), xytext=(5.9, y),
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.5))

        card(ax, 6.0, y - 0.32, 5.75, 0.75, facecolor=WHITE, edgecolor=color, radius=0.05)
        ax.text(6.2, y + 0.17, label, ha="left", va="center",
                fontsize=10, color=color, fontweight="bold")
        ax.text(6.2, y - 0.12, question, ha="left", va="center",
                fontsize=9, color=DEEP_NAVY, linespacing=1.4)

    save(fig, "29_yaml_anatomy.png")


# ─────────────────────────────────────────────────────────────
# 29_old_vs_new.png — Old world vs new world
# ─────────────────────────────────────────────────────────────
def make_old_vs_new():
    fig = plt.figure(figsize=(13, 6.5), facecolor=WHITE)
    add_header_bar(fig, "Building Automation: Then vs. Now  |  Article 29  |  PythonMuse LLC")
    add_footer(fig)

    ax = fig.add_axes([0.03, 0.10, 0.94, 0.82])
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5)
    ax.axis("off")
    ax.set_facecolor(WHITE)

    # ── LEFT: Old World ───────────────────────────────────────
    card(ax, 0.15, 0.3, 5.0, 4.4, facecolor=LIGHT_GRAY, edgecolor=ALERT_RED, radius=0.1)
    card(ax, 0.15, 4.1, 5.0, 0.6, facecolor=ALERT_RED, radius=0.08)
    ax.text(2.65, 4.4, "OLD WORLD", ha="center", va="center",
            fontsize=14, color=WHITE, fontweight="bold")

    old_items = [
        "1 developer to write the scripts",
        "1 infrastructure engineer",
        "1 scheduler / DevOps setup",
        "1 automation engineer",
        "6 weeks of planning",
        "IT tickets and approvals",
        "Testing environment setup",
        "Deployment pipeline",
    ]
    for i, item in enumerate(old_items):
        y_pos = 3.75 - i * 0.41
        ax.text(0.55, y_pos, f"▸  {item}", ha="left", va="center",
                fontsize=9.5, color=DEEP_NAVY)

    # ── VS divider ────────────────────────────────────────────
    ax.text(6.0, 2.5, "VS", ha="center", va="center",
            fontsize=22, color=DEEP_NAVY, fontweight="bold", alpha=0.3)

    # ── RIGHT: New World ──────────────────────────────────────
    card(ax, 6.85, 0.3, 4.9, 4.4, facecolor=LIGHT_GRAY, edgecolor=BRIGHT_TEAL, radius=0.1)
    card(ax, 6.85, 4.1, 4.9, 0.6, facecolor=BRIGHT_TEAL, radius=0.08)
    ax.text(9.3, 4.4, "NEW WORLD", ha="center", va="center",
            fontsize=14, color=DEEP_NAVY, fontweight="bold")

    new_items = [
        (SOFT_SAGE,   "1 accountant with a prompt"),
        (BRIGHT_TEAL, "AI generates the full stack"),
        (BRIGHT_TEAL, "Seconds, not weeks"),
        (GOLDEN_YELLOW, ""),
        (GOLDEN_YELLOW, "But governance stays:"),
        (WARM_GLOW,   "  Review the trigger"),
        (WARM_GLOW,   "  Validate permissions"),
        (WARM_GLOW,   "  Approve before running"),
    ]
    for i, (color, item) in enumerate(new_items):
        y_pos = 3.75 - i * 0.41
        if item:
            prefix = "▸  " if not item.startswith("  ") else ""
            ax.text(7.1, y_pos, f"{prefix}{item}", ha="left", va="center",
                    fontsize=9.5, color=color,
                    fontweight="bold" if color == GOLDEN_YELLOW else "normal")

    # Bottom line
    ax.text(6.0, 0.13,
            "Capability shifted.  Accountability did not.",
            ha="center", va="center", fontsize=11,
            color=DEEP_NAVY, fontweight="bold", style="italic")

    save(fig, "29_old_vs_new.png")


# ─────────────────────────────────────────────────────────────
# 29_review_checklist.png — 5-question review checklist
# ─────────────────────────────────────────────────────────────
def make_review_checklist():
    fig = plt.figure(figsize=(12, 7.5), facecolor=WHITE)
    add_header_bar(fig, "Before You Click Run: 5 Questions Every Accountant Should Ask  |  Article 29")
    add_footer(fig)

    ax = fig.add_axes([0.03, 0.10, 0.94, 0.82])
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.set_facecolor(WHITE)

    ax.text(6.0, 5.7, "AI can generate the workflow.  You still need to approve it.",
            ha="center", va="center", fontsize=11,
            color=DEEP_NAVY, style="italic")

    checklist = [
        (BRIGHT_TEAL,   "1",  "THE TRIGGER",
         'trigger:\n  type: email\n  subject: "Invoicing complete"',
         "What starts this process?\nCould it fire accidentally or\nmore than once?"),

        (GOLDEN_YELLOW, "2",  "THE SEQUENCE",
         "steps:\n  - pull_sales_data\n  - build_dashboard\n  - notify_finance",
         "Does the order make sense?\nIs notification gated after\nvalidation?"),

        (SOFT_SAGE,     "3",  "THE PERMISSIONS",
         "permissions:\n  allowed_folders:\n    - data/raw\n    - outputs/",
         "What can this workflow touch?\nIs raw data protected from\nbeing overwritten?"),

        (WARM_GLOW,     "4",  "THE RETRY RULES",
         "retry:\n  attempts: 3\n  delay_seconds: 60",
         "What happens if it fails?\nCould retries create duplicate\noutputs or double-sends?"),

        (ALERT_ORANGE,  "5",  "THE HUMAN GATE",
         "approval:\n  required: true\n  approver_role: finance_manager",
         "Does a human review before\nanything is published or\ndistributed externally?"),
    ]

    for i, (color, num, title, code, question) in enumerate(checklist):
        y = 4.65 - i * 0.97
        card(ax, 0.15, y - 0.3, 11.7, 0.88, facecolor=WHITE, edgecolor=color, radius=0.06)

        # Number badge
        card(ax, 0.15, y - 0.3, 0.55, 0.88, facecolor=color, radius=0.06)
        ax.text(0.425, y + 0.14, num, ha="center", va="center",
                fontsize=16, color=DEEP_NAVY, fontweight="bold")

        # Title
        ax.text(1.0, y + 0.22, title, ha="left", va="center",
                fontsize=10, color=color, fontweight="bold")

        # Code snippet
        ax.text(1.0, y - 0.06, code, ha="left", va="center",
                fontsize=7.5, color=MIDNIGHT_TEAL, fontfamily="monospace",
                linespacing=1.4)

        # Question (right column)
        ax.text(8.0, y + 0.14, question, ha="left", va="center",
                fontsize=9.5, color=DEEP_NAVY, linespacing=1.5)

    save(fig, "29_review_checklist.png")


# ─────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating Article 29 visuals...")
    make_hero()
    make_four_layers()
    make_yaml_anatomy()
    make_old_vs_new()
    make_review_checklist()
    print("Done.")
