"""
Generate Article 10 visuals -- AI in Accounting: Real Use Cases and How to Structure Them.

Visual 01: Hero / front image
Visual 02: Decision Framework
Visual 03: Three-Part Series Overview

Saved to articles/10-ai-use-cases-and-structure/visuals/
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

ax1.text(6, 3.8, "AI in Accounting",
         ha="center", va="center",
         fontsize=30, fontweight="bold", color=DEEP_NAVY,
         linespacing=1.3)

ax1.text(6, 2.8, "Real Use Cases -- and How to Structure Them Correctly",
         ha="center", va="center",
         fontsize=14, color=OCEAN_TEAL, style="italic")

ax1.text(6, 1.4, "PythonMuse LLC  |  github.com/PythonMuse/ai-ledger",
         ha="center", va="center",
         fontsize=12, color=OCEAN_TEAL, alpha=0.7)

ax1.plot([2, 10], [2.1, 2.1], color=BRIGHT_TEAL, linewidth=1.5, alpha=0.5)

fig1.savefig(os.path.join(OUT_DIR, "10_visual_front.png"),
             dpi=180, bbox_inches="tight", facecolor=fig1.get_facecolor())
plt.close(fig1)
print("  Saved 10_visual_front.png")

# ---------------------------------------------------------------------------
# Visual 02 -- Decision Framework
# ---------------------------------------------------------------------------
fig2, ax2 = plt.subplots(figsize=(12, 8))
fig2.patch.set_facecolor(WHITE)
ax2.set_facecolor(WHITE)
ax2.set_xlim(0, 12)
ax2.set_ylim(0, 10)
ax2.axis("off")

ax2.text(6, 9.4, "How to Classify Your AI Use Case",
         ha="center", va="center",
         fontsize=20, fontweight="bold", color=DEEP_NAVY)

# Three tier boxes
tiers = [
    (2, 6.5, "Exploratory", "One-time analysis\nTesting ideas\nLearning AI", SOFT_SAGE, "Low Risk"),
    (6, 6.5, "Repeatable\nWorkflow", "Monthly processes\nRecurring analysis\nStructured outputs", SEA_GREEN, "Medium Risk"),
    (10, 6.5, "Agent-Run /\nAudit-Ready", "AI executes alone\nRequires controls\nMust survive audit", GOLDEN_YELLOW, "High Risk"),
]

for x, y, title, desc, color, risk in tiers:
    tc = text_color_for(color)
    box = FancyBboxPatch((x - 1.7, y - 1.5), 3.4, 3,
                         boxstyle="round,pad=0.2",
                         facecolor=color, edgecolor="none",
                         alpha=0.9)
    ax2.add_patch(box)
    ax2.text(x, y + 0.7, title, ha="center", va="center",
             fontsize=13, fontweight="bold", color=tc,
             linespacing=1.1)
    ax2.text(x, y - 0.3, desc, ha="center", va="center",
             fontsize=12, color=tc, alpha=0.85,
             linespacing=1.3)
    ax2.text(x, y - 1.8, risk, ha="center", va="center",
             fontsize=12, fontweight="bold", color=color)

# Arrows between tiers
for x_from, x_to in [(3.7, 4.3), (7.7, 8.3)]:
    ax2.annotate("", xy=(x_to, 6.5), xytext=(x_from, 6.5),
                 arrowprops=dict(arrowstyle="->", color=OCEAN_TEAL, lw=2))

# Decision questions at the bottom
questions = [
    (3, 3.2, "Will I do this again?"),
    (6, 3.2, "Does someone need to\nreview it?"),
    (9, 3.2, "Would this hold up\nin an audit?"),
]

for x, y, q in questions:
    box = FancyBboxPatch((x - 1.8, y - 0.6), 3.6, 1.2,
                         boxstyle="round,pad=0.15",
                         facecolor=DEEP_NAVY, edgecolor="none",
                         alpha=0.9)
    ax2.add_patch(box)
    ax2.text(x, y, q, ha="center", va="center",
             fontsize=12, color=WHITE, linespacing=1.2)

for x_q, x_t in [(3, 2), (6, 6), (9, 10)]:
    ax2.annotate("", xy=(x_t, 5.0), xytext=(x_q, 3.8),
                 arrowprops=dict(arrowstyle="->", color=BRIGHT_TEAL,
                                 lw=1.2, connectionstyle="arc3,rad=0.1"))

ax2.text(6, 1.5, "Start with what frustrates you. Those are your best automation candidates.",
         ha="center", va="center",
         fontsize=12, color=OCEAN_TEAL, style="italic")

fig2.savefig(os.path.join(OUT_DIR, "10_decision_framework.png"),
             dpi=180, bbox_inches="tight", facecolor=fig2.get_facecolor())
plt.close(fig2)
print("  Saved 10_decision_framework.png")

# ---------------------------------------------------------------------------
# Visual 03 -- Three-Part Series Overview
# ---------------------------------------------------------------------------
fig3, ax3 = plt.subplots(figsize=(14, 7))
fig3.patch.set_facecolor(WHITE)
ax3.set_facecolor(WHITE)
ax3.set_xlim(0, 14)
ax3.set_ylim(0, 8)
ax3.axis("off")

ax3.text(7, 7.3, "Three-Part Series: From Use Cases to Audit Readiness",
         ha="center", va="center",
         fontsize=18, fontweight="bold", color=DEEP_NAVY)

articles = [
    (2.5, 4.5, "Article 10", "Identify &\nClassify", "What should I\nautomate?",
     SOFT_SAGE, "Use Cases"),
    (7, 4.5, "Article 11", "Build &\nDesign", "How do I build\nit safely?",
     SEA_GREEN, "Workflows"),
    (11.5, 4.5, "Article 12", "Control &\nAudit", "How do I make\nit audit-ready?",
     GOLDEN_YELLOW, "Governance"),
]

for x, y, num, action, question, color, label in articles:
    tc = text_color_for(color)
    box = FancyBboxPatch((x - 2, y - 1.8), 4, 3.6,
                         boxstyle="round,pad=0.2",
                         facecolor=color, edgecolor="none",
                         alpha=0.9)
    ax3.add_patch(box)
    ax3.text(x, y + 1.1, num, ha="center", va="center",
             fontsize=12, fontweight="bold", color=tc, alpha=0.6)
    ax3.text(x, y + 0.3, action, ha="center", va="center",
             fontsize=15, fontweight="bold", color=tc,
             linespacing=1.1)
    ax3.text(x, y - 0.8, question, ha="center", va="center",
             fontsize=12, color=tc, alpha=0.85,
             linespacing=1.2)
    ax3.text(x, y - 2.2, label, ha="center", va="center",
             fontsize=12, fontweight="bold", color=color)

for x_from, x_to in [(4.5, 5.0), (9.0, 9.5)]:
    ax3.annotate("", xy=(x_to, 4.5), xytext=(x_from, 4.5),
                 arrowprops=dict(arrowstyle="-|>", color=OCEAN_TEAL, lw=2.5,
                                 mutation_scale=20))

ax3.text(7, 1.2, "Exploratory  \u2192  Repeatable  \u2192  Audit-Ready",
         ha="center", va="center",
         fontsize=14, fontweight="bold", color=OCEAN_TEAL)

ax3.text(7, 0.5, "Each article builds on the previous. Each maps to a tier of AI workflow maturity.",
         ha="center", va="center",
         fontsize=12, color=DEEP_NAVY, alpha=0.7, style="italic")

fig3.savefig(os.path.join(OUT_DIR, "10_series_overview.png"),
             dpi=180, bbox_inches="tight", facecolor=fig3.get_facecolor())
plt.close(fig3)
print("  Saved 10_series_overview.png")

print("\nAll Article 10 visuals generated.")
