"""
Generate Article 14 visuals -- Stop Using One AI Like It Is Excel.

Visual 01: Hero / front image
Visual 02: Model Orchestration workflow (Plan -> Build -> Execute -> Explain)

Saved to articles/14-ai-team-for-accountants/visuals/
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

ax1.text(6, 3.8, "Stop Using One AI Like It Is Excel",
         ha="center", va="center",
         fontsize=22, fontweight="bold", color=DEEP_NAVY,
         linespacing=1.4)

ax1.text(6, 2.6, "How accountants should actually use Claude, ChatGPT, and Copilot together",
         ha="center", va="center",
         fontsize=14, color=OCEAN_TEAL, style="italic")

ax1.text(6, 1.5, "PythonMuse LLC  |  github.com/PythonMuse/ai-ledger",
         ha="center", va="center",
         fontsize=12, color=OCEAN_TEAL, alpha=0.70)

ax1.plot([2, 10], [2.05, 2.05], color=BRIGHT_TEAL, linewidth=1.5, alpha=0.5)

tagline = FancyBboxPatch((3.5, 0.3), 5, 0.7,
                          boxstyle="round,pad=0.1",
                          facecolor=DEEP_NAVY, edgecolor="none",
                          alpha=0.9)
ax1.add_patch(tagline)
ax1.text(6, 0.65, "AI is not a tool. It is a team.",
         ha="center", va="center",
         fontsize=14, fontweight="bold", color=WHITE)

fig1.savefig(os.path.join(OUT_DIR, "14_visual_front.png"),
             dpi=180, bbox_inches="tight", facecolor=fig1.get_facecolor())
plt.close(fig1)
print("  Saved 14_visual_front.png")

# =============================================================================
# Visual 02 -- Model Orchestration Workflow
# =============================================================================
fig2, ax2 = plt.subplots(figsize=(14, 9))
fig2.patch.set_facecolor(WHITE)
ax2.set_facecolor(WHITE)
ax2.set_xlim(0, 14)
ax2.set_ylim(0, 10)
ax2.axis("off")

# Title
ax2.text(7, 9.4, "Assign the Right AI to the Right Job",
         ha="center", va="center",
         fontsize=22, fontweight="bold", color=DEEP_NAVY)

ax2.text(7, 8.8, "Model orchestration for accounting workflows",
         ha="center", va="center",
         fontsize=14, color=OCEAN_TEAL, style="italic")

# Four workflow steps
steps = [
    {
        "num":   "Step 1",
        "label": "Plan",
        "model": "Claude Opus",
        "desc":  "Design the workflow.\nIdentify steps, edge cases,\nand assumptions.",
        "color": BRIGHT_TEAL,
    },
    {
        "num":   "Step 2",
        "label": "Build",
        "model": "Claude Sonnet",
        "desc":  "Write the script.\nImplement logic, structure\ndata pipelines.",
        "color": SEA_GREEN,
    },
    {
        "num":   "Step 3",
        "label": "Execute",
        "model": "Claude Haiku",
        "desc":  "Run across files.\nSummarize differences,\nflag exceptions.",
        "color": GOLDEN_YELLOW,
    },
    {
        "num":   "Step 4",
        "label": "Explain",
        "model": "ChatGPT",
        "desc":  "Summarize results.\nPlain English for\nCFO or auditor review.",
        "color": WARM_GLOW,
    },
]

card_w = 2.8
card_h = 4.2
gap    = 0.35
total_w = len(steps) * card_w + (len(steps) - 1) * gap
x_start = (14 - total_w) / 2
y_top   = 8.0

for i, s in enumerate(steps):
    x = x_start + i * (card_w + gap)
    tc = text_color_for(s["color"])

    # Card background
    card = FancyBboxPatch((x, y_top - card_h), card_w, card_h,
                           boxstyle="round,pad=0.15",
                           facecolor=s["color"], edgecolor="none",
                           alpha=0.92)
    ax2.add_patch(card)

    # Step number badge
    badge = FancyBboxPatch((x + 0.2, y_top - 0.6), card_w - 0.4, 0.45,
                            boxstyle="round,pad=0.06",
                            facecolor=DEEP_NAVY, edgecolor="none", alpha=0.3)
    ax2.add_patch(badge)
    ax2.text(x + card_w / 2, y_top - 0.38,
             s["num"],
             ha="center", va="center",
             fontsize=12, fontweight="bold", color=tc, alpha=0.85)

    # Label (big)
    ax2.text(x + card_w / 2, y_top - 1.1,
             s["label"],
             ha="center", va="center",
             fontsize=16, fontweight="bold", color=tc)

    # Model
    ax2.text(x + card_w / 2, y_top - 1.65,
             s["model"],
             ha="center", va="center",
             fontsize=13, fontweight="bold", color=tc)

    # Description
    ax2.text(x + card_w / 2, y_top - 2.7,
             s["desc"],
             ha="center", va="center",
             fontsize=12, color=tc, linespacing=1.4)

    # Arrow between cards
    if i < len(steps) - 1:
        arrow_x = x + card_w + gap / 2
        ax2.annotate("",
                     xy=(arrow_x + 0.12, y_top - card_h / 2),
                     xytext=(arrow_x - 0.12, y_top - card_h / 2),
                     arrowprops=dict(arrowstyle="->", color=OCEAN_TEAL,
                                     lw=2.5))

# Copilot row at bottom
copilot_y = 2.4
cop_box = FancyBboxPatch((x_start, copilot_y - 0.8), total_w, 1.5,
                          boxstyle="round,pad=0.15",
                          facecolor=DEEP_NAVY, edgecolor="none",
                          alpha=0.90)
ax2.add_patch(cop_box)

ax2.text(7, copilot_y + 0.25,
         "GitHub Copilot -- Works across all steps inside VS Code",
         ha="center", va="center",
         fontsize=13, fontweight="bold", color=WHITE)

ax2.text(7, copilot_y - 0.25,
         "Reads your folder structure, file names, and Markdown instructions",
         ha="center", va="center",
         fontsize=12, color=WHITE)

# Footer
ax2.text(7, 0.6,
         "Your folder structure is your prompt.",
         ha="center", va="center",
         fontsize=13, fontweight="bold", color=OCEAN_TEAL)

ax2.text(7, 0.2, "PythonMuse LLC  |  github.com/PythonMuse/ai-ledger",
         ha="center", va="center",
         fontsize=10, color=DEEP_NAVY, alpha=0.50)

fig2.savefig(os.path.join(OUT_DIR, "14_model_orchestration.png"),
             dpi=180, bbox_inches="tight", facecolor=fig2.get_facecolor())
plt.close(fig2)
print("  Saved 14_model_orchestration.png")

print("\nAll Article 14 visuals generated.")
