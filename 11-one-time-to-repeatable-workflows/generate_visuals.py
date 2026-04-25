"""
Generate Article 11 visuals -- From One-Time Analysis to Repeatable Workflows.

Visual 01: Hero / front image
  Branded title card.

Visual 02: Nine-Step Workflow Pattern
  Visual showing the 9 steps from goal to SKILL.

Saved to articles/11-one-time-to-repeatable-workflows/visuals/
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

# -- Text contrast helper (SKILL.md mandatory rule 3) -----------------------
DARK_BG_COLORS = {DEEP_NAVY, MIDNIGHT_TEAL, OCEAN_TEAL, SEA_GREEN}

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

ax1.text(6, 3.8, "From One-Time Analysis to\nRepeatable Workflows",
         ha="center", va="center",
         fontsize=26, fontweight="bold", color=DEEP_NAVY,
         linespacing=1.3)

ax1.text(6, 2.4, "Designing AI Projects That Actually Scale",
         ha="center", va="center",
         fontsize=14, color=OCEAN_TEAL, style="italic")

ax1.text(6, 1.4, "PythonMuse LLC  |  github.com/PythonMuse/ai-ledger",
         ha="center", va="center",
         fontsize=12, color=OCEAN_TEAL, alpha=0.7)

ax1.plot([2, 10], [1.9, 1.9], color=BRIGHT_TEAL, linewidth=1.5, alpha=0.5)

fig1.savefig(os.path.join(OUT_DIR, "11_visual_front.png"),
             dpi=180, bbox_inches="tight", facecolor=fig1.get_facecolor())
plt.close(fig1)
print("  Saved 11_visual_front.png")

# -----------------------------------------------------------------------------
# Visual 02 -- Nine-Step Workflow Pattern
# -----------------------------------------------------------------------------
fig2, ax2 = plt.subplots(figsize=(14, 10))
fig2.patch.set_facecolor(WHITE)
ax2.set_facecolor(WHITE)
ax2.set_xlim(0, 14)
ax2.set_ylim(0, 12)
ax2.axis("off")

ax2.text(7, 11.4, "The PythonMuse Safe AI Workflow Pattern",
         ha="center", va="center",
         fontsize=20, fontweight="bold", color=DEEP_NAVY)

ax2.text(7, 10.8, "Nine steps from goal to reusable SKILL",
         ha="center", va="center",
         fontsize=14, color=OCEAN_TEAL, style="italic")

steps = [
    ("1", "Start with Structure", "Define the goal\nbefore sharing data", OCEAN_TEAL),
    ("2", "Provide Headers Only", "Send column names,\nnot real data", OCEAN_TEAL),
    ("3", "Ask AI for a Plan", "Get a step-by-step\napproach first", SEA_GREEN),
    ("4", "Approve the Plan", "Your first\ncontrol point", SEA_GREEN),
    ("5", "Mask Data", "Remove sensitive\nfields", ALERT_RED),
    ("6", "Add Hooks", "Pre-flight checks\nbefore execution", ALERT_RED),
    ("7", "Execute Analysis", "AI runs with\ncontrols in place", BRIGHT_TEAL),
    ("8", "Ask: Do This Again?", "The most important\nquestion", GOLDEN_YELLOW),
    ("9", "Convert to SKILL", "Document for\nreuse", GOLDEN_YELLOW),
]

# Layout: vertical flow with two columns
for i, (num, title, desc, color) in enumerate(steps):
    col = i % 2
    row = i // 2
    x = 4 if col == 0 else 10
    y = 9.5 - row * 1.9

    tc = text_color_for(color)

    # Box
    box = FancyBboxPatch((x - 2.5, y - 0.7), 5, 1.4,
                         boxstyle="round,pad=0.15",
                         facecolor=color, edgecolor="none",
                         alpha=0.9)
    ax2.add_patch(box)

    # Step number circle
    ax2.text(x - 1.8, y, num, ha="center", va="center",
             fontsize=14, fontweight="bold", color=DEEP_NAVY,
             bbox=dict(boxstyle="circle,pad=0.3", facecolor=WHITE,
                       edgecolor="none", alpha=0.9))

    # Title and description
    ax2.text(x + 0.3, y + 0.2, title, ha="center", va="center",
             fontsize=13, fontweight="bold", color=tc)
    ax2.text(x + 0.3, y - 0.3, desc, ha="center", va="center",
             fontsize=12, color=tc, alpha=0.85,
             linespacing=1.2)

    # Arrow to next step
    if i < len(steps) - 1:
        next_col = (i + 1) % 2
        next_row = (i + 1) // 2
        x_next = 4 if next_col == 0 else 10
        y_next = 9.5 - next_row * 1.9

        if col == 0 and next_col == 1:
            # Same row, left to right
            ax2.annotate("", xy=(x_next - 2.5, y), xytext=(x + 2.5, y),
                         arrowprops=dict(arrowstyle="->", color=OCEAN_TEAL,
                                         lw=1.2))
        elif col == 1 and next_col == 0:
            # Right to left, down
            ax2.annotate("", xy=(x_next + 2.5, y_next + 0.7),
                         xytext=(x - 2.5, y - 0.7),
                         arrowprops=dict(arrowstyle="->", color=OCEAN_TEAL,
                                         lw=1.2,
                                         connectionstyle="arc3,rad=-0.3"))

# Legend at bottom
ax2.text(7, 0.6, "Design  \u2192  Protect  \u2192  Execute  \u2192  Reuse",
         ha="center", va="center",
         fontsize=13, fontweight="bold", color=OCEAN_TEAL)

fig2.savefig(os.path.join(OUT_DIR, "11_workflow_steps.png"),
             dpi=180, bbox_inches="tight", facecolor=fig2.get_facecolor())
plt.close(fig2)
print("  Saved 11_workflow_steps.png")

print("\nAll Article 11 visuals generated.")
