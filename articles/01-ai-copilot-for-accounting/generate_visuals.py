"""
Generate article visuals for the CodeCritters AI Finance Demo article.
Produces 5 PNG charts saved to Demo/article_visuals/
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import os

# ── Output directory ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(SCRIPT_DIR, "article_visuals")
os.makedirs(OUT_DIR, exist_ok=True)

# ── Brand colors ──
TEAL      = "#0F7B6C"
TEAL_LT   = "#5CB8A7"
SLATE     = "#3D4F5F"
CORAL     = "#E05C4D"
GOLD      = "#E8A838"
BLUE      = "#4A90D9"
GRAY_BG   = "#F7F7F7"
GRAY_LINE = "#CCCCCC"

def style_ax(ax, title, ylabel=None):
    ax.set_facecolor(GRAY_BG)
    ax.set_title(title, fontsize=14, fontweight="bold", color=SLATE, pad=14)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=10, color=SLATE)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(GRAY_LINE)
    ax.spines["bottom"].set_color(GRAY_LINE)
    ax.tick_params(colors=SLATE, labelsize=9)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))


# ════════════════════════════════════════════════════════════════
# CHART 1  ─  Gross Margin % by Order
# ════════════════════════════════════════════════════════════════

orders = [
    "1001","1002","1003","1004","1005","1006","1007","1008","1009","1010",
    "2001","2002","2003","2004","2005","2006","2007","2008","2009","2010",
]
margins = [
    41.3, 39.6, 41.3, 24.8, 41.2, 42.7, 39.6, 38.0, 42.9, 26.6,
    40.7, 29.3, 41.7, 17.6, 33.1, 39.2, 28.8, 17.1, 33.7, 16.4,
]
colors_1 = [CORAL if m < 20 else TEAL for m in margins]

fig, ax = plt.subplots(figsize=(14, 5))
fig.patch.set_facecolor("white")
bars = ax.bar(orders, margins, color=colors_1, edgecolor="white", linewidth=0.5)
ax.axhline(20, color=CORAL, linewidth=1, linestyle="--", alpha=0.7)
ax.text(19.6, 21, "20% threshold", color=CORAL, fontsize=8, va="bottom", ha="right")
ax.axvline(9.5, color=GRAY_LINE, linewidth=1, linestyle=":")
ax.text(4.5, 46, "2024", fontsize=11, ha="center", color=SLATE, fontstyle="italic")
ax.text(14.5, 46, "2025", fontsize=11, ha="center", color=SLATE, fontstyle="italic")
style_ax(ax, "Gross Margin by Order — Three Orders Fall Below 20%", "Gross Margin %")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.0f}%"))
ax.set_xlabel("Order ID", fontsize=10, color=SLATE)
# Label the three bad orders
for i, (o, m) in enumerate(zip(orders, margins)):
    if m < 20:
        ax.text(i, m + 1.0, f"{m:.1f}%", ha="center", fontsize=8, color=CORAL, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "01_margin_by_order.png"), dpi=180)
plt.close()
print("[OK] 01_margin_by_order.png")


# ════════════════════════════════════════════════════════════════
# CHART 2  ─  Year-over-Year Revenue vs Gross Profit
# ════════════════════════════════════════════════════════════════

years = ["2024", "2025"]
revenue = [60099, 76344]
gp      = [23017, 22919]

fig, ax = plt.subplots(figsize=(8, 5))
fig.patch.set_facecolor("white")
x = np.arange(len(years))
w = 0.32
b1 = ax.bar(x - w/2, revenue, w, label="Revenue", color=TEAL, edgecolor="white")
b2 = ax.bar(x + w/2, gp, w, label="Gross Profit", color=GOLD, edgecolor="white")

# Annotations
ax.annotate("+27.0%", xy=(1 - w/2, revenue[1]), xytext=(0.45, 82000),
            fontsize=10, fontweight="bold", color=TEAL,
            arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.2))
ax.annotate("-0.4%", xy=(1 + w/2, gp[1]), xytext=(1.35, 35000),
            fontsize=10, fontweight="bold", color=CORAL,
            arrowprops=dict(arrowstyle="->", color=CORAL, lw=1.2))

# Margin labels
for i, (r, g) in enumerate(zip(revenue, gp)):
    pct = g / r * 100
    ax.text(i + w/2, g + 1500, f"{pct:.1f}% margin", ha="center", fontsize=9,
            color=SLATE, fontstyle="italic")

ax.set_xticks(x)
ax.set_xticklabels(years, fontsize=12)
ax.legend(fontsize=10, loc="upper left", framealpha=0.9)
style_ax(ax, "Revenue Up 27%, Gross Profit Flat", "Dollars ($)")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "02_yoy_comparison.png"), dpi=180)
plt.close()
print("[OK] 02_yoy_comparison.png")


# ════════════════════════════════════════════════════════════════
# CHART 3  ─  Salesperson Gross Profit + Margin Rate
# ════════════════════════════════════════════════════════════════

names  = ["Emma\nChen", "Sophia\nRamirez", "Liam\nCarter", "Olivia\nBrooks", "Noah\nPatel"]
sp_gp  = [18145, 9582, 7212, 5825, 5172]
sp_mgn = [38.5, 37.6, 29.2, 40.8, 20.8]
bar_c  = [TEAL, TEAL, TEAL_LT, BLUE, CORAL]

fig, ax1 = plt.subplots(figsize=(10, 5.5))
fig.patch.set_facecolor("white")
x = np.arange(len(names))
bars = ax1.bar(x, sp_gp, 0.55, color=bar_c, edgecolor="white", linewidth=0.5)
style_ax(ax1, "Salesperson Performance: Gross Profit vs. Margin Rate", "Gross Profit ($)")
ax1.set_xticks(x)
ax1.set_xticklabels(names, fontsize=10)

ax2 = ax1.twinx()
ax2.plot(x, sp_mgn, color=SLATE, marker="D", markersize=7, linewidth=2, zorder=5)
ax2.set_ylabel("Gross Margin %", fontsize=10, color=SLATE)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_color(GRAY_LINE)
ax2.tick_params(colors=SLATE, labelsize=9)
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.0f}%"))
ax2.set_ylim(10, 50)

for i, (g, m) in enumerate(zip(sp_gp, sp_mgn)):
    ax1.text(i, g + 400, f"${g:,}", ha="center", fontsize=9, color=SLATE, fontweight="bold")
    ax2.text(i, m + 2.2, f"{m}%", ha="center", fontsize=8, color=SLATE)

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "03_salesperson_gp.png"), dpi=180)
plt.close()
print("[OK] 03_salesperson_gp.png")


# ════════════════════════════════════════════════════════════════
# CHART 4  ─  Revenue Concentration Donut
# ════════════════════════════════════════════════════════════════

labels = ["Emma Chen\n34.5%", "Sophia Ramirez\n18.7%", "Noah Patel\n18.3%",
          "Liam Carter\n18.1%", "Olivia Brooks\n10.5%"]
sizes  = [34.5, 18.7, 18.3, 18.1, 10.5]
colors_4 = [CORAL, TEAL, TEAL_LT, BLUE, GOLD]
explode = (0.06, 0, 0, 0, 0)

fig, ax = plt.subplots(figsize=(7, 7))
fig.patch.set_facecolor("white")
wedges, texts = ax.pie(
    sizes, labels=labels, colors=colors_4, explode=explode,
    startangle=90, pctdistance=0.78,
    wedgeprops=dict(width=0.45, edgecolor="white", linewidth=2),
    textprops=dict(fontsize=10, color=SLATE),
)
ax.text(0, 0, "Revenue\nConcentration", ha="center", va="center",
        fontsize=12, fontweight="bold", color=SLATE)
ax.set_title("Revenue Concentration Risk", fontsize=14, fontweight="bold",
             color=SLATE, pad=18)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "04_revenue_concentration.png"), dpi=180)
plt.close()
print("[OK] 04_revenue_concentration.png")


# ════════════════════════════════════════════════════════════════
# CHART 5  ─  Vendor Material Cost Inflation
# ════════════════════════════════════════════════════════════════

vendors   = ["SiliconSerpent\nSupply Co", "QuantumCoil\nMaterials", "NeuralNest\nComponents"]
v_2024    = [2725, 2400, 2600]
v_2025    = [4020, 3267, 3500]
v_pct     = [47.5, 36.1, 34.6]

fig, ax = plt.subplots(figsize=(10, 5.5))
fig.patch.set_facecolor("white")
x = np.arange(len(vendors))
w = 0.32
b1 = ax.bar(x - w/2, v_2024, w, label="2024 Avg", color=TEAL_LT, edgecolor="white")
b2 = ax.bar(x + w/2, v_2025, w, label="2025 Avg", color=CORAL, edgecolor="white")

for i, pct in enumerate(v_pct):
    top = max(v_2024[i], v_2025[i])
    ax.text(i, top + 150, f"+{pct}%", ha="center", fontsize=11,
            fontweight="bold", color=CORAL)

ax.legend(fontsize=10, loc="upper right", framealpha=0.9)
ax.set_xticks(x)
ax.set_xticklabels(vendors, fontsize=10)
style_ax(ax, "Vendor Material Cost Inflation (Avg per Order)", "Avg Material Cost ($)")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "05_vendor_costs.png"), dpi=180)
plt.close()
print("[OK] 05_vendor_costs.png")

print(f"\nAll charts saved to: {OUT_DIR}")
