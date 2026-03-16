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
import os

# ── Output directory ──────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR    = os.path.join(SCRIPT_DIR, "visuals")
os.makedirs(OUT_DIR, exist_ok=True)

# ── Brand colors ──────────────────────────────────────────────────────────────
TEAL      = "#0F7B6C"
TEAL_LT   = "#5CB8A7"
SLATE     = "#3D4F5F"
CORAL     = "#E05C4D"
GOLD      = "#E8A838"
BLUE      = "#4A90D9"
GRAY_BG   = "#F4F6F7"
GRAY_LINE = "#CCCCCC"
WHITE     = "#FFFFFF"


# ─────────────────────────────────────────────────────────────────────────────
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

    # Full box border (light-grey background, coloured edge)
    full_box = Rectangle(
        (x_left, body_bottom), width, header_h + body_h,
        facecolor=GRAY_BG, edgecolor=header_color,
        linewidth=2.0, zorder=1
    )
    ax.add_patch(full_box)

    # Header band
    header_rect = Rectangle(
        (x_left, header_bottom), width, header_h,
        facecolor=header_color, edgecolor=header_color,
        linewidth=0, zorder=2
    )
    ax.add_patch(header_rect)

    # Title
    ax.text(cx, header_bottom + header_h / 2, title,
            ha="center", va="center",
            fontsize=13, fontweight="bold", color=WHITE, zorder=3)

    # Body items
    n = len(items)
    for i, item in enumerate(items):
        iy = header_bottom - (i + 0.5) * (body_h / n)
        ax.text(cx, iy, item,
                ha="center", va="center",
                fontsize=11, color=SLATE, zorder=3)

    return body_bottom


# ─────────────────────────────────────────────────────────────────────────────
# Figure canvas
# ─────────────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 13))
fig.patch.set_facecolor(WHITE)
ax.set_facecolor(WHITE)
ax.set_xlim(0, 10)
ax.set_ylim(0, 13)
ax.axis("off")

# ── Title ─────────────────────────────────────────────────────────────────────
ax.text(5, 12.55, "AI Tools in Finance – Safe Architecture",
        ha="center", va="center",
        fontsize=16, fontweight="bold", color=SLATE)

ax.text(5, 12.05,
        "The architecture controls what leaves — not the tools themselves",
        ha="center", va="center",
        fontsize=10.5, color=SLATE, fontstyle="italic")

# ── Organisational boundary (dashed rectangle) ───────────────────────────────
# Precomputed extents (must match box layout below):
#   BOX1_TOP=11.7  box1_bottom=10.05  ARROW1_END=9.50
#   box2_bottom=6.65  ARROW2_END=6.10
#   box3_bottom=3.25
ORG_Y_TOP    = 11.95
ORG_Y_BOTTOM = 3.0
org_box = Rectangle(
    (0.7, ORG_Y_BOTTOM), 8.6, ORG_Y_TOP - ORG_Y_BOTTOM,
    facecolor="none", edgecolor=GRAY_LINE,
    linewidth=1.5, linestyle="--", zorder=0
)
ax.add_patch(org_box)

# Label: top-left inside the boundary
ax.text(1.05, ORG_Y_TOP - 0.12, "Your Organisation  ·  Local System",
        ha="left", va="top",
        fontsize=8, color=GRAY_LINE)

# ── BOX 1 : Financial Data Sources ───────────────────────────────────────────
#   top=11.7, header=0.75, body=0.9  →  bottom=10.05
BOX1_TOP = 11.7
box1_bottom = draw_arch_box(
    ax, cx=5, top_y=BOX1_TOP,
    width=7.5, header_h=0.75, body_h=0.90,
    title="Financial Data Sources",
    items=["ERP Systems     /     Excel Files     /     Databases"],
    header_color=TEAL
)

# ── Arrow 1 ───────────────────────────────────────────────────────────────────
#   from box1_bottom (10.05) down 0.55 to box2 top (9.5)
ARROW1_END = box1_bottom - 0.55
ax.annotate("", xy=(5, ARROW1_END), xytext=(5, box1_bottom),
            arrowprops=dict(arrowstyle="-|>", color=SLATE,
                            lw=2.5, mutation_scale=22), zorder=4)

# ── BOX 2 : Local Computer ────────────────────────────────────────────────────
#   top=ARROW1_END, header=0.75, body=2.1  →  bottom≈7.15
BOX2_TOP = ARROW1_END
box2_bottom = draw_arch_box(
    ax, cx=5, top_y=BOX2_TOP,
    width=7.5, header_h=0.75, body_h=2.10,
    title="Local Computer",
    items=["VS Code", "Python Scripts", "AI Assistant  (optional — review data policies)"],
    header_color=BLUE
)

# "Data stays here" badge – centred below Box 3, inside the boundary
ax.text(5, 3.12, "Designed to keep data within this boundary",
        ha="center", va="center",
        fontsize=9, color=TEAL, fontstyle="italic",
        bbox=dict(boxstyle="round,pad=0.3",
                  facecolor="#E6F4F1", edgecolor=TEAL, linewidth=1.0),
        zorder=5)

# ── Arrow 2 ───────────────────────────────────────────────────────────────────
ARROW2_END = box2_bottom - 0.55
ax.annotate("", xy=(5, ARROW2_END), xytext=(5, box2_bottom),
            arrowprops=dict(arrowstyle="-|>", color=SLATE,
                            lw=2.5, mutation_scale=22), zorder=4)

# ── BOX 3 : Outputs ───────────────────────────────────────────────────────────
BOX3_TOP = ARROW2_END
box3_bottom = draw_arch_box(
    ax, cx=5, top_y=BOX3_TOP,
    width=7.5, header_h=0.75, body_h=2.10,
    title="Outputs",
    items=["Reports", "Dashboards", "Automations"],
    header_color=TEAL_LT
)

# ── Key message ───────────────────────────────────────────────────────────────
ax.text(5, 1.55,
        "With the right design, AI tools can keep your organisation's financial data secure.",
        ha="center", va="center",
        fontsize=11.5, fontweight="bold", color=SLATE,
        bbox=dict(boxstyle="round,pad=0.55",
                  facecolor="#FFF9EC", edgecolor=GOLD, linewidth=2.0),
        zorder=5)

ax.text(5, 0.65,
        "The tools are neutral. The design is the risk — or the safeguard.",
        ha="center", va="center",
        fontsize=10, color=SLATE, fontstyle="italic")

# ── Save ──────────────────────────────────────────────────────────────────────
out_path = os.path.join(OUT_DIR, "03_safe_architecture.png")
plt.savefig(out_path, dpi=180, bbox_inches="tight")
plt.close()
print(f"[OK] 03_safe_architecture.png  ->  {OUT_DIR}")


# ─────────────────────────────────────────────────────────────────────────────
# Visual 02 – "What IT Imagines vs What Actually Happens"
# ─────────────────────────────────────────────────────────────────────────────
fig2, ax2 = plt.subplots(figsize=(11, 7))
fig2.patch.set_facecolor(WHITE)
ax2.set_facecolor(WHITE)
ax2.set_xlim(0, 11)
ax2.set_ylim(0, 7)
ax2.axis("off")

# ── Title ──────────────────────────────────────────────────────────────────
ax2.text(5.5, 6.55, "What IT Imagines vs. What Actually Happens",
         ha="center", va="center",
         fontsize=16, fontweight="bold", color=SLATE)

# ── Column headers ─────────────────────────────────────────────────────────
left_hdr = Rectangle((0.35, 5.35), 4.85, 0.80,
                      facecolor=CORAL, edgecolor=CORAL, linewidth=0, zorder=2)
ax2.add_patch(left_hdr)
ax2.text(2.775, 5.75, "What IT Imagines",
         ha="center", va="center",
         fontsize=13, fontweight="bold", color=WHITE, zorder=3)

right_hdr = Rectangle((5.8, 5.35), 4.85, 0.80,
                       facecolor=TEAL, edgecolor=TEAL, linewidth=0, zorder=2)
ax2.add_patch(right_hdr)
ax2.text(8.225, 5.75, "What Actually Happens",
         ha="center", va="center",
         fontsize=13, fontweight="bold", color=WHITE, zorder=3)

# ── Centre divider ─────────────────────────────────────────────────────────
ax2.plot([5.5, 5.5], [0.9, 6.15], color=GRAY_LINE,
         linewidth=1.5, linestyle="--", zorder=1)

# ── Content rows ───────────────────────────────────────────────────────────
rows = [
    ("Hacker movie screens",       "Writing a reconciliation script"),
    ("Data flying to the cloud",   "Local CSV file analysis"),
    ("AI replacing core systems",  "Automating spreadsheet tasks"),
]
row_y_positions = [4.55, 3.50, 2.45]

for (left_text, right_text), y in zip(rows, row_y_positions):
    bg = Rectangle((0.35, y - 0.42), 10.3, 0.84,
                   facecolor=GRAY_BG, edgecolor=GRAY_LINE,
                   linewidth=0.7, zorder=1)
    ax2.add_patch(bg)
    ax2.text(2.775, y, left_text,
             ha="center", va="center",
             fontsize=11.5, color=SLATE, zorder=3)
    ax2.text(8.225, y, right_text,
             ha="center", va="center",
             fontsize=11.5, color=SLATE, zorder=3)

# ── Footer callout ─────────────────────────────────────────────────────────
ax2.text(5.5, 0.78,
         "The tools are practical.  The work is familiar.",
         ha="center", va="center",
         fontsize=11.5, color=TEAL, fontstyle="italic",
         bbox=dict(boxstyle="round,pad=0.45",
                   facecolor="#E6F4F1", edgecolor=TEAL, linewidth=1.5),
         zorder=5)

out_path2 = os.path.join(OUT_DIR, "03_it_thinks_vs_reality.png")
plt.savefig(out_path2, dpi=180, bbox_inches="tight")
plt.close()
print(f"[OK] 03_it_thinks_vs_reality.png  ->  {OUT_DIR}")


# ─────────────────────────────────────────────────────────────────────────────
# Visual 03 – "Where These Tools Are Used" – Industry Bar Chart
# ─────────────────────────────────────────────────────────────────────────────
industries = ["Automation", "Academia", "Finance & FinTech", "Data Science", "Engineering"]
values     = [55, 62, 70, 85, 90]
bar_colors = [TEAL_LT, BLUE, GOLD, TEAL, SLATE]

fig3, ax3 = plt.subplots(figsize=(10, 6))
fig3.patch.set_facecolor(WHITE)
ax3.set_facecolor(GRAY_BG)
ax3.set_xlim(0, 105)

bars = ax3.barh(industries, values, color=bar_colors, height=0.55, zorder=2)

# Value labels on bars
for bar, val in zip(bars, values):
    ax3.text(val + 1.2, bar.get_y() + bar.get_height() / 2,
             f"{val}%",
             va="center", ha="left",
             fontsize=11.5, color=SLATE, fontweight="bold", zorder=3)

ax3.set_title("Industries Using Python & AI Developer Tools",
              fontsize=15, fontweight="bold", color=SLATE, pad=14)
ax3.tick_params(axis="y", labelsize=12.5, colors=SLATE)
ax3.xaxis.set_visible(False)
ax3.spines["top"].set_visible(False)
ax3.spines["right"].set_visible(False)
ax3.spines["bottom"].set_visible(False)
ax3.spines["left"].set_color(GRAY_LINE)

# Trusted-by footnote
trusted = "Used by:  Google   \u00b7   Netflix   \u00b7   JPMorgan   \u00b7   NASA   \u00b7   Universities worldwide"
fig3.text(0.5, 0.01, trusted,
          ha="center", fontsize=10, color=SLATE, fontstyle="italic")

fig3.tight_layout(rect=[0, 0.07, 1, 1])
out_path3 = os.path.join(OUT_DIR, "03_industry_adoption.png")
plt.savefig(out_path3, dpi=180, bbox_inches="tight")
plt.close()
print(f"[OK] 03_industry_adoption.png  ->  {OUT_DIR}")


# ─────────────────────────────────────────────────────────────────────────────
# Visual 04 – IT Approval Checklist
# ─────────────────────────────────────────────────────────────────────────────
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

# ── Title header ───────────────────────────────────────────────────────────
title_bar = Rectangle((0.4, 6.3), 8.2, 0.85,
                       facecolor=TEAL, linewidth=0, zorder=2)
ax4.add_patch(title_bar)
ax4.text(4.5, 6.725, "IT Approval Checklist",
         ha="center", va="center",
         fontsize=16, fontweight="bold", color=WHITE, zorder=3)

# ── Subtitle ───────────────────────────────────────────────────────────────
ax4.text(4.5, 5.95,
         "What finance teams can prepare before requesting tool access",
         ha="center", va="center",
         fontsize=10.5, color=SLATE, fontstyle="italic")

# ── Checklist rows ─────────────────────────────────────────────────────────
row_top    = 5.35
row_height = 0.72
row_gap    = 0.08

for i, item in enumerate(checklist):
    y_top = row_top - i * (row_height + row_gap)
    y_mid = y_top - row_height / 2

    bg_color = "#E6F4F1" if i % 2 == 0 else GRAY_BG
    bg = Rectangle((0.4, y_top - row_height), 8.2, row_height,
                   facecolor=bg_color, edgecolor=GRAY_LINE,
                   linewidth=0.7, zorder=1)
    ax4.add_patch(bg)

    # Check circle
    circ = plt.Circle((1.22, y_mid), 0.22, color=TEAL, zorder=3)
    ax4.add_patch(circ)
    ax4.text(1.22, y_mid, "\u2713",
             ha="center", va="center",
             fontsize=13, color=WHITE, fontweight="bold", zorder=4)

    ax4.text(1.72, y_mid, item,
             ha="left", va="center",
             fontsize=12.5, color=SLATE, zorder=3)

# ── "Admin password moment" callout ────────────────────────────────────────
ax4.text(4.5, 0.75,
         '"The biggest barrier to AI adoption in finance\n'
         "wasn't technology.  It was the admin password.",
         ha="center", va="center",
         fontsize=10.5, color=SLATE, fontstyle="italic",
         bbox=dict(boxstyle="round,pad=0.55",
                   facecolor="#FFF9EC", edgecolor=GOLD, linewidth=2.0),
         zorder=5)

out_path4 = os.path.join(OUT_DIR, "03_it_approval_checklist.png")
plt.savefig(out_path4, dpi=180, bbox_inches="tight")
plt.close()
print(f"[OK] 03_it_approval_checklist.png  ->  {OUT_DIR}")
