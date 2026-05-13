"""
Generate article visuals for Article 26 — When Your AI Enters Month-End Close Mode

Produces the following PNGs saved to visuals/:
  26_hero.png           — Hero: "Session Start" vs "25 Prompts Later" comparison
  26_workflow.png       — Bad Workflow vs Structured Pipeline comparison
  26_carousel_01.png    — Carousel Slide 1: Hook
  26_carousel_02.png    — Carousel Slide 2: "This Is Amazing"
  26_carousel_03.png    — Carousel Slide 3: "Just One More Thing"
  26_carousel_04.png    — Carousel Slide 4: "Something Feels Off"
  26_carousel_05.png    — Carousel Slide 5: Why It Happens
  26_carousel_06.png    — Carousel Slide 6: The Fix
  26_carousel_07.png    — Carousel Slide 7: Final Thought / CTA

Branding: white background, Deep Navy text, Bright Teal / Golden Yellow accents.
Per SKILL.md — Matplotlib Visuals (Article Charts).
DPI: 180. Font sizes follow SKILL.md minimums.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import os

# ── Output directory ──────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(SCRIPT_DIR, "visuals")
os.makedirs(OUT_DIR, exist_ok=True)

# ── PythonMuse brand colors ───────────────────────────────────
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

FOOTER_TEXT = "PythonMuse LLC  |  pythonmuse.com"
FOOTER_URL  = "github.com/PythonMuse/ai-ledger"


def save(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  saved -> {path}")


def add_footer(fig, y_bar=0.0, bar_h=0.065):
    """Deep Navy footer bar with PythonMuse branding."""
    bar = fig.add_axes([0.0, y_bar, 1.0, bar_h], facecolor=DEEP_NAVY)
    bar.set_axis_off()
    fig.text(0.5, y_bar + bar_h * 0.55, FOOTER_TEXT,
             ha="center", va="center", fontsize=10, color=WHITE, fontweight="bold")
    fig.text(0.5, y_bar + bar_h * 0.18, FOOTER_URL,
             ha="center", va="center", fontsize=9, color=BRIGHT_TEAL)


def add_header_bar(fig, label, y_bar=0.935, bar_h=0.065):
    """Deep Navy header bar with label."""
    bar = fig.add_axes([0.0, y_bar, 1.0, bar_h], facecolor=DEEP_NAVY)
    bar.set_axis_off()
    fig.text(0.5, y_bar + bar_h * 0.55, label,
             ha="center", va="center", fontsize=12, color=GOLDEN_YELLOW, fontweight="bold")


def card(ax, x, y, w, h, facecolor, edgecolor=None, alpha=1.0, radius=0.03):
    """Draw a rounded rectangle card on the given axes."""
    ec = edgecolor or facecolor
    patch = FancyBboxPatch((x, y), w, h,
                           boxstyle=f"round,pad=0,rounding_size={radius}",
                           facecolor=facecolor, edgecolor=ec,
                           linewidth=1.5, alpha=alpha,
                           transform=ax.transData, clip_on=False)
    ax.add_patch(patch)
    return patch


# ─────────────────────────────────────────────────────────────
# 26_hero.png — Session Start vs 25 Prompts Later
# ─────────────────────────────────────────────────────────────
def make_hero():
    fig = plt.figure(figsize=(12, 6), facecolor=WHITE)
    add_header_bar(fig, "When Your AI Enters Month-End Close Mode  |  Article 26")
    add_footer(fig)

    ax = fig.add_axes([0.03, 0.10, 0.94, 0.80])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis("off")
    ax.set_facecolor(WHITE)

    # ── LEFT PANEL: Session Start ──────────────────────────────
    card(ax, 0.1, 0.2, 4.3, 3.5, facecolor=LIGHT_GRAY, edgecolor=BRIGHT_TEAL, radius=0.08)

    ax.text(2.25, 3.45, "SESSION START", ha="center", va="center",
            fontsize=14, fontweight="bold", color=DEEP_NAVY)
    ax.text(2.25, 3.1, "8:00 AM", ha="center", va="center",
            fontsize=11, color=OCEAN_TEAL, style="italic")

    items_left = [
        (SOFT_SAGE,   "✓  Clean assumptions"),
        (SOFT_SAGE,   "✓  Sharp, consistent output"),
        (SOFT_SAGE,   "✓  Formatting stays put"),
        (SOFT_SAGE,   "✓  Logic ties out"),
        (SOFT_SAGE,   "✓  Numbers match"),
    ]
    for i, (dot_color, text) in enumerate(items_left):
        y_pos = 2.65 - i * 0.48
        card(ax, 0.25, y_pos - 0.12, 3.95, 0.38, facecolor=WHITE, edgecolor=dot_color, radius=0.04)
        ax.text(0.52, y_pos + 0.04, "●", ha="center", va="center",
                fontsize=11, color=dot_color)
        ax.text(0.75, y_pos + 0.04, text, ha="left", va="center",
                fontsize=11, color=DEEP_NAVY)

    # ── ARROW in center ────────────────────────────────────────
    ax.annotate("", xy=(5.8, 2.0), xytext=(4.6, 2.0),
                arrowprops=dict(arrowstyle="-|>", color=OCEAN_TEAL, lw=2.5))
    ax.text(5.2, 2.25, "25 prompts", ha="center", va="center",
            fontsize=9, color=OCEAN_TEAL, style="italic")
    ax.text(5.2, 1.78, "later…", ha="center", va="center",
            fontsize=9, color=OCEAN_TEAL, style="italic")

    # ── RIGHT PANEL: 25 Prompts Later ─────────────────────────
    card(ax, 5.6, 0.2, 4.3, 3.5, facecolor=LIGHT_GRAY, edgecolor=ALERT_RED, radius=0.08)

    ax.text(7.75, 3.45, "25 PROMPTS LATER", ha="center", va="center",
            fontsize=14, fontweight="bold", color=DEEP_NAVY)
    ax.text(7.75, 3.1, "11:30 PM", ha="center", va="center",
            fontsize=11, color=ALERT_RED, style="italic")

    items_right = [
        (ALERT_RED,    "✗  Margin % quietly shifted"),
        (ALERT_RED,    "✗  Excluded cost came back"),
        (ALERT_ORANGE, "⚠  Formatting changed again"),
        (ALERT_ORANGE, "⚠  Earlier logic ignored"),
        (ALERT_RED,    "✗  Still sounds confident"),
    ]
    for i, (dot_color, text) in enumerate(items_right):
        y_pos = 2.65 - i * 0.48
        card(ax, 5.75, y_pos - 0.12, 3.95, 0.38, facecolor=WHITE, edgecolor=dot_color, radius=0.04)
        ax.text(6.02, y_pos + 0.04, "●", ha="center", va="center",
                fontsize=11, color=dot_color)
        ax.text(6.25, y_pos + 0.04, text, ha="left", va="center",
                fontsize=11, color=DEEP_NAVY)

    save(fig, "26_hero.png")


# ─────────────────────────────────────────────────────────────
# 26_workflow.png — Bad Workflow vs Structured Pipeline
# ─────────────────────────────────────────────────────────────
def make_workflow():
    fig = plt.figure(figsize=(12, 6.5), facecolor=WHITE)
    add_header_bar(fig, "One Giant Session vs. Structured Pipeline")
    add_footer(fig)

    ax = fig.add_axes([0.02, 0.09, 0.96, 0.82])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.5)
    ax.axis("off")
    ax.set_facecolor(WHITE)

    # ── LEFT: The Giant Session ────────────────────────────────
    ax.text(2.25, 4.25, "❌  The Giant Session", ha="center", va="center",
            fontsize=14, fontweight="bold", color=ALERT_RED)
    ax.text(2.25, 3.92, "Everything in one conversation", ha="center", va="center",
            fontsize=10, color=OCEAN_TEAL, style="italic")

    card(ax, 0.1, 0.3, 4.3, 3.4, facecolor="#FFF5F5", edgecolor=ALERT_RED,
         alpha=0.9, radius=0.08)

    chaos_items = [
        "📎  trial balance upload",
        "📝  variance commentary",
        "🔄  exclude legal fees",
        "📊  marketing moved depts",
        "💬  adjust EBITDA",
        "🖼️  screenshot from CFO",
        "📎  another file uploaded",
        "❓  + 12 more prompts…",
    ]
    for i, item in enumerate(chaos_items):
        col = ALERT_RED if i % 2 == 0 else ALERT_ORANGE
        y_pos = 3.35 - i * 0.38
        ax.text(2.25, y_pos, item, ha="center", va="center",
                fontsize=9.5, color=col, style="italic" if i % 3 == 2 else "normal")

    ax.text(2.25, 0.45, "→  Context drift enters here", ha="center",
            fontsize=9, color=ALERT_RED, style="italic")

    # ── Divider ────────────────────────────────────────────────
    ax.plot([5.0, 5.0], [0.2, 4.35], color=OCEAN_TEAL, lw=1.5, linestyle="--", alpha=0.5)

    # ── RIGHT: Structured Pipeline ────────────────────────────
    ax.text(7.75, 4.25, "✓  Structured Pipeline", ha="center", va="center",
            fontsize=14, fontweight="bold", color=SEA_GREEN)
    ax.text(7.75, 3.92, "Focused sessions with checkpoints", ha="center", va="center",
            fontsize=10, color=OCEAN_TEAL, style="italic")

    pipeline_steps = [
        (BRIGHT_TEAL,   "1  Raw Data & Assumptions"),
        (SEA_GREEN,     "2  Cleaning Session"),
        (OCEAN_TEAL,    "3  Calculations Session"),
        (BRIGHT_TEAL,   "4  Commentary Session"),
        (GOLDEN_YELLOW, "5  Checkpoint → status_update.md"),
        (SOFT_SAGE,     "6  Review & Export"),
    ]
    step_y_start = 3.5
    for i, (color, label) in enumerate(pipeline_steps):
        y_pos = step_y_start - i * 0.52
        card(ax, 5.25, y_pos - 0.17, 4.45, 0.38,
             facecolor=color if color == GOLDEN_YELLOW else WHITE,
             edgecolor=color, radius=0.05)
        ax.text(5.52, y_pos + 0.04, "►", ha="left", va="center",
                fontsize=10, color=color, fontweight="bold")
        ax.text(5.82, y_pos + 0.04, label, ha="left", va="center",
                fontsize=10, color=DEEP_NAVY, fontweight="bold" if color == GOLDEN_YELLOW else "normal")

        if i < len(pipeline_steps) - 1:
            ax.annotate("", xy=(7.5, y_pos - 0.19), xytext=(7.5, y_pos - 0.06),
                        arrowprops=dict(arrowstyle="-|>", color=color, lw=1.2))

    ax.text(7.75, 0.55, "→  Session stays sharp", ha="center",
            fontsize=9, color=SEA_GREEN, style="italic")

    save(fig, "26_workflow.png")


# ─────────────────────────────────────────────────────────────
# Social Carousel — 7 square slides (1080×1080 equiv.)
# ─────────────────────────────────────────────────────────────
CAROUSEL_SIZE = (7.5, 7.5)


def carousel_base(title_text, subtitle_text=None, bg_color=WHITE):
    """Create a square carousel slide with header, footer, and optional subtitle."""
    fig = plt.figure(figsize=CAROUSEL_SIZE, facecolor=bg_color)

    # Header bar
    bar_top = fig.add_axes([0.0, 0.88, 1.0, 0.12], facecolor=DEEP_NAVY)
    bar_top.set_axis_off()

    # Footer bar
    bar_bot = fig.add_axes([0.0, 0.0, 1.0, 0.09], facecolor=DEEP_NAVY)
    bar_bot.set_axis_off()
    fig.text(0.5, 0.055, FOOTER_TEXT, ha="center", va="center",
             fontsize=10, color=WHITE, fontweight="bold")
    fig.text(0.5, 0.018, FOOTER_URL, ha="center", va="center",
             fontsize=9, color=BRIGHT_TEAL)

    # Header label
    fig.text(0.5, 0.944, title_text, ha="center", va="center",
             fontsize=13, color=GOLDEN_YELLOW, fontweight="bold")
    if subtitle_text:
        fig.text(0.5, 0.91, subtitle_text, ha="center", va="center",
                 fontsize=10, color=WARM_GLOW)

    # Content axes
    ax = fig.add_axes([0.06, 0.11, 0.88, 0.76])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis("off")
    ax.set_facecolor(bg_color)
    return fig, ax


def make_carousel_01():
    """Hook slide."""
    fig, ax = carousel_base("Article 26  |  PythonMuse")
    ax.text(5, 6.5, "Your AI just entered", ha="center", va="center",
            fontsize=22, color=DEEP_NAVY, fontweight="bold")
    ax.text(5, 5.5, "month-end close mode.", ha="center", va="center",
            fontsize=22, color=ALERT_RED, fontweight="bold")
    ax.plot([1, 9], [4.8, 4.8], color=OCEAN_TEAL, lw=1.5, alpha=0.4)
    ax.text(5, 3.9, "Still functioning.", ha="center", va="center",
            fontsize=14, color=OCEAN_TEAL)
    ax.text(5, 3.2, "Slightly overwhelmed.", ha="center", va="center",
            fontsize=14, color=OCEAN_TEAL)
    ax.text(5, 2.5, "Confidently inconsistent.", ha="center", va="center",
            fontsize=14, color=ALERT_ORANGE, style="italic")
    ax.plot([1, 9], [1.6, 1.6], color=OCEAN_TEAL, lw=1.5, alpha=0.4)
    ax.text(5, 0.9, "Here's what's happening and how to fix it →",
            ha="center", va="center", fontsize=11, color=OCEAN_TEAL, style="italic")
    save(fig, "26_carousel_01.png")


def make_carousel_02():
    """This Is Amazing slide."""
    fig, ax = carousel_base("The Honeymoon Phase")
    ax.text(5, 7.0, "The session started", ha="center", va="center",
            fontsize=18, color=DEEP_NAVY, fontweight="bold")
    ax.text(5, 6.2, "beautifully.", ha="center", va="center",
            fontsize=18, color=BRIGHT_TEAL, fontweight="bold")

    checks = [
        "✓  Professional tone",
        "✓  Clear explanations",
        "✓  Numbers that tie",
        "✓  Sounds board-ready",
    ]
    for i, text in enumerate(checks):
        card(ax, 1.0, 4.6 - i * 1.1, 8.0, 0.85,
             facecolor=WHITE, edgecolor=BRIGHT_TEAL, radius=0.06)
        ax.text(1.5, 5.08 - i * 1.1, text, ha="left", va="center",
                fontsize=13, color=DEEP_NAVY)

    ax.text(5, 0.5, '"I have discovered free labor."',
            ha="center", va="center", fontsize=11, color=OCEAN_TEAL, style="italic")
    save(fig, "26_carousel_02.png")


def make_carousel_03():
    """Just One More Thing slide."""
    fig, ax = carousel_base("Then the session grew…")
    ax.text(5, 7.2, '"Just one more thing."', ha="center", va="center",
            fontsize=18, color=DEEP_NAVY, fontweight="bold", style="italic")

    prompts = [
        '"Exclude one-time legal fees"',
        '"Marketing moved departments"',
        '"Ignore the accrual reversal"',
        '"Use adjusted EBITDA"',
        '"No tables. Actually, tables."',
        '"I uploaded another file."',
    ]
    for i, p in enumerate(prompts):
        col = ALERT_ORANGE if i % 2 == 0 else ALERT_RED
        ax.text(5, 5.9 - i * 0.88, p, ha="center", va="center",
                fontsize=11, color=col, style="italic")

    ax.plot([1, 9], [0.85, 0.85], color=OCEAN_TEAL, lw=1, alpha=0.4)
    ax.text(5, 0.45, "Twenty prompts later…  context has drifted.",
            ha="center", va="center", fontsize=10, color=OCEAN_TEAL, style="italic")
    save(fig, "26_carousel_03.png")


def make_carousel_04():
    """Something Feels Off slide."""
    fig, ax = carousel_base("Something Feels Off")
    ax.text(5, 7.1, "The output still sounds smart.", ha="center", va="center",
            fontsize=15, color=DEEP_NAVY, fontweight="bold")
    ax.text(5, 6.35, "That's what makes it dangerous.", ha="center", va="center",
            fontsize=13, color=ALERT_RED, fontweight="bold")
    ax.plot([1, 9], [5.7, 5.7], color=OCEAN_TEAL, lw=1, alpha=0.4)

    signs = [
        ("Gross margin:  42%  →  39%", ALERT_RED),
        ("Excluded cost quietly came back", ALERT_ORANGE),
        ("Terminology changed mid-session", ALERT_ORANGE),
        ('"I thought that was the version"', OCEAN_TEAL),
    ]
    for i, (text, color) in enumerate(signs):
        ax.text(5, 4.9 - i * 1.1, text, ha="center", va="center",
                fontsize=12, color=color, style="italic" if i == 3 else "normal")

    ax.text(5, 0.55, "The AI didn't lie. It compressed.",
            ha="center", va="center", fontsize=11, color=DEEP_NAVY, fontweight="bold")
    save(fig, "26_carousel_04.png")


def make_carousel_05():
    """Why It Happens slide."""
    fig, ax = carousel_base("Why This Happens")
    ax.text(5, 7.1, "The Context Window", ha="center", va="center",
            fontsize=20, color=BRIGHT_TEAL, fontweight="bold")
    ax.text(5, 6.3, "= AI's working memory", ha="center", va="center",
            fontsize=14, color=DEEP_NAVY)

    ax.plot([1, 9], [5.55, 5.55], color=OCEAN_TEAL, lw=1, alpha=0.4)

    ax.text(5, 4.9, "As the session grows:", ha="center", va="center",
            fontsize=13, color=OCEAN_TEAL)

    bullets = [
        "Earlier instructions get compressed",
        "Nuance gets summarized away",
        "Assumptions lose priority",
        "Output slowly drifts",
    ]
    for i, b in enumerate(bullets):
        ax.text(2.5, 4.0 - i * 0.88, "►", ha="center", va="center",
                fontsize=12, color=ALERT_ORANGE)
        ax.text(3.0, 4.0 - i * 0.88, b, ha="left", va="center",
                fontsize=11, color=DEEP_NAVY)

    card(ax, 0.8, 0.15, 8.4, 0.65, facecolor=WARM_GLOW, edgecolor=GOLDEN_YELLOW, radius=0.05)
    ax.text(5, 0.48, "Same reason month-end close gets messy by 11:30 PM.",
            ha="center", va="center", fontsize=10, color=DEEP_NAVY, fontweight="bold")
    save(fig, "26_carousel_05.png")


def make_carousel_06():
    """The Fix slide."""
    fig, ax = carousel_base("How to Reduce Context Drift")

    fixes = [
        (BRIGHT_TEAL,   "1",  "Treat each session as temporary"),
        (SEA_GREEN,     "2",  "Externalize context → SKILL files"),
        (OCEAN_TEAL,    "3",  "Checkpoint with status_update.md"),
        (GOLDEN_YELLOW, "4",  "Separate sessions by task type"),
    ]
    ax.text(5, 7.5, "4 Controls", ha="center", va="center",
            fontsize=20, color=DEEP_NAVY, fontweight="bold")
    ax.text(5, 6.8, "Accountants already know these.", ha="center", va="center",
            fontsize=12, color=OCEAN_TEAL, style="italic")

    for i, (color, num, label) in enumerate(fixes):
        y = 5.5 - i * 1.25
        card(ax, 0.5, y - 0.3, 9.0, 0.85,
             facecolor=color if color == GOLDEN_YELLOW else WHITE,
             edgecolor=color, radius=0.06)
        circle = plt.Circle((1.2, y + 0.12), 0.28, color=color, zorder=3)
        ax.add_patch(circle)
        ax.text(1.2, y + 0.12, num, ha="center", va="center",
                fontsize=13, color=DEEP_NAVY if color == GOLDEN_YELLOW else WHITE,
                fontweight="bold", zorder=4)
        ax.text(2.0, y + 0.12, label, ha="left", va="center",
                fontsize=12, color=DEEP_NAVY, fontweight="bold")

    save(fig, "26_carousel_06.png")


def make_carousel_07():
    """Final Thought / CTA slide."""
    fig, ax = carousel_base("Final Thought  |  pythonmuse.com")
    ax.text(5, 7.1, "The future of AI in accounting", ha="center", va="center",
            fontsize=15, color=DEEP_NAVY, fontweight="bold")
    ax.text(5, 6.4, "belongs to the teams that know how to:", ha="center", va="center",
            fontsize=13, color=OCEAN_TEAL)

    traits = [
        "structure memory",
        "preserve assumptions",
        "checkpoint logic",
        "build repeatable processes",
    ]
    for i, t in enumerate(traits):
        ax.text(5, 5.3 - i * 0.88, t, ha="center", va="center",
                fontsize=13, color=BRIGHT_TEAL, fontweight="bold")

    ax.plot([1, 9], [1.55, 1.55], color=GOLDEN_YELLOW, lw=2)
    ax.text(5, 1.1, "Accountants already call these:", ha="center", va="center",
            fontsize=11, color=DEEP_NAVY)
    ax.text(5, 0.55, "controls  ·  documentation  ·  governance",
            ha="center", va="center", fontsize=11, color=OCEAN_TEAL, fontweight="bold")
    save(fig, "26_carousel_07.png")


# ─────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating Article 26 visuals…")
    make_hero()
    make_workflow()
    make_carousel_01()
    make_carousel_02()
    make_carousel_03()
    make_carousel_04()
    make_carousel_05()
    make_carousel_06()
    make_carousel_07()
    print("Done. All visuals saved to visuals/")
