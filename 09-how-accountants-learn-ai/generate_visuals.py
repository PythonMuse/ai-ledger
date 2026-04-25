"""
Generate Article 09 visuals — How Accountants Learn AI.

Visual 01: Hero / front image
Visual 02: Training Gap (bar chart)
Visual 03: Learning Path (Excel vs AI)
Visual 04: The 13-Skill Framework Grid

Saved to articles/09-how-accountants-learn-ai/visuals/
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
GRAY_LINE     = "#CCCCCC"

# -- Text contrast helper (SKILL.md mandatory rule 3) -----------------------
DARK_BG_COLORS = {DEEP_NAVY, MIDNIGHT_TEAL, OCEAN_TEAL, SEA_GREEN}

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

ax1.text(6, 3.8, "How Accountants Learn AI",
         ha="center", va="center",
         fontsize=28, fontweight="bold", color=DEEP_NAVY,
         linespacing=1.3)

ax1.text(6, 2.6, "From Excel Shortcuts to AI Workflows",
         ha="center", va="center",
         fontsize=16, color=OCEAN_TEAL, style="italic")

ax1.text(6, 1.4, "PythonMuse LLC  |  github.com/PythonMuse/ai-ledger",
         ha="center", va="center",
         fontsize=12, color=OCEAN_TEAL, alpha=0.7)

ax1.plot([3, 9], [1.9, 1.9], color=BRIGHT_TEAL, linewidth=2)

fig1.savefig(os.path.join(OUT_DIR, "09_visual_front.png"),
             dpi=180, bbox_inches="tight", facecolor=fig1.get_facecolor())
plt.close(fig1)
print("  Saved 09_visual_front.png")

# ---------------------------------------------------------------------------
# Visual 02 -- Training Gap Bar Chart
# ---------------------------------------------------------------------------
fig2, ax2 = plt.subplots(figsize=(10, 6))
fig2.patch.set_facecolor(WHITE)
ax2.set_facecolor(WHITE)

categories = ["Excel Courses", "AI Courses\n(General)", "AI for\nAccounting"]
values = [4250, 2750, 150]
colors = [OCEAN_TEAL, SEA_GREEN, GOLDEN_YELLOW]

bars = ax2.bar(categories, values, color=colors, width=0.55, edgecolor="none")

for bar, val in zip(bars, values):
    label = f"~{val:,}" if val > 200 else f"<{val}"
    ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 100,
             label, ha="center", va="bottom",
             fontsize=14, fontweight="bold", color=DEEP_NAVY)

ax2.set_ylabel("Estimated Courses Available (U.S., Early 2026)", fontsize=12, color=DEEP_NAVY)
ax2.set_title("The AI Training Gap for Accountants",
              fontsize=18, fontweight="bold", color=DEEP_NAVY, pad=15)
ax2.set_ylim(0, 5500)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.spines["left"].set_color(GRAY_LINE)
ax2.spines["bottom"].set_color(GRAY_LINE)
ax2.tick_params(colors=DEEP_NAVY, labelsize=12)

ax2.annotate("AI training exists.\nBut almost none of it\nis built for accounting.",
             xy=(2, 150), xytext=(2.3, 3200),
             fontsize=12, color=ALERT_RED, fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=ALERT_RED, lw=1.5),
             ha="center")

fig2.savefig(os.path.join(OUT_DIR, "09_training_gap.png"),
             dpi=180, bbox_inches="tight")
plt.close(fig2)
print("  Saved 09_training_gap.png")

# ---------------------------------------------------------------------------
# Visual 03 -- Excel Learning Path vs AI Learning Path
# ---------------------------------------------------------------------------
fig3, (ax3a, ax3b) = plt.subplots(1, 2, figsize=(14, 6))
fig3.patch.set_facecolor(WHITE)

# Excel path (structured)
ax3a.set_facecolor(WHITE)
ax3a.set_xlim(0, 10)
ax3a.set_ylim(0, 10)
ax3a.axis("off")
ax3a.set_title("Excel Learning Path", fontsize=14, fontweight="bold",
               color=DEEP_NAVY, pad=10)

excel_levels = [
    (5, 8.5, "Expert", "VBA, automation", GOLDEN_YELLOW),
    (5, 6.8, "Advanced", "Power Query, dashboards", BRIGHT_TEAL),
    (5, 5.1, "Intermediate", "Lookups, pivot tables", SEA_GREEN),
    (5, 3.4, "Beginner", "Formulas, basic functions", SOFT_SAGE),
]

for x, y, level, desc, color in excel_levels:
    tc = text_color_for(color)
    box = FancyBboxPatch((1.5, y - 0.6), 7, 1.2,
                         boxstyle="round,pad=0.15",
                         facecolor=color, edgecolor="none", alpha=0.9)
    ax3a.add_patch(box)
    ax3a.text(x, y + 0.15, level, ha="center", va="center",
              fontsize=13, fontweight="bold", color=tc)
    ax3a.text(x, y - 0.25, desc, ha="center", va="center",
              fontsize=12, color=tc, alpha=0.8)

for i in range(len(excel_levels) - 1):
    y_from = excel_levels[i + 1][1] + 0.6
    y_to = excel_levels[i][1] - 0.6
    ax3a.annotate("", xy=(5, y_to), xytext=(5, y_from),
                  arrowprops=dict(arrowstyle="->", color=OCEAN_TEAL, lw=1.5))

ax3a.text(5, 1.5, "Clear path. Clear expectations.",
          ha="center", va="center",
          fontsize=12, color=OCEAN_TEAL, style="italic")

# AI path (fragmented)
ax3b.set_facecolor(WHITE)
ax3b.set_xlim(0, 10)
ax3b.set_ylim(0, 10)
ax3b.axis("off")
ax3b.set_title("AI Learning Path (Today)", fontsize=14, fontweight="bold",
               color=ALERT_RED, pad=10)

ai_items = [
    (2, 8, '"What is ChatGPT?"'),
    (7, 7, '"Write better prompts"'),
    (4, 5.5, '"Build an app"'),
    (8, 4, '"Use this API"'),
    (2, 3.5, '"Try this tool"'),
    (6, 2, '"AI for business"'),
]

for x, y, text in ai_items:
    box = FancyBboxPatch((x - 2, y - 0.5), 4, 1,
                         boxstyle="round,pad=0.1",
                         facecolor=LIGHT_GRAY, edgecolor="none",
                         alpha=0.9)
    ax3b.add_patch(box)
    ax3b.text(x, y, text, ha="center", va="center",
              fontsize=12, color=DEEP_NAVY, style="italic")

ax3b.text(5, 0.8, "Disconnected from real accounting work.",
          ha="center", va="center",
          fontsize=12, color=ALERT_RED, style="italic")

fig3.suptitle("The Gap: Structured vs Fragmented Learning",
              fontsize=18, fontweight="bold", color=DEEP_NAVY, y=1.02)
fig3.savefig(os.path.join(OUT_DIR, "09_learning_path.png"),
             dpi=180, bbox_inches="tight", facecolor=fig3.get_facecolor())
plt.close(fig3)
print("  Saved 09_learning_path.png")

# ---------------------------------------------------------------------------
# Visual 04 -- The 13-Skill Framework Grid
# ---------------------------------------------------------------------------
fig4, ax4 = plt.subplots(figsize=(14, 8))
fig4.patch.set_facecolor(WHITE)
ax4.set_facecolor(WHITE)
ax4.set_xlim(0, 14)
ax4.set_ylim(0, 10)
ax4.axis("off")

ax4.text(7, 9.5, "The AI Accounting Framework",
         ha="center", va="center",
         fontsize=20, fontweight="bold", color=DEEP_NAVY)
ax4.text(7, 8.9, "13 Skills for Accountants Learning AI",
         ha="center", va="center",
         fontsize=14, color=OCEAN_TEAL, style="italic")

skills = [
    ("01", "Working\nWith AI", OCEAN_TEAL, 1.5, 7),
    ("02", "Markdown", OCEAN_TEAL, 4.5, 7),
    ("03", "Python", OCEAN_TEAL, 7.5, 7),
    ("04", "VS Code", OCEAN_TEAL, 10.5, 7),
    ("05", "AI\nPermissions", SEA_GREEN, 1.5, 5),
    ("06", "Hooks as\nControls", SEA_GREEN, 4.5, 5),
    ("07", "Canary\nConcept", SEA_GREEN, 7.5, 5),
    ("08", "Project\nHygiene", SEA_GREEN, 10.5, 5),
    ("09", "Data\nStructure", BRIGHT_TEAL, 1.5, 3),
    ("10", "Excel\nvs CSV", BRIGHT_TEAL, 4.5, 3),
    ("11", "Git for\nAccountants", BRIGHT_TEAL, 7.5, 3),
    ("12", "SQL\nAccess", BRIGHT_TEAL, 10.5, 3),
    ("13", "Skills, Agents\n& Models", GOLDEN_YELLOW, 6, 1),
]

for num, label, color, x, y in skills:
    tc = text_color_for(color)
    w = 2.5 if num != "13" else 3
    box = FancyBboxPatch((x - w / 2, y - 0.75), w, 1.5,
                         boxstyle="round,pad=0.15",
                         facecolor=color, edgecolor="none")
    ax4.add_patch(box)
    ax4.text(x, y + 0.25, num, ha="center", va="center",
             fontsize=12, fontweight="bold", color=tc)
    ax4.text(x, y - 0.15, label, ha="center", va="center",
             fontsize=13, fontweight="bold", color=tc,
             linespacing=1.1)

# Row labels
ax4.text(13.5, 7, "Foundations", ha="center", va="center",
         fontsize=13, fontweight="bold", color=OCEAN_TEAL)
ax4.text(13.5, 5, "Controls", ha="center", va="center",
         fontsize=13, fontweight="bold", color=SEA_GREEN)
ax4.text(13.5, 3, "Practical Skills", ha="center", va="center",
         fontsize=13, fontweight="bold", color=BRIGHT_TEAL)
ax4.text(13.5, 1, "Advanced", ha="center", va="center",
         fontsize=13, fontweight="bold", color=GOLDEN_YELLOW)

fig4.savefig(os.path.join(OUT_DIR, "09_framework_grid.png"),
             dpi=180, bbox_inches="tight", facecolor=fig4.get_facecolor())
plt.close(fig4)
print("  Saved 09_framework_grid.png")

print("\nAll Article 09 visuals generated.")
