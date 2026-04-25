"""
Generate Article 07 visuals — AI Governance for Controllers.

Visual 01: Hero / front image
  Branded title card: "AI Governance for Controllers".

Visual 02: Governance Flow Diagram
  Vertical flow from AI Policy down to Evidence & Monitoring (7 steps).

Visual 03: Repository Architecture as Governance Layers
  Horizontal stacked layers showing how each folder serves a governance purpose.

Saved to articles/07-ai-governance-for-controllers/visuals/
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image as PILImage
import numpy as np
import os

# ── Output directory ──────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR    = os.path.join(SCRIPT_DIR, "visuals")
os.makedirs(OUT_DIR, exist_ok=True)

# ── Logo mark ─────────────────────────────────────────────────────────────────
LOGO_DIR         = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", "..", "..", "Presentations", "docs"))
LOGO_SKETCH_TEAL = os.path.join(LOGO_DIR, "01-Sketch-teal.png")

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


def add_logo(ax, logo_path=None, size=80):
    path = logo_path or LOGO_SKETCH_TEAL
    try:
        img = PILImage.open(path)
        img.thumbnail((size, size), PILImage.LANCZOS)
        imagebox = OffsetImage(np.array(img), zoom=1.0)
        imagebox.image.axes = ax
        ab = AnnotationBbox(imagebox, (0.97, 0.03),
                            xycoords="axes fraction", frameon=False,
                            box_alignment=(1.0, 0.0))
        ax.add_artist(ab)
    except Exception:
        pass


# ─────────────────────────────────────────────────────────────────────────────
# Visual 01 – Hero / Front Image
# ─────────────────────────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────
fig1, ax1 = plt.subplots(figsize=(12, 6))
fig1.patch.set_facecolor(WHITE)
ax1.set_facecolor(WHITE)
ax1.set_xlim(0, 12)
ax1.set_ylim(0, 6)
ax1.axis("off")

# Title
ax1.text(6, 3.8, "AI Governance for Controllers",
         ha="center", va="center",
         fontsize=26, fontweight="bold", color=DEEP_NAVY,
         linespacing=1.3)

# Subtitle
ax1.text(6, 2.6, "Turning Policy Into Real Controls\nUsing Claude and VS Code",
         ha="center", va="center",
         fontsize=16, color=OCEAN_TEAL, fontstyle="italic",
         linespacing=1.3)

# Divider line
ax1.plot([3, 9], [1.7, 1.7], color=BRIGHT_TEAL, linewidth=2)

# Byline
ax1.text(6, 1.0, "PythonMuse LLC",
         ha="center", va="center",
         fontsize=12, color=OCEAN_TEAL, alpha=0.7)

add_logo(ax1)
out_path1 = os.path.join(OUT_DIR, "07_visual_front.png")
plt.savefig(out_path1, dpi=180, bbox_inches="tight")
plt.close()
print(f"[OK] 07_visual_front.png  ->  {OUT_DIR}")


# ─────────────────────────────────────────────────────────────────────────────
# Visual 02 – From AI Policy to Operational Controls
# ─────────────────────────────────────────────────────────────────────────────
fig2, ax2 = plt.subplots(figsize=(10, 12))
fig2.patch.set_facecolor(WHITE)
ax2.set_facecolor(WHITE)
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 12)
ax2.axis("off")

# Title
ax2.text(5, 11.5, "From AI Policy to Operational Controls",
         ha="center", va="center",
         fontsize=18, fontweight="bold", color=DEEP_NAVY)
ax2.text(5, 11.0, "The controller's governance framework",
         ha="center", va="center",
         fontsize=14, color=OCEAN_TEAL, fontstyle="italic")

# Seven vertical flow steps
steps = [
    ("AI Policy",             ALERT_RED,       text_color_for(ALERT_RED)),
    ("Use Case Inventory",    GOLDEN_YELLOW,   text_color_for(GOLDEN_YELLOW)),
    ("Risk Assessment",       GOLDEN_YELLOW,   text_color_for(GOLDEN_YELLOW)),
    ("Control Design",        OCEAN_TEAL,      text_color_for(OCEAN_TEAL)),
    ("AI Skills",             BRIGHT_TEAL,     text_color_for(BRIGHT_TEAL)),
    ("AI Agents",             SEA_GREEN,       text_color_for(SEA_GREEN)),
    ("Evidence & Monitoring", SOFT_SAGE,       text_color_for(SOFT_SAGE)),
]

box_width = 6.0
box_height = 0.9
cx = 5.0
# Spread 7 boxes from y=9.8 down to y=2.6
y_positions = [9.8, 8.6, 7.4, 6.2, 5.0, 3.8, 2.6]

for i, ((label, bg, fg), y) in enumerate(zip(steps, y_positions)):
    box = FancyBboxPatch(
        (cx - box_width / 2, y - box_height / 2), box_width, box_height,
        boxstyle="round,pad=0.1",
        facecolor=bg, edgecolor="none",
        linewidth=2, zorder=2
    )
    ax2.add_patch(box)
    ax2.text(cx, y, label, ha="center", va="center",
             fontsize=13, fontweight="bold", color=fg,
             zorder=3)

    # Arrow to next step
    if i < len(steps) - 1:
        ax2.annotate("",
                     xy=(cx, y_positions[i + 1] + box_height / 2 + 0.05),
                     xytext=(cx, y - box_height / 2 - 0.05),
                     arrowprops=dict(arrowstyle="-|>", color=DEEP_NAVY,
                                     lw=2.5, mutation_scale=20),
                     zorder=4)

# Bottom callout
ax2.text(5, 1.4,
         "Policy becomes operational. Controls become enforceable.",
         ha="center", va="center",
         fontsize=11, color=DEEP_NAVY, fontstyle="italic",
         bbox=dict(boxstyle="round,pad=0.45",
                   facecolor="#FFF9EC", edgecolor="none", linewidth=2.0),
         zorder=5)

add_logo(ax2)
out_path2 = os.path.join(OUT_DIR, "07_governance_flow.png")
plt.savefig(out_path2, dpi=180, bbox_inches="tight")
plt.close()
print(f"[OK] 07_governance_flow.png  ->  {OUT_DIR}")


# ─────────────────────────────────────────────────────────────────────────────
# Visual 03 – Controller Governance Repository (layer stack)
# ─────────────────────────────────────────────────────────────────────────────
fig3, ax3 = plt.subplots(figsize=(12, 10))
fig3.patch.set_facecolor(WHITE)
ax3.set_facecolor(WHITE)
ax3.set_xlim(0, 12)
ax3.set_ylim(0, 10)
ax3.axis("off")

# Title
ax3.text(6, 9.5, "Controller Governance Repository",
         ha="center", va="center",
         fontsize=18, fontweight="bold", color=DEEP_NAVY)
ax3.text(6, 9.0, "Each layer serves a governance purpose",
         ha="center", va="center",
         fontsize=14, color=OCEAN_TEAL, fontstyle="italic")

# Seven horizontal stacked layers, bottom to top
# (folder, description, bg_color, text_color)
layers = [
    (".claude/",       "Configuration & Guardrails",    DEEP_NAVY,     text_color_for(DEEP_NAVY)),
    ("evidence/",      "Audit Trail & Outputs",         OCEAN_TEAL,    text_color_for(OCEAN_TEAL)),
    ("agents/",        "Automated Orchestration",       SEA_GREEN,     text_color_for(SEA_GREEN)),
    ("skills/",        "Approved AI Workflows",         BRIGHT_TEAL,   text_color_for(BRIGHT_TEAL)),
    ("assessments/",   "Risk Analysis",                 GOLDEN_YELLOW, text_color_for(GOLDEN_YELLOW)),
    ("inventory/",     "Use Case Register",             WARM_GLOW,     text_color_for(WARM_GLOW)),
    ("docs/",          "Policy & Controls",             SOFT_SAGE,     text_color_for(SOFT_SAGE)),
]

layer_width = 9.0
layer_height = 0.85
layer_x = 1.5                # left edge
layer_gap = 0.15             # vertical gap between layers
bottom_y = 2.0               # starting y for the bottom layer

for i, (folder, desc, bg, fg) in enumerate(layers):
    y = bottom_y + i * (layer_height + layer_gap)

    box = FancyBboxPatch(
        (layer_x, y), layer_width, layer_height,
        boxstyle="round,pad=0.08",
        facecolor=bg, edgecolor="none",
        linewidth=1.5, zorder=2
    )
    ax3.add_patch(box)

    # Folder name on the left
    ax3.text(layer_x + 0.6, y + layer_height / 2, folder,
             ha="left", va="center",
             fontsize=13, fontweight="bold", fontfamily="monospace",
             color=fg, zorder=3)

    # Description on the right
    ax3.text(layer_x + layer_width - 0.6, y + layer_height / 2, desc,
             ha="right", va="center",
             fontsize=12, color=fg, zorder=3)

# Bottom callout
ax3.text(6, 1.0,
         "The repository IS the control system.",
         ha="center", va="center",
         fontsize=12, color=DEEP_NAVY, fontweight="bold", fontstyle="italic",
         bbox=dict(boxstyle="round,pad=0.45",
                   facecolor="#FFF9EC", edgecolor="none", linewidth=2.0),
         zorder=5)

add_logo(ax3)
out_path3 = os.path.join(OUT_DIR, "07_repo_architecture.png")
plt.savefig(out_path3, dpi=180, bbox_inches="tight")
plt.close()
print(f"[OK] 07_repo_architecture.png  ->  {OUT_DIR}")
