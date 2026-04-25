"""
Generate Article 13 visuals -- AI in Accounting Isn't Just About Efficiency -- It's About Control.

Visual 01: Hero / front image
  Branded title card.

Visual 02: Trust Ladder
  Four-level framework from Unsafe to Verified AI workflows.

Visual 03: Checklist Overview
  Summary of the six-section Trust but Verify checklist.

Saved to articles/13-zero-trust-ai-accounting/visuals/
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np
import os

# -- Output directory --------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR    = os.path.join(SCRIPT_DIR, "visuals")
os.makedirs(OUT_DIR, exist_ok=True)

# -- Logo mark ---------------------------------------------------------------

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
DARK_BG_COLORS = {DEEP_NAVY, MIDNIGHT_TEAL, OCEAN_TEAL, SEA_GREEN, ALERT_RED, ALERT_ORANGE}

def text_color_for(bg):
    """Return correct text color per SKILL.md contrast rule."""
    if bg in DARK_BG_COLORS:
        return WHITE
    return DEEP_NAVY

# -----------------------------------------------------------------------------
# Visual 01 -- Hero / Front Image
# -----------------------------------------------------------------------------
fig1, ax1 = plt.subplots(figsize=(12, 6))
fig1.patch.set_facecolor(WHITE)
ax1.set_facecolor(WHITE)
ax1.set_xlim(0, 12)
ax1.set_ylim(0, 6)
ax1.axis("off")

ax1.text(6, 3.8, "AI in Accounting Isn't Just\nAbout Efficiency -- It's About Control",
         ha="center", va="center",
         fontsize=22, fontweight="bold", color=DEEP_NAVY,
         linespacing=1.4)

ax1.text(6, 2.4, "Why Zero Trust principles are already built into how good accountants think",
         ha="center", va="center",
         fontsize=14, color=OCEAN_TEAL, style="italic")

ax1.text(6, 1.4, "PythonMuse LLC  |  github.com/PythonMuse/ai-ledger",
         ha="center", va="center",
         fontsize=12, color=OCEAN_TEAL, alpha=0.7)

ax1.plot([2, 10], [1.9, 1.9], color=BRIGHT_TEAL, linewidth=1.5, alpha=0.5)

# Trust but Verify label — standout callout
trust_box = FancyBboxPatch((4.6, 0.35), 2.8, 0.6,
                            boxstyle="round,pad=0.08",
                            facecolor=GOLDEN_YELLOW, edgecolor="none")
ax1.add_patch(trust_box)
ax1.text(6, 0.65, "Trust, but verify.",
         ha="center", va="center",
         fontsize=15, fontweight="bold", color=DEEP_NAVY)

fig1.savefig(os.path.join(OUT_DIR, "13_visual_front.png"),
             dpi=180, bbox_inches="tight", facecolor=fig1.get_facecolor())
plt.close(fig1)
print("  Saved 13_visual_front.png")

# -----------------------------------------------------------------------------
# Visual 02 -- The Four-Level Trust Ladder
# -----------------------------------------------------------------------------
fig2, ax2 = plt.subplots(figsize=(13, 11))
fig2.patch.set_facecolor(WHITE)
ax2.set_facecolor(WHITE)
ax2.set_xlim(0, 13)
ax2.set_ylim(0, 12)
ax2.axis("off")

ax2.text(6.5, 11.4, "Trust, but Verify",
         ha="center", va="center",
         fontsize=22, fontweight="bold", color=DEEP_NAVY)

ax2.text(6.5, 10.8, "Applying Accounting Discipline to AI Workflows",
         ha="center", va="center",
         fontsize=14, color=OCEAN_TEAL, style="italic")

# Level definitions
levels = [
    {
        "num": "Level 1",
        "label": "Unsafe",
        "color": ALERT_RED,
        "points": [
            "Raw data pasted into AI",
            "No masking or documentation",
            "Outputs trusted immediately",
            "No audit trail",
        ],
        "risk": "Risk: Data exposure + unreliable results",
    },
    {
        "num": "Level 2",
        "label": "Aware",
        "color": ALERT_ORANGE,
        "points": [
            "Some hesitation before sharing data",
            "Partial masking applied",
            "Manual review of outputs",
            "No consistent workflow",
        ],
        "risk": "Risk: Inconsistent controls",
    },
    {
        "num": "Level 3",
        "label": "Controlled  (PythonMuse Starting Point)",
        "color": GOLDEN_YELLOW,
        "points": [
            "Data masked before processing",
            "Only necessary fields shared",
            "AI asked for a plan first",
            "Outputs reviewed before use",
        ],
        "risk": "Most teams should aim here first",
    },
    {
        "num": "Level 4",
        "label": "Verified  (Audit-Ready)",
        "color": SEA_GREEN,
        "points": [
            "Structured input/output folders",
            "plan.md + status_update.md",
            "Reproducible workflows",
            "Documented and reviewable",
        ],
        "risk": "Aligned with COSO + Zero Trust principles",
    },
]

card_height   = 2.1
card_gap      = 0.25
cards_top     = 10.2
card_x_left   = 1.2
card_width    = 10.8

for i, lv in enumerate(levels):
    y_top = cards_top - i * (card_height + card_gap)
    y_center = y_top - card_height / 2

    tc = text_color_for(lv["color"])

    bg = FancyBboxPatch((card_x_left, y_top - card_height), card_width, card_height,
                        boxstyle="round,pad=0.15",
                        facecolor=lv["color"], edgecolor="none",
                        alpha=0.92)
    ax2.add_patch(bg)

    # Level number badge
    badge = FancyBboxPatch((card_x_left + 0.15, y_center - 0.35), 1.5, 0.7,
                            boxstyle="round,pad=0.08",
                            facecolor=DEEP_NAVY, edgecolor="none", alpha=0.25)
    ax2.add_patch(badge)
    ax2.text(card_x_left + 0.9, y_center,
             lv["num"], ha="center", va="center",
             fontsize=10, fontweight="bold", color=tc, alpha=0.9)

    # Level label
    ax2.text(card_x_left + 2.0, y_top - 0.42,
             lv["label"],
             ha="left", va="center",
             fontsize=15, fontweight="bold", color=tc)

    # Bullet points (two columns of two)
    for j, pt in enumerate(lv["points"]):
        col = j % 2
        row = j // 2
        px = card_x_left + 2.0 + col * 5.0
        py = y_top - 0.95 - row * 0.52
        ax2.text(px, py, f"  {pt}",
                 ha="left", va="center",
                 fontsize=12, color=tc, alpha=0.88)

    # Risk / note line
    ax2.text(card_x_left + 2.0, y_top - 1.82,
             lv["risk"],
             ha="left", va="center",
             fontsize=12, color=tc, alpha=0.7, style="italic")

# Bottom tagline
ax2.text(6.5, 0.55,
         "AI in accounting should follow the same principle we have always used:  Trust, but verify.",
         ha="center", va="center",
         fontsize=12, color=OCEAN_TEAL, style="italic")

ax2.text(6.5, 0.18, "PythonMuse LLC  |  github.com/PythonMuse/ai-ledger",
         ha="center", va="center",
         fontsize=10, color=DEEP_NAVY, alpha=0.45)

fig2.savefig(os.path.join(OUT_DIR, "13_trust_ladder.png"),
             dpi=180, bbox_inches="tight", facecolor=fig2.get_facecolor())
plt.close(fig2)
print("  Saved 13_trust_ladder.png")

# -----------------------------------------------------------------------------
# Visual 03 -- Checklist Overview
# -----------------------------------------------------------------------------
fig3, ax3 = plt.subplots(figsize=(12, 9))
fig3.patch.set_facecolor(WHITE)
ax3.set_facecolor(WHITE)
ax3.set_xlim(0, 12)
ax3.set_ylim(0, 10)
ax3.axis("off")

ax3.text(6, 9.5, "PythonMuse -- Trust but Verify Checklist",
         ha="center", va="center",
         fontsize=20, fontweight="bold", color=DEEP_NAVY)

ax3.text(6, 9.0, "Audit-Friendly AI Workflow for Accounting",
         ha="center", va="center",
         fontsize=14, color=OCEAN_TEAL, style="italic")

sections = [
    ("1. Before Using AI",   "Data Control",          ALERT_RED,     "Mask, minimize, confirm data"),
    ("2. Define the Task",   "Plan Before Processing", ALERT_ORANGE,  "Get AI approval on approach first"),
    ("3. Processing",        "Controlled Execution",  GOLDEN_YELLOW, "Verify steps are logical and clear"),
    ("4. Output Review",     "Trust but Verify",      WARM_GLOW,     "Tie results back to source data"),
    ("5. Documentation",     "Make It Reproducible",  SOFT_SAGE,     "Save inputs, outputs, and steps"),
    ("6. Final Check",       "Control Mindset",       SEA_GREEN,     "Could you explain this to an auditor?"),
]

# 2-column grid
positions = [
    (1.5, 7.5), (7.0, 7.5),
    (1.5, 5.4), (7.0, 5.4),
    (1.5, 3.3), (7.0, 3.3),
]

for (x, y), (num, title, color, desc) in zip(positions, sections):
    tc = text_color_for(color)

    box = FancyBboxPatch((x - 1.2, y - 0.95), 4.3, 1.75,
                         boxstyle="round,pad=0.15",
                         facecolor=color, edgecolor="none",
                         alpha=0.9)
    ax3.add_patch(box)

    ax3.text(x + 0.95, y + 0.45, num,
             ha="center", va="center",
             fontsize=10, fontweight="bold", color=tc, alpha=0.65)

    ax3.text(x + 0.95, y - 0.05, title,
             ha="center", va="center",
             fontsize=13, fontweight="bold", color=tc)

    ax3.text(x + 0.95, y - 0.54, desc,
             ha="center", va="center",
             fontsize=12, color=tc, alpha=0.82, style="italic")

ax3.text(6, 1.6,
         "If you can check every box -- your workflow is controlled and reviewable.",
         ha="center", va="center",
         fontsize=13, fontweight="bold", color=OCEAN_TEAL)

ax3.text(6, 1.1,
         "Controlled  |  Repeatable  |  Reviewable  |  Explainable",
         ha="center", va="center",
         fontsize=12, color=OCEAN_TEAL)

ax3.text(6, 0.4, "PythonMuse -- Practical AI for Accounting and Finance Professionals",
         ha="center", va="center",
         fontsize=10, color=DEEP_NAVY, alpha=0.45)

fig3.savefig(os.path.join(OUT_DIR, "13_checklist_overview.png"),
             dpi=180, bbox_inches="tight", facecolor=fig3.get_facecolor())
plt.close(fig3)
print("  Saved 13_checklist_overview.png")

print("\nAll Article 13 visuals generated.")
