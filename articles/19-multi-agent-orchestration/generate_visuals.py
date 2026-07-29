"""
Generate Article 19 visuals — When One Agent Is Not Enough.
Social-media optimized: white backgrounds, large fonts, footer on every visual.

Visual 01: Hero / front image
Visual 02: Orchestration flow — month-end close with named agents
Visual 03: Sequential vs Parallel workflows
Visual 04: Digital Coworker onboarding checklist
Visual 05: One Long Chat vs Orchestrated Workflow (social card)

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
LIGHT_TEAL    = "#E8F8F8"

FOOTER_TEXT = "PythonMuse LLC   |   github.com/PythonMuse"

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


# FancyBboxPatch with boxstyle="round,pad=r" renders OUTSIDE the given (x, y, w, h)
# rectangle by r in every direction (matplotlib expands the box by the pad before
# rounding). GAP must exceed the default r below or arrows visibly poke into boxes.
GAP = 0.13


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
ax.text(W/2, 6.3,
        "When One Agent Is Not Enough",
        ha="center", va="center",
        fontsize=36, fontweight="bold", color=DEEP_NAVY)

# Subtitle
ax.text(W/2, 5.3,
        "Orchestrating AI Workflows in Accounting",
        ha="center", va="center",
        fontsize=24, color=OCEAN_TEAL)

# Divider
ax.plot([2.0, W - 2.0], [4.9, 4.9], color=BRIGHT_TEAL, linewidth=3)

# Three agent boxes at bottom
agent_data = [
    (2.2,  BRIGHT_TEAL,   "GL\nAgent"),
    (5.8,  OCEAN_TEAL,    "Bank Rec\nAgent"),
    (9.4,  SEA_GREEN,     "Variance\nAgent"),
]
for bx, bc, label in agent_data:
    rbox(ax, bx, 1.55, 2.5, 1.35, bc, ec=DEEP_NAVY, lw=2, zorder=3)
    ax.text(bx + 1.25, 2.225, label, ha="center", va="center",
            fontsize=16, fontweight="bold", color=text_color_for(bc), zorder=4)

# Orchestrator above
rbox(ax, 5.0, 3.55, 4.0, 0.92, GOLDEN_YELLOW, ec=DEEP_NAVY, lw=2.5, zorder=3)
ax.text(7.0, 4.01, "ORCHESTRATOR", ha="center", va="center",
        fontsize=17, fontweight="bold", color=DEEP_NAVY, zorder=4)

# Arrows from orchestrator to agents (3.55 = orchestrator bottom, 2.9 = agent top)
for bx in [3.45, 7.0, 10.65]:
    arrow(ax, 7.0, 3.55 - GAP, bx, 2.9 + GAP, color=DEEP_NAVY, lw=2)

add_footer(ax, W, 0)
plt.tight_layout(pad=0)
plt.savefig(os.path.join(OUT_DIR, "19_visual_front.png"),
            dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()
print("[OK] 19_visual_front.png")


# ═════════════════════════════════════════════════════════════════════════════
# Visual 02 – Orchestration Flow: Month-End Close
# ═════════════════════════════════════════════════════════════════════════════
W, H = 16, 14
fig, ax = plt.subplots(figsize=(W, H))
fig.patch.set_facecolor(WHITE)
ax.set_facecolor(WHITE)
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

ax.text(W/2, H - 0.6, "Month-End Close: Orchestrated Workflow",
        ha="center", va="center",
        fontsize=28, fontweight="bold", color=DEEP_NAVY)
ax.text(W/2, H - 1.35, "Each agent has a role. The files hold the memory. You hold the judgment.",
        ha="center", va="center",
        fontsize=17, fontstyle="italic", color=OCEAN_TEAL)

# Orchestrator — top center
rbox(ax, 5.5, 10.5, 5.0, 1.2, GOLDEN_YELLOW, ec=DEEP_NAVY, lw=2.5, zorder=3)
ax.text(8.0, 11.1, "ORCHESTRATOR", ha="center", va="center",
        fontsize=20, fontweight="bold", color=DEEP_NAVY, zorder=4)
ax.text(8.0, 10.7, "Controller  ·  Tracks dependencies  ·  Escalates to human",
        ha="center", va="center", fontsize=12, color=OCEAN_TEAL, zorder=4)

# Column headers for the three subagents
col_xs = [1.5, 6.3, 11.1]
col_colors = [BRIGHT_TEAL, OCEAN_TEAL, SEA_GREEN]
col_labels = ["GL Agent", "Bank Rec Agent", "Variance Agent"]
col_subs   = ["Senior GL Accountant", "Bank Rec Specialist", "FP&A Analyst"]

for cx, cc, cl, cs in zip(col_xs, col_colors, col_labels, col_subs):
    # Arrow from orchestrator (bottom=10.5) to agent header (top=9.8)
    arrow(ax, 8.0, 10.5 - GAP, cx + 2.0, 9.8 + GAP, color=DEEP_NAVY, lw=2)
    rbox(ax, cx, 8.8, 4.0, 1.0, cc, ec=DEEP_NAVY, lw=2, zorder=3)
    ax.text(cx + 2.0, 9.3, cl, ha="center", va="center",
            fontsize=16, fontweight="bold", color=text_color_for(cc), zorder=4)
    ax.text(cx + 2.0, 8.98, cs, ha="center", va="center",
            fontsize=12, color=text_color_for(cc), zorder=4)

# Step cards per column
steps = [
    # GL Agent steps
    ["Reads GL export", "Validates completeness", "Flags anomalies", "Saves gl-validated.xlsx"],
    # Bank Rec Agent steps
    ["Reads bank statement", "Loads gl-validated.xlsx", "Runs match logic", "Saves bank-rec-complete.xlsx"],
    # Variance Agent steps
    ["Reads validated GL", "Reads budget file", "Drafts commentary", "Saves variance-commentary.md"],
]
step_colors = [
    ["#E8F8F8", "#D4F0EE", "#C0E8E6", "#AADEDC"],
    ["#E0EEF4", "#C0DCE8", "#A0CADC", "#80B8D0"],
    ["#E0F4F0", "#C0E8E0", "#A0DCD0", "#80D0C0"],
]
step_borders = [BRIGHT_TEAL, OCEAN_TEAL, SEA_GREEN]

for ci, (cx, steps_col, scols, sborder) in enumerate(
        zip(col_xs, steps, step_colors, step_borders)):
    for si, (step, sc) in enumerate(zip(steps_col, scols)):
        sy = 7.6 - si * 1.55
        rbox(ax, cx, sy - 0.52, 4.0, 1.0, sc, ec=sborder, lw=1.5, zorder=3)
        ax.text(cx + 2.0, sy, step, ha="center", va="center",
                fontsize=13, color=DEEP_NAVY, zorder=4)
        if si < len(steps_col) - 1:
            # current box bottom = sy - 0.52; next box top = (sy - 1.55) + 0.48
            arrow(ax, cx + 2.0, sy - 0.52 - GAP,
                      cx + 2.0, sy - 1.07 + GAP,
                  color=sborder, lw=1.8)

# Human review box at bottom
rbox(ax, 3.0, 0.75, 10.0, 1.1, LIGHT_GRAY, ec=GOLDEN_YELLOW, lw=2.5, zorder=3)
ax.text(8.0, 1.3, "HUMAN REVIEW & APPROVAL",
        ha="center", va="center",
        fontsize=18, fontweight="bold", color=DEEP_NAVY, zorder=4)
ax.text(8.0, 0.95, "Review outputs  ·  Approve or escalate  ·  Sign off",
        ha="center", va="center",
        fontsize=13, color=OCEAN_TEAL, zorder=4)

# Arrows from each agent column bottom (last step bottom = 2.43) to human review (top = 1.85)
for cx in col_xs:
    arrow(ax, cx + 2.0, 2.43 - GAP,
              8.0 + (cx - 6.3) * 0.3, 1.85 + GAP,
          color=DEEP_NAVY, lw=1.8)

add_footer(ax, W, 0)
plt.tight_layout(pad=0)
plt.savefig(os.path.join(OUT_DIR, "19_orchestration_flow.png"),
            dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()
print("[OK] 19_orchestration_flow.png")


# ═════════════════════════════════════════════════════════════════════════════
# Visual 03 – Sequential vs Parallel
# ═════════════════════════════════════════════════════════════════════════════
W, H = 16, 12
fig, ax = plt.subplots(figsize=(W, H))
fig.patch.set_facecolor(WHITE)
ax.set_facecolor(WHITE)
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

ax.text(W/2, H - 0.6, "Sequential vs. Parallel: Know the Difference",
        ha="center", va="center",
        fontsize=27, fontweight="bold", color=DEEP_NAVY)
ax.text(W/2, H - 1.35, "Same agents. Different structure. Completely different efficiency.",
        ha="center", va="center",
        fontsize=17, fontstyle="italic", color=OCEAN_TEAL)

# Divider
ax.plot([W/2, W/2], [0.7, H - 1.7], color=OCEAN_TEAL, lw=2, linestyle="--", alpha=0.5)

# ── LEFT: Sequential ──────────────────────────────────────────────────────────
ax.text(3.8, H - 1.9, "SEQUENTIAL", ha="center", va="center",
        fontsize=22, fontweight="bold", color=OCEAN_TEAL)
ax.text(3.8, H - 2.5, "Each step waits for the previous one",
        ha="center", va="center", fontsize=14, color=OCEAN_TEAL, fontstyle="italic")

seq_steps = [
    (BRIGHT_TEAL, "1  Validate GL Extract"),
    (SEA_GREEN,   "2  Run Bank Reconciliation"),
    (OCEAN_TEAL,  "3  Draft Variance Commentary"),
    (GOLDEN_YELLOW, "4  Human Review & Approval"),
]
top_y = H - 3.4
step_h = 0.88
step_gap = 0.35
for i, (color, label) in enumerate(seq_steps):
    y = top_y - i * (step_h + step_gap)
    rbox(ax, 0.5, y - step_h/2, 6.5, step_h, color, ec=DEEP_NAVY, lw=2, zorder=3)
    ax.text(3.75, y, label, ha="center", va="center",
            fontsize=16, fontweight="bold", color=text_color_for(color), zorder=4)
    if i < len(seq_steps) - 1:
        # current box bottom = y - step_h/2; next box top = y - (step_h + step_gap) + step_h/2
        arrow(ax, 3.75, y - step_h/2 - GAP,
                  3.75, y - step_h - step_gap + step_h/2 + GAP,
              color=OCEAN_TEAL, lw=2.2)

# Key label
rbox(ax, 0.8, 1.2, 6.0, 0.7, "#E0EEF4", ec=OCEAN_TEAL, lw=2, zorder=3)
ax.text(3.8, 1.55, "Dependency chain  ·  Step 2 needs Step 1's output",
        ha="center", va="center", fontsize=12, color=DEEP_NAVY, zorder=4)

# ── RIGHT: Parallel ───────────────────────────────────────────────────────────
ax.text(12.2, H - 1.9, "PARALLEL", ha="center", va="center",
        fontsize=22, fontweight="bold", color=SOFT_SAGE)
ax.text(12.2, H - 2.35, "Independent tasks run at the same time",
        ha="center", va="center", fontsize=14, color=OCEAN_TEAL, fontstyle="italic")

# Trigger box at top
rbox(ax, 8.7, 8.3, 7.0, 0.85, GOLDEN_YELLOW, ec=DEEP_NAVY, lw=2.5, zorder=3)
ax.text(12.2, 8.725, "ORCHESTRATOR: Start close workflow",
        ha="center", va="center",
        fontsize=15, fontweight="bold", color=DEEP_NAVY, zorder=4)

# Three parallel branches
par_data = [
    (8.8,  BRIGHT_TEAL,   "Pull GL\nExport"),
    (10.9, SEA_GREEN,     "Pull Bank\nStatement"),
    (13.0, SOFT_SAGE,     "Pull Budget\nFile"),
]
for bx, bc, bl in par_data:
    # trigger box bottom = 8.3, branch box top = 7.85
    arrow(ax, 12.2, 8.3 - GAP, bx + 0.9, 7.85 + GAP, color=DEEP_NAVY, lw=1.8)
    rbox(ax, bx, 6.85, 1.8, 1.0, bc, ec=DEEP_NAVY, lw=1.8, zorder=3)
    ax.text(bx + 0.9, 7.35, bl, ha="center", va="center",
            fontsize=13, fontweight="bold", color=text_color_for(bc),
            linespacing=1.3, zorder=4)
    # branch box bottom = 6.85, merge box top = 6.40
    arrow(ax, bx + 0.9, 6.85 - GAP, bx + 0.9, 6.40 + GAP, color=DEEP_NAVY, lw=1.8)

# Merge box
rbox(ax, 8.7, 5.55, 7.0, 0.85, MIDNIGHT_TEAL, ec=BRIGHT_TEAL, lw=2.5, zorder=3)
ax.text(12.2, 5.975, "All inputs ready -- begin processing",
        ha="center", va="center",
        fontsize=15, fontweight="bold", color=WHITE, zorder=4)

# Processing steps after merge
proc_steps = [
    (SEA_GREEN,   "Run Reconciliation & Variance"),
    (OCEAN_TEAL,  "Human Review & Approval"),
]
prev_bottom = 5.55  # merge box bottom
for i, (color, label) in enumerate(proc_steps):
    y = 4.66 - i * 1.33
    top, bottom = y + 0.44, y - 0.44
    rbox(ax, 8.7, bottom, 7.0, 0.88, color, ec=DEEP_NAVY, lw=2, zorder=3)
    ax.text(12.2, y, label, ha="center", va="center",
            fontsize=15, fontweight="bold", color=text_color_for(color), zorder=4)
    arrow(ax, 12.2, prev_bottom - GAP, 12.2, top + GAP,
          color=(DEEP_NAVY if i == 0 else OCEAN_TEAL), lw=2)
    prev_bottom = bottom

# Key label
rbox(ax, 9.0, 1.2, 6.4, 0.7, "#E0F4F0", ec=SEA_GREEN, lw=2, zorder=3)
ax.text(12.2, 1.55, "No dependency  ·  All three run simultaneously",
        ha="center", va="center", fontsize=12, color=DEEP_NAVY, zorder=4)

add_footer(ax, W, 0)
plt.tight_layout(pad=0)
plt.savefig(os.path.join(OUT_DIR, "19_sequential_vs_parallel.png"),
            dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()
print("[OK] 19_sequential_vs_parallel.png")


# ═════════════════════════════════════════════════════════════════════════════
# Visual 04 – Digital Coworker Onboarding Checklist
# ═════════════════════════════════════════════════════════════════════════════
W, H = 14, 16
fig, ax = plt.subplots(figsize=(W, H))
fig.patch.set_facecolor(WHITE)
ax.set_facecolor(WHITE)
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

# Title area
rbox(ax, 0, H - 2.0, W, 2.0, DEEP_NAVY, ec="none", r=0, zorder=1)
ax.text(W/2, H - 0.7, "Onboarding Your Digital Coworker",
        ha="center", va="center",
        fontsize=28, fontweight="bold", color=WHITE, zorder=2)
ax.text(W/2, H - 1.45, "Agents need the same things a new hire needs.",
        ha="center", va="center",
        fontsize=17, color=BRIGHT_TEAL, zorder=2)

# Checklist items
checklist = [
    (BRIGHT_TEAL,   "Defined Role",
     "What is this agent responsible for?\nWhat is outside its scope?"),
    (GOLDEN_YELLOW, "Written Instructions",
     "What are the exact steps?\nWhat files should it read? What should it produce?"),
    (SEA_GREEN,     "Access Boundaries",
     "What files can it read?\nWhat can it never overwrite or delete?"),
    (OCEAN_TEAL,    "Examples of Good Work",
     "What does a correct output look like?\nProvide a sample if you have one."),
    (SOFT_SAGE,     "Clear Definition of Done",
     "How does it know the task is complete?\nWhat file does it save and where?"),
    (WARM_GLOW,     "Escalation Rules",
     "When should it stop and ask a human?\nWhat is a judgment call vs. a formula?"),
    (BRIGHT_TEAL,   "A Human Reviewer",
     "Who checks the output before it moves forward?\nReview is not optional."),
]

card_h = 1.55
card_gap = 0.15
top_y = H - 2.3

for i, (color, title, body) in enumerate(checklist):
    y = top_y - i * (card_h + card_gap)
    rbox(ax, 0.5, y - card_h, W - 1.0, card_h, LIGHT_GRAY, ec=color, lw=3, zorder=2)

    # Color tab on left
    rbox(ax, 0.5, y - card_h, 0.55, card_h, color, ec="none", r=0.05, zorder=3)

    # Number badge
    badge = plt.Circle((1.45, y - card_h/2), 0.36, color=color, ec=DEEP_NAVY, lw=2, zorder=4)
    ax.add_patch(badge)
    ax.text(1.45, y - card_h/2, str(i + 1),
            ha="center", va="center",
            fontsize=16, fontweight="bold", color=text_color_for(color), zorder=5)

    # Title
    ax.text(2.1, y - 0.42, title,
            ha="left", va="center",
            fontsize=17, fontweight="bold", color=DEEP_NAVY, zorder=3)

    # Body
    ax.text(2.1, y - 0.98, body,
            ha="left", va="center",
            fontsize=13, color=OCEAN_TEAL, linespacing=1.4, zorder=3)

# Bottom callout
rbox(ax, 0.5, 0.7, W - 1.0, 0.82, "#FFF9EC", ec=GOLDEN_YELLOW, lw=2, zorder=2)
ax.text(W/2, 1.11,
        "If it looks like a new-hire checklist, that is because it is.",
        ha="center", va="center",
        fontsize=15, fontstyle="italic", color=DEEP_NAVY, zorder=3)

add_footer(ax, W, 0)
plt.tight_layout(pad=0)
plt.savefig(os.path.join(OUT_DIR, "19_digital_coworker.png"),
            dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()
print("[OK] 19_digital_coworker.png")

# ═════════════════════════════════════════════════════════════════════════════
# Visual 05 – One Long Chat vs. Orchestrated Workflow (social card)
# ═════════════════════════════════════════════════════════════════════════════
W, H = 16, 10
fig, ax = plt.subplots(figsize=(W, H))
fig.patch.set_facecolor(WHITE)
ax.set_facecolor(WHITE)
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

# Top header bar
rbox(ax, 0, H - 1.1, W, 1.1, DEEP_NAVY, ec="none", r=0, zorder=1)
ax.text(W / 2, H - 0.52,
        "One Long Chat  vs.  Orchestrated Workflow",
        ha="center", va="center",
        fontsize=26, fontweight="bold", color=WHITE, zorder=2)

# Centre divider
ax.plot([W / 2, W / 2], [0.65, H - 1.15],
        color=OCEAN_TEAL, lw=2, linestyle="--", alpha=0.6)

# ── LEFT: One Long Chat ───────────────────────────────────────────────────────
ax.text(3.8, H - 1.65, "ONE LONG CHAT",
        ha="center", va="center",
        fontsize=20, fontweight="bold", color=ALERT_RED)

chat_msgs = [
    (LIGHT_TEAL,   BRIGHT_TEAL, "Here is the full trial balance..."),
    (LIGHT_TEAL,   BRIGHT_TEAL, "And the bank statement..."),
    (LIGHT_TEAL,   BRIGHT_TEAL, "Also the accrual schedule..."),
    ("#FFF0F0",    ALERT_RED,   "Wait, which version are we on?"),
    ("#FFF0F0",    ALERT_RED,   "I thought we agreed not to touch that..."),
    ("#FFF4E5",    ALERT_ORANGE,"Summarizing instead of following process..."),
]
top_y = H - 2.3
msg_h = 0.72
msg_gap = 0.12
for i, (bg, tc, msg) in enumerate(chat_msgs):
    y = top_y - i * (msg_h + msg_gap)
    alpha = 1.0 - i * 0.06
    rbox(ax, 0.4, y - msg_h, 6.8, msg_h, bg, ec=tc, lw=1.5, r=0.08, zorder=3)
    ax.text(3.8, y - msg_h / 2, msg,
            ha="center", va="center",
            fontsize=13, color=tc, alpha=max(alpha, 0.7), zorder=4)

# Label at bottom-left
rbox(ax, 0.4, 1.0, 6.8, 0.78, "#FFF0F0", ec=ALERT_RED, lw=2, zorder=3)
ax.text(3.8, 1.39,
        "Forgets earlier instructions. Drifts. Gets messy.",
        ha="center", va="center",
        fontsize=13, color=ALERT_RED, zorder=4)

# ── RIGHT: Orchestrated Workflow ──────────────────────────────────────────────
ax.text(12.2, H - 1.65, "ORCHESTRATED WORKFLOW",
        ha="center", va="center",
        fontsize=20, fontweight="bold", color=SEA_GREEN)

# Orchestrator box
rbox(ax, 9.1, 7.05, 6.2, 0.9, GOLDEN_YELLOW, ec=DEEP_NAVY, lw=2.5, zorder=3)
ax.text(12.2, 7.5, "ORCHESTRATOR",
        ha="center", va="center",
        fontsize=16, fontweight="bold", color=DEEP_NAVY, zorder=4)

# Three agent boxes
agt_data = [
    (9.1,  BRIGHT_TEAL,  "GL Agent"),
    (11.3, OCEAN_TEAL,   "Bank Rec\nAgent"),
    (13.5, SEA_GREEN,    "Variance\nAgent"),
]
for ax_x, ac, al in agt_data:
    # orchestrator bottom = 7.05, agent box top = 6.25
    arrow(ax, 12.2, 7.05 - GAP, ax_x + 1.0, 6.25 + GAP, color=DEEP_NAVY, lw=1.8)
    rbox(ax, ax_x, 5.35, 2.0, 0.9, ac, ec=DEEP_NAVY, lw=1.8, zorder=3)
    ax.text(ax_x + 1.0, 5.8, al,
            ha="center", va="center",
            fontsize=13, fontweight="bold", color=text_color_for(ac),
            linespacing=1.3, zorder=4)

# File outputs
file_items = [
    (9.1,  "gl-validated.xlsx"),
    (11.3, "bank-rec-complete.xlsx"),
    (13.5, "variance-commentary.md"),
]
for fx, fn in file_items:
    # agent box bottom = 5.35, file box top = 4.60
    arrow(ax, fx + 1.0, 5.35 - GAP, fx + 1.0, 4.60 + GAP, color=OCEAN_TEAL, lw=1.6)
    rbox(ax, fx, 3.75, 2.0, 0.85, LIGHT_GRAY, ec=OCEAN_TEAL, lw=1.5, r=0.06, zorder=3)
    ax.text(fx + 1.0, 4.175, fn,
            ha="center", va="center",
            fontsize=11, color=DEEP_NAVY, zorder=4)

# Human review box
rbox(ax, 9.3, 2.45, 5.8, 0.9, LIGHT_GRAY, ec=GOLDEN_YELLOW, lw=2.5, zorder=3)
ax.text(12.2, 2.9, "HUMAN REVIEW & APPROVAL",
        ha="center", va="center",
        fontsize=14, fontweight="bold", color=DEEP_NAVY, zorder=4)
# file box bottom = 3.75, human review box top = 3.35
arrow(ax, 12.2, 3.75 - GAP, 12.2, 3.35 + GAP, color=DEEP_NAVY, lw=1.8)

# Label at bottom-right
rbox(ax, 9.1, 1.0, 6.3, 0.78, LIGHT_TEAL, ec=SEA_GREEN, lw=2, zorder=3)
ax.text(12.2, 1.39,
        "Structure holds the memory. Agents stay focused.",
        ha="center", va="center",
        fontsize=13, color=SEA_GREEN, zorder=4)

# ── Centre pull-quote ─────────────────────────────────────────────────────────
ax.text(W / 2, 0.38,
        "The context window is the AI's working memory.  Orchestration is the workflow's memory.",
        ha="center", va="center",
        fontsize=11, fontstyle="italic", color=OCEAN_TEAL, zorder=5)

add_footer(ax, W, -0.02)
plt.tight_layout(pad=0)
plt.savefig(os.path.join(OUT_DIR, "19_one_chat_vs_orchestrated.png"),
            dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()
print("[OK] 19_one_chat_vs_orchestrated.png")


print("\nAll 5 visuals generated successfully.")
