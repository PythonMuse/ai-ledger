"""
Generate Article 12 visuals -- When to Trust AI to Run Your Accounting Workflows.

Visual 01: Hero / front image
  Branded title card.

Visual 02: Audit-Ready Framework
  The six elements needed for audit-ready AI workflows.

Visual 03: COSO to PythonMuse Mapping
  Visual mapping COSO's five components to PythonMuse implementations.

Visual 04: Series Connection Diagram
  Shows how Articles 10, 11, 12 form a progression (reused across series).

Saved to articles/12-audit-ready-ai-workflows/visuals/
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

# -----------------------------------------------------------------------------
# Visual 01 -- Hero / Front Image
# -----------------------------------------------------------------------------
fig1, ax1 = plt.subplots(figsize=(12, 6))
fig1.patch.set_facecolor(WHITE)
ax1.set_facecolor(WHITE)
ax1.set_xlim(0, 12)
ax1.set_ylim(0, 6)
ax1.axis("off")

ax1.text(6, 3.8, "When to Trust AI to Run\nYour Accounting Workflows",
         ha="center", va="center",
         fontsize=26, fontweight="bold", color=DEEP_NAVY,
         linespacing=1.3)

ax1.text(6, 2.4, "And How to Make Them Audit-Ready",
         ha="center", va="center",
         fontsize=14, color=OCEAN_TEAL, style="italic")

ax1.text(6, 1.4, "PythonMuse LLC  |  github.com/PythonMuse/ai-ledger",
         ha="center", va="center",
         fontsize=12, color=OCEAN_TEAL, alpha=0.7)

ax1.plot([2, 10], [1.9, 1.9], color=BRIGHT_TEAL, linewidth=1.5, alpha=0.5)

fig1.savefig(os.path.join(OUT_DIR, "12_visual_front.png"),
             dpi=180, bbox_inches="tight", facecolor=fig1.get_facecolor())
plt.close(fig1)
print("  Saved 12_visual_front.png")

# -----------------------------------------------------------------------------
# Visual 02 -- Audit-Ready Framework (Six Elements)
# -----------------------------------------------------------------------------
fig2, ax2 = plt.subplots(figsize=(14, 8))
fig2.patch.set_facecolor(WHITE)
ax2.set_facecolor(WHITE)
ax2.set_xlim(0, 14)
ax2.set_ylim(0, 10)
ax2.axis("off")

ax2.text(7, 9.3, "The PythonMuse Audit-Ready Framework",
         ha="center", va="center",
         fontsize=20, fontweight="bold", color=DEEP_NAVY)

ax2.text(7, 8.7, "Six elements every audit-ready AI workflow must have",
         ha="center", va="center",
         fontsize=14, color=OCEAN_TEAL, style="italic")

elements = [
    ("1", "Defined\nInputs & Outputs", "What goes in,\nwhat comes out", OCEAN_TEAL),
    ("2", "Masked\nData", "No raw sensitive\ndata to AI", ALERT_RED),
    ("3", "Approved\nPlans", "Reviewed before\nexecution", SEA_GREEN),
    ("4", "Validation\nHooks", "Automated\npre-flight checks", SEA_GREEN),
    ("5", "Logged\nExecution", "status_update.md\naudit trail", BRIGHT_TEAL),
    ("6", "Documented\nWorkflow", "plan.md as\nworkpaper", BRIGHT_TEAL),
]

# Arrange in 2 rows of 3
for i, (num, title, desc, color) in enumerate(elements):
    col = i % 3
    row = i // 3
    x = 2.5 + col * 4.5
    y = 6.5 - row * 3

    tc = text_color_for(color)

    # Outer box
    box = FancyBboxPatch((x - 1.8, y - 1.2), 3.6, 2.4,
                         boxstyle="round,pad=0.2",
                         facecolor=color, edgecolor="none",
                         alpha=0.9)
    ax2.add_patch(box)

    # Number
    ax2.text(x, y + 0.7, num, ha="center", va="center",
             fontsize=16, fontweight="bold", color=tc, alpha=0.5)

    # Title
    ax2.text(x, y + 0.0, title, ha="center", va="center",
             fontsize=13, fontweight="bold", color=tc,
             linespacing=1.1)

    # Description
    ax2.text(x, y - 0.8, desc, ha="center", va="center",
             fontsize=12, color=tc, alpha=0.85,
             linespacing=1.2)

# Center label
ax2.text(7, 1.0, "If any element is missing, the workflow is not audit-ready.",
         ha="center", va="center",
         fontsize=13, fontweight="bold", color=OCEAN_TEAL)

fig2.savefig(os.path.join(OUT_DIR, "12_audit_framework.png"),
             dpi=180, bbox_inches="tight", facecolor=fig2.get_facecolor())
plt.close(fig2)
print("  Saved 12_audit_framework.png")

# -----------------------------------------------------------------------------
# Visual 03 -- COSO to PythonMuse Mapping
# -----------------------------------------------------------------------------
fig3, ax3 = plt.subplots(figsize=(14, 9))
fig3.patch.set_facecolor(WHITE)
ax3.set_facecolor(WHITE)
ax3.set_xlim(0, 14)
ax3.set_ylim(0, 11)
ax3.axis("off")

ax3.text(7, 10.3, "COSO Framework Mapped to AI Workflows",
         ha="center", va="center",
         fontsize=20, fontweight="bold", color=DEEP_NAVY)

ax3.text(7, 9.7, "COSO tells you what. PythonMuse shows you how.",
         ha="center", va="center",
         fontsize=14, color=OCEAN_TEAL, style="italic")

mappings = [
    ("Control\nEnvironment", "CLAUDE.md\nProject Instructions", OCEAN_TEAL),
    ("Risk\nAssessment", "Data Classification\nRisk Templates", SEA_GREEN),
    ("Control\nActivities", "Masking, Hooks\nApproval Gates", BRIGHT_TEAL),
    ("Information &\nCommunication", "plan.md, SKILL.md\nOutput Files", WARM_GLOW),
    ("Monitoring\nActivities", "status_update.md\nPeriodic Review", GOLDEN_YELLOW),
]

for i, (coso, pm, color) in enumerate(mappings):
    y = 8.0 - i * 1.5

    # COSO box (left)
    coso_box = FancyBboxPatch((0.5, y - 0.5), 4, 1,
                              boxstyle="round,pad=0.15",
                              facecolor=DEEP_NAVY, edgecolor="none")
    ax3.add_patch(coso_box)
    ax3.text(2.5, y, coso, ha="center", va="center",
             fontsize=12, fontweight="bold", color=WHITE,
             linespacing=1.1)

    # Arrow
    ax3.annotate("", xy=(5.5, y), xytext=(4.5, y),
                 arrowprops=dict(arrowstyle="-|>", color=color, lw=2,
                                 mutation_scale=18))

    # PythonMuse box (right)
    tc = text_color_for(color)
    pm_box = FancyBboxPatch((5.5, y - 0.5), 5, 1,
                            boxstyle="round,pad=0.15",
                            facecolor=color, edgecolor="none")
    ax3.add_patch(pm_box)
    ax3.text(8, y, pm, ha="center", va="center",
             fontsize=12, fontweight="bold", color=tc,
             linespacing=1.1)

# Column headers
ax3.text(2.5, 9.1, "COSO Component", ha="center", va="center",
         fontsize=14, fontweight="bold", color=DEEP_NAVY)
ax3.text(8, 9.1, "PythonMuse Implementation", ha="center", va="center",
         fontsize=14, fontweight="bold", color=DEEP_NAVY)

# Governance repo reference
ax3.text(7, 0.5, "Templates and examples: github.com/PythonMuse/accounting_and_finance-ai-governance",
         ha="center", va="center",
         fontsize=13, color=OCEAN_TEAL, style="italic")

fig3.savefig(os.path.join(OUT_DIR, "12_coso_mapping.png"),
             dpi=180, bbox_inches="tight", facecolor=fig3.get_facecolor())
plt.close(fig3)
print("  Saved 12_coso_mapping.png")

# -----------------------------------------------------------------------------
# Visual 04 -- Series Connection (shared diagram)
# -----------------------------------------------------------------------------
fig4, ax4 = plt.subplots(figsize=(14, 7))
fig4.patch.set_facecolor(WHITE)
ax4.set_facecolor(WHITE)
ax4.set_xlim(0, 14)
ax4.set_ylim(0, 8)
ax4.axis("off")

ax4.text(7, 7.3, "The Complete Journey: Use Cases to Audit Readiness",
         ha="center", va="center",
         fontsize=20, fontweight="bold", color=DEEP_NAVY)

articles = [
    (2.5, 4.5, "Article 10", "Identify &\nClassify", "What should I\nautomate?",
     SOFT_SAGE, "Exploratory"),
    (7, 4.5, "Article 11", "Build &\nDesign", "How do I build\nit safely?",
     SEA_GREEN, "Repeatable"),
    (11.5, 4.5, "Article 12", "Control &\nAudit", "How do I make\nit audit-ready?",
     GOLDEN_YELLOW, "Audit-Ready"),
]

for x, y, num, action, question, color, label in articles:
    tc = text_color_for(color)
    box = FancyBboxPatch((x - 2, y - 1.8), 4, 3.6,
                         boxstyle="round,pad=0.2",
                         facecolor=color, edgecolor="none")
    ax4.add_patch(box)
    ax4.text(x, y + 1.1, num, ha="center", va="center",
             fontsize=14, fontweight="bold", color=tc)
    ax4.text(x, y + 0.2, action, ha="center", va="center",
             fontsize=16, fontweight="bold", color=tc,
             linespacing=1.1)
    ax4.text(x, y - 0.9, question, ha="center", va="center",
             fontsize=14, color=tc,
             linespacing=1.2)
    ax4.text(x, y - 2.2, label, ha="center", va="center",
             fontsize=14, fontweight="bold", color=color)

# Arrows
for x_from, x_to in [(4.5, 5.0), (9.0, 9.5)]:
    ax4.annotate("", xy=(x_to, 4.5), xytext=(x_from, 4.5),
                 arrowprops=dict(arrowstyle="-|>", color=OCEAN_TEAL, lw=2.5,
                                 mutation_scale=20))

ax4.text(7, 1.2, "Exploratory  \u2192  Repeatable  \u2192  Audit-Ready",
         ha="center", va="center",
         fontsize=15, fontweight="bold", color=OCEAN_TEAL)

ax4.text(7, 0.5, "Each stage builds on the previous. Structure grows with risk.",
         ha="center", va="center",
         fontsize=14, color=DEEP_NAVY, style="italic")

fig4.savefig(os.path.join(OUT_DIR, "12_series_connection.png"),
             dpi=180, bbox_inches="tight", facecolor=fig4.get_facecolor())
plt.close(fig4)
print("  Saved 12_series_connection.png")

print("\nAll Article 12 visuals generated.")
