"""
Generate Article 08 visuals — Why Claude "Forgets".

Visual 01: Hero / front image
  Branded title card: "Why Claude 'Forgets'".

Visual 02: Context Window Problem
  Diagram showing how the context window fills and loses earlier information.

Visual 03: External Memory System
  Three-file system (plan.md, status_update.md, CLAUDE.md) diagram.

Saved to articles/08-why-claude-forgets/visuals/
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
DARK_BG_COLORS = {DEEP_NAVY, MIDNIGHT_TEAL, OCEAN_TEAL, SEA_GREEN, ALERT_RED}

def text_color_for(bg):
    """Return correct text color per SKILL.md contrast rule."""
    if bg in DARK_BG_COLORS:
        return WHITE
    return DEEP_NAVY

# ---------------------------------------------------------------------------
# Visual 01 -- Hero / Front Image
# ---------------------------------------------------------------------------
fig1, ax1 = plt.subplots(figsize=(12, 6))
fig1.patch.set_facecolor(WHITE)
ax1.set_facecolor(WHITE)
ax1.set_xlim(0, 12)
ax1.set_ylim(0, 6)
ax1.axis("off")

ax1.text(6, 3.8, 'Why Claude "Forgets"',
         ha="center", va="center",
         fontsize=28, fontweight="bold", color=DEEP_NAVY,
         linespacing=1.3)

ax1.text(6, 2.6, "And How to Fix It with\nSimple Project Files",
         ha="center", va="center",
         fontsize=16, color=OCEAN_TEAL, fontstyle="italic",
         linespacing=1.3)

ax1.plot([3, 9], [1.7, 1.7], color=BRIGHT_TEAL, linewidth=2)

ax1.text(6, 1.0, "PythonMuse LLC  |  github.com/PythonMuse/ai-ledger",
         ha="center", va="center",
         fontsize=12, color=OCEAN_TEAL, alpha=0.7)

plt.savefig(os.path.join(OUT_DIR, "08_visual_front.png"),
            dpi=180, bbox_inches="tight", facecolor=fig1.get_facecolor())
plt.close()
print("  Saved 08_visual_front.png")

# ---------------------------------------------------------------------------
# Visual 02 -- The Context Window Problem
#   Landscape layout with solid brand fills for PowerPoint readability
# ---------------------------------------------------------------------------
fig2, ax2 = plt.subplots(figsize=(14, 7.5))
fig2.patch.set_facecolor(WHITE)
ax2.set_facecolor(WHITE)
ax2.set_xlim(0, 14)
ax2.set_ylim(0, 7.5)
ax2.axis("off")

ax2.text(7, 7.05, "The Context Window Problem",
         ha="center", va="center",
         fontsize=20, fontweight="bold", color=DEEP_NAVY)
ax2.text(7, 6.5, "What happens as your conversation grows",
         ha="center", va="center",
         fontsize=14, color=OCEAN_TEAL, fontstyle="italic")

# -- Context window arrow label --
bar_top = 5.75
ax2.text(1.0, bar_top + 0.2, "Context Window",
         fontsize=13, fontweight="bold", color=DEEP_NAVY, va="bottom")
ax2.annotate("",
             xy=(13.0, bar_top + 0.25),
             xytext=(3.6, bar_top + 0.25),
             arrowprops=dict(arrowstyle="->", color=DEEP_NAVY, lw=1.8))

# -- Three context segments side-by-side (solid fills) --
seg_y = 3.95
seg_h = 1.7
seg_gap = 0.15
total_w = 12.0
seg_left = 1.0

segments = [
    ("Early Decisions", "Fading from context", ALERT_RED, 0.30),
    ("Middle Work",     "Losing detail",       GOLDEN_YELLOW, 0.30),
    ("Recent Messages", "Clear and active",    BRIGHT_TEAL, 0.35),
]

x = seg_left
for title, desc, bg, frac in segments:
    w = total_w * frac
    seg_box = FancyBboxPatch(
        (x, seg_y), w, seg_h,
        boxstyle="round,pad=0.12",
        facecolor=bg, edgecolor="none", zorder=2)
    ax2.add_patch(seg_box)

    tc = text_color_for(bg)
    cx = x + w / 2
    cy = seg_y + seg_h / 2

    ax2.text(cx, cy + 0.25, title,
             ha="center", va="center",
             fontsize=13, fontweight="bold", color=tc, zorder=3)
    ax2.text(cx, cy - 0.25, desc,
             ha="center", va="center",
             fontsize=12, color=tc, zorder=3)

    x += w + seg_gap

# -- Three failure scenario cards (solid fills) --
scenarios = [
    ("Session Timeout",   "Everything disappears",    ALERT_RED),
    ("New Session",       "Zero memory of prior work", OCEAN_TEAL),
    ("Long Conversation", "Early details lost",        SEA_GREEN),
]

card_w = 3.6
card_h = 1.3
card_y = 1.3
card_gap = (total_w - 3 * card_w) / 2
card_x_start = seg_left

for i, (title, desc, bg) in enumerate(scenarios):
    cx_left = card_x_start + i * (card_w + card_gap)
    card = FancyBboxPatch(
        (cx_left, card_y), card_w, card_h,
        boxstyle="round,pad=0.12",
        facecolor=bg, edgecolor="none", zorder=2)
    ax2.add_patch(card)

    tc = text_color_for(bg)
    cx = cx_left + card_w / 2
    cy = card_y + card_h / 2

    ax2.text(cx, cy + 0.18, title,
             ha="center", va="center",
             fontsize=13, fontweight="bold", color=tc, zorder=3)
    ax2.text(cx, cy - 0.2, desc,
             ha="center", va="center",
             fontsize=12, color=tc, zorder=3)

# -- Bottom callout --
ax2.text(7, 0.45,
         "Chat history is not project memory.",
         ha="center", va="center",
         fontsize=14, color=DEEP_NAVY, fontweight="bold", fontstyle="italic",
         bbox=dict(boxstyle="round,pad=0.45",
                   facecolor=WARM_GLOW, edgecolor="none"),
         zorder=5)

plt.savefig(os.path.join(OUT_DIR, "08_context_problem.png"),
            dpi=180, bbox_inches="tight")
plt.close()
print("  Saved 08_context_problem.png")

# ---------------------------------------------------------------------------
# Visual 03 -- The Three-File External Memory System
#   Landscape layout — wider cards with gaps, Claude box fits all text
# ---------------------------------------------------------------------------
fig3, ax3 = plt.subplots(figsize=(14, 8))
fig3.patch.set_facecolor(WHITE)
ax3.set_facecolor(WHITE)
ax3.set_xlim(0, 14)
ax3.set_ylim(0, 8)
ax3.axis("off")

ax3.text(7, 7.5, "The External Memory System",
         ha="center", va="center",
         fontsize=20, fontweight="bold", color=DEEP_NAVY)
ax3.text(7, 6.95, "Three files that survive session resets",
         ha="center", va="center",
         fontsize=14, color=OCEAN_TEAL, fontstyle="italic")

# Three file cards — evenly spaced across full width
files = [
    ("plan.md", "The Blueprint", "Objective, rules,\nsteps, constraints",
     OCEAN_TEAL),
    ("status_update.md", "The Save Button", "Completed, outputs,\nissues, next steps",
     GOLDEN_YELLOW),
    ("CLAUDE.md", "The Instructor", "Behavior rules,\nsession startup, guardrails",
     BRIGHT_TEAL),
]

card_width = 3.4
card_height = 2.6
card_y_center = 5.0
card_gap = (14 - 3 * card_width) / 4   # equal gutters on edges and between

card_centers = []
for i, (fname, subtitle, desc, bg) in enumerate(files):
    cx = card_gap + card_width / 2 + i * (card_width + card_gap)
    card_centers.append(cx)
    tc = text_color_for(bg)

    card = FancyBboxPatch(
        (cx - card_width / 2, card_y_center - card_height / 2),
        card_width, card_height,
        boxstyle="round,pad=0.12",
        facecolor=bg, edgecolor="none",
        zorder=2
    )
    ax3.add_patch(card)

    ax3.text(cx, card_y_center + 0.7, fname,
             ha="center", va="center",
             fontsize=14, fontweight="bold", fontfamily="monospace",
             color=tc, zorder=3)
    ax3.text(cx, card_y_center + 0.15, subtitle,
             ha="center", va="center",
             fontsize=13, fontstyle="italic",
             color=tc, zorder=3)
    ax3.text(cx, card_y_center - 0.6, desc,
             ha="center", va="center",
             fontsize=12, color=tc,
             linespacing=1.4, zorder=3)

# Claude session box — wide enough for description text
claude_width = 6.0
claude_height = 1.4
claude_cx = 7.0
claude_cy = 1.6

claude_box = FancyBboxPatch(
    (claude_cx - claude_width / 2, claude_cy - claude_height / 2),
    claude_width, claude_height,
    boxstyle="round,pad=0.12",
    facecolor=DEEP_NAVY, edgecolor="none",
    zorder=2
)
ax3.add_patch(claude_box)
ax3.text(claude_cx, claude_cy + 0.25, "Claude Session",
         ha="center", va="center",
         fontsize=14, fontweight="bold", color=BRIGHT_TEAL, zorder=3)
ax3.text(claude_cx, claude_cy - 0.25,
         "Reads files at start, updates as work progresses",
         ha="center", va="center",
         fontsize=12, color=WHITE, zorder=3)

# Arrows from cards down to Claude box
for cx in card_centers:
    ax3.annotate("",
                 xy=(claude_cx, claude_cy + claude_height / 2 + 0.05),
                 xytext=(cx, card_y_center - card_height / 2 - 0.05),
                 arrowprops=dict(arrowstyle="-|>", color=DEEP_NAVY,
                                 lw=2, mutation_scale=18,
                                 connectionstyle="arc3,rad=0"),
                 zorder=4)

# Update arrow back to status_update.md
ax3.annotate("",
             xy=(card_centers[1], card_y_center - card_height / 2 - 0.05),
             xytext=(claude_cx + 0.5, claude_cy + claude_height / 2 + 0.05),
             arrowprops=dict(arrowstyle="-|>", color=GOLDEN_YELLOW,
                             lw=2.5, mutation_scale=18,
                             connectionstyle="arc3,rad=-0.3",
                             linestyle="--"),
             zorder=4)
ax3.text(10.5, 3.15, "updates",
         ha="center", va="center",
         fontsize=13, fontweight="bold", color=GOLDEN_YELLOW,
         fontstyle="italic", zorder=5)

# Bottom callout
ax3.text(7, 0.35,
         "AI is not your memory -- your files are.",
         ha="center", va="center",
         fontsize=14, color=DEEP_NAVY, fontweight="bold", fontstyle="italic",
         bbox=dict(boxstyle="round,pad=0.45",
                   facecolor=WARM_GLOW, edgecolor="none"),
         zorder=5)

plt.savefig(os.path.join(OUT_DIR, "08_external_memory.png"),
            dpi=180, bbox_inches="tight")
plt.close()
print("  Saved 08_external_memory.png")
