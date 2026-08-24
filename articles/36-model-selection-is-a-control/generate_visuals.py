"""Generate branded visuals for Article 36 -- Model Selection Is an Accounting Control.

Run from the article folder:
    python generate_visuals.py
"""

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

plt.rcParams["font.family"] = "sans-serif"


def add_header_bar(fig, title, subtitle, height=0.13):
    bar = FancyBboxPatch(
        (0, 1 - height), 1, height,
        boxstyle="square,pad=0", transform=fig.transFigure,
        facecolor=DEEP_NAVY, edgecolor="none", zorder=0,
    )
    fig.patches.append(bar)
    fig.text(0.03, 1 - height / 2 + 0.018, title, fontsize=22, fontweight="bold",
             color=WHITE, va="center", ha="left")
    fig.text(0.03, 1 - height / 2 - 0.032, subtitle, fontsize=12,
             color=WARM_GLOW, va="center", ha="left", alpha=1.0)
    fig.text(0.97, 1 - height / 2, "PythonMuse LLC", fontsize=9,
             color=WHITE, va="center", ha="right", alpha=0.70)


# FancyBboxPatch inflates each box by `pad` on every side. Keep this small so
# that the gaps computed in each layout below survive and the connector arrows
# stay visible -- a larger pad silently eats them.
BOX_PAD = 0.004


def rounded_box(ax, xy, w, h, color, text_color=WHITE, text="", fontsize=12,
                sub="", subsize=10, sub_color=None, bold=True, title_offset=0.16,
                sub_offset=0.22, linespacing=1.4, edge=None, lw=0, ha="center",
                text_x=None):
    box = FancyBboxPatch(
        xy, w, h, boxstyle=f"round,pad={BOX_PAD},rounding_size=0.02",
        facecolor=color, edgecolor=edge or "none", linewidth=lw, zorder=2,
    )
    ax.add_patch(box)
    cx, cy = xy[0] + w / 2, xy[1] + h / 2
    tx = text_x if text_x is not None else cx
    if sub:
        ax.text(tx, cy + h * title_offset, text, fontsize=fontsize,
                fontweight="bold" if bold else "normal",
                color=text_color, ha=ha, va="center", zorder=3)
        ax.text(tx, cy - h * sub_offset, sub, fontsize=subsize, color=sub_color or text_color,
                ha=ha, va="center", zorder=3, alpha=1.0, linespacing=linespacing)
    else:
        ax.text(tx, cy, text, fontsize=fontsize, fontweight="bold" if bold else "normal",
                color=text_color, ha=ha, va="center", zorder=3, linespacing=linespacing)


def arrow_v(ax, x, y1, y2, color=OCEAN_TEAL, lw=2.2):
    ax.annotate("", xy=(x, y2), xytext=(x, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                mutation_scale=16), zorder=1)


# Anything at or lighter than Bright Teal takes dark text -- white on Bright
# Teal is the contrast violation that is easiest to ship without noticing.
LIGHT_FILLS = (BRIGHT_TEAL, GOLDEN_YELLOW, WARM_GLOW, SOFT_SAGE, "#F5F5F5", WHITE)

# On the yellow family, Ocean Teal reads as a deliberate secondary tone. On the
# teal family it just looks muddy, so subtitles there stay Deep Navy too.
TEAL_FILLS = (BRIGHT_TEAL, SOFT_SAGE)


def text_colors(fill):
    """Return (title_color, subtitle_color) for text sitting on `fill`."""
    if fill in TEAL_FILLS:
        return DEEP_NAVY, DEEP_NAVY
    if fill in LIGHT_FILLS:
        return DEEP_NAVY, OCEAN_TEAL
    return WHITE, WARM_GLOW


# The escalation ladder, shared between its own visual and the social variant.
# Bottom rung first -- each layout reverses as needed.
ESCALATION = [
    ("Fast capability", "Structured, rule-based, quickly verified", SEA_GREEN),
    ("General-purpose capability", "Interpretation inside defined boundaries", OCEAN_TEAL),
    ("Reasoning capability", "Multi-step analysis, ambiguity, competing explanations", MIDNIGHT_TEAL),
    ("The accounting professional", "Judgment, materiality, accountability", GOLDEN_YELLOW),
]


# ---------------------------------------------------------------------------
# 1. Hero -- capability x environment grid with real accounting tasks
# ---------------------------------------------------------------------------
def make_hero():
    fig, ax = plt.subplots(figsize=(13.4, 8.5), facecolor=WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_position([0, 0, 1, 1])

    add_header_bar(fig, "Two Questions, Not One",
                   "Capability answers what level of work is needed. Environment answers where the data is allowed to go.",
                   height=0.105)

    environments = [
        "Approved cloud",
        "Enterprise-controlled",
        "Private or local",
    ]
    # Top row first. (capability label, sublabel, color, [task per environment])
    capabilities = [
        ("Reasoning", "Multi-step, ambiguous", MIDNIGHT_TEAL, [
            "Research an accounting\ntreatment using no\nentity data",
            "Analyze a complex lease\nacross interacting\nprovisions",
            "Investigate an unexplained\nmargin variance on\nrestricted data",
        ]),
        ("General-purpose", "Interpretation, bounded", OCEAN_TEAL, [
            "Summarize a published\naccounting standard",
            "Draft variance commentary\nfrom validated\nfigures",
            "Categorize confidential\nvendor descriptions",
        ]),
        ("Fast", "Structured, verifiable", SEA_GREEN, [
            "Reformat dates and\ncolumns in public\nsample data",
            "Standardize vendor names\nin a system export",
            "Extract defined fields\nfrom payroll\nrecords",
        ]),
    ]

    label_w = 0.185
    x0 = 0.045
    grid_x = x0 + label_w + 0.012
    grid_w = 1 - grid_x - 0.045
    col_gap = 0.012
    col_w = (grid_w - 2 * col_gap) / 3

    top = 0.800
    row_h = 0.203
    row_gap = 0.024

    # Column headers for the environment dimension.
    for c, env in enumerate(environments):
        cx = grid_x + c * (col_w + col_gap) + col_w / 2
        ax.text(cx, top + 0.038, env, fontsize=13, fontweight="bold",
                color=BRIGHT_TEAL, ha="center", va="center", zorder=3)

    ax.text(x0 + label_w / 2, top + 0.038, "Capability level", fontsize=13,
            fontweight="bold", color=DEEP_NAVY, ha="center", va="center", zorder=3)

    for r, (cap, capsub, color, tasks) in enumerate(capabilities):
        y = top - r * (row_h + row_gap) - row_h

        # Row label: the capability dimension.
        tc, sc = text_colors(color)
        rounded_box(ax, (x0, y), label_w, row_h, color, text_color=tc,
                    text=cap, fontsize=16.5,
                    sub=capsub, subsize=12.5, sub_color=sc,
                    title_offset=0.15, sub_offset=0.20)

        # Cells: one accounting task per environment.
        for c, task in enumerate(tasks):
            cxy = (grid_x + c * (col_w + col_gap), y)
            rounded_box(ax, cxy, col_w, row_h, "#F5F5F5", text_color=DEEP_NAVY,
                        text=task, fontsize=13, bold=False, linespacing=1.45)

    fig.text(0.5, 0.072,
             "Extracting payroll fields needs little reasoning and a highly controlled environment. "
             "Researching a treatment needs strong reasoning and no confidential data at all.",
             fontsize=11, color=OCEAN_TEAL, ha="center", va="center", style="italic", alpha=1.0)
    fig.text(0.5, 0.026,
             "PythonMuse LLC  |  github.com/PythonMuse/ai-ledger",
             fontsize=9, color=OCEAN_TEAL, ha="center", va="center", alpha=0.75)

    fig.savefig("visuals/36_hero.png", dpi=180, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)


# ---------------------------------------------------------------------------
# 2. Complexity vs. consequence -- the distinction the article turns on
# ---------------------------------------------------------------------------
def make_complexity_consequence():
    fig, ax = plt.subplots(figsize=(11.6, 10.2), facecolor=WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_position([0, 0, 1, 1])

    add_header_bar(fig, "Complexity and Consequence Are Different Axes",
                   "Higher complexity may require a stronger model. Higher consequence requires stronger controls.",
                   height=0.11)

    # (col, row, color, headline, detail) -- row 1 is the top row.
    quadrants = [
        (0, 1, OCEAN_TEAL, "Stronger model\nNormal review",
         "Complex, low consequence\n\nResearch a treatment question\nusing no entity data"),
        (1, 1, MIDNIGHT_TEAL, "Stronger model AND\nstronger controls",
         "Complex, high consequence\n\nInterpret a debt covenant\nEscalate to the professional"),
        (0, 0, SEA_GREEN, "Fast model\nLight review",
         "Simple, low consequence\n\nReformat transaction\ndescriptions to a defined rule"),
        (1, 0, GOLDEN_YELLOW, "A stronger model is\nnot the answer here",
         "Simple, high consequence\n\nExtract payroll fields\nControls, not capability"),
    ]

    pad_l, pad_b = 0.155, 0.185
    grid_w = 1 - pad_l - 0.055
    grid_h = 0.790 - pad_b
    gap = 0.016
    cell_w = (grid_w - gap) / 2
    cell_h = (grid_h - gap) / 2

    for col, row, color, headline, detail in quadrants:
        x = pad_l + col * (cell_w + gap)
        y = pad_b + row * (cell_h + gap)
        text_color, sub_color = text_colors(color)
        rounded_box(ax, (x, y), cell_w, cell_h, color, text_color=text_color,
                    text=headline, fontsize=18,
                    sub=detail, subsize=14, sub_color=sub_color,
                    title_offset=0.22, sub_offset=0.13, linespacing=1.4)

    # Axis labels.
    ax.annotate("", xy=(pad_l + grid_w, pad_b - 0.042),
                xytext=(pad_l, pad_b - 0.042),
                arrowprops=dict(arrowstyle="-|>", color=DEEP_NAVY, lw=2.0,
                                mutation_scale=16))
    ax.text(pad_l + grid_w / 2, pad_b - 0.078,
            "Consequence if the output is wrong",
            fontsize=13, fontweight="bold", color=DEEP_NAVY, ha="center", va="center")

    ax.annotate("", xy=(pad_l - 0.042, pad_b + grid_h),
                xytext=(pad_l - 0.042, pad_b),
                arrowprops=dict(arrowstyle="-|>", color=DEEP_NAVY, lw=2.0,
                                mutation_scale=16))
    ax.text(pad_l - 0.078, pad_b + grid_h / 2, "Task complexity",
            fontsize=13, fontweight="bold", color=DEEP_NAVY, ha="center",
            va="center", rotation=90)

    fig.text(0.5, 0.038,
             "The bottom-right quadrant is the one accounting teams get wrong most often: "
             "reaching for a bigger model when the real answer is a stronger control.",
             fontsize=11, color=OCEAN_TEAL, ha="center", va="center", style="italic", alpha=1.0)
    fig.text(0.5, 0.012,
             "PythonMuse LLC  |  github.com/PythonMuse/ai-ledger",
             fontsize=9, color=OCEAN_TEAL, ha="center", va="center", alpha=0.75)

    fig.savefig("visuals/36_complexity_vs_consequence.png", dpi=180, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)


# ---------------------------------------------------------------------------
# 3. The escalation ladder -- the top rung is not a model
# ---------------------------------------------------------------------------
def make_escalation_ladder():
    fig, ax = plt.subplots(figsize=(11.2, 9.4), facecolor=WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_position([0, 0, 1, 1])

    add_header_bar(fig, "Model Selection as an Escalation Process",
                   "Start where the work sits. Escalate when the work -- not the impatience -- calls for it.",
                   height=0.115)

    rungs = list(reversed(ESCALATION))  # professional on top
    n = len(rungs)
    box_w = 0.76
    x0 = 0.12
    top = 0.775
    bottom = 0.135
    box_h = 0.125
    gap = ((top - bottom) - n * box_h) / (n - 1)

    centers = []
    for i, (label, desc, color) in enumerate(rungs):
        y = top - i * (box_h + gap) - box_h
        centers.append(y + box_h / 2)
        text_color, sub_color = text_colors(color)
        rounded_box(ax, (x0, y), box_w, box_h, color, text_color=text_color,
                    text=label, fontsize=16.5,
                    sub=desc, subsize=11.5, sub_color=sub_color,
                    title_offset=0.18, sub_offset=0.24)

    # Arrows point upward, from each rung to the one above it.
    for i in range(n - 1, 0, -1):
        arrow_v(ax, x0 + box_w / 2, centers[i] + box_h / 2 + 0.004,
                centers[i - 1] - box_h / 2 - 0.004)

    # Sits in the white gap between the header bar (bottom edge 0.885) and the
    # top rung (top edge 0.775) -- anything at 0.885 is hidden by the bar.
    ax.text(0.5, 0.828, "Escalate", fontsize=12, fontweight="bold",
            color=OCEAN_TEAL, ha="center", va="center")

    fig.text(0.5, 0.062,
             "The top of the escalation ladder is not another AI model. It is the professional.",
             fontsize=12.5, color=DEEP_NAVY, ha="center", va="center", fontweight="bold")
    fig.text(0.5, 0.030,
             "AI can support the analysis. It cannot own the accounting judgment or the consequences of the decision.",
             fontsize=11, color=OCEAN_TEAL, ha="center", va="center", style="italic", alpha=1.0)
    fig.text(0.5, 0.008,
             "PythonMuse LLC  |  github.com/PythonMuse/ai-ledger",
             fontsize=9, color=OCEAN_TEAL, ha="center", va="center", alpha=0.75)

    fig.savefig("visuals/36_escalation_ladder.png", dpi=180, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)


# ---------------------------------------------------------------------------
# 4. The seven-question checklist
# ---------------------------------------------------------------------------
def make_seven_questions():
    fig, ax = plt.subplots(figsize=(12.4, 10.0), facecolor=WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_position([0, 0, 1, 1])

    add_header_bar(fig, "Seven Questions Before You Assign the Work",
                   "Answer these once per workflow, not once per prompt -- then write the answers down.",
                   height=0.11)

    questions = [
        ("1", "What exactly is the task?",
         "Extract, transform, draft, analyze, or support judgment", MIDNIGHT_TEAL),
        ("2", "Is the information permitted here?",
         "Resolve data governance before considering capability", OCEAN_TEAL),
        ("3", "How much reasoning does it require?",
         "Routine work may prioritize speed over depth", OCEAN_TEAL),
        ("4", "What happens if the output is wrong?",
         "Financial, operational, reporting, or compliance consequence", SEA_GREEN),
        ("5", "How easily can the result be verified?",
         "A polished answer is not the same as a reliable answer", SEA_GREEN),
        ("6", "Does the cost match the value?",
         "Matters most for recurring or high-volume workflows", BRIGHT_TEAL),
        ("7", "When should the workflow escalate?",
         "To a stronger model or, more importantly, to a human reviewer", GOLDEN_YELLOW),
    ]

    n = len(questions)
    x0, w = 0.055, 0.89
    top = 0.815
    bottom = 0.105
    row_h = 0.082
    gap = ((top - bottom) - n * row_h) / (n - 1)

    badge_w = 0.052
    for i, (num, q, detail, color) in enumerate(questions):
        y = top - i * (row_h + gap) - row_h
        text_color, sub_color = text_colors(color)

        rounded_box(ax, (x0, y), w, row_h, color, text_color=text_color,
                    text=q, fontsize=16.5, ha="left",
                    text_x=x0 + badge_w + 0.028,
                    sub=detail, subsize=13, sub_color=sub_color,
                    title_offset=0.22, sub_offset=0.26)

        # Number badge sits inside the row, on the left.
        ax.text(x0 + badge_w / 2 + 0.012, y + row_h / 2, num, fontsize=22,
                fontweight="bold", color=text_color, ha="center", va="center",
                zorder=4, alpha=0.9)

    fig.text(0.5, 0.055,
             "Answered once and documented, these seven questions turn a preference into a control.",
             fontsize=11.5, color=DEEP_NAVY, ha="center", va="center", fontweight="bold")
    fig.text(0.5, 0.026,
             "Question 2 comes before capability. Question 7 is the one most workflows forget to define in advance.",
             fontsize=11, color=OCEAN_TEAL, ha="center", va="center", style="italic", alpha=1.0)
    fig.text(0.5, 0.005,
             "PythonMuse LLC  |  github.com/PythonMuse/ai-ledger",
             fontsize=9, color=OCEAN_TEAL, ha="center", va="center", alpha=0.75)

    fig.savefig("visuals/36_seven_questions.png", dpi=180, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)


# ---------------------------------------------------------------------------
# 5. Social square -- the escalation ladder punchline
# ---------------------------------------------------------------------------
def make_social_square():
    fig, ax = plt.subplots(figsize=(8, 8), facecolor=WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_position([0, 0, 1, 1])

    header_h = 0.165
    add_header_bar(fig, "Model Selection Is a Control",
                   "The top of the escalation ladder is not another AI model.",
                   height=header_h)

    rungs = list(reversed(ESCALATION))
    n = len(rungs)
    box_w = 0.88
    x0 = 0.06
    top = 1 - header_h - 0.055
    bottom = 0.185
    box_h = 0.132
    gap = ((top - bottom) - n * box_h) / (n - 1)

    for i, (label, desc, color) in enumerate(rungs):
        y = top - i * (box_h + gap) - box_h
        text_color, sub_color = text_colors(color)
        rounded_box(ax, (x0, y), box_w, box_h, color, text_color=text_color,
                    text=label, fontsize=14.5, ha="left",
                    text_x=x0 + 0.035,
                    sub=desc, subsize=10.5, sub_color=sub_color,
                    title_offset=0.18, sub_offset=0.26)

    fig.text(0.5, 0.132, "It is the professional.", fontsize=15,
             color=DEEP_NAVY, ha="center", va="center", fontweight="bold")
    fig.text(0.5, 0.073,
             "Higher complexity may require stronger models.\nHigher consequence requires stronger controls.",
             fontsize=10.5, color=OCEAN_TEAL, ha="center", va="center",
             style="italic", linespacing=1.6, alpha=1.0)
    fig.text(0.5, 0.020, "PythonMuse LLC  |  pythonmuse.com", fontsize=9.5,
             color=OCEAN_TEAL, ha="center", va="center", alpha=0.85)

    fig.savefig("visuals/36_social_square.png", dpi=180, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)


if __name__ == "__main__":
    make_hero()
    make_complexity_consequence()
    make_escalation_ladder()
    make_seven_questions()
    make_social_square()
    print("Generated 5 visuals for Article 36.")
