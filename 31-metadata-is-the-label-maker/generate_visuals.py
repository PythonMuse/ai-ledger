"""
Generate article visuals for Article 31 — Metadata Is the Label Maker

Produces the following PNGs saved to visuals/:
  31_hero.png          — Junk drawer folder vs. labeled governed folder
  31_governance_stack.png — Layered stack: README → SKILL.md → Manifest → Script → Hook → Evidence
  31_note_vs_control.png  — Guidance text vs. Python enforcement (a note is not a control)
  31_division_of_labor.png — Who does what: Python / Accountant / AI / Hook / Evidence

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
# 31_hero.png — Junk drawer vs. labeled folder
# ─────────────────────────────────────────────────────────────
def make_hero():
    fig = plt.figure(figsize=(13, 7), facecolor=WHITE)
    add_header_bar(fig, "Metadata Is the Label Maker Your AI Workflow Needs  |  Article 31  |  PythonMuse LLC")
    add_footer(fig)

    ax = fig.add_axes([0.03, 0.10, 0.94, 0.82])
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5.5)
    ax.axis("off")
    ax.set_facecolor(WHITE)

    # ── LEFT: Junk drawer ─────────────────────────────────────
    card(ax, 0.1, 0.3, 5.2, 4.8, facecolor=LIGHT_GRAY, edgecolor=ALERT_RED, radius=0.1)
    card(ax, 0.1, 4.5, 5.2, 0.6, facecolor=ALERT_RED, radius=0.08)
    ax.text(2.7, 4.8, "THE JUNK DRAWER", ha="center", va="center",
            fontsize=12, color=WHITE, fontweight="bold")

    junk_files = [
        "bank rec.xlsx",
        "bank rec final.xlsx",
        "bank rec final FINAL.xlsx",
        "bank rec USE THIS ONE.xlsx",
        "bank_statement.pdf",
        "cash_activity_export.csv",
        "old version do not use.xlsx",
    ]
    for i, fname in enumerate(junk_files):
        y_pos = 4.05 - i * 0.51
        color = ALERT_RED if "do not use" in fname.lower() or "FINAL" in fname else DEEP_NAVY
        ax.text(0.45, y_pos, f"  {fname}", ha="left", va="center",
                fontsize=9.5, color=color, fontfamily="monospace")

    ax.text(2.7, 0.62, '"Which file is final? I will guess."',
            ha="center", va="center", fontsize=9.5,
            color=ALERT_RED, style="italic")

    # ── VS divider ────────────────────────────────────────────
    ax.text(6.0, 2.75, "VS", ha="center", va="center",
            fontsize=22, color=DEEP_NAVY, fontweight="bold", alpha=0.25)

    # ── RIGHT: Labeled folder ─────────────────────────────────
    card(ax, 6.7, 0.3, 5.1, 4.8, facecolor=LIGHT_GRAY, edgecolor=BRIGHT_TEAL, radius=0.1)
    card(ax, 6.7, 4.5, 5.1, 0.6, facecolor=BRIGHT_TEAL, radius=0.08)
    ax.text(9.25, 4.8, "THE LABELED FOLDER", ha="center", va="center",
            fontsize=12, color=DEEP_NAVY, fontweight="bold")

    labeled_items = [
        (BRIGHT_TEAL,   "README.md         → human orientation"),
        (GOLDEN_YELLOW, "SKILL.md          → AI orientation"),
        (SOFT_SAGE,     "input_manifest.csv→ file inventory"),
        (SEA_GREEN,     "inputs/           → approved source files"),
        (OCEAN_TEAL,    "scripts/          → validation + execution"),
        (WARM_GLOW,     "outputs/          → reviewed results"),
        (BRIGHT_TEAL,   "evidence/         → audit trail"),
    ]
    for i, (color, label) in enumerate(labeled_items):
        y_pos = 4.05 - i * 0.51
        ax.text(6.95, y_pos, label, ha="left", va="center",
                fontsize=9.5, color=color, fontfamily="monospace")

    ax.text(9.25, 0.62, '"I know exactly what I am looking at."',
            ha="center", va="center", fontsize=9.5,
            color=SEA_GREEN, style="italic")

    save(fig, "31_hero.png")


# ─────────────────────────────────────────────────────────────
# 31_governance_stack.png — The 6-layer governance stack
# ─────────────────────────────────────────────────────────────
def make_governance_stack():
    fig = plt.figure(figsize=(12, 8), facecolor=WHITE)
    add_header_bar(fig, "The Governed Workflow Stack  |  Article 31  |  PythonMuse LLC")
    add_footer(fig)

    ax = fig.add_axes([0.03, 0.10, 0.94, 0.82])
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.5)
    ax.axis("off")
    ax.set_facecolor(WHITE)

    layers = [
        (ALERT_ORANGE,  "EVIDENCE",   "evidence/",          "Proves what happened",          "The audit trail. Timestamped, immutable, reviewable."),
        (WARM_GLOW,     "HOOK",       "pre-run check",       "Stops unsafe work",              "A control point that runs before the workflow proceeds."),
        (SEA_GREEN,     "SCRIPT",     "scripts/*.py",        "Validates and executes",         "Python reads the manifest, checks statuses, stops on violations."),
        (SOFT_SAGE,     "MANIFEST",   "input_manifest.csv",  "Lists files and their status",   "The accountant's file inventory. Approved, draft, blocked."),
        (GOLDEN_YELLOW, "SKILL.md",   "SKILL.md",            "Orients the AI co-pilot",        "Instructions, metadata, approved folders, blocked statuses."),
        (BRIGHT_TEAL,   "README.md",  "README.md",           "Orients the human",              "Purpose, owner, period, data classification, review requirement."),
    ]

    col_x = [0.2, 1.5, 3.4, 5.6, 7.7]

    # Column headers
    card(ax, 0.1, 6.0, 11.8, 0.45, facecolor=DEEP_NAVY, radius=0.06)
    for label, x in zip(["Layer", "File", "Job", "Audience"], col_x[:4]):
        ax.text(x, 6.22, label, ha="left", va="center",
                fontsize=10, color=GOLDEN_YELLOW, fontweight="bold")
    ax.text(col_x[4], 6.22, "What it means in practice", ha="left", va="center",
            fontsize=10, color=GOLDEN_YELLOW, fontweight="bold")

    for i, (color, layer, fname, job, meaning) in enumerate(layers):
        y = 4.75 - i * 0.88
        card(ax, 0.1, y - 0.1, 11.8, 0.8, facecolor=WHITE, edgecolor=color, radius=0.06)
        card(ax, 0.1, y - 0.1, 0.18, 0.8, facecolor=color, radius=0.06)

        ax.text(col_x[0], y + 0.28, layer, ha="left", va="center",
                fontsize=9.5, color=color, fontweight="bold")
        ax.text(col_x[1], y + 0.28, fname, ha="left", va="center",
                fontsize=9, color=MIDNIGHT_TEAL, fontfamily="monospace")
        ax.text(col_x[2], y + 0.28, job, ha="left", va="center",
                fontsize=9.5, color=DEEP_NAVY, fontweight="bold")
        ax.text(col_x[4], y + 0.28, meaning, ha="left", va="center",
                fontsize=9, color=OCEAN_TEAL, linespacing=1.4)

    # Bottom summary
    ax.text(6.0, 0.25,
            "Metadata informs.  Scripts validate.  Hooks enforce.  Evidence proves.",
            ha="center", va="center", fontsize=11,
            color=DEEP_NAVY, fontweight="bold", style="italic")

    save(fig, "31_governance_stack.png")


# ─────────────────────────────────────────────────────────────
# 31_note_vs_control.png — Guidance text vs. Python enforcement
# ─────────────────────────────────────────────────────────────
def make_note_vs_control():
    fig = plt.figure(figsize=(13, 6.5), facecolor=WHITE)
    add_header_bar(fig, "A Note Is Not a Control  |  Article 31  |  PythonMuse LLC")
    add_footer(fig)

    ax = fig.add_axes([0.03, 0.10, 0.94, 0.82])
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5)
    ax.axis("off")
    ax.set_facecolor(WHITE)

    # ── LEFT: The note ────────────────────────────────────────
    card(ax, 0.15, 0.35, 5.1, 4.35, facecolor=LIGHT_GRAY, edgecolor=ALERT_ORANGE, radius=0.1)
    card(ax, 0.15, 4.1, 5.1, 0.6, facecolor=ALERT_ORANGE, radius=0.08)
    ax.text(2.7, 4.4, "THE NOTE  (Guidance)", ha="center", va="center",
            fontsize=12, color=WHITE, fontweight="bold")

    note_lines = [
        "In SKILL.md or README.md:",
        "",
        "  Do not use draft files.",
        "  Do not use files marked",
        "  superseded or do_not_use.",
        "",
        "AI reads this.",
        "AI may or may not follow it.",
        "No enforcement occurs.",
        "No error is raised.",
        "The workflow continues.",
    ]
    for i, line in enumerate(note_lines):
        color = ALERT_ORANGE if "may or may not" in line else DEEP_NAVY
        style = "italic" if "may or may not" in line else "normal"
        ax.text(0.45, 3.75 - i * 0.32, line, ha="left", va="center",
                fontsize=9.5, color=color, fontfamily="monospace",
                style=style)

    # ── VS divider ────────────────────────────────────────────
    ax.text(6.0, 2.55, "VS", ha="center", va="center",
            fontsize=22, color=DEEP_NAVY, fontweight="bold", alpha=0.25)

    # ── RIGHT: The control ────────────────────────────────────
    card(ax, 6.75, 0.35, 5.0, 4.35, facecolor=LIGHT_GRAY, edgecolor=BRIGHT_TEAL, radius=0.1)
    card(ax, 6.75, 4.1, 5.0, 0.6, facecolor=BRIGHT_TEAL, radius=0.08)
    ax.text(9.25, 4.4, "THE CONTROL  (Enforcement)", ha="center", va="center",
            fontsize=12, color=DEEP_NAVY, fontweight="bold")

    code_lines = [
        "blocked = manifest[",
        "  manifest['status']",
        "  .isin(['draft',",
        "         'superseded',",
        "         'do_not_use'])",
        "]",
        "",
        "if not blocked.empty:",
        "  raise ValueError(",
        "    'Workflow stopped.'",
        "  )",
    ]
    for i, line in enumerate(code_lines):
        color = SEA_GREEN if line.startswith("if") or line.startswith("  raise") else MIDNIGHT_TEAL
        ax.text(6.95, 3.75 - i * 0.32, line, ha="left", va="center",
                fontsize=9.5, color=color, fontfamily="monospace")

    # Bottom callout
    ax.text(6.0, 0.15,
            "The policy memo says 'do not approve without dual sign-off'.\n"
            "The accounting system blocks the payment until the second approval posts.\n"
            "Both matter. Only one actually stops the error.",
            ha="center", va="center", fontsize=9.5,
            color=DEEP_NAVY, style="italic", linespacing=1.5)

    save(fig, "31_note_vs_control.png")


# ─────────────────────────────────────────────────────────────
# 31_division_of_labor.png — Who does what
# ─────────────────────────────────────────────────────────────
def make_division_of_labor():
    fig = plt.figure(figsize=(13, 7), facecolor=WHITE)
    add_header_bar(fig, "The Right Division of Labor  |  Article 31  |  PythonMuse LLC")
    add_footer(fig)

    ax = fig.add_axes([0.03, 0.10, 0.94, 0.82])
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5.5)
    ax.axis("off")
    ax.set_facecolor(WHITE)

    ax.text(6.0, 5.25, "This is not replacing accounting judgment.\nIt is making accounting judgment visible to the workflow.",
            ha="center", va="center", fontsize=11,
            color=DEEP_NAVY, style="italic", linespacing=1.5)

    roles = [
        (SEA_GREEN,     "PYTHON",      "Does the boring inventory",
         "Scans the folder, builds the manifest,\nruns the validation check, stops on violations."),
        (GOLDEN_YELLOW, "ACCOUNTANT",  "Applies judgment",
         "Reviews the manifest, marks files final or draft,\nsets approval status, signs off on outputs."),
        (BRIGHT_TEAL,   "AI CO-PILOT", "Follows the instructions",
         "Reads SKILL.md and manifest, uses only approved files,\ncites sources, flags unclear status."),
        (WARM_GLOW,     "HOOK",        "Enforces the controls",
         "Runs before the workflow proceeds, blocks violations,\nwrites validation result to evidence folder."),
        (SOFT_SAGE,     "EVIDENCE",    "Proves what happened",
         "Timestamped log of what ran, what was approved,\nwhat was blocked, and who reviewed the output."),
    ]

    card_w = 2.1
    gap = 0.18
    start_x = 0.15
    card_h = 2.9

    for i, (color, role, tagline, detail) in enumerate(roles):
        x = start_x + i * (card_w + gap)
        card(ax, x, 0.35, card_w, card_h, facecolor=WHITE, edgecolor=color, radius=0.08)
        card(ax, x, 0.35 + card_h - 0.55, card_w, 0.55, facecolor=color, radius=0.08)

        ax.text(x + card_w / 2, 0.35 + card_h - 0.27,
                role, ha="center", va="center",
                fontsize=10, color=DEEP_NAVY, fontweight="bold")

        ax.text(x + card_w / 2, 0.35 + card_h - 0.82,
                tagline, ha="center", va="center",
                fontsize=9.5, color=color, fontweight="bold",
                style="italic")

        ax.text(x + card_w / 2, 0.35 + card_h - 1.9,
                detail, ha="center", va="center",
                fontsize=8.5, color=DEEP_NAVY, linespacing=1.5,
                wrap=True)

    # Bottom tag
    ax.text(6.0, 0.18,
            "Capability shifted.  Accountability did not.",
            ha="center", va="center", fontsize=10.5,
            color=DEEP_NAVY, fontweight="bold", style="italic")

    save(fig, "31_division_of_labor.png")


# ─────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating Article 31 visuals...")
    make_hero()
    make_governance_stack()
    make_note_vs_control()
    make_division_of_labor()
    print("Done.")
