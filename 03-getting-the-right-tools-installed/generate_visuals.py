"""
Generate Article 03 visuals.

Visual 01: AI Tools in Finance – Safe Architecture
  Architecture diagram showing data flows entirely within the local machine—
  reassuring controllers and IT that Python / VS Code are not cloud pipelines.

Visual 02: What IT Imagines vs What Actually Happens
  Two-column humor graphic contrasting IT fears with practical finance reality.

Visual 03: Where These Tools Are Used
  Horizontal bar chart showing Python / AI tool adoption across industries,
  with enterprise-adoption footnote (Google, Netflix, JPMorgan, NASA).

Visual 04: IT Approval Checklist
  Checklist graphic summarising what finance teams can prepare before
  requesting tool access, with the "admin password moment" callout.

Saved to articles/03-getting-the-right-tools-installed/visuals/
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
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

FOOTER_TEXT = "PythonMuse LLC  |  github.com/PythonMuse/ai-ledger"

DARK_BG_COLORS = {DEEP_NAVY, MIDNIGHT_TEAL, OCEAN_TEAL, SEA_GREEN, ALERT_RED}

def text_color_for(bg):
    """Return correct text color per SKILL.md contrast rule."""
    if bg in DARK_BG_COLORS:
        return WHITE
    return DEEP_NAVY

# --------------------------------------------------------------------------
def draw_arch_box(ax, cx, top_y, width, header_h, body_h,
                  title, items, header_color):
    """
    Draw a box with a coloured header band and a light-grey body.
    Items are evenly distributed inside the body.
    Returns the bottom y coordinate of the whole box.
    """
    x_left        = cx - width / 2
    header_bottom = top_y - header_h
    body_bottom   = header_bottom - body_h

    # Full box border (light-grey background, no visible outline)
    full_box = Rectangle(
        (x_left, body_bottom), width, header_h + body_h,
        facecolor=LIGHT_GRAY, edgecolor="none",
        linewidth=0, zorder=1
    )
    ax.add_patch(full_box)

    # Header band
    header_rect = Rectangle(
        (x_left, header_bottom), width, header_h,
        facecolor=header_color, edgecolor="none",
        linewidth=0, zorder=2
    )
    ax.add_patch(header_rect)

    # Title -- WHITE text on dark header
    ax.text(cx, header_bottom + header_h / 2, title,
            ha="center", va="center",
            fontsize=13, fontweight="bold",
            color=text_color_for(header_color), zorder=3)

    # Body items
    n = len(items)
    for i, item in enumerate(items):
        iy = header_bottom - (i + 0.5) * (body_h / n)
        ax.text(cx, iy, item,
                ha="center", va="center",
                fontsize=12, color=DEEP_NAVY, zorder=3)

    return body_bottom

# --------------------------------------------------------------------------
# Visual 01 -- AI Tools in Finance -- Safe Architecture
#   Landscape layout (14x8) — PowerPoint-friendly, horizontal flow
# --------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(14, 8))
fig.patch.set_facecolor(WHITE)
ax.set_facecolor(WHITE)
ax.set_xlim(0, 14)
ax.set_ylim(0, 8)
ax.axis("off")

# -- Title -----------------------------------------------------------------
ax.text(7, 7.5, "AI Tools in Finance \u2013 Safe Architecture",
        ha="center", va="center",
        fontsize=20, fontweight="bold", color=DEEP_NAVY)

ax.text(7, 6.9,
        "The architecture controls what leaves \u2014 not the tools themselves",
        ha="center", va="center",
        fontsize=14, color=DEEP_NAVY, fontstyle="italic")

# -- Organisational boundary (dashed rectangle around all 3 boxes) ----------
ORG_LEFT, ORG_BOT, ORG_W, ORG_H = 0.4, 1.3, 13.2, 5.2
org_box = Rectangle(
    (ORG_LEFT, ORG_BOT), ORG_W, ORG_H,
    facecolor="none", edgecolor=GRAY_LINE,
    linewidth=1.5, linestyle="--", zorder=0
)
ax.add_patch(org_box)
ax.text(ORG_LEFT + 0.15, ORG_BOT + ORG_H - 0.15,
        "Your Organisation  \u00b7  Local System",
        ha="left", va="top",
        fontsize=10, color=GRAY_LINE)

# -- Three boxes side by side (horizontal flow) ----------------------------
box_w = 3.5
box_h = 3.8
y_bot = 1.9       # bottom edge of all 3 boxes
gap = 0.9          # space between boxes
total_w = 3 * box_w + 2 * gap
start_x = (14 - total_w) / 2

boxes = [
    ("Financial Data\nSources",
     "ERP Systems\n\nExcel Files\n\nDatabases",
     OCEAN_TEAL),
    ("Local Computer",
     "VS Code\n\nPython Scripts\n\nAI Co-pilot\n(review data policies)",
     SEA_GREEN),
    ("Outputs",
     "Reports\n\nDashboards\n\nAutomations",
     BRIGHT_TEAL),
]

box_centers = []
for i, (title, items, color) in enumerate(boxes):
    x = start_x + i * (box_w + gap)
    header_h = 0.85

    # Body (light gray background)
    body = Rectangle(
        (x, y_bot), box_w, box_h,
        facecolor=LIGHT_GRAY, edgecolor="none",
        linewidth=0, zorder=1
    )
    ax.add_patch(body)

    # Header band
    header = Rectangle(
        (x, y_bot + box_h - header_h), box_w, header_h,
        facecolor=color, edgecolor="none",
        linewidth=0, zorder=2
    )
    ax.add_patch(header)

    # Header title
    ax.text(x + box_w / 2, y_bot + box_h - header_h / 2, title,
            ha="center", va="center",
            fontsize=14, fontweight="bold",
            color=text_color_for(color), linespacing=1.15, zorder=3)

    # Body items
    body_center_y = y_bot + (box_h - header_h) / 2
    ax.text(x + box_w / 2, body_center_y, items,
            ha="center", va="center",
            fontsize=13, color=DEEP_NAVY,
            linespacing=1.4, zorder=3)

    box_centers.append((x + box_w / 2, y_bot + box_h / 2))

# -- Arrows between boxes --------------------------------------------------
for i in range(2):
    x_start = start_x + (i + 1) * box_w + i * gap + 0.05
    x_end = start_x + (i + 1) * (box_w + gap) - 0.05
    y_mid = y_bot + box_h / 2
    ax.annotate("", xy=(x_end, y_mid), xytext=(x_start, y_mid),
                arrowprops=dict(arrowstyle="-|>", color=DEEP_NAVY,
                                lw=2.5, mutation_scale=22), zorder=4)

# -- "Data stays here" badge -----------------------------------------------
ax.text(7, 1.55, "Designed to keep data within this boundary",
        ha="center", va="center",
        fontsize=12, color=OCEAN_TEAL, fontstyle="italic",
        bbox=dict(boxstyle="round,pad=0.3",
                  facecolor=LIGHT_GRAY, edgecolor="none", linewidth=0),
        zorder=5)

# -- Key message at bottom -------------------------------------------------
ax.text(7, 0.55,
        "The tools are neutral.  The design is the risk \u2014 or the safeguard.",
        ha="center", va="center",
        fontsize=13, color=DEEP_NAVY, fontstyle="italic")

# -- Save ------------------------------------------------------------------
fig.text(0.5, 0.01, FOOTER_TEXT, ha="center", fontsize=8, color=DEEP_NAVY, alpha=0.50)
out_path = os.path.join(OUT_DIR, "03_safe_architecture.png")
plt.savefig(out_path, dpi=180, bbox_inches="tight")
plt.close()
print(f"[OK] 03_safe_architecture.png  ->  {OUT_DIR}")

# --------------------------------------------------------------------------
# Visual 02 -- "What IT Imagines vs What Actually Happens"
# --------------------------------------------------------------------------
fig2, ax2 = plt.subplots(figsize=(11, 7))
fig2.patch.set_facecolor(WHITE)
ax2.set_facecolor(WHITE)
ax2.set_xlim(0, 11)
ax2.set_ylim(0, 7)
ax2.axis("off")

# -- Title -----------------------------------------------------------------
ax2.text(5.5, 6.55, "What IT Imagines vs. What Actually Happens",
         ha="center", va="center",
         fontsize=18, fontweight="bold", color=DEEP_NAVY)

# -- Column headers --------------------------------------------------------
left_hdr = Rectangle((0.35, 5.35), 4.85, 0.80,
                      facecolor=ALERT_RED, edgecolor="none",
                      linewidth=0, zorder=2)
ax2.add_patch(left_hdr)
ax2.text(2.775, 5.75, "What IT Imagines",
         ha="center", va="center",
         fontsize=13, fontweight="bold", color=WHITE, zorder=3)

right_hdr = Rectangle((5.8, 5.35), 4.85, 0.80,
                       facecolor=OCEAN_TEAL, edgecolor="none",
                       linewidth=0, zorder=2)
ax2.add_patch(right_hdr)
ax2.text(8.225, 5.75, "What Actually Happens",
         ha="center", va="center",
         fontsize=13, fontweight="bold", color=WHITE, zorder=3)

# -- Centre divider --------------------------------------------------------
ax2.plot([5.5, 5.5], [0.9, 6.15], color=GRAY_LINE,
         linewidth=1.5, linestyle="--", zorder=1)

# -- Content rows ----------------------------------------------------------
rows = [
    ("Hacker movie screens",       "Writing a reconciliation script"),
    ("Data flying to the cloud",   "Local CSV file analysis"),
    ("AI replacing core systems",  "Automating spreadsheet tasks"),
]
row_y_positions = [4.55, 3.50, 2.45]

for (left_text, right_text), y in zip(rows, row_y_positions):
    bg = Rectangle((0.35, y - 0.42), 10.3, 0.84,
                   facecolor=LIGHT_GRAY, edgecolor="none",
                   linewidth=0, zorder=1)
    ax2.add_patch(bg)
    ax2.text(2.775, y, left_text,
             ha="center", va="center",
             fontsize=12, color=DEEP_NAVY, zorder=3)
    ax2.text(8.225, y, right_text,
             ha="center", va="center",
             fontsize=12, color=DEEP_NAVY, zorder=3)

# -- Footer callout --------------------------------------------------------
ax2.text(5.5, 0.78,
         "The tools are practical.  The work is familiar.",
         ha="center", va="center",
         fontsize=12, color=OCEAN_TEAL, fontstyle="italic",
         bbox=dict(boxstyle="round,pad=0.45",
                   facecolor=LIGHT_GRAY, edgecolor="none", linewidth=0),
         zorder=5)

fig2.text(0.5, 0.01, FOOTER_TEXT, ha="center", fontsize=8, color=DEEP_NAVY, alpha=0.50)
out_path2 = os.path.join(OUT_DIR, "03_it_thinks_vs_reality.png")
plt.savefig(out_path2, dpi=180, bbox_inches="tight")
plt.close()
print(f"[OK] 03_it_thinks_vs_reality.png  ->  {OUT_DIR}")

# --------------------------------------------------------------------------
# Visual 03 -- "Where These Tools Are Used" -- Industry Bar Chart
# --------------------------------------------------------------------------
industries = ["Automation", "Academia", "Finance & FinTech", "Data Science", "Engineering"]
values     = [55, 62, 70, 85, 90]
bar_colors = [BRIGHT_TEAL, SEA_GREEN, GOLDEN_YELLOW, OCEAN_TEAL, DEEP_NAVY]

fig3, ax3 = plt.subplots(figsize=(10, 6))
fig3.patch.set_facecolor(WHITE)
ax3.set_facecolor(WHITE)
ax3.set_xlim(0, 105)

bars = ax3.barh(industries, values, color=bar_colors, height=0.55, zorder=2)

# Value labels on bars
for bar, val in zip(bars, values):
    ax3.text(val + 1.2, bar.get_y() + bar.get_height() / 2,
             f"{val}%",
             va="center", ha="left",
             fontsize=12, color=DEEP_NAVY, fontweight="bold", zorder=3)

ax3.set_title("Industries Using Python & AI Developer Tools",
              fontsize=18, fontweight="bold", color=DEEP_NAVY, pad=14)
ax3.tick_params(axis="y", labelsize=12, colors=DEEP_NAVY)
ax3.xaxis.set_visible(False)
ax3.spines["top"].set_visible(False)
ax3.spines["right"].set_visible(False)
ax3.spines["bottom"].set_visible(False)
ax3.spines["left"].set_color(GRAY_LINE)

# Trusted-by footnote
trusted = "Used by:  Google   \u00b7   Netflix   \u00b7   JPMorgan   \u00b7   NASA   \u00b7   Universities worldwide"
fig3.text(0.5, 0.01, trusted,
          ha="center", fontsize=12, color=DEEP_NAVY, fontstyle="italic")

fig3.tight_layout(rect=[0, 0.07, 1, 1])
fig3.text(0.5, 0.01, FOOTER_TEXT, ha="center", fontsize=8, color=DEEP_NAVY, alpha=0.50)
out_path3 = os.path.join(OUT_DIR, "03_industry_adoption.png")
plt.savefig(out_path3, dpi=180, bbox_inches="tight")
plt.close()
print(f"[OK] 03_industry_adoption.png  ->  {OUT_DIR}")

# --------------------------------------------------------------------------
# Visual 04 -- IT Approval Checklist
# --------------------------------------------------------------------------
checklist = [
    "Tool is from a trusted vendor",
    "Tool does not store company data",
    "Usage is documented",
    "Data policies are followed",
    "Test using sample data first",
]

fig4, ax4 = plt.subplots(figsize=(9, 7.5))
fig4.patch.set_facecolor(WHITE)
ax4.set_facecolor(WHITE)
ax4.set_xlim(0, 9)
ax4.set_ylim(0, 7.5)
ax4.axis("off")

# -- Title header ----------------------------------------------------------
title_bar = Rectangle((0.4, 6.3), 8.2, 0.85,
                       facecolor=OCEAN_TEAL, edgecolor="none",
                       linewidth=0, zorder=2)
ax4.add_patch(title_bar)
ax4.text(4.5, 6.725, "IT Approval Checklist",
         ha="center", va="center",
         fontsize=18, fontweight="bold", color=WHITE, zorder=3)

# -- Subtitle --------------------------------------------------------------
ax4.text(4.5, 5.95,
         "What finance teams can prepare before requesting tool access",
         ha="center", va="center",
         fontsize=14, color=DEEP_NAVY, fontstyle="italic")

# -- Checklist rows --------------------------------------------------------
row_top    = 5.35
row_height = 0.72
row_gap    = 0.08

for i, item in enumerate(checklist):
    y_top = row_top - i * (row_height + row_gap)
    y_mid = y_top - row_height / 2

    bg_color = LIGHT_GRAY if i % 2 == 0 else WHITE
    bg = Rectangle((0.4, y_top - row_height), 8.2, row_height,
                   facecolor=bg_color, edgecolor="none",
                   linewidth=0, zorder=1)
    ax4.add_patch(bg)

    # Check circle
    circ = plt.Circle((1.22, y_mid), 0.22, color=OCEAN_TEAL, zorder=3)
    ax4.add_patch(circ)
    ax4.text(1.22, y_mid, "\u2713",
             ha="center", va="center",
             fontsize=13, color=WHITE, fontweight="bold", zorder=4)

    ax4.text(1.72, y_mid, item,
             ha="left", va="center",
             fontsize=13, color=DEEP_NAVY, zorder=3)

# -- "Admin password moment" callout ---------------------------------------
ax4.text(4.5, 0.75,
         '"The biggest barrier to AI adoption in finance\n'
         "wasn't technology.  It was the admin password.",
         ha="center", va="center",
         fontsize=12, color=DEEP_NAVY, fontstyle="italic",
         bbox=dict(boxstyle="round,pad=0.55",
                   facecolor=WARM_GLOW, edgecolor="none", linewidth=0),
         zorder=5)

fig4.text(0.5, 0.01, FOOTER_TEXT, ha="center", fontsize=8, color=DEEP_NAVY, alpha=0.50)
out_path4 = os.path.join(OUT_DIR, "03_it_approval_checklist.png")
plt.savefig(out_path4, dpi=180, bbox_inches="tight")
plt.close()
print(f"[OK] 03_it_approval_checklist.png  ->  {OUT_DIR}")
