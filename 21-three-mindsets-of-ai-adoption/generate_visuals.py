"""
Generate Article 21 visuals — The 3 Mindsets of AI Adoption in Accounting.
Social-media optimized: white backgrounds, large fonts, footer on every visual.

Visual 01: Hero / front image
Visual 02: Mindset Overview — 3-column card layout (Builder / Stabilizer / Protector)
Visual 03: Progression Arc — Experiment → Standardize → Govern

Footer on every visual: PythonMuse LLC  |  github.com/PythonMuse

NOTE: Quiz handout and workflow comparison handout are generated separately.
      See plan.md for copy instructions from the Presentations repo.
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

# ── Brand colors (SKILL.md standard block) ───────────────────────────────────
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
LIGHT_GRAY    = "#F5F5F5"

FOOTER_TEXT = "PythonMuse LLC   |   github.com/PythonMuse"

# ── Helpers ───────────────────────────────────────────────────────────────────
DARK_BG_COLORS = {DEEP_NAVY, MIDNIGHT_TEAL, OCEAN_TEAL, SEA_GREEN, ALERT_RED}


def text_color_for(bg):
    return WHITE if bg in DARK_BG_COLORS else DEEP_NAVY


def add_footer(ax, xmax, ymin):
    bar = FancyBboxPatch((0, ymin), xmax, 0.55,
                         boxstyle="square,pad=0",
                         facecolor=DEEP_NAVY, edgecolor="none", zorder=10)
    ax.add_patch(bar)
    ax.text(xmax / 2, ymin + 0.275, FOOTER_TEXT,
            ha="center", va="center",
            fontsize=13, color=WHITE, zorder=11)


def rbox(ax, x, y, w, h, fc, ec=DEEP_NAVY, lw=2, r=0.12, zorder=2):
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle=f"round,pad={r}",
                       facecolor=fc, edgecolor=ec,
                       linewidth=lw, zorder=zorder)
    ax.add_patch(p)
    return p


def arrow(ax, x0, y0, x1, y1, color=DEEP_NAVY, lw=2.2):
    ax.annotate("",
                xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=color,
                                lw=lw, mutation_scale=22),
                zorder=5)


# ═════════════════════════════════════════════════════════════════════════════
# Visual 01 – Hero
# ═════════════════════════════════════════════════════════════════════════════
W, H = 14, 8
fig, ax = plt.subplots(figsize=(W, H))
fig.patch.set_facecolor(WHITE)
ax.set_facecolor(WHITE)
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

# Top accent bar
rbox(ax, 0, H - 1.0, W, 1.0, DEEP_NAVY, ec="none", r=0, zorder=1)
ax.text(W / 2, H - 0.5, "PythonMuse  |  AI in Accounting",
        ha="center", va="center", fontsize=14, color=BRIGHT_TEAL)

# Three colored chips (Builder / Stabilizer / Protector)
chip_w, chip_h, chip_y = 2.8, 0.55, 6.0
chip_cx = [3.2, 7.0, 10.8]
chip_colors = [BRIGHT_TEAL, GOLDEN_YELLOW, ALERT_RED]
chip_labels = ["Builder", "Stabilizer", "Protector"]
for cx, cc, cl in zip(chip_cx, chip_colors, chip_labels):
    rbox(ax, cx - chip_w / 2, chip_y, chip_w, chip_h, cc, ec="none", r=0.10, zorder=2)
    ax.text(cx, chip_y + chip_h / 2, cl,
            ha="center", va="center",
            fontsize=15, fontweight="bold", color=text_color_for(cc), zorder=3)

# Divider
ax.plot([2.0, W - 2.0], [5.4, 5.4], color=BRIGHT_TEAL, linewidth=2.5)

# Main title
ax.text(W / 2, 4.5,
        "The 3 Mindsets of AI Adoption\nin Accounting",
        ha="center", va="center",
        fontsize=30, fontweight="bold", color=DEEP_NAVY, linespacing=1.35)

# Subtitle
ax.text(W / 2, 2.7,
        "And Why Tools Aren't the Problem",
        ha="center", va="center",
        fontsize=20, fontstyle="italic", color=OCEAN_TEAL)

# Byline
ax.text(W / 2, 1.8, "By Svetlana Toohey",
        ha="center", va="center",
        fontsize=15, color=OCEAN_TEAL)

add_footer(ax, W, 0)
plt.tight_layout(pad=0)
plt.savefig(os.path.join(OUT_DIR, "21_visual_front.png"),
            dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()
print("[OK] 21_visual_front.png")


# ═════════════════════════════════════════════════════════════════════════════
# Visual 02 – Mindset Overview (3-column cards)
# ═════════════════════════════════════════════════════════════════════════════
W, H = 16, 11
fig, ax = plt.subplots(figsize=(W, H))
fig.patch.set_facecolor(WHITE)
ax.set_facecolor(WHITE)
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

# Title
ax.text(W / 2, H - 0.6,
        "The 3 Mindsets — At a Glance",
        ha="center", va="center",
        fontsize=26, fontweight="bold", color=DEEP_NAVY)
ax.text(W / 2, H - 1.35,
        "Same tools.  Different starting points.  One destination.",
        ha="center", va="center",
        fontsize=16, fontstyle="italic", color=OCEAN_TEAL)

MAR = 0.50
GAP = 0.28
COL_W = (W - MAR * 2 - GAP * 2) / 3
COL_TOP = H - 1.75
FOOTER_H = 0.55
TAKE_H = 0.75
COL_H = COL_TOP - FOOTER_H - TAKE_H - 0.20

mindsets = [
    {
        "label": "Builder",
        "tagline": '"Let me try this"',
        "accent": BRIGHT_TEAL,
        "icon": "\u26A1",
        "need": "Needs: Structure",
        "pain": [
            "Builds things that are hard to repeat",
            "Experiments without documenting",
            "Gets great results once",
        ],
        "upside": "Becomes the person who scales solutions",
        "shift": "One-time prompt  \u2192  Reusable skill",
    },
    {
        "label": "Stabilizer",
        "tagline": '"This works fine today"',
        "accent": GOLDEN_YELLOW,
        "icon": "\u2606",
        "need": "Needs: Proof",
        "pain": [
            "Feels AI is too abstract",
            "Wants to see before trying",
            "Needs reliability first",
        ],
        "upside": "Becomes the bridge between old and new workflows",
        "shift": "Watching others  \u2192  Running first workflow",
    },
    {
        "label": "Protector",
        "tagline": '"This feels risky"',
        "accent": ALERT_RED,
        "icon": "\u2666",
        "need": "Needs: Control",
        "pain": [
            "Worried about data accuracy",
            "Concerned about sensitive data",
            "Focused on audit defensibility",
        ],
        "upside": "Becomes the person who makes AI safe to use",
        "shift": "Blocking AI  \u2192  Designing safe AI",
    },
]

for i, ms in enumerate(mindsets):
    cx = MAR + i * (COL_W + GAP)
    cy = COL_TOP - COL_H
    accent = ms["accent"]
    txt_c = text_color_for(accent)

    # Card background
    rbox(ax, cx, cy, COL_W, COL_H, LIGHT_GRAY, ec=accent, lw=2.5, r=0.10, zorder=1)

    # Header bar
    rbox(ax, cx + 0.08, COL_TOP - 0.72, COL_W - 0.16, 0.64, accent, ec="none", r=0.08, zorder=2)
    ax.text(cx + COL_W / 2, COL_TOP - 0.24,
            f"{ms['icon']}  {ms['label']}",
            ha="center", va="center",
            fontsize=16, fontweight="bold", color=txt_c, zorder=5)
    ax.text(cx + COL_W / 2, COL_TOP - 0.55,
            ms["tagline"],
            ha="center", va="center",
            fontsize=10, fontstyle="italic", color=txt_c, zorder=5)

    # Need badge
    rbox(ax, cx + 0.20, COL_TOP - 1.10, COL_W - 0.40, 0.36,
         OCEAN_TEAL, ec="none", r=0.06, zorder=2)
    ax.text(cx + COL_W / 2, COL_TOP - 0.92,
            ms["need"],
            ha="center", va="center",
            fontsize=12, fontweight="bold", color=WHITE, zorder=5)

    # Pain points
    ax.text(cx + 0.22, COL_TOP - 1.28, "Pain points:", fontsize=10, color=OCEAN_TEAL,
            fontweight="bold", zorder=5)
    py = COL_TOP - 1.52
    for item in ms["pain"]:
        ax.text(cx + 0.22, py, f"\u2022  {item}", fontsize=10, color=DEEP_NAVY,
                zorder=5, va="top")
        py -= 0.32

    # Divider
    ax.plot([cx + 0.20, cx + COL_W - 0.20], [py + 0.18, py + 0.18],
            color=accent, linewidth=1.5, zorder=3)

    # Upside
    ax.text(cx + 0.22, py + 0.06, "Hidden upside:", fontsize=10, color=OCEAN_TEAL,
            fontweight="bold", zorder=5)
    ax.text(cx + 0.22, py - 0.20, ms["upside"], fontsize=10, color=DEEP_NAVY,
            fontstyle="italic", zorder=5)

    # Shift
    py2 = py - 0.58
    rbox(ax, cx + 0.14, py2 - 0.08, COL_W - 0.28, 0.40,
         "#F0FAF9", ec=accent, lw=1.5, r=0.06, zorder=2)
    ax.text(cx + COL_W / 2, py2 + 0.12,
            ms["shift"],
            ha="center", va="center",
            fontsize=9, color=DEEP_NAVY, zorder=5)

# Bottom takeaway strip
TAKE_Y = COL_TOP - COL_H - 0.14 - TAKE_H
rbox(ax, MAR, TAKE_Y, W - MAR * 2, TAKE_H, LIGHT_GRAY, ec="none", lw=0, r=0.08, zorder=1)
ax.text(W / 2, TAKE_Y + TAKE_H - 0.20,
        "The goal is not to pick one mindset.  It is to move through all three.",
        ha="center", va="center",
        fontsize=14, fontweight="bold", color=DEEP_NAVY, zorder=5)
ax.text(W / 2, TAKE_Y + 0.22,
        "Experiment  \u2192  Standardize  \u2192  Govern",
        ha="center", va="center",
        fontsize=13, fontstyle="italic", color=OCEAN_TEAL, zorder=5)

add_footer(ax, W, 0)
plt.tight_layout(pad=0)
plt.savefig(os.path.join(OUT_DIR, "21_mindset_overview.png"),
            dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()
print("[OK] 21_mindset_overview.png")


# ═════════════════════════════════════════════════════════════════════════════
# Visual 03 – Progression Arc: Experiment → Standardize → Govern
# ═════════════════════════════════════════════════════════════════════════════
W, H = 16, 9
fig, ax = plt.subplots(figsize=(W, H))
fig.patch.set_facecolor(WHITE)
ax.set_facecolor(WHITE)
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

# Title
ax.text(W / 2, H - 0.65,
        "The Mindset Progression",
        ha="center", va="center",
        fontsize=28, fontweight="bold", color=DEEP_NAVY)
ax.text(W / 2, H - 1.40,
        "The goal is not to pick one.  It is to move through them.",
        ha="center", va="center",
        fontsize=16, fontstyle="italic", color=OCEAN_TEAL)

# Three stage nodes
stages = [
    {
        "x": 2.8, "y": 5.5,
        "color": BRIGHT_TEAL,
        "icon": "\U0001F7E2",
        "phase": "Experiment",
        "mindset": "Builder",
        "tagline": '"Let me try this"',
        "desc": "Explore what AI can do\non your actual data.\nBuild confidence\nthrough real results.",
    },
    {
        "x": 8.0, "y": 5.5,
        "color": GOLDEN_YELLOW,
        "icon": "\U0001F7E1",
        "phase": "Standardize",
        "mindset": "Stabilizer",
        "tagline": '"This works fine today"',
        "desc": "Take what worked and\nmake it repeatable.\nStop recreating from\nscratch each time.",
    },
    {
        "x": 13.2, "y": 5.5,
        "color": ALERT_RED,
        "icon": "\U0001F534",
        "phase": "Govern",
        "mindset": "Protector",
        "tagline": '"This feels risky"',
        "desc": "Define the boundaries.\nDocument the rules.\nMake the workflow\nsafe for production.",
    },
]

NODE_R = 1.30

# Draw arrows between nodes
arrow_gap = NODE_R + 0.15
for i in range(len(stages) - 1):
    x0 = stages[i]["x"] + arrow_gap
    x1 = stages[i + 1]["x"] - arrow_gap
    mid_x = (x0 + x1) / 2
    y = stages[i]["y"]
    ax.annotate("",
                xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle="-|>", color=OCEAN_TEAL,
                                lw=3.0, mutation_scale=28),
                zorder=4)

for s in stages:
    cx, cy, color = s["x"], s["y"], s["color"]
    txt_c = text_color_for(color)

    # Node circle
    circle = plt.Circle((cx, cy), NODE_R, color=color, ec=DEEP_NAVY, lw=2.5, zorder=3)
    ax.add_patch(circle)

    # Icon
    ax.text(cx, cy + 0.52, s["icon"],
            ha="center", va="center", fontsize=22, zorder=5)

    # Phase label
    ax.text(cx, cy + 0.10,
            s["phase"],
            ha="center", va="center",
            fontsize=17, fontweight="bold", color=txt_c, zorder=5)

    # Mindset label
    ax.text(cx, cy - 0.38,
            s["mindset"],
            ha="center", va="center",
            fontsize=12, fontstyle="italic", color=txt_c, zorder=5)

    # Tagline below node
    ax.text(cx, cy - NODE_R - 0.25,
            s["tagline"],
            ha="center", va="top",
            fontsize=11, fontstyle="italic", color=OCEAN_TEAL, zorder=5)

    # Description card below
    desc_y = cy - NODE_R - 0.55
    card_h = 1.50
    rbox(ax, cx - 1.65, desc_y - card_h, 3.30, card_h,
         LIGHT_GRAY, ec=color, lw=1.5, r=0.10, zorder=2)
    ax.text(cx, desc_y - card_h / 2,
            s["desc"],
            ha="center", va="center",
            fontsize=11, color=DEEP_NAVY, linespacing=1.45, zorder=5)

# Bottom callout
CALL_Y = 0.72
rbox(ax, 1.0, CALL_Y, W - 2.0, 0.72, "#F0FAF9", ec=BRIGHT_TEAL, lw=2, r=0.08, zorder=1)
ax.text(W / 2, CALL_Y + 0.36,
        "Each phase builds on the last.  You do not leave a mindset behind -- you add to it.",
        ha="center", va="center",
        fontsize=13, fontstyle="italic", color=DEEP_NAVY, zorder=5)

add_footer(ax, W, 0)
plt.tight_layout(pad=0)
plt.savefig(os.path.join(OUT_DIR, "21_progression.png"),
            dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()
print("[OK] 21_progression.png")

print("\nAll 3 article visuals generated successfully.")
print("\nNOTE: Quiz handout and workflow comparison handout must be copied separately.")
print("See plan.md for instructions.")
