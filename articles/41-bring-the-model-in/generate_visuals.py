"""Generate branded visuals for Article 41 -- If the Data Can't Leave, Bring
the Model In.

Run from the article folder:
    python generate_visuals.py

Produces four article visuals plus two social cards in ./visuals/.
"""

import os

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

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

LIGHT_GRAY = "#F5F5F5"
LIGHT_TEAL = "#EDF5F5"

plt.rcParams["font.family"] = "sans-serif"

# Font sizes are set at the slide-readable level from SKILL.md (focal card
# text ~28-36pt, header titles in the 40s-50s, footer ~19pt on these large
# canvases). All positions are fractions of the figure (0-1): if a layout
# feels cramped, grow the canvas inches in blank_axes() -- do not shrink text.

FOOTER = "PythonMuse LLC  |  www.pythonmuse.com"

# FancyBboxPatch inflates each box by `pad` on every side. Keep it small so the
# computed gaps survive and connector arrows stay visible.
BOX_PAD = 0.004

LIGHT_FILLS = (BRIGHT_TEAL, GOLDEN_YELLOW, WARM_GLOW, SOFT_SAGE, LIGHT_GRAY,
               LIGHT_TEAL, WHITE)


def text_colors(fill):
    """Return (title_color, secondary_color) for text sitting on `fill`."""
    if fill in (BRIGHT_TEAL, SOFT_SAGE):
        return DEEP_NAVY, DEEP_NAVY
    if fill in LIGHT_FILLS:
        return DEEP_NAVY, OCEAN_TEAL
    return WHITE, WARM_GLOW


def blank_axes(figsize):
    fig, ax = plt.subplots(figsize=figsize, facecolor=WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_position([0, 0, 1, 1])
    return fig, ax


def add_header_bar(fig, title, subtitle, height, title_size, subtitle_size,
                   title_y=0.36, subtitle_y=0.74):
    """Deep Navy bar across the top, in figure coordinates throughout."""
    fig.patches.append(FancyBboxPatch(
        (0, 1 - height), 1, height, boxstyle="square,pad=0",
        transform=fig.transFigure, facecolor=DEEP_NAVY, edgecolor="none",
        zorder=0))
    fig.text(0.03, 1 - height * title_y, title, fontsize=title_size,
             fontweight="bold", color=WHITE, va="center", ha="left")
    fig.text(0.03, 1 - height * subtitle_y, subtitle, fontsize=subtitle_size,
             color=WARM_GLOW, va="center", ha="left")


def box(ax, xy, w, h, fill, edge=None, lw=0, zorder=2, rounding=0.02):
    ax.add_patch(FancyBboxPatch(
        xy, w, h, boxstyle=f"round,pad={BOX_PAD},rounding_size={rounding}",
        facecolor=fill, edgecolor=edge or "none", linewidth=lw, zorder=zorder))


def arrow(ax, start, end, color=OCEAN_TEAL, width=3.2, scale=26, zorder=5):
    ax.annotate("", xy=end, xytext=start,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=width,
                                mutation_scale=scale, shrinkA=0, shrinkB=0),
                zorder=zorder)


def footer(fig, y=0.012, size=19):
    fig.text(0.5, y, FOOTER, fontsize=size, color=OCEAN_TEAL,
             ha="center", va="center", alpha=0.80)


def save(fig, name):
    os.makedirs("visuals", exist_ok=True)
    fig.savefig(f"visuals/{name}", dpi=180, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)


# ---------------------------------------------------------------------------
# 1. Hero -- where does the model run?
# ---------------------------------------------------------------------------
SPECTRUM = [
    ("Consumer\napp", "Free or personal\nchat tools", LIGHT_GRAY),
    ("Enterprise\nsubscription", "ChatGPT Enterprise,\nGemini Enterprise,\nM365 Copilot", SOFT_SAGE),
    ("Your cloud\naccount", "Azure OpenAI,\nAmazon Bedrock,\nGoogle Agent Platform", BRIGHT_TEAL),
    ("Company\nhardware", "Approved workstation\nor internal server,\nshared by browser", OCEAN_TEAL),
    ("Air-gapped", "No network\nconnection\nat all", DEEP_NAVY),
]


def make_hero():
    fig, ax = blank_axes((24, 14))
    add_header_bar(fig, "Where Does the Model Need to Run?",
                   "Not \"can we use AI?\" but \"where can this data go?\"",
                   height=0.165, title_size=50, subtitle_size=30)

    n = len(SPECTRUM)
    gap = 0.026
    w = (0.94 - gap * (n - 1)) / n
    y, h = 0.360, 0.420

    for i, (label, caption, fill) in enumerate(SPECTRUM):
        x = 0.03 + i * (w + gap)
        edge = OCEAN_TEAL if fill == LIGHT_GRAY else None
        box(ax, (x, y), w, h, fill, edge=edge, lw=2.5)
        title_col, sub_col = text_colors(fill)
        ax.text(x + w / 2, y + h * 0.75, label, fontsize=33, fontweight="bold",
                color=title_col, ha="center", va="center", linespacing=1.05,
                zorder=4)
        ax.text(x + w / 2, y + h * 0.30, caption, fontsize=23, color=sub_col,
                ha="center", va="center", linespacing=1.25, zorder=4)
        if i < n - 1:
            arrow(ax, (x + w + 0.003, y + h / 2), (x + w + gap - 0.003, y + h / 2),
                  color=SEA_GREEN, width=3.5, scale=28)

    # Two rising gauges under the spectrum.
    for k, (label, yy) in enumerate((("MORE CONTROL", 0.285), ("MORE RESPONSIBILITY", 0.215))):
        arrow(ax, (0.03, yy), (0.97, yy), color=SEA_GREEN if k == 0 else OCEAN_TEAL,
              width=5, scale=36, zorder=1)
        ax.text(0.5, yy + 0.026, label, fontsize=25, fontweight="bold",
                color=OCEAN_TEAL, ha="center", va="center",
                bbox=dict(facecolor=WHITE, edgecolor="none", pad=4), zorder=6)

    box(ax, (0.03, 0.045), 0.94, 0.105, GOLDEN_YELLOW)
    ax.text(0.5, 0.0975,
            "Match where the model runs to what your contracts and data allow.",
            fontsize=31, fontweight="bold", color=DEEP_NAVY, ha="center",
            va="center", zorder=4)
    footer(fig, y=0.012)
    save(fig, "41_hero.png")


# ---------------------------------------------------------------------------
# 2. Division of labor -- retrieve, calculate, judge
# ---------------------------------------------------------------------------
ROLES = [
    ("AI CO-PILOT", "Retrieves and cites",
     ["Finds the inputs", "Names the source document", "Says \"not enough evidence\""],
     BRIGHT_TEAL),
    ("EXCEL / PYTHON", "Calculates",
     ["DCF, Black-Scholes", "Distribution waterfall", "Same inputs, same answer"],
     OCEAN_TEAL),
    ("VALUATION SPECIALIST", "Judges",
     ["Sets the pass bar", "Reviews the evidence", "Approves the conclusion"],
     DEEP_NAVY),
]


def make_division_of_labor():
    fig, ax = blank_axes((29, 15))
    add_header_bar(fig, "Let Excel Keep Doing What Excel Is Good At",
                   "A cleaner division of responsibilities for valuation work.",
                   height=0.150, title_size=50, subtitle_size=30)

    n = len(ROLES)
    gap = 0.045
    w = (0.94 - gap * (n - 1)) / n
    y, h = 0.215, 0.565

    for i, (who, verb, bullets, fill) in enumerate(ROLES):
        x = 0.03 + i * (w + gap)
        box(ax, (x, y), w, h, fill)
        title_col, sub_col = text_colors(fill)
        ax.text(x + w / 2, y + h - 0.055, who, fontsize=26, fontweight="bold",
                color=sub_col if fill != BRIGHT_TEAL else DEEP_NAVY,
                ha="center", va="center", zorder=4)
        ax.text(x + w / 2, y + h - 0.150, verb, fontsize=40, fontweight="bold",
                color=title_col, ha="center", va="center", zorder=4)
        # Bullets on a light inset so they read on every fill.
        inset_y, inset_h = y + 0.030, h - 0.240
        box(ax, (x + 0.020, inset_y), w - 0.040, inset_h, WHITE, rounding=0.015,
            zorder=3)
        for j, b in enumerate(bullets):
            by = inset_y + inset_h - (j + 0.5) * inset_h / len(bullets)
            ax.text(x + 0.042, by, "•  " + b, fontsize=27, color=DEEP_NAVY,
                    ha="left", va="center", zorder=4)
        if i < n - 1:
            arrow(ax, (x + w + 0.006, y + h / 2), (x + w + gap - 0.006, y + h / 2),
                  color=SEA_GREEN, width=4.5, scale=36)

    box(ax, (0.03, 0.045), 0.94, 0.110, GOLDEN_YELLOW)
    ax.text(0.5, 0.100,
            "Excel does not need to be fired. It just may finally get a co-pilot.",
            fontsize=32, fontweight="bold", color=DEEP_NAVY, ha="center",
            va="center", zorder=4)
    footer(fig, y=0.012)
    save(fig, "41_division_of_labor.png")


# ---------------------------------------------------------------------------
# 3. Cross-client retrieval -- the filter sits before the model
# ---------------------------------------------------------------------------
def flow_row(ax, y, h, steps, widths, gap=0.030, arrow_color=OCEAN_TEAL):
    """Draw a left-to-right row of (label, sub, fill, edge) boxes."""
    x = 0.205
    for i, ((label, sub, fill, edge), w) in enumerate(zip(steps, widths)):
        box(ax, (x, y), w, h, fill, edge=edge, lw=3 if edge else 0)
        title_col, sub_col = text_colors(fill)
        if fill == ALERT_RED:
            title_col, sub_col = WHITE, WHITE
        ax.text(x + w / 2, y + h * 0.66, label, fontsize=27, fontweight="bold",
                color=title_col, ha="center", va="center", linespacing=1.05,
                zorder=4)
        ax.text(x + w / 2, y + h * 0.26, sub, fontsize=21, color=sub_col,
                ha="center", va="center", linespacing=1.15, zorder=4)
        if i < len(steps) - 1:
            arrow(ax, (x + w + 0.004, y + h / 2), (x + w + gap - 0.004, y + h / 2),
                  color=arrow_color, width=4, scale=32)
        x += w + gap


def make_cross_client():
    fig, ax = blank_axes((24, 16))
    add_header_bar(fig, "A Prompt Is Not an Access Control",
                   "Cross-client retrieval: the permission check has to happen before the model sees anything.",
                   height=0.140, title_size=50, subtitle_size=27)

    widths = [0.170, 0.170, 0.150, 0.180]
    row_h = 0.215

    # Wrong way.
    wy = 0.585
    box(ax, (0.03, wy), 0.150, row_h, ALERT_RED)
    ax.text(0.105, wy + row_h / 2, "WRONG", fontsize=32, fontweight="bold",
            color=WHITE, ha="center", va="center", zorder=4)
    flow_row(ax, wy, row_h, [
        ("Every client's\ndeals", "One shared\nknowledge base", LIGHT_GRAY, OCEAN_TEAL),
        ("Polite\nPost-it note", "\"Please respect\nconfidentiality\"", GOLDEN_YELLOW, None),
        ("Model", "Sees everything", MIDNIGHT_TEAL, None),
        ("Another client's\ndeal", "A beautiful example\nyou can't use", ALERT_RED, None),
    ], widths, arrow_color=ALERT_RED)

    # Right way.
    ry = 0.275
    box(ax, (0.03, ry), 0.150, row_h, SEA_GREEN)
    ax.text(0.105, ry + row_h / 2, "RIGHT", fontsize=32, fontweight="bold",
            color=WHITE, ha="center", va="center", zorder=4)
    flow_row(ax, ry, row_h, [
        ("Every client's\ndeals", "One shared\nknowledge base", LIGHT_GRAY, OCEAN_TEAL),
        ("Permission\nfilter", "The ethical wall,\nenforced in code", BRIGHT_TEAL, None),
        ("Model", "Sees only this\nengagement", MIDNIGHT_TEAL, None),
        ("Cited answer", "From authorized\ndocuments only", SOFT_SAGE, None),
    ], widths, arrow_color=SEA_GREEN)

    ax.text(0.5, 0.540,
            "The model did exactly what it was asked. The system still failed.",
            fontsize=24, color=OCEAN_TEAL, style="italic", ha="center",
            va="center")

    box(ax, (0.03, 0.050), 0.94, 0.130, GOLDEN_YELLOW)
    ax.text(0.5, 0.135,
            "If a prompt worked as an access control, we could replace half of",
            fontsize=29, fontweight="bold", color=DEEP_NAVY, ha="center",
            va="center", zorder=4)
    ax.text(0.5, 0.088, "cybersecurity with very polite Post-it notes.",
            fontsize=29, fontweight="bold", color=DEEP_NAVY, ha="center",
            va="center", zorder=4)
    footer(fig, y=0.014)
    save(fig, "41_cross_client.png")


# ---------------------------------------------------------------------------
# 4. Benchmark scorecard
# ---------------------------------------------------------------------------
SCORE_COLUMNS = ["Question", "Pass bar\n(set first)", "Small local\nmodel",
                 "Large local\nmodel", "Approved\nenterprise model"]
SCORE_ROWS = [
    # (question, bar, small, large, enterprise, (small_ok, large_ok))
    ("Did it get the answer right?", "95% or more", "80%", "100%", "?", (False, True)),
    ("Did it cite the correct source?", "95% or more", "84.2%", "94.7%", "?", (False, False)),
    ("Did it invent anything?", "Zero", "1", "1", "?", (False, False)),
    ("How often did an analyst correct it?", "Record it", "5 fields", "1 field", "?", (None, None)),
    ("How much time did it save?", "Record it", "Reviewer\nrecords", "Reviewer\nrecords", "?", (None, None)),
    ("What did it cost to run?", "Record it", "Hardware, power,\nupkeep", "Hardware, power,\nupkeep", "Subscription\nor usage", (None, None)),
]


def make_scorecard():
    fig, ax = blank_axes((24, 24))
    add_header_bar(fig, "Your Work. Your Data. Your Acceptance Criteria.",
                   "A task-specific benchmark: same finished engagements, every model, one pass bar.",
                   height=0.097, title_size=48, subtitle_size=28)

    xs = [0.03, 0.335, 0.500, 0.655, 0.810]
    ws = [0.300, 0.160, 0.150, 0.150, 0.160]
    top = 0.865
    head_h, row_h, gap = 0.070, 0.070, 0.008

    for x, w, label in zip(xs, ws, SCORE_COLUMNS):
        box(ax, (x, top - head_h), w, head_h, DEEP_NAVY, rounding=0.012)
        ax.text(x + w / 2, top - head_h / 2, label, fontsize=23,
                fontweight="bold", color=WHITE, ha="center", va="center",
                linespacing=1.1, zorder=4)

    for r, (q, bar, small, large, ent, oks) in enumerate(SCORE_ROWS):
        y = top - head_h - gap - (r + 1) * row_h - r * gap
        fill = LIGHT_TEAL if r % 2 == 0 else WHITE
        values = [q, bar, small, large, ent]
        for c, (x, w, v) in enumerate(zip(xs, ws, values)):
            cell_fill = fill
            color = DEEP_NAVY
            weight = "normal"
            if c in (2, 3) and oks[c - 2] is not None:
                cell_fill = SOFT_SAGE if oks[c - 2] else "#F6D5D5"
                weight = "bold"
            box(ax, (x, y), w, row_h, cell_fill, edge=OCEAN_TEAL, lw=1.2,
                rounding=0.010)
            if c == 0:
                ax.text(x + 0.012, y + row_h / 2, v, fontsize=23,
                        fontweight="bold", color=DEEP_NAVY, ha="left",
                        va="center", zorder=4)
            else:
                ax.text(x + w / 2, y + row_h / 2, v, fontsize=22 if "\n" in v else 25,
                        fontweight=weight, color=OCEAN_TEAL if v == "?" else color,
                        style="italic" if v == "?" else "normal",
                        ha="center", va="center", linespacing=1.1, zorder=4)

    # Result row.
    n = len(SCORE_ROWS)
    y = top - head_h - gap - (n + 1) * row_h - n * gap - 0.012
    result = ["Meets the pass bar?", "", "No", "No", "Run the same\ncleared set"]
    for c, (x, w, v) in enumerate(zip(xs, ws, result)):
        if c == 1:
            continue
        fill = MIDNIGHT_TEAL if c == 0 else (ALERT_RED if v == "No" else WHITE)
        box(ax, (x, y), w if c else ws[0] + ws[1] + 0.005, row_h, fill,
            edge=OCEAN_TEAL if fill == WHITE else None, lw=1.5, rounding=0.010)
        ax.text((x + (w if c else ws[0] + ws[1] + 0.005) / 2) if c else x + 0.012,
                y + row_h / 2, v, fontsize=27 if c != 4 else 21,
                fontweight="bold",
                color=WHITE if fill != WHITE else OCEAN_TEAL,
                ha="center" if c else "left", va="center", linespacing=1.1,
                zorder=4)

    ax.text(0.03, y - 0.040,
            "Small and large columns: example results from the companion test kit (hand-written responses, not a real model).",
            fontsize=19, color=OCEAN_TEAL, style="italic", ha="left", va="center")
    ax.text(0.03, y - 0.070,
            "Enterprise: the same cleared test set, cleared for sending to that vendor, not just for internal use.",
            fontsize=19, color=OCEAN_TEAL, style="italic", ha="left", va="center")

    box(ax, (0.03, 0.035), 0.94, 0.090, GOLDEN_YELLOW)
    ax.text(0.5, 0.080,
            "Every answer right, one invented citation: still a fail.",
            fontsize=31, fontweight="bold", color=DEEP_NAVY, ha="center",
            va="center", zorder=4)
    footer(fig, y=0.010)
    save(fig, "41_scorecard.png")


# ---------------------------------------------------------------------------
# 5. Social quote card (16:9) -- a prompt is not an access control
# ---------------------------------------------------------------------------
def make_social_prompt_quote():
    fig, ax = blank_axes((16, 9))
    box(ax, (0.03, 0.10), 0.94, 0.85, DEEP_NAVY, rounding=0.03)
    ax.text(0.085, 0.80, "“", fontsize=150, color=GOLDEN_YELLOW,
            ha="center", va="center", fontweight="bold", zorder=4)
    ax.text(0.5, 0.58, "A prompt is not\nan access control.",
            fontsize=60, fontweight="bold", color=WHITE, ha="center",
            va="center", linespacing=1.2, zorder=4)
    ax.text(0.5, 0.235, "If the Data Can't Leave, Bring the Model In",
            fontsize=26, color=WARM_GLOW, style="italic", ha="center",
            va="center", zorder=4)
    footer(fig, y=0.050, size=20)
    save(fig, "41_social_prompt_quote.png")


# ---------------------------------------------------------------------------
# 6. Social square -- local does not mean secure
# ---------------------------------------------------------------------------
def make_social_square():
    fig, ax = blank_axes((13, 13))
    header_h = 0.235
    fig.patches.append(FancyBboxPatch(
        (0, 1 - header_h), 1, header_h, boxstyle="square,pad=0",
        transform=fig.transFigure, facecolor=DEEP_NAVY, edgecolor="none",
        zorder=0))
    fig.text(0.05, 0.955, "Local Does Not\nMean Secure.", fontsize=50,
             fontweight="bold", color=WHITE, va="top", ha="left",
             linespacing=1.1)
    fig.text(0.05, 0.800, "No cybersecurity fairy dust included.",
             fontsize=26, color=WARM_GLOW, va="center", ha="left")

    items = ["Authentication and permissions", "Least-privilege access",
             "Logging and monitoring", "Model-version controls",
             "An ethical wall in retrieval", "Human review"]
    top, h, gap = 0.735, 0.068, 0.014
    for i, s in enumerate(items):
        y = top - i * (h + gap) - h
        fill = [MIDNIGHT_TEAL, OCEAN_TEAL, SEA_GREEN][i % 3]
        box(ax, (0.06, y), 0.88, h, fill, rounding=0.015)
        ax.text(0.10, y + h / 2, "✓", fontsize=30, fontweight="bold",
                color=WARM_GLOW, ha="center", va="center", zorder=4)
        ax.text(0.15, y + h / 2, s, fontsize=30, fontweight="bold",
                color=WHITE, ha="left", va="center", zorder=4)

    box(ax, (0.06, 0.080), 0.88, 0.120, GOLDEN_YELLOW)
    ax.text(0.5, 0.140, "More control. More responsibility.", fontsize=34,
            fontweight="bold", color=DEEP_NAVY, ha="center", va="center",
            zorder=4)
    footer(fig, y=0.030, size=20)
    save(fig, "41_social_square.png")


if __name__ == "__main__":
    make_hero()
    make_division_of_labor()
    make_cross_client()
    make_scorecard()
    make_social_prompt_quote()
    make_social_square()
    print("Generated 6 visuals for Article 41.")
