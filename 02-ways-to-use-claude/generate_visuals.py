"""Generate Article 02 visual – Ways to Use Claude (PythonMuse LLC brand)."""

import os
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# ── Paths ────────────────────────────────────────────────────────────
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "visuals")
os.makedirs(OUT, exist_ok=True)

# ── Brand palette ────────────────────────────────────────────────────
DEEP_NAVY = "#002639"
MIDNIGHT_TEAL = "#003144"
BRIGHT_TEAL = "#3ABFB9"
GOLDEN_YELLOW = "#FFD75E"
WARM_GLOW = "#F5D384"
OCEAN_TEAL = "#005F6F"
SOFT_SAGE = "#91BE8E"
SEA_GREEN = "#2BA19A"
WHITE = "#FFFFFF"
LIGHT_GRAY = "#F5F5F5"

DARK_BG = {DEEP_NAVY, MIDNIGHT_TEAL, OCEAN_TEAL, SEA_GREEN}

def text_color_for(bg):
    return WHITE if bg in DARK_BG else DEEP_NAVY

# ── Card data ────────────────────────────────────────────────────────
CARDS = [
    {
        "title": "Web Chat",
        "color": BRIGHT_TEAL,
        "bullets": ["Ask Questions", "Upload Files", "Summarize Docs"],
        "level": "Beginner",
    },
    {
        "title": "IDE Integration\n(VS Code)",
        "color": GOLDEN_YELLOW,
        "bullets": ["Write Code", "Analyze Data", "Automate Tasks"],
        "level": "Intermediate",
    },
    {
        "title": "API & Automation",
        "color": OCEAN_TEAL,
        "bullets": ["Build Apps", "Integrate Systems", "Automate Workflows"],
        "level": "Advanced",
    },
]

def generate():
    fig, ax = plt.subplots(figsize=(14, 8.5))
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8.5)
    ax.axis("off")

    # ── Title & subtitle ─────────────────────────────────────────────
    ax.text(
        7, 8.05, "Ways to Use Claude",
        ha="center", va="center",
        fontsize=24, fontweight="bold", color=DEEP_NAVY,
    )
    ax.text(
        7, 7.55, "Choosing the Right Interface",
        ha="center", va="center",
        fontsize=14, color=OCEAN_TEAL, style="italic",
    )

    # ── Central hub ──────────────────────────────────────────────────
    hub_x, hub_y = 7, 6.55
    hub = FancyBboxPatch(
        (hub_x - 1.1, hub_y - 0.30), 2.2, 0.60,
        boxstyle="round,pad=0.12",
        facecolor=DEEP_NAVY, edgecolor="none", alpha=0.92,
        zorder=3,
    )
    ax.add_patch(hub)
    ax.text(
        hub_x, hub_y, "Using Claude",
        ha="center", va="center",
        fontsize=13, fontweight="bold", color=WHITE, zorder=4,
    )

    # ── Cards ────────────────────────────────────────────────────────
    card_width = 3.6
    card_height = 3.6
    card_xs = [0.7, 5.2, 9.7]
    card_y_top = 5.6

    for i, (cx, card) in enumerate(zip(card_xs, CARDS)):
        cy = card_y_top - card_height

        # Card body (light gray)
        body = FancyBboxPatch(
            (cx, cy), card_width, card_height,
            boxstyle="round,pad=0.15",
            facecolor=LIGHT_GRAY, edgecolor="none", alpha=0.92,
            zorder=1,
        )
        ax.add_patch(body)

        # Header banner
        hdr_h = 0.95 if "\n" in card["title"] else 0.70
        hdr = FancyBboxPatch(
            (cx + 0.15, card_y_top - hdr_h - 0.10), card_width - 0.30, hdr_h,
            boxstyle="round,pad=0.10",
            facecolor=card["color"], edgecolor="none", alpha=0.92,
            zorder=2,
        )
        ax.add_patch(hdr)

        # Header text
        hdr_center_y = card_y_top - 0.10 - hdr_h / 2
        ax.text(
            cx + card_width / 2, hdr_center_y, card["title"],
            ha="center", va="center",
            fontsize=15, fontweight="bold",
            color=text_color_for(card["color"]),
            zorder=3, linespacing=1.1,
        )

        # Bullet points
        bullet_start_y = card_y_top - hdr_h - 0.55
        for j, bullet in enumerate(card["bullets"]):
            by = bullet_start_y - j * 0.55
            # Dot in card accent color
            ax.text(
                cx + 0.45, by, "\u2022",
                ha="center", va="center",
                fontsize=16, color=card["color"], zorder=2,
            )
            ax.text(
                cx + 0.70, by, bullet,
                ha="left", va="center",
                fontsize=13, color=DEEP_NAVY, zorder=2,
            )

        # ── Curved arrow from hub to card header ─────────────────────
        target_x = cx + card_width / 2
        target_y = card_y_top - 0.05

        # Choose arc direction based on column position
        if i == 0:
            conn = "arc3,rad=0.3"
        elif i == 1:
            conn = "arc3,rad=0.0"
        else:
            conn = "arc3,rad=-0.3"

        arrow = FancyArrowPatch(
            (hub_x, hub_y - 0.30),
            (target_x, target_y),
            connectionstyle=conn,
            arrowstyle="->,head_width=0.15,head_length=0.10",
            color=DEEP_NAVY, linewidth=1.8,
            zorder=2, alpha=0.6,
        )
        ax.add_patch(arrow)

    # ── Skill-level progression bar ──────────────────────────────────
    bar_y = 0.55
    bar_h = 0.50
    bar_colors = [BRIGHT_TEAL, GOLDEN_YELLOW, OCEAN_TEAL]
    bar_labels = ["BEGINNER", "INTERMEDIATE", "ADVANCED"]
    bar_widths = [4.0, 4.6, 4.2]
    bar_x = 0.7

    for k in range(3):
        bx = bar_x
        bw = bar_widths[k]

        seg = FancyBboxPatch(
            (bx, bar_y), bw, bar_h,
            boxstyle="round,pad=0.06",
            facecolor=bar_colors[k], edgecolor="none", alpha=0.85,
            zorder=2,
        )
        ax.add_patch(seg)

        ax.text(
            bx + bw / 2, bar_y + bar_h / 2, bar_labels[k],
            ha="center", va="center",
            fontsize=12, fontweight="bold",
            color=text_color_for(bar_colors[k]),
            zorder=3,
        )

        # Arrow indicator between segments
        if k < 2:
            ax.text(
                bx + bw + 0.15, bar_y + bar_h / 2, "\u25B6",
                ha="center", va="center",
                fontsize=10, color=DEEP_NAVY, alpha=0.5, zorder=3,
            )

        bar_x += bw + 0.30

    # ── Footer branding ──────────────────────────────────────────────
    ax.text(
        7, 0.10, "PythonMuse LLC  |  github.com/PythonMuse/ai-ledger",
        ha="center", va="center",
        fontsize=10, color=DEEP_NAVY, alpha=0.50,
    )

    # ── Save ─────────────────────────────────────────────────────────
    out_path = os.path.join(OUT, "02_visual_ways_to_use_Claude.png")
    fig.savefig(
        out_path, dpi=180, bbox_inches="tight",
        facecolor=fig.get_facecolor(),
    )
    plt.close(fig)
    print(f"Saved: {out_path}")

if __name__ == "__main__":
    generate()
