"""
Generate article visuals for Article 23 — Don't Trust the Model to Find What You Already Know Is There.

Produces the following PNGs saved to visuals/:
  23_hero.png                — Hero / Cover card: Probabilistic vs. Schema-Driven contrast
  23_pipeline.png            — 7-stage sanitization pipeline with Local vs. Cloud zones
  23_field_classification.png — Field classification grid: Direct / Quasi / Analytical Payload

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
ALERT_ORANGE  = "#E07D3B"
LIGHT_GRAY    = "#F5F5F5"
LIGHT_TEAL    = "#EDF5F5"

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


# ─────────────────────────────────────────────────────────────
# 1. Hero — Probabilistic vs. Schema-Driven contrast card
# ─────────────────────────────────────────────────────────────
def make_hero():
    fig, ax = plt.subplots(figsize=(12, 6.3))
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # ── Header bar ──
    ax.add_patch(FancyBboxPatch((0, 0.82), 1, 0.18, transform=ax.transAxes,
                                boxstyle="square,pad=0", linewidth=0,
                                facecolor=DEEP_NAVY, clip_on=False))
    ax.text(0.5, 0.935, "Don't Trust the Model to Find What You Already Know Is There",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=16, fontweight="bold", color=WHITE)
    ax.text(0.5, 0.855, "Schema-driven data sanitization for accounting in the age of AI",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=11, color=BRIGHT_TEAL)

    # ── Left card — wrong approach ──
    ax.add_patch(FancyBboxPatch((0.04, 0.10), 0.43, 0.66,
                                boxstyle="round,pad=0.015", linewidth=2,
                                edgecolor=ALERT_RED, facecolor=LIGHT_GRAY))
    ax.text(0.255, 0.715, "Probabilistic Model", transform=ax.transAxes,
            ha="center", va="center", fontsize=14, fontweight="bold",
            color=ALERT_RED)
    ax.text(0.255, 0.645, "Guesses what's sensitive\nbased on learned patterns",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=11, color=DEEP_NAVY)

    bullets_left = [
        ("✗", "May miss uncommon vendor names"),
        ("✗", "Can't detect contextual sensitivity"),
        ("✗", "Over-redacts common words"),
        ("✗", "Different result each run"),
    ]
    for i, (icon, text) in enumerate(bullets_left):
        y = 0.545 - i * 0.095
        ax.text(0.12, y, icon, transform=ax.transAxes,
                ha="center", va="center", fontsize=13, fontweight="bold",
                color=ALERT_RED)
        ax.text(0.28, y, text, transform=ax.transAxes,
                ha="center", va="center", fontsize=10, color=DEEP_NAVY)

    ax.text(0.255, 0.155, "Best as a verification backstop",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=10, fontstyle="italic", color=OCEAN_TEAL)

    # ── Right card — right approach ──
    ax.add_patch(FancyBboxPatch((0.53, 0.10), 0.43, 0.66,
                                boxstyle="round,pad=0.015", linewidth=2,
                                edgecolor=BRIGHT_TEAL, facecolor=LIGHT_TEAL))
    ax.text(0.745, 0.715, "Schema-Driven Pipeline", transform=ax.transAxes,
            ha="center", va="center", fontsize=14, fontweight="bold",
            color=OCEAN_TEAL)
    ax.text(0.745, 0.645, "Knows what's sensitive\nbecause you defined it",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=11, color=DEEP_NAVY)

    bullets_right = [
        ("✓", "Deterministic — same result every run"),
        ("✓", "Handles your schema's exact structure"),
        ("✓", "Detects contextual sensitivity"),
        ("✓", "Auditable, testable, version-controlled"),
    ]
    for i, (icon, text) in enumerate(bullets_right):
        y = 0.545 - i * 0.095
        ax.text(0.61, y, icon, transform=ax.transAxes,
                ha="center", va="center", fontsize=11, color=SEA_GREEN)
        ax.text(0.775, y, text, transform=ax.transAxes,
                ha="center", va="center", fontsize=10, color=DEEP_NAVY)

    ax.text(0.745, 0.155, "Primary control for structured accounting data",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=10, fontstyle="italic", color=OCEAN_TEAL)

    # ── VS divider ──
    ax.text(0.5, 0.43, "vs.", transform=ax.transAxes,
            ha="center", va="center", fontsize=20, fontweight="bold",
            color=OCEAN_TEAL, alpha=0.5)

    add_footer(fig, y=0.01)
    save(fig, "23_hero.png")


# ─────────────────────────────────────────────────────────────
# 2. Pipeline — 7-stage flow with Local vs. Cloud zones
# ─────────────────────────────────────────────────────────────
def make_pipeline():
    fig, ax = plt.subplots(figsize=(16, 6))
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # ── Header bar ──
    ax.add_patch(FancyBboxPatch((0, 0.86), 1, 0.14, transform=ax.transAxes,
                                boxstyle="square,pad=0", linewidth=0,
                                facecolor=DEEP_NAVY, clip_on=False))
    ax.text(0.5, 0.945, "Schema-Driven Sanitization Pipeline",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=18, fontweight="bold", color=WHITE)
    ax.text(0.5, 0.878, "Stages 1–5 and 7 run locally. Only sanitized data reaches the cloud.",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=11, color=BRIGHT_TEAL)

    # ── Zone bands ──
    # Local zone: stages 1-5 (boxes at positions 0-4 of 7) + stage 7 (position 6)
    # Cloud zone: stage 6 (position 5)
    # We'll draw the bands behind the boxes using a light fill

    # Stages layout: 7 boxes spread across x=0.02 to 0.98
    box_w = 0.115
    box_h = 0.44
    box_y = 0.27
    gap = (1.0 - 0.04 - 7 * box_w) / 6  # space between boxes
    starts = [0.02 + i * (box_w + gap) for i in range(7)]

    # Zone background bands (behind boxes)
    # Local: covers stages 1-5 (indices 0-4) and stage 7 (index 6)
    local_x_end = starts[4] + box_w + gap * 0.5
    ax.add_patch(FancyBboxPatch((0.01, box_y - 0.12), local_x_end - 0.01, box_h + 0.20,
                                boxstyle="round,pad=0.01", linewidth=1.5,
                                edgecolor=SEA_GREEN, facecolor="#EDF5F5", zorder=0))
    ax.text(local_x_end * 0.5, box_y - 0.075, "LOCAL  —  your machine",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=9, fontweight="bold", color=SEA_GREEN, zorder=1)

    # Cloud: stage 6 (index 5)
    cloud_x_start = starts[5] - gap * 0.5
    cloud_x_end = starts[5] + box_w + gap * 0.5
    ax.add_patch(FancyBboxPatch((cloud_x_start, box_y - 0.12),
                                cloud_x_end - cloud_x_start, box_h + 0.20,
                                boxstyle="round,pad=0.01", linewidth=1.5,
                                edgecolor=GOLDEN_YELLOW, facecolor="#FFFBEA", zorder=0))
    ax.text((cloud_x_start + cloud_x_end) / 2, box_y - 0.075, "CLOUD",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=9, fontweight="bold", color=ALERT_ORANGE, zorder=1)

    # Local: stage 7 (index 6)
    local2_x_start = starts[6] - gap * 0.5
    ax.add_patch(FancyBboxPatch((local2_x_start, box_y - 0.12),
                                1.0 - local2_x_start - 0.01, box_h + 0.20,
                                boxstyle="round,pad=0.01", linewidth=1.5,
                                edgecolor=SEA_GREEN, facecolor="#EDF5F5", zorder=0))
    ax.text((local2_x_start + 1.0 - 0.01) / 2, box_y - 0.075, "LOCAL",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=9, fontweight="bold", color=SEA_GREEN, zorder=1)

    stages = [
        ("1", "Schema\nInventory", "Know what\nyou have"),
        ("2", "Synthetic\nData Gen", "Build a safe\ntest set"),
        ("3", "Transform\nScript Dev", "Write\ndeterministic\nrules"),
        ("4", "Deterministic\nSanitization", "Apply to\nreal data"),
        ("5", "Verification\n(Privacy Filter)", "Catch what\nwas missed"),
        ("6", "Cloud\nAnalysis", "Run the\nanalysis"),
        ("7", "Re-identify\n(Local)", "Map results\nback"),
    ]

    box_colors = [LIGHT_TEAL, LIGHT_TEAL, LIGHT_TEAL, LIGHT_TEAL,
                  LIGHT_TEAL, WARM_GLOW, LIGHT_TEAL]
    num_colors = [OCEAN_TEAL, OCEAN_TEAL, OCEAN_TEAL, OCEAN_TEAL,
                  OCEAN_TEAL, ALERT_ORANGE, OCEAN_TEAL]
    border_colors = [BRIGHT_TEAL, BRIGHT_TEAL, BRIGHT_TEAL, BRIGHT_TEAL,
                     BRIGHT_TEAL, GOLDEN_YELLOW, BRIGHT_TEAL]

    for i, (num, name, desc) in enumerate(stages):
        x = starts[i]
        # Box
        ax.add_patch(FancyBboxPatch((x, box_y), box_w, box_h,
                                    boxstyle="round,pad=0.01", linewidth=2,
                                    edgecolor=border_colors[i],
                                    facecolor=box_colors[i], zorder=2))
        # Number badge
        ax.add_patch(plt.Circle((x + box_w / 2, box_y + box_h - 0.055), 0.028,
                                transform=ax.transAxes, color=num_colors[i], zorder=3))
        ax.text(x + box_w / 2, box_y + box_h - 0.055, num,
                transform=ax.transAxes, ha="center", va="center",
                fontsize=11, fontweight="bold", color=WHITE, zorder=4)
        # Name
        ax.text(x + box_w / 2, box_y + box_h * 0.56, name,
                transform=ax.transAxes, ha="center", va="center",
                fontsize=9, fontweight="bold", color=DEEP_NAVY, zorder=3,
                multialignment="center")
        # Description
        ax.text(x + box_w / 2, box_y + box_h * 0.22, desc,
                transform=ax.transAxes, ha="center", va="center",
                fontsize=8.5, color=OCEAN_TEAL, zorder=3,
                multialignment="center")

        # Arrow to next box
        if i < 6:
            ax.annotate("", xy=(starts[i + 1], box_y + box_h / 2),
                        xytext=(x + box_w, box_y + box_h / 2),
                        xycoords="axes fraction", textcoords="axes fraction",
                        arrowprops=dict(arrowstyle="->", color=OCEAN_TEAL,
                                        lw=1.5), zorder=5)

    # Key label on the arrow between stage 5 and 6
    mid_arrow_x = (starts[4] + box_w + starts[5]) / 2
    ax.text(mid_arrow_x, box_y + box_h / 2 + 0.09,
            "sanitized\nonly",
            transform=ax.transAxes, ha="center", va="bottom",
            fontsize=8, fontstyle="italic", color=ALERT_ORANGE)

    add_footer(fig, y=0.01)
    save(fig, "23_pipeline.png")


# ─────────────────────────────────────────────────────────────
# 3. Field Classification — three-column grid
# ─────────────────────────────────────────────────────────────
def make_field_classification():
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # ── Header bar ──
    ax.add_patch(FancyBboxPatch((0, 0.88), 1, 0.12, transform=ax.transAxes,
                                boxstyle="square,pad=0", linewidth=0,
                                facecolor=DEEP_NAVY, clip_on=False))
    ax.text(0.5, 0.955, "Classifying Your Accounting Data Fields",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=20, fontweight="bold", color=WHITE)
    ax.text(0.5, 0.9, "The schema inventory step — before any data leaves your environment",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=11, color=BRIGHT_TEAL)

    columns = [
        {
            "title": "Direct Identifiers",
            "subtitle": "Pseudonymize or Drop",
            "header_color": ALERT_RED,
            "card_color": "#FEF0F0",
            "border_color": ALERT_RED,
            "x": 0.03,
            "fields": [
                "Vendor Name",
                "Employee Name",
                "Customer Name",
                "Tax ID / EIN",
                "Bank Routing Number",
                "Contact Email / Phone",
            ],
        },
        {
            "title": "Quasi-Identifiers",
            "subtitle": "Generalize or Suppress",
            "header_color": ALERT_ORANGE,
            "card_color": "#FFF6ED",
            "border_color": ALERT_ORANGE,
            "x": 0.355,
            "fields": [
                "Date + Amount + GL Code",
                "Vendor ID + Period",
                "Check Number",
                "Location + Transaction",
                "Memo / Notes Field",
                "Bank Feed Description",
            ],
        },
        {
            "title": "Analytical Payload",
            "subtitle": "Pass Through",
            "header_color": SEA_GREEN,
            "card_color": LIGHT_TEAL,
            "border_color": BRIGHT_TEAL,
            "x": 0.68,
            "fields": [
                "GL Account Code",
                "GL Account Category",
                "Transaction Amount",
                "Period / Fiscal Month",
                "Status (Posted / Void)",
                "Expense Category",
            ],
        },
    ]

    col_w = 0.29
    header_h = 0.09
    pill_h = 0.068
    pill_gap = 0.012
    col_top = 0.82
    pills_start = col_top - header_h - 0.015

    for col in columns:
        x = col["x"]

        # Column background card
        total_h = header_h + 0.015 + len(col["fields"]) * (pill_h + pill_gap) + 0.02
        ax.add_patch(FancyBboxPatch((x, col_top - total_h), col_w, total_h,
                                    boxstyle="round,pad=0.01", linewidth=2,
                                    edgecolor=col["border_color"],
                                    facecolor=col["card_color"]))

        # Column header band
        ax.add_patch(FancyBboxPatch((x, col_top - header_h), col_w, header_h,
                                    boxstyle="round,pad=0.01", linewidth=0,
                                    facecolor=col["header_color"]))
        ax.text(x + col_w / 2, col_top - header_h * 0.35, col["title"],
                transform=ax.transAxes, ha="center", va="center",
                fontsize=13, fontweight="bold", color=WHITE)
        ax.text(x + col_w / 2, col_top - header_h * 0.78, col["subtitle"],
                transform=ax.transAxes, ha="center", va="center",
                fontsize=10, color=WHITE, alpha=0.9)

        # Field pills
        for j, field in enumerate(col["fields"]):
            py = pills_start - j * (pill_h + pill_gap) - pill_h
            ax.add_patch(FancyBboxPatch((x + 0.015, py), col_w - 0.03, pill_h,
                                        boxstyle="round,pad=0.008", linewidth=1,
                                        edgecolor=col["border_color"],
                                        facecolor=WHITE, alpha=0.85))
            ax.text(x + col_w / 2, py + pill_h / 2, field,
                    transform=ax.transAxes, ha="center", va="center",
                    fontsize=10, color=DEEP_NAVY)

    # ── Rule-of-thumb callout box at bottom ──
    callout_y = 0.115
    ax.add_patch(FancyBboxPatch((0.03, callout_y), 0.94, 0.085,
                                boxstyle="round,pad=0.01", linewidth=2,
                                edgecolor=GOLDEN_YELLOW, facecolor=WARM_GLOW))
    ax.text(0.5, callout_y + 0.06, "Rule of thumb:",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=11, fontweight="bold", color=DEEP_NAVY)
    ax.text(0.5, callout_y + 0.025,
            "Direct → Pseudonymize or Drop    |    Quasi → Generalize or Suppress    |    Payload → Pass Through",
            transform=ax.transAxes, ha="center", va="center",
            fontsize=10.5, color=DEEP_NAVY)

    add_footer(fig, y=0.02)
    save(fig, "23_field_classification.png")


if __name__ == "__main__":
    print("Generating Article 23 visuals...")
    make_hero()
    make_pipeline()
    make_field_classification()
    print("Done.")
