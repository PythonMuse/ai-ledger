"""
Generate Article 16 visuals -- The PDF Token Trap.

Visual 01: Hero / front image
Visual 02: Side-by-side workflow comparison (token-heavy vs token-efficient)
Visual 03: Accountant translation table (PDF concepts to accounting concepts)

Saved to articles/16-pdf-token-trap/visuals/
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

# -- Output directory --------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR    = os.path.join(SCRIPT_DIR, "visuals")
os.makedirs(OUT_DIR, exist_ok=True)

# -- PythonMuse brand colors (SKILL.md standard block) -----------------------
DEEP_NAVY     = "#002639"
MIDNIGHT_TEAL = "#003144"
BRIGHT_TEAL   = "#3ABFB9"
GOLDEN_YELLOW = "#FFD75E"
WARM_GLOW     = "#F5D384"
OCEAN_TEAL    = "#005F6F"
SOFT_SAGE     = "#91BE8E"
SEA_GREEN     = "#2BA19A"
WHITE         = "#FFFFFF"
LIGHT_GRAY    = "#F5F5F5"
ALERT_RED     = "#E05252"
ALERT_ORANGE  = "#E07D3B"

# -- Text contrast helper (SKILL.md mandatory rule 3) -----------------------
DARK_BG_COLORS = {DEEP_NAVY, MIDNIGHT_TEAL, OCEAN_TEAL, SEA_GREEN}

def text_color_for(bg):
    """Return correct text color per SKILL.md contrast rule."""
    if bg in DARK_BG_COLORS:
        return WHITE
    return DEEP_NAVY

FOOTER_TEXT = "PythonMuse LLC  |  github.com/PythonMuse/ai-ledger"

# =============================================================================
# Visual 01 -- Hero / Front Image
# =============================================================================
fig1, ax1 = plt.subplots(figsize=(12, 6))
fig1.patch.set_facecolor(WHITE)
ax1.set_facecolor(WHITE)
ax1.set_xlim(0, 12)
ax1.set_ylim(0, 6)
ax1.axis("off")

ax1.text(6, 3.9, "The PDF Token Trap",
         ha="center", va="center",
         fontsize=24, fontweight="bold", color=DEEP_NAVY,
         linespacing=1.4)

ax1.text(6, 2.8, "Why my PDF ate 20% of my tokens -- and the workflow that fixed it",
         ha="center", va="center",
         fontsize=14, color=OCEAN_TEAL, style="italic")

ax1.text(6, 1.5, FOOTER_TEXT,
         ha="center", va="center",
         fontsize=12, color=OCEAN_TEAL, alpha=0.70)

ax1.plot([2, 10], [2.15, 2.15], color=BRIGHT_TEAL, linewidth=1.5, alpha=0.5)

tagline = FancyBboxPatch((2.2, 0.3), 7.6, 0.7,
                          boxstyle="round,pad=0.1",
                          facecolor=DEEP_NAVY, edgecolor="none",
                          alpha=0.9)
ax1.add_patch(tagline)
ax1.text(6, 0.65, "Don't send documents. Send structure.",
         ha="center", va="center",
         fontsize=14, fontweight="bold", color=WHITE)

fig1.savefig(os.path.join(OUT_DIR, "16_visual_front.png"),
             dpi=180, bbox_inches="tight", facecolor=fig1.get_facecolor())
plt.close(fig1)
print("  Saved 16_visual_front.png")

# =============================================================================
# Visual 02 -- Side-by-Side Workflow Comparison
# =============================================================================
fig2, ax2 = plt.subplots(figsize=(14, 9))
fig2.patch.set_facecolor(WHITE)
ax2.set_facecolor(WHITE)
ax2.set_xlim(0, 14)
ax2.set_ylim(0, 10)
ax2.axis("off")

# Title
ax2.text(7, 9.5, "Same PDF. Two Workflows.",
         ha="center", va="center",
         fontsize=22, fontweight="bold", color=DEEP_NAVY)

ax2.text(7, 8.9, "Token-heavy vs. token-efficient approaches to PDF processing",
         ha="center", va="center",
         fontsize=14, color=OCEAN_TEAL, style="italic")

# -- LEFT COLUMN: Token-Heavy (bad way) --------------------------------------
left_x = 0.8
col_w = 5.4

# Column header
left_header = FancyBboxPatch((left_x, 7.5), col_w, 0.8,
                              boxstyle="round,pad=0.1",
                              facecolor=ALERT_RED, edgecolor="none",
                              alpha=0.15)
ax2.add_patch(left_header)
ax2.text(left_x + col_w / 2, 7.9,
         "PDF to AI Every Time",
         ha="center", va="center",
         fontsize=15, fontweight="bold", color=ALERT_RED)

# Left flow steps
left_steps = ["PDF", "Claude", "Parse &\nGuess Structure", "Output"]
left_colors = [WARM_GLOW, WARM_GLOW, WARM_GLOW, WARM_GLOW]
step_w = 3.6
step_h = 0.65
step_x = left_x + (col_w - step_w) / 2

for i, (label, color) in enumerate(zip(left_steps, left_colors)):
    y = 6.8 - i * 1.0
    box = FancyBboxPatch((step_x, y - step_h / 2), step_w, step_h,
                          boxstyle="round,pad=0.08",
                          facecolor=color, edgecolor="none", alpha=0.85)
    ax2.add_patch(box)
    ax2.text(step_x + step_w / 2, y,
             label, ha="center", va="center",
             fontsize=12, fontweight="bold", color=DEEP_NAVY)

    if i < len(left_steps) - 1:
        ax2.annotate("",
                     xy=(step_x + step_w / 2, y - step_h / 2 - 0.05),
                     xytext=(step_x + step_w / 2, y - step_h / 2 - 0.30),
                     arrowprops=dict(arrowstyle="<-", color=ALERT_RED, lw=1.8))

# Left callouts
left_issues = [
    "High token usage",
    "Repeated work every run",
    "Inconsistent results",
    "Hard to audit",
]
for i, issue in enumerate(left_issues):
    y = 3.2 - i * 0.38
    ax2.text(left_x + 0.4, y, "X", ha="center", va="center",
             fontsize=11, fontweight="bold", color=ALERT_RED)
    ax2.text(left_x + 0.8, y, issue, ha="left", va="center",
             fontsize=12, color=DEEP_NAVY)

# -- RIGHT COLUMN: Token-Efficient (good way) --------------------------------
right_x = 7.8

# Column header
right_header = FancyBboxPatch((right_x, 7.5), col_w, 0.8,
                               boxstyle="round,pad=0.1",
                               facecolor=BRIGHT_TEAL, edgecolor="none",
                               alpha=0.15)
ax2.add_patch(right_header)
ax2.text(right_x + col_w / 2, 7.9,
         "PDF to Markdown to Skill",
         ha="center", va="center",
         fontsize=15, fontweight="bold", color=OCEAN_TEAL)

# Right flow steps
right_steps = ["PDF", "Markdown\n(once)", "Mask &\nApply Skill", "Output"]
right_colors = [SOFT_SAGE, BRIGHT_TEAL, SEA_GREEN, BRIGHT_TEAL]
step_x_r = right_x + (col_w - step_w) / 2

for i, (label, color) in enumerate(zip(right_steps, right_colors)):
    y = 6.8 - i * 1.0
    tc = text_color_for(color)
    box = FancyBboxPatch((step_x_r, y - step_h / 2), step_w, step_h,
                          boxstyle="round,pad=0.08",
                          facecolor=color, edgecolor="none", alpha=0.85)
    ax2.add_patch(box)
    ax2.text(step_x_r + step_w / 2, y,
             label, ha="center", va="center",
             fontsize=12, fontweight="bold", color=tc)

    if i < len(right_steps) - 1:
        ax2.annotate("",
                     xy=(step_x_r + step_w / 2, y - step_h / 2 - 0.05),
                     xytext=(step_x_r + step_w / 2, y - step_h / 2 - 0.30),
                     arrowprops=dict(arrowstyle="<-", color=OCEAN_TEAL, lw=1.8))

# Right callouts
right_benefits = [
    "Low token usage",
    "Reusable structure",
    "Controlled inputs",
    "Audit-friendly",
]
for i, benefit in enumerate(right_benefits):
    y = 3.2 - i * 0.38
    ax2.text(right_x + 0.25, y, "+",
             ha="center", va="center",
             fontsize=13, fontweight="bold", color=SEA_GREEN)
    ax2.text(right_x + 0.65, y, benefit, ha="left", va="center",
             fontsize=12, color=DEEP_NAVY)

# Bottom insight box
insight_box = FancyBboxPatch((2, 0.6), 10, 0.7,
                              boxstyle="round,pad=0.1",
                              facecolor=DEEP_NAVY, edgecolor="none",
                              alpha=0.90)
ax2.add_patch(insight_box)
ax2.text(7, 0.95,
         "Convert once. Reuse forever. Control everything.",
         ha="center", va="center",
         fontsize=14, fontweight="bold", color=WHITE)

# Footer
ax2.text(7, 0.15, FOOTER_TEXT,
         ha="center", va="center",
         fontsize=10, color=DEEP_NAVY, alpha=0.50)

fig2.savefig(os.path.join(OUT_DIR, "16_workflow_comparison.png"),
             dpi=180, bbox_inches="tight", facecolor=fig2.get_facecolor())
plt.close(fig2)
print("  Saved 16_workflow_comparison.png")

# =============================================================================
# Visual 03 -- Accountant Translation Table
# =============================================================================
fig3, ax3 = plt.subplots(figsize=(14, 9))
fig3.patch.set_facecolor(WHITE)
ax3.set_facecolor(WHITE)
ax3.set_xlim(0, 14)
ax3.set_ylim(0, 10)
ax3.axis("off")

# Title
ax3.text(7, 9.5, "The Accountant Translation",
         ha="center", va="center",
         fontsize=22, fontweight="bold", color=DEEP_NAVY)

ax3.text(7, 8.9, "PDF workflows in terms you already understand",
         ha="center", va="center",
         fontsize=14, color=OCEAN_TEAL, style="italic")

# Four translation rows
rows = [
    {
        "term":    "PDF",
        "meaning": "A box of receipts\ndumped on the desk",
        "color":   GOLDEN_YELLOW,
    },
    {
        "term":    "Markdown",
        "meaning": "A clean, reconciled\nschedule ready to use",
        "color":   BRIGHT_TEAL,
    },
    {
        "term":    "Skill",
        "meaning": "Your repeatable\nmonth-end close process",
        "color":   SOFT_SAGE,
    },
    {
        "term":    "Token Savings",
        "meaning": "Less rework,\nfewer wasted hours",
        "color":   SEA_GREEN,
    },
]

card_w = 10
card_h = 1.4
x_start = 2
y_top = 8.2

for i, r in enumerate(rows):
    y = y_top - i * (card_h + 0.25)
    tc = text_color_for(r["color"])

    # Card background
    card = FancyBboxPatch((x_start, y - card_h), card_w, card_h,
                           boxstyle="round,pad=0.15",
                           facecolor=r["color"], edgecolor="none",
                           alpha=0.92)
    ax3.add_patch(card)

    # Term (left side)
    ax3.text(x_start + 1.8, y - card_h / 2,
             r["term"],
             ha="center", va="center",
             fontsize=16, fontweight="bold", color=tc)

    # Separator
    ax3.text(x_start + 3.3, y - card_h / 2,
             "=",
             ha="center", va="center",
             fontsize=18, fontweight="bold", color=tc, alpha=0.6)

    # Meaning (right side)
    ax3.text(x_start + 6.8, y - card_h / 2,
             r["meaning"],
             ha="center", va="center",
             fontsize=14, color=tc, linespacing=1.3)

    # Arrow between rows
    if i < len(rows) - 1:
        arrow_y = y - card_h - 0.125
        ax3.annotate("",
                     xy=(7, arrow_y - 0.04),
                     xytext=(7, arrow_y + 0.04),
                     arrowprops=dict(arrowstyle="->", color=OCEAN_TEAL,
                                     lw=2.0))

# Bottom callout
callout_box = FancyBboxPatch((x_start, 0.55), card_w, 0.9,
                              boxstyle="round,pad=0.15",
                              facecolor=DEEP_NAVY, edgecolor="none",
                              alpha=0.90)
ax3.add_patch(callout_box)

ax3.text(7, 1.0,
         "Structure your inputs. Reduce your rework. Control your workflow.",
         ha="center", va="center",
         fontsize=13, fontweight="bold", color=WHITE)

# Footer
ax3.text(7, 0.2, FOOTER_TEXT,
         ha="center", va="center",
         fontsize=10, color=DEEP_NAVY, alpha=0.50)

fig3.savefig(os.path.join(OUT_DIR, "16_accountant_translation.png"),
             dpi=180, bbox_inches="tight", facecolor=fig3.get_facecolor())
plt.close(fig3)
print("  Saved 16_accountant_translation.png")

print("\nAll Article 16 visuals generated.")
