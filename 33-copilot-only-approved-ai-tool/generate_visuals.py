"""
Generate article visuals for Article 33 — When Copilot Is the Only Approved AI Tool

Produces the following PNGs saved to visuals/:
  33_hero.png                 — Corporate cafeteria (Copilot) vs. controlled kitchen (harness)
  33_validation_comparison.png — Validation comparison: harness vs. Copilot, card layout
  33_effort_over_time.png     — Ongoing user involvement: Copilot (flat) vs. harness (front-loaded)
  33_quote_card.png           — Social pull-quote card: "managing the conversation" vs. "managing the system"

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


def add_footer(fig, y_bar=0.0, bar_h=0.065, dark_bg=False):
    bar = fig.add_axes([0.0, y_bar, 1.0, bar_h])
    bar.set_xlim(0, 1); bar.set_ylim(0, 1)
    bar.set_axis_off()
    bar_color = MIDNIGHT_TEAL if dark_bg else DEEP_NAVY
    bar.add_patch(FancyBboxPatch((0, 0), 1, 1, boxstyle="square,pad=0",
                                 facecolor=bar_color, edgecolor="none",
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
# 33_hero.png — Corporate cafeteria vs. controlled kitchen
# ─────────────────────────────────────────────────────────────
def make_hero():
    fig = plt.figure(figsize=(13, 7), facecolor=WHITE)
    add_header_bar(fig, "When Copilot Is the Only Approved AI Tool  |  Article 33  |  PythonMuse LLC")
    add_footer(fig)

    ax = fig.add_axes([0.03, 0.10, 0.94, 0.82])
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5.5)
    ax.axis("off")
    ax.set_facecolor(WHITE)

    # ── LEFT: The corporate cafeteria ─────────────────────────
    card(ax, 0.1, 0.3, 5.2, 4.8, facecolor=LIGHT_GRAY, edgecolor=OCEAN_TEAL, radius=0.1)
    card(ax, 0.1, 4.5, 5.2, 0.6, facecolor=OCEAN_TEAL, radius=0.08)
    ax.text(2.7, 4.8, "THE CORPORATE CAFETERIA", ha="center", va="center",
            fontsize=13.5, color=WHITE, fontweight="bold")
    ax.text(2.7, 4.32, "Microsoft Copilot", ha="center", va="center",
            fontsize=11, color=OCEAN_TEAL, style="italic", fontweight="bold")

    cafeteria_items = [
        "Already approved by IT",
        "Familiar Microsoft 365 surface",
        "Attachment & instruction limits",
        "Validation is review-driven",
        "Evidence spread across chat & exports",
    ]
    for i, item in enumerate(cafeteria_items):
        y_pos = 3.78 - i * 0.56
        ax.text(0.4, y_pos, f"  {item}", ha="left", va="center",
                fontsize=10.5, color=DEEP_NAVY)

    ax.text(2.7, 0.62, '"That sounds interesting, but we\nare only allowed to use Copilot."',
            ha="center", va="center", fontsize=10, color=OCEAN_TEAL, style="italic",
            linespacing=1.4)

    # ── VS divider ────────────────────────────────────────────
    ax.text(6.0, 2.75, "VS", ha="center", va="center",
            fontsize=24, color=DEEP_NAVY, fontweight="bold", alpha=0.25)

    # ── RIGHT: The controlled kitchen ─────────────────────────
    card(ax, 6.7, 0.3, 5.1, 4.8, facecolor=LIGHT_GRAY, edgecolor=BRIGHT_TEAL, radius=0.1)
    card(ax, 6.7, 4.5, 5.1, 0.6, facecolor=BRIGHT_TEAL, radius=0.08)
    ax.text(9.25, 4.8, "THE CONTROLLED KITCHEN", ha="center", va="center",
            fontsize=13.5, color=DEEP_NAVY, fontweight="bold")
    ax.text(9.25, 4.32, "Harness — PythonMuse framework", ha="center", va="center",
            fontsize=11, color=OCEAN_TEAL, style="italic", fontweight="bold")

    kitchen_items = [
        "Folders, skills, and scripts define the work",
        "Model is swappable — Claude, GPT, Gemini",
        "No attachment limit to manage every run",
        "Validation is built into the workflow",
        "Evidence saved together, automatically",
    ]
    for i, item in enumerate(kitchen_items):
        y_pos = 3.78 - i * 0.56
        ax.text(6.9, y_pos, f"  {item}", ha="left", va="center",
                fontsize=10.5, color=DEEP_NAVY)

    ax.text(9.25, 0.62, '"The workflow already knows —\nsame files, every single time."',
            ha="center", va="center", fontsize=10, color=SEA_GREEN, style="italic",
            linespacing=1.4)

    save(fig, "33_hero.png")


# ─────────────────────────────────────────────────────────────
# 33_validation_comparison.png — Validation comparison, card layout
# ─────────────────────────────────────────────────────────────
def make_validation_comparison():
    fig = plt.figure(figsize=(13, 9.2), facecolor=WHITE)
    add_header_bar(fig, "Validation Comparison  |  Article 33  |  PythonMuse LLC")
    add_footer(fig)

    ax = fig.add_axes([0.03, 0.08, 0.94, 0.85])
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8.0)
    ax.axis("off")
    ax.set_facecolor(WHITE)

    # Column headers
    card(ax, 0.1, 7.3, 11.8, 0.58, facecolor=DEEP_NAVY, radius=0.06)
    ax.text(2.2, 7.59, "Validation Step", ha="center", va="center",
            fontsize=13, color=GOLDEN_YELLOW, fontweight="bold")
    ax.text(6.3, 7.59, "Harness (PythonMuse framework)", ha="center", va="center",
            fontsize=13, color=BRIGHT_TEAL, fontweight="bold")
    ax.text(10.1, 7.59, "Microsoft Copilot", ha="center", va="center",
            fontsize=13, color=WARM_GLOW, fontweight="bold")

    rows = [
        ("Recalculate\nvariances",
         "Deterministic script\nor formula",
         "Copilot calculation\nor manual check"),
        ("Apply materiality\nrules",
         "Automated\nthreshold logic",
         "Applied via instructions,\nverified independently"),
        ("Tie output to\nsource data",
         "Scripted tie-out\nbuilt into the workflow",
         "Manual or\nCopilot-assisted"),
        ("Generate reviewer\nchecklist",
         "Included\nautomatically",
         "Must be requested\nor fit in instructions"),
        ("Preserve validation\nevidence",
         "Saved with outputs,\nlogs, and reports",
         "Must be exported,\ndownloaded, or copied"),
        ("Reperform\nthe work",
         "Rerun the workflow,\ncompare versions",
         "Rerun the chat,\noutput may vary"),
    ]

    ROW_H = 1.14
    row_top = 6.85

    for i, (step, harness_ans, copilot_ans) in enumerate(rows):
        y = row_top - i * ROW_H
        bg = LIGHT_GRAY if i % 2 == 0 else WHITE
        card(ax, 0.1, y - ROW_H / 2 + 0.06, 11.8, ROW_H - 0.12, facecolor=bg, edgecolor=bg, radius=0.04)

        ax.text(0.25, y, step, ha="left", va="center",
                fontsize=12, color=DEEP_NAVY, fontweight="bold", linespacing=1.35)
        ax.text(4.05, y, harness_ans, ha="left", va="center",
                fontsize=11.5, color=SEA_GREEN, linespacing=1.35)
        ax.text(8.05, y, copilot_ans, ha="left", va="center",
                fontsize=11.5, color=OCEAN_TEAL, linespacing=1.35)

        y0 = y - ROW_H / 2 + 0.06
        y1 = y + ROW_H / 2 - 0.06
        ax.axvline(4.0, ymin=y0 / 8.0, ymax=y1 / 8.0,
                   color=OCEAN_TEAL, linewidth=0.7, alpha=0.4)
        ax.axvline(8.0, ymin=y0 / 8.0, ymax=y1 / 8.0,
                   color=OCEAN_TEAL, linewidth=0.7, alpha=0.4)

    ax.text(6.0, 0.35,
            'Copilot can help create the reviewer checklist.\nInside a harness, the scripts can execute parts of it.',
            ha="center", va="center", fontsize=12,
            color=DEEP_NAVY, style="italic", linespacing=1.4)

    save(fig, "33_validation_comparison.png")


# ─────────────────────────────────────────────────────────────
# 33_effort_over_time.png — Ongoing user involvement over time
# ─────────────────────────────────────────────────────────────
def make_effort_over_time():
    fig = plt.figure(figsize=(12, 7), facecolor=WHITE)
    add_header_bar(fig, "Ongoing User Involvement Over Time  |  Article 33  |  PythonMuse LLC")
    add_footer(fig)

    ax = fig.add_axes([0.09, 0.14, 0.86, 0.74])
    ax.set_facecolor(WHITE)

    months = list(range(0, 7))
    copilot_effort  = [7.2, 7.0, 7.3, 6.9, 7.1, 7.0, 7.2]
    harness_effort  = [9.0, 3.0, 2.2, 1.8, 1.6, 1.5, 1.4]

    ax.plot(months, copilot_effort, color=OCEAN_TEAL, linewidth=3,
            marker="o", markersize=7, label="Microsoft Copilot — managing the conversation")
    ax.plot(months, harness_effort, color=BRIGHT_TEAL, linewidth=3,
            marker="o", markersize=7, label="Harness — managing the system")

    ax.set_xlim(-0.3, 6.3)
    ax.set_ylim(0, 10)
    ax.set_xticks(months)
    ax.set_xticklabels(["Setup", "Month 1", "Month 2", "Month 3", "Month 4", "Month 5", "Month 6"],
                        fontsize=10, color=DEEP_NAVY)
    ax.set_yticks([])
    ax.set_ylabel("User effort per run", fontsize=11, color=DEEP_NAVY, fontweight="bold")

    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color(OCEAN_TEAL)

    ax.annotate("Repeated decisions every month:\nwhat to attach, what to explain,\nwhere to save it",
                xy=(4, 7.05), xytext=(3.4, 8.6),
                fontsize=8.8, color=OCEAN_TEAL, style="italic", ha="center",
                arrowprops=dict(arrowstyle="->", color=OCEAN_TEAL, alpha=0.6))

    ax.annotate("Design cost up front,\nthen the workflow just runs",
                xy=(2, 2.2), xytext=(2.6, 4.6),
                fontsize=8.8, color=SEA_GREEN, style="italic", ha="center",
                arrowprops=dict(arrowstyle="->", color=SEA_GREEN, alpha=0.6))

    ax.legend(loc="center right", bbox_to_anchor=(0.99, 0.46),
              fontsize=9.5, frameon=False, labelcolor=DEEP_NAVY)

    fig.text(0.5, 0.895,
             "In Copilot, I was managing the conversation. In the harness, I was managing the system.",
             ha="center", va="center", fontsize=11, color=DEEP_NAVY, style="italic")

    save(fig, "33_effort_over_time.png")


# ─────────────────────────────────────────────────────────────
# 33_quote_card.png — Social pull-quote card
# ─────────────────────────────────────────────────────────────
def make_quote_card():
    fig = plt.figure(figsize=(9, 4.3), facecolor=WHITE)

    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.75)
    ax.axis("off")
    ax.set_facecolor(WHITE)

    # Deep Navy card inset on the white canvas — per SKILL.md, the
    # figure/axes background stays white; brand color is a panel, not the canvas.
    card(ax, 0.3, 0.3, 9.4, 4.15, facecolor=DEEP_NAVY, radius=0.06)

    ax.text(5, 4.05, "PYTHONMUSE LLC", ha="center", va="center",
            fontsize=12, color=BRIGHT_TEAL, fontweight="bold", alpha=0.9)
    ax.text(5, 3.75, "Article 33 — When Copilot Is the Only Approved AI Tool",
            ha="center", va="center", fontsize=9, color=WARM_GLOW, alpha=0.85)

    ax.text(5, 2.65,
            "“In Copilot, I was managing the conversation.\nIn the harness, I was managing the system.”",
            ha="center", va="center", fontsize=18, color=GOLDEN_YELLOW,
            fontweight="bold", linespacing=1.45)

    ax.plot([3.5, 6.5], [1.75, 1.75], color=BRIGHT_TEAL, linewidth=2, alpha=0.8)

    ax.text(5, 1.35, "The tool changes. The accounting control logic does not.",
            ha="center", va="center", fontsize=10, color=WHITE, style="italic")

    ax.text(5, 0.6, "pythonmuse.com  |  github.com/PythonMuse/ai-ledger",
            ha="center", va="center", fontsize=9, color=BRIGHT_TEAL, alpha=0.85)

    save(fig, "33_quote_card.png")


# ─────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating Article 33 visuals...")
    make_hero()
    make_validation_comparison()
    make_effort_over_time()
    make_quote_card()
    print("Done.")
