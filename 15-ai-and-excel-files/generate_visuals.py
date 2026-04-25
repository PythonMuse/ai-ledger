"""
Generate Article 15 visuals -- "AI Can't Work With Our Excel Files"... or Can It?

Visual 01: Hero / front image
Visual 02: Three-tier data approach (SQL > CSV > Excel + Skill)

Saved to articles/15-ai-and-excel-files/visuals/
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
DARK_BG_COLORS = {DEEP_NAVY, MIDNIGHT_TEAL, OCEAN_TEAL, SEA_GREEN}

def text_color_for(bg):
    """Return correct text color per SKILL.md contrast rule."""
    if bg in DARK_BG_COLORS:
        return WHITE
    return DEEP_NAVY

# =============================================================================
# Visual 01 -- Hero / Front Image
# =============================================================================
fig1, ax1 = plt.subplots(figsize=(12, 6))
fig1.patch.set_facecolor(WHITE)
ax1.set_facecolor(WHITE)
ax1.set_xlim(0, 12)
ax1.set_ylim(0, 6)
ax1.axis("off")

ax1.text(6, 4.0, '"AI Can\'t Work With Our\nExcel Files"... or Can It?',
         ha="center", va="center",
         fontsize=22, fontweight="bold", color=DEEP_NAVY,
         linespacing=1.4)

ax1.text(6, 2.6, "Why the problem is not Excel -- it is the missing instruction layer",
         ha="center", va="center",
         fontsize=14, color=OCEAN_TEAL, style="italic")

ax1.text(6, 1.5, "PythonMuse LLC  |  github.com/PythonMuse/ai-ledger",
         ha="center", va="center",
         fontsize=12, color=OCEAN_TEAL, alpha=0.70)

ax1.plot([2, 10], [2.05, 2.05], color=BRIGHT_TEAL, linewidth=1.5, alpha=0.5)

tagline = FancyBboxPatch((2.5, 0.3), 7, 0.7,
                          boxstyle="round,pad=0.1",
                          facecolor=DEEP_NAVY, edgecolor="none",
                          alpha=0.9)
ax1.add_patch(tagline)
ax1.text(6, 0.65, "Excel is not the problem. Lack of structure is.",
         ha="center", va="center",
         fontsize=14, fontweight="bold", color=WHITE)

fig1.savefig(os.path.join(OUT_DIR, "15_visual_front.png"),
             dpi=180, bbox_inches="tight", facecolor=fig1.get_facecolor())
plt.close(fig1)
print("  Saved 15_visual_front.png")

# =============================================================================
# Visual 02 -- Three-Tier Data Approach
# =============================================================================
fig2, ax2 = plt.subplots(figsize=(14, 10))
fig2.patch.set_facecolor(WHITE)
ax2.set_facecolor(WHITE)
ax2.set_xlim(0, 14)
ax2.set_ylim(0, 11)
ax2.axis("off")

# Title
ax2.text(7, 10.4, "Three-Tier Data Approach for AI",
         ha="center", va="center",
         fontsize=22, fontweight="bold", color=DEEP_NAVY)

ax2.text(7, 9.8, "Not all data sources are equal -- choose the right tier for your workflow",
         ha="center", va="center",
         fontsize=14, color=OCEAN_TEAL, style="italic")

# -- Three tier cards (stacked top-to-bottom, best at top) -------------------
tiers = [
    {
        "level":  "Level 1 -- Best",
        "label":  "Direct Data (SQL)",
        "points": "Clean, structured, fully AI-ready\nNo interpretation needed\nBest for production workflows",
        "color":  SOFT_SAGE,
        "badge":  "Best",
    },
    {
        "level":  "Level 2 -- Better",
        "label":  "CSV Export",
        "points": "Flat and predictable\nMinimal noise\nEasy for AI to interpret",
        "color":  GOLDEN_YELLOW,
        "badge":  "Better",
    },
    {
        "level":  "Level 3 -- Complex",
        "label":  "Excel + Skill",
        "points": "Multi-layered, visual-heavy\nRequires instruction layer (Skill)\nFully workable once documented",
        "color":  BRIGHT_TEAL,
        "badge":  "Complex",
    },
]

card_w = 10
card_h = 1.9
x_start = 2
y_top = 9.0

for i, t in enumerate(tiers):
    y = y_top - i * (card_h + 0.3)
    tc = text_color_for(t["color"])
    note_c = OCEAN_TEAL if tc == DEEP_NAVY else WARM_GLOW

    # Card background
    card = FancyBboxPatch((x_start, y - card_h), card_w, card_h,
                           boxstyle="round,pad=0.15",
                           facecolor=t["color"], edgecolor="none",
                           alpha=0.92)
    ax2.add_patch(card)

    # Badge
    badge_w = 1.4
    badge = FancyBboxPatch((x_start + 0.2, y - 0.55), badge_w, 0.4,
                            boxstyle="round,pad=0.06",
                            facecolor=DEEP_NAVY, edgecolor="none", alpha=0.25)
    ax2.add_patch(badge)
    ax2.text(x_start + 0.2 + badge_w / 2, y - 0.35,
             t["badge"],
             ha="center", va="center",
             fontsize=10, fontweight="bold", color=tc, alpha=0.90)

    # Level + label
    ax2.text(x_start + 2.0, y - 0.35,
             t["level"],
             ha="left", va="center",
             fontsize=13, fontweight="bold", color=tc)

    ax2.text(x_start + card_w - 0.4, y - 0.35,
             t["label"],
             ha="right", va="center",
             fontsize=14, fontweight="bold", color=tc)

    # Bullet points
    ax2.text(x_start + 2.0, y - 1.2,
             t["points"],
             ha="left", va="center",
             fontsize=12, color=tc, linespacing=1.3)

    # Arrow between tiers
    if i < len(tiers) - 1:
        arrow_y = y - card_h - 0.15
        ax2.annotate("",
                     xy=(7, arrow_y - 0.05),
                     xytext=(7, arrow_y + 0.05),
                     arrowprops=dict(arrowstyle="->", color=OCEAN_TEAL,
                                     lw=2.0))

# -- Skill callout box at bottom ---------------------------------------------
skill_y = 1.6
skill_box = FancyBboxPatch((x_start, skill_y - 0.8), card_w, 1.5,
                             boxstyle="round,pad=0.15",
                             facecolor=DEEP_NAVY, edgecolor="none",
                             alpha=0.90)
ax2.add_patch(skill_box)

ax2.text(7, skill_y + 0.25,
         "The Skill is the bridge -- a training manual for your Excel file",
         ha="center", va="center",
         fontsize=13, fontweight="bold", color=WHITE)

ax2.text(7, skill_y - 0.25,
         "Create it once. Reuse it every month. No retraining required.",
         ha="center", va="center",
         fontsize=12, color=WHITE)

# Footer
ax2.text(7, 0.2, "PythonMuse LLC  |  github.com/PythonMuse/ai-ledger",
         ha="center", va="center",
         fontsize=10, color=DEEP_NAVY, alpha=0.50)

fig2.savefig(os.path.join(OUT_DIR, "15_data_tiers.png"),
             dpi=180, bbox_inches="tight", facecolor=fig2.get_facecolor())
plt.close(fig2)
print("  Saved 15_data_tiers.png")

print("\nAll Article 15 visuals generated.")
