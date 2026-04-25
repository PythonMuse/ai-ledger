"""
Generate Article 04 visuals — AI in Accounting Is Not the Wild West Anymore.

Visual 01: Hero / front image
  Branded title card for the article.

Visual 02: COSO Five Components for Generative AI
  Circular diagram showing the five COSO IC components with GenAI at center.

Visual 03: Traceable AI Workflow
  Horizontal flow: Defined Inputs → Transparent Transformation → Human Review → Evidence Retention.

Saved to articles/04-ai-governance-in-accounting/visuals/
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle, FancyBboxPatch
import numpy as np
import os

# ── Output directory ──────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR    = os.path.join(SCRIPT_DIR, "visuals")
os.makedirs(OUT_DIR, exist_ok=True)

# ── PythonMuse brand colors ──────────────────────────────────────────────────
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
GRAY_BG       = "#F4F6F7"
GRAY_LINE     = "#CCCCCC"
LIGHT_GRAY    = "#F5F5F5"

# -- Text contrast helper (SKILL.md mandatory rule 3) -----------------------
DARK_BG_COLORS = {DEEP_NAVY, MIDNIGHT_TEAL, OCEAN_TEAL, SEA_GREEN}

def text_color_for(bg):
    """Return correct text color per SKILL.md contrast rule."""
    if bg in DARK_BG_COLORS:
        return WHITE
    return DEEP_NAVY

# ─────────────────────────────────────────────────────────────────────────────
# Visual 01 – Hero / Front Image
# ─────────────────────────────────────────────────────────────────────────────
fig1, ax1 = plt.subplots(figsize=(12, 6))
fig1.patch.set_facecolor(WHITE)
ax1.set_facecolor(WHITE)
ax1.set_xlim(0, 12)
ax1.set_ylim(0, 6)
ax1.axis("off")

# Title
ax1.text(6, 3.8, "AI in Accounting Is Not\nthe Wild West Anymore",
         ha="center", va="center",
         fontsize=26, fontweight="bold", color=DEEP_NAVY,
         linespacing=1.3)

# Subtitle
ax1.text(6, 2.2, "But It's Also Not Plug-and-Play",
         ha="center", va="center",
         fontsize=16, color=OCEAN_TEAL, fontstyle="italic")

# Divider line
ax1.plot([3, 9], [1.5, 1.5], color=BRIGHT_TEAL, linewidth=2)

# Byline
ax1.text(6, 0.9, "PythonMuse LLC  |  github.com/PythonMuse/ai-ledger",
         ha="center", va="center",
         fontsize=12, color=OCEAN_TEAL)

out_path1 = os.path.join(OUT_DIR, "04_visual_front.png")
plt.savefig(out_path1, dpi=180, bbox_inches="tight")
plt.close()
print(f"[OK] 04_visual_front.png  ->  {OUT_DIR}")

# ─────────────────────────────────────────────────────────────────────────────
# Visual 02 – COSO Five Components for Generative AI
#   Landscape layout — PowerPoint-friendly, text fits in rounded-rect cards
# ─────────────────────────────────────────────────────────────────────────────
fig2, ax2 = plt.subplots(figsize=(14, 10))
fig2.patch.set_facecolor(WHITE)
ax2.set_facecolor(WHITE)
ax2.set_xlim(0, 14)
ax2.set_ylim(0, 10)
ax2.axis("off")

# Title — top of canvas with clear space above cards
ax2.text(7, 9.55, "COSO Internal Control Components",
         ha="center", va="center",
         fontsize=20, fontweight="bold", color=DEEP_NAVY)
ax2.text(7, 9.0, "Applied to Generative AI Governance",
         ha="center", va="center",
         fontsize=14, color=OCEAN_TEAL, fontstyle="italic")

# Center hub — "Generative AI"
hub_w, hub_h = 3.0, 1.3
hub_cx, hub_cy = 7, 5.0
hub_box = FancyBboxPatch(
    (hub_cx - hub_w / 2, hub_cy - hub_h / 2), hub_w, hub_h,
    boxstyle="round,pad=0.2",
    facecolor=DEEP_NAVY, edgecolor="none", zorder=5)
ax2.add_patch(hub_box)
ax2.text(hub_cx, hub_cy, "Generative AI",
         ha="center", va="center",
         fontsize=16, fontweight="bold",
         color=text_color_for(DEEP_NAVY), zorder=6)

# Five component cards — 3 on top row, 2 on bottom row
components = [
    ("Control\nEnvironment",         "Ownership, governance\npolicies, oversight",         BRIGHT_TEAL),
    ("Risk\nAssessment",             "Prompt manipulation,\nmodel drift, data leakage",    GOLDEN_YELLOW),
    ("Control\nActivities",          "Approval workflows,\nvalidation, access controls",   SEA_GREEN),
    ("Information &\nCommunication", "Traceability of inputs\nand outputs",                SOFT_SAGE),
    ("Monitoring\nActivities",       "Performance evaluation,\ndetect unexpected behavior", OCEAN_TEAL),
]

card_w = 3.6
card_h = 2.0

# Top row: 3 cards evenly spaced, below title with clear gap
top_y = 6.3                             # bottom edge of top-row cards (tops at 8.1)
top_gap = (14 - 3 * card_w) / 4        # equal gutters
top_xs = [top_gap + i * (card_w + top_gap) for i in range(3)]

# Bottom row: 2 cards centred
bot_y = 0.8
bot_gap = (14 - 2 * card_w) / 3
bot_xs = [bot_gap + i * (card_w + bot_gap) for i in range(2)]

positions = [(top_xs[0], top_y), (top_xs[1], top_y), (top_xs[2], top_y),
             (bot_xs[0], bot_y), (bot_xs[1], bot_y)]

hub_cx, hub_cy = 7, 5.0

for i, (title, desc, color) in enumerate(components):
    x, y = positions[i]

    card = FancyBboxPatch(
        (x, y), card_w, card_h,
        boxstyle="round,pad=0.15",
        facecolor=color, edgecolor="none", zorder=3)
    ax2.add_patch(card)

    txt = text_color_for(color)
    cx = x + card_w / 2
    cy = y + card_h / 2

    # Title (upper portion of card)
    ax2.text(cx, cy + 0.32, title,
             ha="center", va="center",
             fontsize=13, fontweight="bold", color=txt,
             linespacing=1.1, zorder=4)

    # Description (lower portion of card)
    ax2.text(cx, cy - 0.42, desc,
             ha="center", va="center",
             fontsize=12, color=txt,
             linespacing=1.2, zorder=4)

    # Dashed connector line from card centre toward hub centre
    dx = hub_cx - cx
    dy = hub_cy - cy
    dist = (dx**2 + dy**2) ** 0.5
    if dist > 0:
        ux, uy = dx / dist, dy / dist
        lx1 = cx + ux * 1.25
        ly1 = cy + uy * 1.25
        lx2 = hub_cx - ux * 1.0
        ly2 = hub_cy - uy * 1.0
        ax2.plot([lx1, lx2], [ly1, ly2],
                 color=GRAY_LINE, linewidth=1.5,
                 linestyle="--", zorder=1)

out_path2 = os.path.join(OUT_DIR, "04_coso_five_components.png")
plt.savefig(out_path2, dpi=180, bbox_inches="tight")
plt.close()
print(f"[OK] 04_coso_five_components.png  ->  {OUT_DIR}")

# ─────────────────────────────────────────────────────────────────────────────
# Visual 03 – Traceable AI Workflow
# ─────────────────────────────────────────────────────────────────────────────
fig3, ax3 = plt.subplots(figsize=(14, 6))
fig3.patch.set_facecolor(WHITE)
ax3.set_facecolor(WHITE)
ax3.set_xlim(0, 14)
ax3.set_ylim(0, 6)
ax3.axis("off")

# Title
ax3.text(7, 5.5, "Structuring AI Workflows for Audit-Ready Evidence",
         ha="center", va="center",
         fontsize=18, fontweight="bold", color=DEEP_NAVY)
ax3.text(7, 5.0, "Every output must be traceable",
         ha="center", va="center",
         fontsize=12, color=OCEAN_TEAL, fontstyle="italic")

# Four workflow steps
steps = [
    ("1. Defined\nInputs",           "GL exports, contracts,\nbank files, recon data",  BRIGHT_TEAL),
    ("2. Transparent\nTransformation", "What was asked?\nWhat data provided?\nWhat output generated?", SEA_GREEN),
    ("3. Human\nReview",              "AI assists.\nHumans approve\nfinal conclusions.",  GOLDEN_YELLOW),
    ("4. Evidence\nRetention",        "Source data +\nprocess + output +\nhuman sign-off", OCEAN_TEAL),
]

box_width = 2.6
box_height = 2.8
y_center = 2.5
x_positions = [1.2, 4.4, 7.6, 10.8]

for i, (title, desc, color) in enumerate(steps):
    x = x_positions[i]

    # Box
    box = FancyBboxPatch(
        (x, y_center - box_height / 2), box_width, box_height,
        boxstyle="round,pad=0.15",
        facecolor=color, edgecolor="none", linewidth=2, zorder=2
    )
    ax3.add_patch(box)

    # Determine text color based on background
    txt_color = text_color_for(color)

    # Title
    ax3.text(x + box_width / 2, y_center + 0.65, title,
             ha="center", va="center",
             fontsize=13, fontweight="bold", color=txt_color,
             linespacing=1.2, zorder=3)

    # Description
    ax3.text(x + box_width / 2, y_center - 0.55, desc,
             ha="center", va="center",
             fontsize=12, color=txt_color, alpha=0.9,
             linespacing=1.3, zorder=3)

    # Arrow between boxes
    if i < 3:
        arrow_x_start = x + box_width + 0.05
        arrow_x_end = x_positions[i + 1] - 0.05
        ax3.annotate("",
                     xy=(arrow_x_end, y_center),
                     xytext=(arrow_x_start, y_center),
                     arrowprops=dict(arrowstyle="-|>", color=GOLDEN_YELLOW,
                                     lw=3, mutation_scale=25),
                     zorder=4)

# Bottom callout
ax3.text(7, 0.45,
         '"How do you know this number is correct?"  —  If you can show all four steps, the result is defensible evidence.',
         ha="center", va="center",
         fontsize=10.5, color=DEEP_NAVY, fontstyle="italic",
         bbox=dict(boxstyle="round,pad=0.45",
                   facecolor="#FFF9EC", edgecolor="none", linewidth=2.0),
         zorder=5)

out_path3 = os.path.join(OUT_DIR, "04_traceable_workflow.png")
plt.savefig(out_path3, dpi=180, bbox_inches="tight")
plt.close()
print(f"[OK] 04_traceable_workflow.png  ->  {OUT_DIR}")
