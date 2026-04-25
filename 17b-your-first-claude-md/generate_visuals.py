"""
Generate Article 17b visuals — Your First CLAUDE.md.
Social-media optimized: white backgrounds, large fonts, footer on every visual.

Visual 01: Hero / front image
Visual 02: Anatomy of a CLAUDE.md (five sections diagram)
Visual 03: How to Start (five-step guide)
Visual 04: CLAUDE.md as Governance (hub and spoke)

Footer on every visual: PythonMuse LLC  |  github.com/PythonMuse
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
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
ALERT_ORANGE  = "#E07D3B"

LIGHT_GRAY    = "#F5F5F5"

FOOTER_TEXT = "PythonMuse LLC   |   github.com/PythonMuse"

# ── Text contrast helper (SKILL.md mandatory rule) ───────────────────────────
DARK_BG_COLORS = {DEEP_NAVY, MIDNIGHT_TEAL, OCEAN_TEAL, SEA_GREEN, ALERT_RED, ALERT_ORANGE}

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


def arrow(ax, x0, y0, x1, y1, color=DEEP_NAVY, lw=2.2, style="arc3,rad=0"):
    ax.annotate("",
                xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=color,
                                lw=lw, mutation_scale=20,
                                connectionstyle=style),
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
ax.text(W/2, H - 0.5, "PythonMuse  |  AI in Accounting",
        ha="center", va="center", fontsize=14, color=BRIGHT_TEAL)

# Main title
ax.text(W/2, 5.6,
        "Your First CLAUDE.md",
        ha="center", va="center",
        fontsize=38, fontweight="bold", color=DEEP_NAVY)

# Subtitle
ax.text(W/2, 4.4,
        "How Accountants Define the Agent",
        ha="center", va="center",
        fontsize=24, color=OCEAN_TEAL)

# Divider
ax.plot([2.5, W - 2.5], [3.55, 3.55], color=BRIGHT_TEAL, linewidth=3)

# Tagline
ax.text(W/2, 2.75,
        "Set the rules once.  Every session follows them.",
        ha="center", va="center",
        fontsize=19, fontstyle="italic", color=DEEP_NAVY)

# Byline
ax.text(W/2, 1.75, "By Svetlana Toohey",
        ha="center", va="center",
        fontsize=15, color=OCEAN_TEAL)

add_footer(ax, W, 0)
plt.tight_layout(pad=0)
plt.savefig(os.path.join(OUT_DIR, "17b_visual_front.png"),
            dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()
print("[OK] 17b_visual_front.png")


# ═════════════════════════════════════════════════════════════════════════════
# Visual 02 – Anatomy of a CLAUDE.md
# Five sections, vertical stack with explanations
# ═════════════════════════════════════════════════════════════════════════════
W, H = 16, 13
fig, ax = plt.subplots(figsize=(W, H))
fig.patch.set_facecolor(WHITE)
ax.set_facecolor(WHITE)
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

ax.text(W/2, H - 0.6, "Anatomy of a CLAUDE.md",
        ha="center", va="center",
        fontsize=28, fontweight="bold", color=DEEP_NAVY)
ax.text(W/2, H - 1.35, "Five sections that govern how AI behaves in your accounting project.",
        ha="center", va="center",
        fontsize=17, fontstyle="italic", color=OCEAN_TEAL)

sections = [
    (OCEAN_TEAL,    "ROLE",           "What AI is here to do — and what it must not decide on its own."),
    (BRIGHT_TEAL,   "RULES",          "The non-negotiables: data masking, approval gates, no guessing."),
    (GOLDEN_YELLOW, "DATA LOCATIONS", "Where inputs, outputs, scripts, and audit evidence live."),
    (SEA_GREEN,     "SKILLS",         "How to find and run your reusable accounting skill files."),
    (SOFT_SAGE,     "TONE",           "How outputs should read — professional, concise, workpaper-ready."),
]

section_h = 1.45
gap       = 0.22
top_y     = H - 2.1

for i, (color, title, desc) in enumerate(sections):
    y = top_y - i * (section_h + gap)
    tc = text_color_for(color)

    # Section card
    rbox(ax, 0.6, y - section_h, W - 1.2, section_h, color, ec=DEEP_NAVY, lw=1.5)

    # Section number badge
    badge_bg = DEEP_NAVY if tc == WHITE else MIDNIGHT_TEAL
    rbox(ax, 0.8, y - section_h + 0.22, 1.1, section_h - 0.44,
         badge_bg, ec="none", lw=0, r=0.10)
    ax.text(1.35, y - section_h / 2, str(i + 1),
            ha="center", va="center",
            fontsize=20, fontweight="bold", color=WHITE)

    # Title
    ax.text(2.4, y - section_h / 2 + 0.22, title,
            ha="left", va="center",
            fontsize=16, fontweight="bold", color=tc)

    # Description
    ax.text(2.4, y - section_h / 2 - 0.28, desc,
            ha="left", va="center",
            fontsize=13, color=tc)

# Bottom callout
rbox(ax, 0.6, 0.85, W - 1.2, 0.75, LIGHT_GRAY, ec=GOLDEN_YELLOW, lw=2)
ax.text(W/2, 1.22,
        "Plain text. Version-controlled. Readable by anyone who reviews your work.",
        ha="center", va="center",
        fontsize=14, fontstyle="italic", color=DEEP_NAVY)

add_footer(ax, W, 0)
plt.tight_layout(pad=0)
plt.savefig(os.path.join(OUT_DIR, "17b_anatomy.png"),
            dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()
print("[OK] 17b_anatomy.png")


# ═════════════════════════════════════════════════════════════════════════════
# Visual 03 – How to Start: Five Steps
# ═════════════════════════════════════════════════════════════════════════════
W, H = 16, 12
fig, ax = plt.subplots(figsize=(W, H))
fig.patch.set_facecolor(WHITE)
ax.set_facecolor(WHITE)
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

ax.text(W/2, H - 0.6, "How to Start: Five Steps",
        ha="center", va="center",
        fontsize=28, fontweight="bold", color=DEEP_NAVY)
ax.text(W/2, H - 1.35, "You do not write it from scratch — you copy, adapt, and refine.",
        ha="center", va="center",
        fontsize=17, fontstyle="italic", color=OCEAN_TEAL)

steps = [
    (BRIGHT_TEAL,   "1",
     "Copy the template",
     "Start from the PythonMuse workflow kit.\nCreate CLAUDE.md at your project root."),
    (GOLDEN_YELLOW, "2",
     "Adjust the Role section",
     "Make it specific to your workflow.\n\"Monthly close, US GAAP, entity XYZ.\""),
    (OCEAN_TEAL,    "3",
     "Add your 3 non-negotiables",
     "What can never happen in this workflow?\nData masking? No source file edits?"),
    (SEA_GREEN,     "4",
     "Set your data locations",
     "Map raw inputs, processed data,\noutputs, and audit evidence folders."),
    (SOFT_SAGE,     "5",
     "Run one real task",
     "Open the project. Watch Claude read\nthe rules before it does anything."),
]

step_h  = 1.55
gap     = 0.25
top_y   = H - 2.05
left_x  = 0.7
card_w  = W - 1.4

for i, (color, num, title, desc) in enumerate(steps):
    y = top_y - i * (step_h + gap)
    tc = text_color_for(color)

    rbox(ax, left_x, y - step_h, card_w, step_h, color, ec=DEEP_NAVY, lw=1.5)

    # Number circle
    circ = plt.Circle((left_x + 0.85, y - step_h / 2), 0.48,
                       color=DEEP_NAVY, ec="none", zorder=3)
    ax.add_patch(circ)
    ax.text(left_x + 0.85, y - step_h / 2, num,
            ha="center", va="center",
            fontsize=18, fontweight="bold", color=WHITE, zorder=4)

    # Title
    ax.text(left_x + 1.9, y - step_h / 2 + 0.28, title,
            ha="left", va="center",
            fontsize=15, fontweight="bold", color=tc)

    # Description
    ax.text(left_x + 1.9, y - step_h / 2 - 0.32, desc,
            ha="left", va="center",
            fontsize=12, color=tc, linespacing=1.35)

    # Connector arrow between steps
    if i < len(steps) - 1:
        arrow(ax, W / 2, y - step_h - 0.04,
                  W / 2, y - step_h - gap + 0.04,
              color=OCEAN_TEAL, lw=2)

add_footer(ax, W, 0)
plt.tight_layout(pad=0)
plt.savefig(os.path.join(OUT_DIR, "17b_how_to_start.png"),
            dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()
print("[OK] 17b_how_to_start.png")


# ═════════════════════════════════════════════════════════════════════════════
# Visual 04 – CLAUDE.md as Governance Hub
# ═════════════════════════════════════════════════════════════════════════════
W, H = 16, 14
fig, ax = plt.subplots(figsize=(W, H))
fig.patch.set_facecolor(WHITE)
ax.set_facecolor(WHITE)
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

ax.text(W/2, H - 0.8, "CLAUDE.md as Governance",
        ha="center", va="center",
        fontsize=32, fontweight="bold", color=DEEP_NAVY)
ax.text(W/2, H - 1.30, "One file connects rules, skills, and audit evidence.",
        ha="center", va="center",
        fontsize=20, fontstyle="italic", color=OCEAN_TEAL)

# Center hub
cx, cy, cr = W/2, 7.2, 1.9
hub = plt.Circle((cx, cy), cr, color=DEEP_NAVY, ec="none", zorder=3)
ax.add_patch(hub)
ax.text(cx, cy + 0.25, "CLAUDE.md", ha="center", va="center",
        fontsize=18, fontweight="bold", color=WHITE, zorder=4)
ax.text(cx, cy - 0.45, "The Agent", ha="center", va="center",
        fontsize=13, color=BRIGHT_TEAL, fontstyle="italic", zorder=4)

# Spokes: (label, sub-label, angle_deg, color)
spokes = [
    ("RULES",          "Governs every session",       90,   BRIGHT_TEAL),
    ("SKILLS",         "Calls reusable logic",         30,   GOLDEN_YELLOW),
    ("DATA\nBOUNDARIES","Controls what AI can touch",  -30,  SOFT_SAGE),
    ("AUDIT TRAIL",    "Logs what happened",           -90,  SEA_GREEN),
    ("VERSION\nHISTORY","Every change recorded",      -150,  WARM_GLOW),
    ("GOVERNANCE\nDOCS","Reviewable by management",    150,  OCEAN_TEAL),
]

orbit  = 3.8
sat_r  = 1.2

for label, sublabel, deg, color in spokes:
    rad = np.radians(deg)
    sx  = cx + orbit * np.cos(rad)
    sy  = cy + orbit * np.sin(rad)
    ux, uy = np.cos(rad), np.sin(rad)

    # Connector
    ax.plot([cx + ux * (cr + 0.1), sx - ux * (sat_r + 0.1)],
            [cy + uy * (cr + 0.1), sy - uy * (sat_r + 0.1)],
            color=OCEAN_TEAL, lw=1.8, alpha=0.45, zorder=2)

    # Satellite
    sc = plt.Circle((sx, sy), sat_r, color=color, ec="none", zorder=3)
    ax.add_patch(sc)
    ax.text(sx, sy + 0.2, label, ha="center", va="center",
            fontsize=13, fontweight="bold", color=text_color_for(color),
            linespacing=1.3, zorder=4)
    ax.text(sx, sy - 0.42, sublabel, ha="center", va="center",
            fontsize=10, color=text_color_for(color),
            fontstyle="italic", linespacing=1.2, zorder=4)

# Bottom callout
rbox(ax, 1.0, 1.0, W - 2.0, 0.85, LIGHT_GRAY, ec=GOLDEN_YELLOW, lw=2)
ax.text(W/2, 1.42,
        "Readable by auditors.  Updateable by you.  Enforceable every session.",
        ha="center", va="center",
        fontsize=14, fontstyle="italic", color=DEEP_NAVY)

add_footer(ax, W, 0)
plt.tight_layout(pad=0)
plt.savefig(os.path.join(OUT_DIR, "17b_governance.png"),
            dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()
print("[OK] 17b_governance.png")

print("\nAll 4 visuals generated successfully.")
