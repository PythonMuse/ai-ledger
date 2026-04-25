"""
Generate Article 17 visuals — Skills and Agents for Accountants.
Social-media optimized: white backgrounds, large fonts, footer on every visual.

Visual 01: Hero / front image
Visual 02: Skills vs Agents
Visual 03: Bank Reconciliation Before vs After
Visual 04: From SOPs to Living Systems (loop + Git as explicit step)
Visual 05: You Are the Designer (center = "YOU", no role title)

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
    """Return correct text color per SKILL.md contrast rule."""
    return WHITE if bg in DARK_BG_COLORS else DEEP_NAVY


def add_footer(ax, xmax, ymin):
    """Draw a branded footer bar at the bottom of the axes."""
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
ax.text(W/2, 5.5,
        "The Power of Skills and Agents",
        ha="center", va="center",
        fontsize=38, fontweight="bold", color=DEEP_NAVY)

# Subtitle
ax.text(W/2, 4.3,
        "How Accountants Actually Use AI",
        ha="center", va="center",
        fontsize=26, color=OCEAN_TEAL)

# Divider
ax.plot([2.5, W - 2.5], [3.4, 3.4], color=BRIGHT_TEAL, linewidth=3)

# Tagline
ax.text(W/2, 2.6,
        "Stop asking AI.  Start building with it.",
        ha="center", va="center",
        fontsize=20, fontstyle="italic", color=DEEP_NAVY)

# Byline
ax.text(W/2, 1.7, "By Svetlana Toohey",
        ha="center", va="center",
        fontsize=15, color=OCEAN_TEAL)

add_footer(ax, W, 0)
plt.tight_layout(pad=0)
plt.savefig(os.path.join(OUT_DIR, "17_visual_front.png"),
            dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()
print("[OK] 17_visual_front.png")


# ═════════════════════════════════════════════════════════════════════════════
# Visual 02 – Skills vs Agents
# ═════════════════════════════════════════════════════════════════════════════
W, H = 16, 11
fig, ax = plt.subplots(figsize=(W, H))
fig.patch.set_facecolor(WHITE)
ax.set_facecolor(WHITE)
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

# Title
ax.text(W/2, H - 0.6, "Skills vs Agents — Explained for Accountants",
        ha="center", va="center",
        fontsize=28, fontweight="bold", color=DEEP_NAVY)
ax.text(W/2, H - 1.35, "Skills do the work.  Agents control how the work gets done.",
        ha="center", va="center",
        fontsize=18, fontstyle="italic", color=OCEAN_TEAL)

# ── LEFT panel: Skills ────────────────────────────────────────────────────────
# Height reduced to 7.3 (was 8.0) so top border clears subtitle text above
rbox(ax, 0.4, 1.5, 6.8, 7.3, LIGHT_GRAY, ec=BRIGHT_TEAL, lw=3)
ax.text(3.8, 8.4, "SKILLS", ha="center", va="center",
        fontsize=24, fontweight="bold", color=DEEP_NAVY)
ax.text(3.8, 7.85, "Reusable building blocks",
        ha="center", va="center", fontsize=15, color=OCEAN_TEAL, fontstyle="italic")

skill_items = [
    (BRIGHT_TEAL, "Extract bank data"),
    (SEA_GREEN,   "Clean GL records"),
    (OCEAN_TEAL,  "Match transactions"),
    (SOFT_SAGE,   "Format Excel output"),
]
for i, (color, label) in enumerate(skill_items):
    y = 7.1 - i * 1.45
    rbox(ax, 0.9, y - 0.48, 5.8, 0.96, color, ec=DEEP_NAVY, lw=1.5)
    ax.text(3.8, y, label, ha="center", va="center",
            fontsize=17, fontweight="bold", color=text_color_for(color))

ax.text(3.8, 1.75, '"Build it once.  Reuse it everywhere."',
        ha="center", va="center",
        fontsize=16, color=OCEAN_TEAL, fontstyle="italic")

# ── CENTER arrow ──────────────────────────────────────────────────────────────
arrow(ax, 7.4, 5.0, 8.6, 5.0, color=DEEP_NAVY, lw=3)
ax.text(8.0, 5.45, "uses", ha="center", va="center",
        fontsize=13, color=OCEAN_TEAL, fontstyle="italic")

# ── RIGHT panel: Agent ────────────────────────────────────────────────────────
rbox(ax, 8.8, 1.5, 6.8, 7.3, LIGHT_GRAY, ec=GOLDEN_YELLOW, lw=3)
ax.text(12.2, 8.4, "AGENT", ha="center", va="center",
        fontsize=24, fontweight="bold", color=DEEP_NAVY)
ax.text(12.2, 7.85, "The controller of the process",
        ha="center", va="center", fontsize=15, color=OCEAN_TEAL, fontstyle="italic")

# Central badge
rbox(ax, 10.3, 6.4, 3.8, 1.0, OCEAN_TEAL, ec=DEEP_NAVY, lw=2)
ax.text(12.2, 6.9, "CONTROLS THE WORKFLOW",
        ha="center", va="center",
        fontsize=14, fontweight="bold", color=WHITE)

agent_rules = [
    "Selects which skills to run",
    "Enforces rules and boundaries",
    "Never overwrites source files",
    "Logs every action taken",
]
for i, rule in enumerate(agent_rules):
    y = 5.65 - i * 1.1
    ax.plot([9.3, 9.65], [y, y], color=GOLDEN_YELLOW, linewidth=2.5)
    ax.text(9.85, y, rule, ha="left", va="center",
            fontsize=15, color=DEEP_NAVY)

# Quote raised inside panel (was y=1.25 — clipped below panel border)
ax.text(12.2, 1.85, '"Skills do the work.\nAgents control how."',
        ha="center", va="center",
        fontsize=13, color=OCEAN_TEAL, fontstyle="italic", linespacing=1.4)

add_footer(ax, W, 0)
plt.tight_layout(pad=0)
plt.savefig(os.path.join(OUT_DIR, "17_skills_vs_agents.png"),
            dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()
print("[OK] 17_skills_vs_agents.png")


# ═════════════════════════════════════════════════════════════════════════════
# Visual 03 – Bank Reconciliation: Before vs After
# ═════════════════════════════════════════════════════════════════════════════
W, H = 16, 12
fig, ax = plt.subplots(figsize=(W, H))
fig.patch.set_facecolor(WHITE)
ax.set_facecolor(WHITE)
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

# Title
ax.text(W/2, H - 0.55, "Bank Reconciliation: Before vs After",
        ha="center", va="center",
        fontsize=28, fontweight="bold", color=DEEP_NAVY)
ax.text(W/2, H - 1.25, "Same data.  Completely different workflow.",
        ha="center", va="center",
        fontsize=18, fontstyle="italic", color=OCEAN_TEAL)

# Divider — Ocean Teal per SKILL.md "borders and dividers"
ax.plot([W/2, W/2], [0.7, H - 1.6], color=OCEAN_TEAL, lw=2, linestyle="--", alpha=0.5)

# ── LEFT: BEFORE ──────────────────────────────────────────────────────────────
ax.text(3.8, H - 1.85, "BEFORE", ha="center", va="center",
        fontsize=22, fontweight="bold", color=ALERT_RED)

before_steps = [
    "Download PDF statement",
    "Export GL to Excel",
    "Manual PDF → usable format",
    "Match transactions using Excel formulas",
    "Investigate differences",
    "Document manually remaining variances",
]
step_h = 0.82
step_gap = 0.32
top_y = H - 2.7
for i, step in enumerate(before_steps):
    y = top_y - i * (step_h + step_gap)
    rbox(ax, 0.4, y - step_h/2, 6.8, step_h, "#FFF0F0", ec=ALERT_RED, lw=1.5)
    ax.text(3.8, y, step, ha="center", va="center",
            fontsize=15, color=DEEP_NAVY)
    if i < len(before_steps) - 1:
        arrow(ax, 3.8, y - step_h/2 - 0.04,
                  3.8, y - step_h/2 - step_gap + 0.04,
              color=ALERT_RED, lw=2)

# Friction badge — raised to y=1.55 to match check badge on the right
rbox(ax, 0.9, 1.55, 5.8, 0.72, "#FFF0F0", ec=ALERT_RED, lw=2)
ax.text(3.8, 1.91, "errors  ·  rework  ·  inconsistency  ·  time",
        ha="center", va="center", fontsize=13, color=ALERT_RED, fontweight="bold")

# ── RIGHT: AFTER ──────────────────────────────────────────────────────────────
ax.text(12.2, H - 1.85, "AFTER", ha="center", va="center",
        fontsize=22, fontweight="bold", color=SEA_GREEN)

# Harness wrapper — bottom at y=1.3 so rendered border (y≈1.18) clears the footer top (y=0.55)
harness = FancyBboxPatch((8.5, 1.3), 7.0, H - 3.45,
                         boxstyle="round,pad=0.15",
                         facecolor="#F2FAFA", edgecolor=BRIGHT_TEAL,
                         linewidth=2.5, linestyle="--", zorder=1)
ax.add_patch(harness)
ax.text(12.0, H - 2.15,
        "Harness  (VS Code or your approved environment)",
        ha="center", va="center",
        fontsize=13, color=OCEAN_TEAL, fontstyle="italic")

layers = [
    (H - 3.15, 1.05, LIGHT_GRAY,     DEEP_NAVY,    OCEAN_TEAL,
     "INPUT LAYER",    "Bank statement  ·  GL export"),
    (H - 4.85, 1.25, BRIGHT_TEAL,    DEEP_NAVY,    DEEP_NAVY,
     "SKILLS LAYER",   "Extract  ·  Clean  ·  Match  ·  Handle exceptions"),
    (H - 6.65, 1.25, OCEAN_TEAL,     WHITE,        GOLDEN_YELLOW,
     "AGENT LAYER",    "No overwrite  ·  Version control  ·  Approval required"),
    (H - 8.35, 1.0,  SOFT_SAGE,      DEEP_NAVY,    DEEP_NAVY,
     "OUTPUT",         "Clean, versioned Excel file  ·  Audit-ready"),
]
for (ly, lh, fc, title_c, body_c, title, body) in layers:
    rbox(ax, 8.85, ly - lh/2, 6.3, lh, fc, ec=DEEP_NAVY, lw=1.5)
    ax.text(12.0, ly + 0.15, title, ha="center", va="center",
            fontsize=12, fontweight="bold", color=title_c)
    ax.text(12.0, ly - 0.28, body, ha="center", va="center",
            fontsize=13, color=body_c)

# Arrows between layers
for i in range(len(layers) - 1):
    y_top = layers[i][0] - layers[i][1]/2 - 0.05
    y_bot = layers[i+1][0] + layers[i+1][1]/2 + 0.05
    arrow(ax, 12.0, y_top, 12.0, y_bot, color=DEEP_NAVY, lw=2)

# Check badge — sits inside harness with clear space below it and above footer
rbox(ax, 9.2, 1.55, 5.6, 0.65, "#E8F8F0", ec=SEA_GREEN, lw=2)
ax.text(12.0, 1.88, "Consistent  ·  Controlled  ·  Auditable",
        ha="center", va="center", fontsize=13, color=SEA_GREEN, fontweight="bold")

add_footer(ax, W, 0)
plt.tight_layout(pad=0)
plt.savefig(os.path.join(OUT_DIR, "17_bank_rec_before_after.png"),
            dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()
print("[OK] 17_bank_rec_before_after.png")


# ═════════════════════════════════════════════════════════════════════════════
# Visual 04 – From SOPs to Living Systems
# ═════════════════════════════════════════════════════════════════════════════
W, H = 16, 12
fig, ax = plt.subplots(figsize=(W, H))
fig.patch.set_facecolor(WHITE)
ax.set_facecolor(WHITE)
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

ax.text(W/2, H - 0.55, "From SOPs → Living Systems",
        ha="center", va="center",
        fontsize=28, fontweight="bold", color=DEEP_NAVY)
ax.text(W/2, H - 1.3, "Your process improves every time you use it.",
        ha="center", va="center",
        fontsize=18, fontstyle="italic", color=OCEAN_TEAL)

# ── LOOP (left half) ──────────────────────────────────────────────────────────
lcx, lcy, lr = 4.6, 5.6, 3.0

node_labels  = ["Run\nProcess", "Identify\nImprovement",
                "Prompt AI\nto Update Skill", "Review\n& Approve",
                "Save Version\n(Git)", "Repeat"]
node_colors  = [BRIGHT_TEAL, GOLDEN_YELLOW, SEA_GREEN,
                OCEAN_TEAL,  SOFT_SAGE,     WARM_GLOW]
angles_deg   = [90, 30, -30, -90, -150, 150]

positions = [(lcx + lr * np.cos(np.radians(a)),
              lcy + lr * np.sin(np.radians(a))) for a in angles_deg]

# Node radius — defined here so the arrow offset can use it
nr = 0.75

# Arrows between nodes — start/end at circle edges, not centers
for i in range(len(positions)):
    x0, y0 = positions[i]
    x1, y1 = positions[(i + 1) % len(positions)]
    dx, dy = x1 - x0, y1 - y0
    dist = np.sqrt(dx**2 + dy**2)
    ux_a, uy_a = dx / dist, dy / dist
    margin = nr + 0.1
    arrow(ax, x0 + ux_a * margin, y0 + uy_a * margin,
              x1 - ux_a * margin, y1 - uy_a * margin,
          color=OCEAN_TEAL, lw=2.2, style="arc3,rad=0.28")

# Nodes — text_color_for() applied to each
for (nx, ny), label, bg in zip(positions, node_labels, node_colors):
    c = plt.Circle((nx, ny), nr, color=bg, ec=DEEP_NAVY, lw=2, zorder=3)
    ax.add_patch(c)
    ax.text(nx, ny, label, ha="center", va="center",
            fontsize=11, fontweight="bold", color=text_color_for(bg),
            linespacing=1.3, zorder=4)

# Center label
ax.text(lcx, lcy, "Living\nSystem", ha="center", va="center",
        fontsize=16, fontweight="bold", color=DEEP_NAVY, linespacing=1.3)

# ── COMPARISON (right half) ───────────────────────────────────────────────────
# Divider — Ocean Teal per SKILL.md
ax.plot([8.8, 8.8], [0.8, H - 1.65], color=OCEAN_TEAL, lw=2, linestyle="--", alpha=0.5)

# OLD WAY — moved down 0.5 so top border clears subtitle "Your process..." at y=10.7
rbox(ax, 9.0, 7.0, 6.8, 3.0, "#FFF0F0", ec=ALERT_RED, lw=2)
ax.text(12.4, 9.75, "OLD WAY", ha="center", va="center",
        fontsize=18, fontweight="bold", color=ALERT_RED)
old_items = ["SOP written once",
             "Rarely updated",
             "Goes stale quickly",
             "Lives on a shared drive"]
for i, item in enumerate(old_items):
    ax.text(9.45, 9.25 - i * 0.58, f"x  {item}",
            ha="left", va="center", fontsize=14, color=ALERT_RED)

# NEW WAY — moved down 0.5 to stay consistent with Old Way shift
rbox(ax, 9.0, 2.8, 6.8, 3.9, "#E8F8F0", ec=SEA_GREEN, lw=2)
ax.text(12.4, 6.45, "NEW WAY", ha="center", va="center",
        fontsize=18, fontweight="bold", color=SEA_GREEN)
new_items = ["Skills updated continuously",
             "AI assists documentation",
             "Captures real exceptions",
             "Version-controlled (Git)",
             "Every version can be reversed"]
for i, item in enumerate(new_items):
    ax.text(9.45, 5.9 - i * 0.62, f"+  {item}",
            ha="left", va="center", fontsize=14, color=SEA_GREEN)

# Bottom callout — raised to y=0.85 (was 0.75) to clear footer border
rbox(ax, 1.0, 0.85, W - 2.0, 0.82, "#FFF9EC", ec=GOLDEN_YELLOW, lw=2)
ax.text(W/2, 1.26,
        "Version control is the safety net that makes continuous improvement sustainable.",
        ha="center", va="center",
        fontsize=14, fontstyle="italic", color=DEEP_NAVY)

add_footer(ax, W, 0)
plt.tight_layout(pad=0)
plt.savefig(os.path.join(OUT_DIR, "17_living_documentation.png"),
            dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()
print("[OK] 17_living_documentation.png")


# ═════════════════════════════════════════════════════════════════════════════
# Visual 05 – You Are the Designer
# Center badge = "YOU" — applies to all levels
# ═════════════════════════════════════════════════════════════════════════════
W, H = 16, 16
fig, ax = plt.subplots(figsize=(W, H))
fig.patch.set_facecolor(WHITE)
ax.set_facecolor(WHITE)
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

# Title
ax.text(W/2, H - 0.8, "You Are the Designer",
        ha="center", va="center",
        fontsize=34, fontweight="bold", color=DEEP_NAVY)
ax.text(W/2, H - 1.85, "AI builds.  You decide.",
        ha="center", va="center",
        fontsize=22, fontstyle="italic", color=OCEAN_TEAL)

# Center circle
cx, cy, cr = W/2, 8.0, 1.8
center = plt.Circle((cx, cy), cr, color=OCEAN_TEAL, ec="none", zorder=3)
ax.add_patch(center)
ax.text(cx, cy, "YOU", ha="center", va="center",
        fontsize=30, fontweight="bold", color=WHITE, zorder=4)

# Satellites — text_color_for() applied
satellites = [
    ("SKILLS",           "Define what\neach skill does",   90,   BRIGHT_TEAL),
    ("AGENT",            "Set the rules\nit must follow",  30,   GOLDEN_YELLOW),
    ("DATA\nINPUTS",     "Control what\nAI can access",   -30,   SOFT_SAGE),
    ("OUTPUTS",          "Review and\napprove results",   -90,   SEA_GREEN),
    ("VERSION\nCONTROL", "Revert, track\naudit changes",  -150,  WARM_GLOW),
    ("GOVERNANCE",       "Define the\nboundaries",         150,  ALERT_RED),
]

sat_orbit = 3.4
sat_r     = 1.35

for label, anchor, deg, bg in satellites:
    rad = np.radians(deg)
    sx = cx + sat_orbit * np.cos(rad)
    sy = cy + sat_orbit * np.sin(rad)
    ux, uy = np.cos(rad), np.sin(rad)

    # Connector line — Ocean Teal per SKILL.md "borders and dividers"
    ax.plot([cx + ux * (cr + 0.12), sx - ux * (sat_r + 0.12)],
            [cy + uy * (cr + 0.12), sy - uy * (sat_r + 0.12)],
            color=OCEAN_TEAL, lw=2, alpha=0.5, zorder=2)

    # Satellite circle
    sc = plt.Circle((sx, sy), sat_r, color=bg, ec="none", zorder=3)
    ax.add_patch(sc)
    ax.text(sx, sy, label, ha="center", va="center",
            fontsize=14, fontweight="bold", color=text_color_for(bg),
            linespacing=1.3, zorder=4)

    # Anchor text outside satellite — OUTPUTS repositioned below-left of its circle
    # to avoid overlapping with the VERSION CONTROL bubble (which sits at deg=-150)
    if label == "OUTPUTS":
        ox, oy = 4.8, 3.5
        ax.text(ox, oy, anchor, ha="center", va="center",
                fontsize=15, color=DEEP_NAVY, linespacing=1.4, zorder=4)
    else:
        ox = cx + (sat_orbit + sat_r + 0.85) * ux
        oy = cy + (sat_orbit + sat_r + 0.85) * uy
        ax.text(ox, oy, anchor, ha="center", va="center",
                fontsize=15, color=DEEP_NAVY, linespacing=1.4, zorder=4)

# Bottom role box — y=1.05 so rendered bottom (≈0.93) sits clearly above footer top (y=0.55)
rbox(ax, 1.0, 1.05, W - 2.0, 1.53, LIGHT_GRAY, ec="none", lw=0)
ax.text(W/2, 2.30, "Define the process  ·  Set the rules",
        ha="center", va="center",
        fontsize=18, fontweight="bold", color=DEEP_NAVY)
ax.text(W/2, 1.60, "Review the output  ·  You lead — AI executes",
        ha="center", va="center",
        fontsize=18, fontweight="bold", color=DEEP_NAVY)

add_footer(ax, W, 0)
plt.tight_layout(pad=0)
plt.savefig(os.path.join(OUT_DIR, "17_you_are_the_designer.png"),
            dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()
print("[OK] 17_you_are_the_designer.png")

print("\nAll 5 visuals generated successfully.")
