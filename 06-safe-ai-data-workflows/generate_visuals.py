"""
Generate Article 06 visuals — How to Use AI in Accounting Without Sending the Wrong Data.

Visual 01: Data Flow — Local vs Cloud Processing
  Shows how data moves from your computer to AI services and back.

Visual 02: Finance Data Risk Pyramid
  Three tiers: Safest (structure only), Safer (masked), Use Caution (raw).

Visual 03: Safe AI Workflow
  End-to-end flow: QuickBooks Export → Masking → Validation → AI → Output.

Saved to articles/06-safe-ai-data-workflows/visuals/
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
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

FOOTER_TEXT = "PythonMuse LLC  |  github.com/PythonMuse/ai-ledger"

# -- Text contrast helper (SKILL.md mandatory rule 3) -----------------------
DARK_BG_COLORS = {DEEP_NAVY, MIDNIGHT_TEAL, OCEAN_TEAL, SEA_GREEN, ALERT_RED}

def text_color_for(bg):
    """Return correct text color per SKILL.md contrast rule."""
    if bg in DARK_BG_COLORS:
        return WHITE
    return DEEP_NAVY

# ─────────────────────────────────────────────────────────────────────────────
# Visual 01 – Data Flow: Local vs Cloud Processing
# ─────────────────────────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────
fig1, ax1 = plt.subplots(figsize=(12, 8))
fig1.patch.set_facecolor(WHITE)
ax1.set_facecolor(WHITE)
ax1.set_xlim(0, 12)
ax1.set_ylim(0, 8)
ax1.axis("off")

# Title
ax1.text(6, 7.5, "Data Flow: Local vs Cloud Processing",
         ha="center", va="center",
         fontsize=18, fontweight="bold", color=DEEP_NAVY)
ax1.text(6, 7.0, "Understanding where your data goes when using AI tools",
         ha="center", va="center",
         fontsize=14, color=OCEAN_TEAL, fontstyle="italic")

# Left column: Local Processing
local_header = FancyBboxPatch((0.5, 5.2), 4.8, 0.8,
                               boxstyle="round,pad=0.1",
                               facecolor=BRIGHT_TEAL, edgecolor="none",
                               linewidth=2, zorder=2)
ax1.add_patch(local_header)
ax1.text(2.9, 5.6, "Local Processing", ha="center", va="center",
         fontsize=14, fontweight="bold", color=DEEP_NAVY, zorder=3)

local_items = [
    "Python scripts",
    "Data transformations",
    "Masking / preprocessing",
    "Spreadsheet automation",
]
local_box = FancyBboxPatch((0.5, 2.4), 4.8, 2.6,
                            boxstyle="round,pad=0.1",
                            facecolor="#E6F4F1", edgecolor="none",
                            linewidth=1.5, zorder=1)
ax1.add_patch(local_box)
for i, item in enumerate(local_items):
    ax1.text(2.9, 4.5 - i * 0.55, f"  {item}", ha="center", va="center",
             fontsize=12, color=DEEP_NAVY, zorder=3)

ax1.text(2.9, 1.8, "Data stays on your machine",
         ha="center", va="center",
         fontsize=12, fontweight="bold", color=BRIGHT_TEAL,
         bbox=dict(boxstyle="round,pad=0.3", facecolor="#E6F4F1",
                   edgecolor="none", linewidth=1.5))

# Right column: Cloud Processing
cloud_header = FancyBboxPatch((6.7, 5.2), 4.8, 0.8,
                               boxstyle="round,pad=0.1",
                               facecolor=GOLDEN_YELLOW, edgecolor="none",
                               linewidth=2, zorder=2)
ax1.add_patch(cloud_header)
ax1.text(9.1, 5.6, "Cloud Processing", ha="center", va="center",
         fontsize=14, fontweight="bold", color=DEEP_NAVY, zorder=3)

# Flow boxes for cloud
flow_data = [
    ("Your Computer", OCEAN_TEAL, WHITE),
    ("AI Provider Server", GOLDEN_YELLOW, DEEP_NAVY),
    ("Response Returned", OCEAN_TEAL, WHITE),
]
flow_y = [4.6, 3.5, 2.4]
for (label, bg, fg), y in zip(flow_data, flow_y):
    box = FancyBboxPatch((7.1, y - 0.3), 4.0, 0.6,
                          boxstyle="round,pad=0.1",
                          facecolor=bg, edgecolor="none",
                          linewidth=1.5, zorder=2)
    ax1.add_patch(box)
    ax1.text(9.1, y, label, ha="center", va="center",
             fontsize=12, fontweight="bold", color=fg, zorder=3)

# Arrows between flow boxes
for i in range(2):
    ax1.annotate("", xy=(9.1, flow_y[i + 1] + 0.35),
                 xytext=(9.1, flow_y[i] - 0.35),
                 arrowprops=dict(arrowstyle="-|>", color=DEEP_NAVY,
                                 lw=2, mutation_scale=18), zorder=4)

# Arrow labels
ax1.text(9.8, (flow_y[0] + flow_y[1]) / 2, "prompt / context",
         ha="left", va="center", fontsize=12, color=DEEP_NAVY, fontstyle="italic")
ax1.text(9.8, (flow_y[1] + flow_y[2]) / 2, "model response",
         ha="left", va="center", fontsize=12, color=DEEP_NAVY, fontstyle="italic")

ax1.text(9.1, 1.8, "Data leaves your environment",
         ha="center", va="center",
         fontsize=12, fontweight="bold", color=ALERT_RED,
         bbox=dict(boxstyle="round,pad=0.3", facecolor="#FDE8E8",
                   edgecolor="none", linewidth=1.5))

# Center divider
ax1.plot([6.1, 6.1], [1.4, 6.2], color=GRAY_LINE,
         linewidth=1.5, linestyle="--", zorder=0)

# Bottom callout
ax1.text(6, 0.7,
         "Know the difference. Mask sensitive data before it crosses the boundary.",
         ha="center", va="center",
         fontsize=12, color=DEEP_NAVY, fontstyle="italic",
         bbox=dict(boxstyle="round,pad=0.45",
                   facecolor="#FFF9EC", edgecolor="none", linewidth=2.0),
         zorder=5)

fig1.text(0.5, 0.01, FOOTER_TEXT, ha="center", fontsize=8, color=DEEP_NAVY, alpha=0.50)
out_path1 = os.path.join(OUT_DIR, "06_data_flow.png")
plt.savefig(out_path1, dpi=180, bbox_inches="tight")
plt.close()
print(f"[OK] 06_data_flow.png  ->  {OUT_DIR}")

# ─────────────────────────────────────────────────────────────────────────────
# Visual 02 – Finance Data Risk Pyramid
# ─────────────────────────────────────────────────────────────────────────────
fig2, ax2 = plt.subplots(figsize=(10, 8))
fig2.patch.set_facecolor(WHITE)
ax2.set_facecolor(WHITE)
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 8)
ax2.axis("off")

# Title
ax2.text(5, 7.5, "Finance Data Risk Pyramid for AI Usage",
         ha="center", va="center",
         fontsize=18, fontweight="bold", color=DEEP_NAVY)
ax2.text(5, 7.0, "What to share, what to mask, and what to keep internal",
         ha="center", va="center",
         fontsize=14, color=OCEAN_TEAL, fontstyle="italic")

# Three tiers (bottom to top: unsafe, mask, safe)
tiers = [
    {
        "label": "USE CAUTION",
        "subtitle": "Raw Data",
        "items": "SSNs, bank accounts, payroll,\npersonal addresses, contracts",
        "color": ALERT_RED,
        "text_color": WHITE,
        "y": 1.5, "height": 1.6, "x": 1.0, "width": 8.0,
    },
    {
        "label": "SAFER",
        "subtitle": "Mask Before Sharing",
        "items": "Vendor names, invoice numbers,\ntransaction amounts, project IDs",
        "color": GOLDEN_YELLOW,
        "text_color": DEEP_NAVY,
        "y": 3.3, "height": 1.6, "x": 2.0, "width": 6.0,
    },
    {
        "label": "SAFEST",
        "subtitle": "Structure & Metadata Only",
        "items": "Column names, file structure,\nworkflow descriptions, code snippets",
        "color": BRIGHT_TEAL,
        "text_color": DEEP_NAVY,
        "y": 5.1, "height": 1.6, "x": 3.0, "width": 4.0,
    },
]

for tier in tiers:
    box = FancyBboxPatch(
        (tier["x"], tier["y"]), tier["width"], tier["height"],
        boxstyle="round,pad=0.15",
        facecolor=tier["color"], edgecolor="none",
        linewidth=2, zorder=2
    )
    ax2.add_patch(box)

    cx = tier["x"] + tier["width"] / 2
    cy = tier["y"] + tier["height"] / 2

    ax2.text(cx, cy + 0.35, tier["label"],
             ha="center", va="center",
             fontsize=15, fontweight="bold", color=tier["text_color"], zorder=3)
    ax2.text(cx, cy - 0.05, tier["subtitle"],
             ha="center", va="center",
             fontsize=12, color=tier["text_color"], fontstyle="italic",
             alpha=0.9, zorder=3)
    ax2.text(cx, cy - 0.5, tier["items"],
             ha="center", va="center",
             fontsize=12, color=tier["text_color"], alpha=0.85,
             linespacing=1.2, zorder=3)

# Bottom note
ax2.text(5, 0.6,
         "Start at the top. Only move down when the AI truly needs more detail.",
         ha="center", va="center",
         fontsize=12, color=DEEP_NAVY, fontstyle="italic",
         bbox=dict(boxstyle="round,pad=0.4",
                   facecolor="#FFF9EC", edgecolor="none", linewidth=1.5))

fig2.text(0.5, 0.01, FOOTER_TEXT, ha="center", fontsize=8, color=DEEP_NAVY, alpha=0.50)
out_path2 = os.path.join(OUT_DIR, "06_risk_pyramid.png")
plt.savefig(out_path2, dpi=180, bbox_inches="tight")
plt.close()
print(f"[OK] 06_risk_pyramid.png  ->  {OUT_DIR}")

# ─────────────────────────────────────────────────────────────────────────────
# Visual 03 – Safe AI Workflow (end-to-end)
# ─────────────────────────────────────────────────────────────────────────────
fig3, ax3 = plt.subplots(figsize=(12, 8))
fig3.patch.set_facecolor(WHITE)
ax3.set_facecolor(WHITE)
ax3.set_xlim(0, 12)
ax3.set_ylim(0, 8)
ax3.axis("off")

# Title
ax3.text(6, 7.5, "Safe AI Workflow for Accounting Data",
         ha="center", va="center",
         fontsize=18, fontweight="bold", color=DEEP_NAVY)
ax3.text(6, 7.0, "From raw export to AI-assisted output — without exposing sensitive data",
         ha="center", va="center",
         fontsize=14, color=OCEAN_TEAL, fontstyle="italic")

# Vertical flow
steps = [
    ("QuickBooks Export\n(raw financial data)",              ALERT_RED,      WHITE),
    ("Masking Script\n(Python — runs locally)",              GOLDEN_YELLOW,  DEEP_NAVY),
    ("Validation Hook\n(verify data is masked)",             OCEAN_TEAL,     WHITE),
    ("AI Assistant\n(code generation / analysis)",           BRIGHT_TEAL,    DEEP_NAVY),
    ("Automation or Report Output\n(applied to real data)",  SEA_GREEN,      WHITE),
]

box_width = 6.0
box_height = 0.9
cx = 6.0
y_positions = [5.8, 4.6, 3.4, 2.2, 1.0]

for i, ((label, bg, fg), y) in enumerate(zip(steps, y_positions)):
    box = FancyBboxPatch(
        (cx - box_width / 2, y - box_height / 2), box_width, box_height,
        boxstyle="round,pad=0.1",
        facecolor=bg, edgecolor="none",
        linewidth=2, zorder=2
    )
    ax3.add_patch(box)
    ax3.text(cx, y, label, ha="center", va="center",
             fontsize=13, fontweight="bold", color=fg,
             linespacing=1.2, zorder=3)

    # Arrow to next step
    if i < len(steps) - 1:
        ax3.annotate("",
                     xy=(cx, y_positions[i + 1] + box_height / 2 + 0.05),
                     xytext=(cx, y - box_height / 2 - 0.05),
                     arrowprops=dict(arrowstyle="-|>", color=DEEP_NAVY,
                                     lw=2.5, mutation_scale=20),
                     zorder=4)

# Side annotations
annotations = [
    (y_positions[0], "Sensitive data\nstarts here", "right", ALERT_RED),
    (y_positions[2], "Stops unmasked\ndata", "right", OCEAN_TEAL),
    (y_positions[3], "AI never sees\nreal data", "right", BRIGHT_TEAL),
]
for y, text, side, color in annotations:
    ax3.text(cx + box_width / 2 + 0.4, y, text,
             ha="left", va="center",
             fontsize=12, color=color, fontstyle="italic", zorder=3)

fig3.text(0.5, 0.01, FOOTER_TEXT, ha="center", fontsize=8, color=DEEP_NAVY, alpha=0.50)
out_path3 = os.path.join(OUT_DIR, "06_safe_workflow.png")
plt.savefig(out_path3, dpi=180, bbox_inches="tight")
plt.close()
print(f"[OK] 06_safe_workflow.png  ->  {OUT_DIR}")
