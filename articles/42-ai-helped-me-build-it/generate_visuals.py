"""Generate branded visuals for Article 42 -- AI Helped Me Build It. AI Does
Not Have to Run It.

Run from anywhere:
    python generate_visuals.py

Produces six article visuals plus three square social cards in ./visuals/.
The social cards are exported at exactly 1080 x 1080 px. Seven slide-ready
variants (13.333 x 7.5 in, 24pt body) go to ./visuals/slides/.
"""

import sys
from pathlib import Path

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

plt.rcParams["font.family"] = "sans-serif"

# Every position below is a fraction of the figure (0-1): the axes fill the
# whole figure, so ax data coordinates and figure fractions are the same
# thing. If a layout feels cramped, grow the canvas inches in blank_axes()
# first -- do not shrink the text.

FOOTER = "PythonMuse LLC  |  www.pythonmuse.com"
OUT = Path(__file__).parent / "visuals"

# FancyBboxPatch inflates each box by `pad` on every side. Keep it small so the
# gaps computed below survive and the connector arrows stay visible.
BOX_PAD = 0.004


def blank_axes(figsize):
    fig, ax = plt.subplots(figsize=figsize, facecolor=WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_position([0, 0, 1, 1])
    return fig, ax


def add_header_bar(fig, title, subtitle, height, title_size, subtitle_size,
                   title_y=0.36, subtitle_y=0.74):
    """Deep Navy bar across the top. title_y / subtitle_y are fractions of the
    bar's height measured down from the top edge of the figure."""
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


def arrow(ax, start, end, color=OCEAN_TEAL, width=3.2, scale=26, zorder=5,
          rad=0.0):
    ax.annotate("", xy=end, xytext=start,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=width,
                                mutation_scale=scale, shrinkA=0, shrinkB=0,
                                connectionstyle=f"arc3,rad={rad}"),
                zorder=zorder)


def footer(fig, y=0.012, size=19):
    fig.text(0.5, y, FOOTER, fontsize=size, color=OCEAN_TEAL,
             ha="center", va="center", alpha=0.80)


def save(fig, name):
    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / name, dpi=180, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)


def save_square(fig, name, inches=13):
    """Social cards: exact 1080 x 1080 px, so no tight bbox (it would trim)."""
    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / name, dpi=1080 / inches, facecolor=fig.get_facecolor())
    plt.close(fig)


# ---------------------------------------------------------------------------
# 1. Hero -- build time vs. run time
# ---------------------------------------------------------------------------
BUILD_STEPS = [
    "Explain the existing procedure",
    "Draft the script or query",
    "Generate mock test data",
    "Suggest edge cases and tests",
    "Draft the documentation",
]
RUN_STEPS = [
    "Same approved rules, every run",
    "Production data stays put",
    "Run log and exception report",
    "Accountant reviews exceptions",
]


def make_hero():
    fig, ax = blank_axes((24, 15))
    add_header_bar(fig, "AI Helped Me Build It. AI Does Not Have to Run It.",
                   "Build-time AI designs the workflow once. The approved process runs it every month.",
                   height=0.150, title_size=48, subtitle_size=28)

    top, bottom = 0.810, 0.215
    h = top - bottom
    lx, lw = 0.03, 0.395
    rx, rw = 0.575, 0.395

    # Left: build time.
    box(ax, (lx, bottom), lw, h, LIGHT_GRAY, edge=OCEAN_TEAL, lw=2.5)
    ax.text(lx + 0.025, top - 0.050, "BUILD TIME", fontsize=34,
            fontweight="bold", color=OCEAN_TEAL, ha="left", va="center")
    ax.text(lx + 0.025, top - 0.105, "Once. You + your AI co-pilot.",
            fontsize=26, color=DEEP_NAVY, ha="left", va="center")
    step_h, gap = 0.058, 0.012
    y0 = top - 0.165
    for i, s in enumerate(BUILD_STEPS):
        y = y0 - i * (step_h + gap) - step_h
        box(ax, (lx + 0.025, y), lw - 0.050, step_h, WHITE, edge=BRIGHT_TEAL,
            lw=2, rounding=0.012, zorder=3)
        ax.text(lx + 0.045, y + step_h / 2, s, fontsize=27, color=DEEP_NAVY,
                ha="left", va="center", zorder=4)
    ax.text(lx + lw / 2, bottom + 0.035, "The model sees mock data only",
            fontsize=25, style="italic", color=OCEAN_TEAL, ha="center",
            va="center")

    # Middle: hand-off.
    mx = (lx + lw + rx) / 2
    mid_y = bottom + h / 2
    arrow(ax, (lx + lw + 0.012, mid_y), (rx - 0.012, mid_y), color=SEA_GREEN,
          width=6, scale=48)
    ax.text(mx, mid_y + 0.115, "Tested.\nApproved.", fontsize=28,
            fontweight="bold", color=DEEP_NAVY, ha="center", va="center",
            linespacing=1.2)
    ax.text(mx, mid_y - 0.115, "The model\ngoes home.", fontsize=28,
            fontweight="bold", color=OCEAN_TEAL, ha="center", va="center",
            linespacing=1.2)

    # Right: run time.
    box(ax, (rx, bottom), rw, h, DEEP_NAVY)
    ax.text(rx + 0.025, top - 0.050, "RUN TIME", fontsize=34,
            fontweight="bold", color=WARM_GLOW, ha="left", va="center",
            zorder=4)
    ax.text(rx + 0.025, top - 0.105, "Every month. The script keeps working.",
            fontsize=26, color=WHITE, ha="left", va="center", zorder=4)
    step_h2, gap2 = 0.080, 0.022
    for i, s in enumerate(RUN_STEPS):
        y = y0 - i * (step_h2 + gap2) - step_h2
        box(ax, (rx + 0.025, y), rw - 0.050, step_h2, MIDNIGHT_TEAL,
            edge=BRIGHT_TEAL, lw=2, rounding=0.012, zorder=3)
        ax.text(rx + 0.045, y + step_h2 / 2, s, fontsize=28, color=WHITE,
                ha="left", va="center", zorder=4)

    box(ax, (0.03, 0.050), 0.94, 0.120, GOLDEN_YELLOW)
    ax.text(0.5, 0.127, "AI can still have a run-time role.",
            fontsize=32, fontweight="bold", color=DEEP_NAVY, ha="center",
            va="center", zorder=4)
    ax.text(0.5, 0.080, "That should be a design decision, not a default.",
            fontsize=27, color=OCEAN_TEAL, ha="center", va="center", zorder=4)
    footer(fig, y=0.016)
    save(fig, "42_hero.png")


# ---------------------------------------------------------------------------
# 2. Asking the chatbot every month vs. building it once
# ---------------------------------------------------------------------------
COMPARISON = [
    ("Production data goes to\nthe model every run", "The model sees mock data\nduring development"),
    ("The approach may shift\nfrom run to run", "The same rules\nrun every time"),
    ("You re-validate the\nmodel's math monthly", "Test the logic once, then control\ninputs, changes, and performance"),
    ("\"Why did it flag that?\"", "Read the rule"),
    ("Evidence = a chat transcript", "Evidence = run log, exception\nreport, version history"),
]


def make_chatbot_vs_build():
    fig, ax = blank_axes((24, 17))
    add_header_bar(fig, "Asking the Chatbot Every Month vs. Building It Once",
                   "Same task. Very different evidence when the reviewer asks how you got the answer.",
                   height=0.130, title_size=46, subtitle_size=28)

    col_x = [0.03, 0.51]
    col_w = 0.46
    head_y, head_h = 0.770, 0.075
    heads = [("ASKING THE CHATBOT EVERY MONTH", OCEAN_TEAL),
             ("BUILDING IT ONCE", DEEP_NAVY)]
    for (label, fill), x in zip(heads, col_x):
        box(ax, (x, head_y), col_w, head_h, fill, rounding=0.012)
        ax.text(x + col_w / 2, head_y + head_h / 2, label, fontsize=29,
                fontweight="bold", color=WHITE, ha="center", va="center",
                zorder=4)

    row_h, gap = 0.104, 0.014
    for i, (left, right) in enumerate(COMPARISON):
        y = head_y - 0.018 - (i + 1) * row_h - i * gap
        box(ax, (col_x[0], y), col_w, row_h, LIGHT_GRAY, edge=OCEAN_TEAL,
            lw=1.8, rounding=0.012)
        box(ax, (col_x[1], y), col_w, row_h, WHITE, edge=SEA_GREEN, lw=3,
            rounding=0.012)
        ax.text(col_x[0] + col_w / 2, y + row_h / 2, left, fontsize=28,
                color=DEEP_NAVY, ha="center", va="center", linespacing=1.2,
                zorder=4)
        ax.text(col_x[1] + col_w / 2, y + row_h / 2, right, fontsize=28,
                fontweight="bold", color=DEEP_NAVY, ha="center", va="center",
                linespacing=1.2, zorder=4)

    box(ax, (0.03, 0.045), 0.94, 0.085, GOLDEN_YELLOW)
    ax.text(0.5, 0.0875,
            "If a script can do the exact calculation, asking a model every month adds variability, not value.",
            fontsize=26, fontweight="bold", color=DEEP_NAVY, ha="center",
            va="center", zorder=4)
    footer(fig, y=0.014)
    save(fig, "42_chatbot_vs_build.png")


# ---------------------------------------------------------------------------
# 3. Four kinds of work
# ---------------------------------------------------------------------------
KINDS = [
    ("RULES", "Can we state exactly how the\nresult is calculated?",
     "Excel, Power Query, SQL, Python", "Aging buckets, thresholds, matching",
     DEEP_NAVY),
    ("PATTERNS", "Do past examples hold a pattern\nwe can't write down?",
     "Machine learning on your history", "Which receivables may go delinquent",
     OCEAN_TEAL),
    ("LANGUAGE", "Does it need reading or writing\nunstructured text?",
     "An LLM, with validation and review", "Contract summaries, draft commentary",
     SEA_GREEN),
    ("JUDGMENT", "Does it need accountability or\na facts-and-circumstances call?",
     "A qualified person", "Approvals, conclusions, sign-off",
     GOLDEN_YELLOW),
]


def make_four_kinds():
    fig, ax = blank_axes((24, 18))
    add_header_bar(fig, "Four Kinds of Work Inside Every Process",
                   "Classify each step, not the whole process. Different work, different tools.",
                   height=0.125, title_size=48, subtitle_size=29)

    col_w, row_h = 0.458, 0.338
    gx, gy = 0.024, 0.026
    top = 0.845
    for idx, (name, question, tool, example, fill) in enumerate(KINDS):
        r, c = divmod(idx, 2)
        x = 0.03 + c * (col_w + gx)
        y = top - (r + 1) * row_h - r * gy
        box(ax, (x, y), col_w, row_h, fill)
        dark_text = fill == GOLDEN_YELLOW
        title_col = DEEP_NAVY if dark_text else WARM_GLOW
        body_col = DEEP_NAVY if dark_text else WHITE
        ax.text(x + 0.028, y + row_h - 0.045, name, fontsize=36,
                fontweight="bold", color=title_col, ha="left", va="center",
                zorder=4)
        ax.text(x + 0.028, y + row_h - 0.122, question, fontsize=31,
                color=body_col, ha="left", va="center", linespacing=1.2,
                zorder=4)
        # Tool tag.
        tag_h = 0.068
        box(ax, (x + 0.028, y + 0.098), col_w - 0.056, tag_h, WHITE,
            rounding=0.010, zorder=3)
        ax.text(x + 0.045, y + 0.098 + tag_h / 2, tool, fontsize=27,
                fontweight="bold", color=DEEP_NAVY, ha="left", va="center",
                zorder=4)
        ax.text(x + 0.028, y + 0.045, "e.g. " + example, fontsize=25,
                style="italic", color=body_col, ha="left", va="center",
                zorder=4)

    ax.text(0.5, 0.075,
            "AI can help build the workflow for all four. Judgment stays with a person.",
            fontsize=31, fontweight="bold", color=DEEP_NAVY, ha="center",
            va="center")
    footer(fig, y=0.016)
    save(fig, "42_four_kinds_of_work.png")


# ---------------------------------------------------------------------------
# 4. Per-step decision tree
# ---------------------------------------------------------------------------
TREE = [
    ("1", "Is the step necessary and understood?", "No", "Simplify, document,\nor redesign first", LIGHT_GRAY),
    ("2", "Can we write the rule, and should the same\ninput always give the same result?", "Yes", "Deterministic\nautomation", DEEP_NAVY),
    ("3", "Does it require interpreting\nlanguage or context?", "Yes", "Consider an LLM, with\nvalidation and review", SEA_GREEN),
    ("4", "Do reliable historical examples hold a\npattern we can't write as rules?", "Yes", "Consider machine\nlearning", OCEAN_TEAL),
]


def make_decision_tree():
    fig, ax = blank_axes((24, 28))
    add_header_bar(fig, "A Decision Tree for Each Step",
                   "Ask it of every step, not once for the whole process.",
                   height=0.077, title_size=50, subtitle_size=30)

    qx, qw = 0.03, 0.555
    ox, ow = 0.700, 0.270
    q_h, gap = 0.085, 0.045
    top = 0.895
    centers = []
    for i, (num, q, branch, outcome, fill) in enumerate(TREE):
        y = top - i * (q_h + gap) - q_h
        box(ax, (qx, y), qw, q_h, WHITE, edge=OCEAN_TEAL, lw=2.5)
        # Number badge.
        bw = 0.056
        box(ax, (qx + 0.016, y + q_h / 2 - 0.024), bw, 0.048, BRIGHT_TEAL,
            rounding=0.010, zorder=3)
        ax.text(qx + 0.016 + bw / 2, y + q_h / 2, num, fontsize=34,
                fontweight="bold", color=DEEP_NAVY, ha="center", va="center",
                zorder=4)
        ax.text(qx + 0.090, y + q_h / 2, q, fontsize=29, color=DEEP_NAVY,
                ha="left", va="center", linespacing=1.2, zorder=4)
        # Outcome to the right.
        edge = OCEAN_TEAL if fill == LIGHT_GRAY else None
        box(ax, (ox, y), ow, q_h, fill, edge=edge, lw=2.5)
        txt_col = DEEP_NAVY if fill == LIGHT_GRAY else WHITE
        ax.text(ox + ow / 2, y + q_h / 2, outcome, fontsize=28,
                fontweight="bold", color=txt_col, ha="center", va="center",
                linespacing=1.15, zorder=4)
        arrow(ax, (qx + qw + 0.010, y + q_h / 2), (ox - 0.010, y + q_h / 2),
              color=SEA_GREEN, width=4, scale=32)
        ax.text((qx + qw + ox) / 2, y + q_h / 2 + 0.019, branch, fontsize=27,
                fontweight="bold", color=OCEAN_TEAL, ha="center", va="center")
        centers.append(y)

    # Down arrows between questions, labelled with the "continue" branch.
    cont = ["Yes", "No", "No"]
    for i in range(len(TREE) - 1):
        y = centers[i]
        x = qx + 0.300
        arrow(ax, (x, y - 0.006), (x, y - gap + 0.006), color=OCEAN_TEAL,
              width=4, scale=30)
        ax.text(x + 0.016, y - gap / 2, cont[i], fontsize=26,
                fontweight="bold", color=OCEAN_TEAL, ha="left", va="center")

    # Final "No" from Q4.
    y4 = centers[-1]
    no_h = 0.065
    no_y = y4 - gap - no_h
    arrow(ax, (qx + 0.300, y4 - 0.006), (qx + 0.300, no_y + no_h + 0.006),
          color=OCEAN_TEAL, width=4, scale=30)
    ax.text(qx + 0.316, y4 - gap / 2, "No", fontsize=26, fontweight="bold",
            color=OCEAN_TEAL, ha="left", va="center")
    box(ax, (qx + 0.130, no_y), 0.340, no_h, GOLDEN_YELLOW)
    ax.text(qx + 0.300, no_y + no_h / 2, "Keep it human-led, or redesign",
            fontsize=27, fontweight="bold", color=DEEP_NAVY, ha="center",
            va="center", zorder=4)

    # Control questions band.
    band_top = no_y - 0.030
    band_h = 0.220
    band_y = band_top - band_h
    box(ax, (0.03, band_y), 0.94, band_h, DEEP_NAVY)
    ax.text(0.055, band_top - 0.035, "THEN, FOR EVERY OPTION ABOVE",
            fontsize=30, fontweight="bold", color=WARM_GLOW, ha="left",
            va="center", zorder=4)
    controls = [
        ("5", "Judgment, approval, restricted data, or contract limits?",
         "A qualified person stays responsible, whatever prepared the work."),
        ("6", "What evidence will show it worked as intended?",
         "Define validation, logging, exceptions, and sign-off before you build."),
    ]
    for k, (num, q, a) in enumerate(controls):
        yy = band_top - 0.095 - k * 0.080
        box(ax, (0.055, yy - 0.024), 0.050, 0.048, GOLDEN_YELLOW,
            rounding=0.010, zorder=3)
        ax.text(0.080, yy, num, fontsize=32, fontweight="bold",
                color=DEEP_NAVY, ha="center", va="center", zorder=4)
        ax.text(0.125, yy + 0.014, q, fontsize=28, fontweight="bold",
                color=WHITE, ha="left", va="center", zorder=4)
        ax.text(0.125, yy - 0.017, a, fontsize=25, color=WARM_GLOW,
                ha="left", va="center", zorder=4)

    footer(fig, y=0.012)
    save(fig, "42_decision_tree.png")


# ---------------------------------------------------------------------------
# 5. Variance workflow swimlane
# ---------------------------------------------------------------------------
LANES = [
    ("SCRIPT", "Rules", DEEP_NAVY),
    ("LLM", "If permitted", SEA_GREEN),
    ("ACCOUNTANT", "Judgment", GOLDEN_YELLOW),
]
SWIM_STEPS = [  # (lane index, label)
    (0, "Confirm\nfiles and\nfields"),
    (0, "Validate\nperiods and\ntotals"),
    (0, "Calculate\n$ and %\nchanges"),
    (0, "Apply\nmateriality\nthresholds"),
    (0, "Retrieve\nsupporting\ndetail"),
    (1, "Draft\nquestions and\ncommentary"),
    (2, "Find and\nsupport the\nexplanation"),
    (2, "Approve\nthe final\nanalysis"),
]


def make_variance_swimlane():
    fig, ax = blank_axes((30, 16))
    add_header_bar(fig, "Year-Over-Year Variance Analysis, Step by Step",
                   "Python calculates the 27 percent. AI suggests questions. The accountant finds, supports, and owns the explanation.",
                   height=0.135, title_size=50, subtitle_size=27)

    label_w = 0.135
    lane_x = 0.03
    lane_w = 0.94
    lane_h, lane_gap = 0.205, 0.020
    top = 0.820
    lane_y = []
    for i, (name, sub, fill) in enumerate(LANES):
        y = top - (i + 1) * lane_h - i * lane_gap
        lane_y.append(y)
        box(ax, (lane_x, y), lane_w, lane_h, LIGHT_GRAY, edge=OCEAN_TEAL,
            lw=1.5, rounding=0.012, zorder=1)
        box(ax, (lane_x, y), label_w, lane_h, fill, rounding=0.012, zorder=2)
        dark = fill == GOLDEN_YELLOW
        ax.text(lane_x + label_w / 2, y + lane_h * 0.60, name, fontsize=30,
                fontweight="bold", color=DEEP_NAVY if dark else WHITE,
                ha="center", va="center", zorder=4)
        ax.text(lane_x + label_w / 2, y + lane_h * 0.32, sub, fontsize=24,
                style="italic", color=OCEAN_TEAL if dark else WARM_GLOW,
                ha="center", va="center", zorder=4)

    n = len(SWIM_STEPS)
    start_x = lane_x + label_w + 0.018
    span = lane_x + lane_w - 0.012 - start_x
    gap = 0.024
    cw = (span - gap * (n - 1)) / n
    ch = lane_h - 0.040
    pos = []
    for i, (lane, label) in enumerate(SWIM_STEPS):
        x = start_x + i * (cw + gap)
        y = lane_y[lane] + 0.020
        fill = LANES[lane][2]
        box(ax, (x, y), cw, ch, WHITE, edge=fill if fill != GOLDEN_YELLOW else OCEAN_TEAL,
            lw=3.5, rounding=0.010, zorder=3)
        ax.text(x + cw / 2, y + ch / 2, label, fontsize=23, color=DEEP_NAVY,
                ha="center", va="center", linespacing=1.15, zorder=4)
        ax.text(x + 0.010, y + ch - 0.022, str(i + 1), fontsize=21,
                fontweight="bold", color=OCEAN_TEAL, ha="left", va="center",
                zorder=4)
        pos.append((x, y, lane))

    for i in range(n - 1):
        x, y, lane = pos[i]
        nx, ny, nlane = pos[i + 1]
        if lane == nlane:
            arrow(ax, (x + cw + 0.001, y + ch / 2), (nx - 0.001, ny + ch / 2),
                  color=SEA_GREEN, width=3.5, scale=24)
        else:
            # Drop down to the next lane.
            arrow(ax, (x + cw * 0.5, y - 0.002), (nx + cw * 0.15, ny + ch + 0.002),
                  color=SEA_GREEN, width=3.5, scale=24)

    box(ax, (0.03, 0.040), 0.94, 0.075, GOLDEN_YELLOW)
    ax.text(0.5, 0.0775,
            "Not \"AI-driven\" and not \"deterministic\": a controlled workflow containing different kinds of work.",
            fontsize=28, fontweight="bold", color=DEEP_NAVY, ha="center",
            va="center", zorder=4)
    footer(fig, y=0.012, size=20)
    save(fig, "42_variance_swimlane.png")


# ---------------------------------------------------------------------------
# 6. Control or polite request?
# ---------------------------------------------------------------------------
EQUIVALENTS = [
    ("Claude Code", "permissions.deny,\nsubagent tools: allowlist, sandbox"),
    ("OpenAI Codex", "sandbox_mode,\napproval_policy"),
    ("Copilot in VS Code", "tools picker,\ntool and terminal approvals"),
    ("Excel, no harness", "folder permissions,\nworkbook protection"),
]


def make_control_or_request():
    fig, ax = blank_axes((24, 19))
    add_header_bar(fig, "Control, or Polite Request?",
                   "A sentence in an agent file asks. A harness setting enforces.",
                   height=0.115, title_size=52, subtitle_size=30)

    top, bottom = 0.850, 0.360
    h = top - bottom
    lx, w = 0.03, 0.455
    rx = 0.515

    # Left: polite request.
    box(ax, (lx, bottom), w, h, LIGHT_GRAY, edge=OCEAN_TEAL, lw=2.5)
    ax.text(lx + 0.025, top - 0.045, "POLITE REQUEST", fontsize=34,
            fontweight="bold", color=OCEAN_TEAL, ha="left", va="center")
    ax.text(lx + 0.025, top - 0.095, "Written in the agent or skill file",
            fontsize=25, color=DEEP_NAVY, ha="left", va="center")
    code_h = 0.150
    box(ax, (lx + 0.025, top - 0.140 - code_h), w - 0.050, code_h,
        MIDNIGHT_TEAL, rounding=0.010, zorder=3)
    ax.text(lx + 0.045, top - 0.140 - code_h / 2,
            "## Boundaries\nDo not touch the\npayroll folder.",
            fontsize=27, family="monospace", color=WHITE, ha="left",
            va="center", linespacing=1.3, zorder=4)
    ax.text(lx + 0.025, bottom + 0.085, "The model is asked to follow it.",
            fontsize=28, fontweight="bold", color=DEEP_NAVY, ha="left",
            va="center")
    ax.text(lx + 0.025, bottom + 0.040, "Usually it does. Usually.",
            fontsize=26, style="italic", color=OCEAN_TEAL, ha="left",
            va="center")

    # Right: control.
    box(ax, (rx, bottom), w, h, DEEP_NAVY)
    ax.text(rx + 0.025, top - 0.045, "CONTROL", fontsize=34,
            fontweight="bold", color=WARM_GLOW, ha="left", va="center",
            zorder=4)
    ax.text(rx + 0.025, top - 0.095, "Claude Code .claude/settings.json",
            fontsize=25, color=WHITE, ha="left", va="center", zorder=4)
    box(ax, (rx + 0.025, top - 0.140 - code_h), w - 0.050, code_h,
        MIDNIGHT_TEAL, edge=BRIGHT_TEAL, lw=2, rounding=0.010, zorder=3)
    ax.text(rx + 0.045, top - 0.140 - code_h / 2,
            "\"deny\": [\n  \"Read(./payroll/**)\",\n  \"Edit(./payroll/**)\" ]",
            fontsize=27, family="monospace", color=WHITE, ha="left",
            va="center", linespacing=1.3, zorder=4)
    ax.text(rx + 0.025, bottom + 0.085, "The harness blocks the file tools.",
            fontsize=28, fontweight="bold", color=WHITE, ha="left",
            va="center", zorder=4)
    ax.text(rx + 0.025, bottom + 0.040, "Whatever the model decides.",
            fontsize=26, style="italic", color=WARM_GLOW, ha="left",
            va="center", zorder=4)

    # Equivalents row.
    ax.text(0.03, 0.310, "SAME IDEA, DIFFERENT HARNESS", fontsize=27,
            fontweight="bold", color=SEA_GREEN, ha="left", va="center")
    n = len(EQUIVALENTS)
    gap = 0.016
    cw = (0.94 - gap * (n - 1)) / n
    ch = 0.135
    cy = 0.140
    for i, (tool, how) in enumerate(EQUIVALENTS):
        x = 0.03 + i * (cw + gap)
        box(ax, (x, cy), cw, ch, WHITE, edge=SEA_GREEN, lw=3, rounding=0.012)
        ax.text(x + cw / 2, cy + ch - 0.032, tool, fontsize=26,
                fontweight="bold", color=DEEP_NAVY, ha="center", va="center",
                zorder=4)
        ax.text(x + cw / 2, cy + 0.048, how, fontsize=22, color=OCEAN_TEAL,
                ha="center", va="center", linespacing=1.2, zorder=4)

    ax.text(0.5, 0.080,
            "Know which of your boundaries are controls, and which are polite requests.",
            fontsize=30, fontweight="bold", color=DEEP_NAVY, ha="center",
            va="center")
    ax.text(0.5, 0.043,
            "Settings change often. Check your provider's current documentation.",
            fontsize=22, style="italic", color=OCEAN_TEAL, ha="center",
            va="center")
    footer(fig, y=0.012)
    save(fig, "42_control_or_request.png")


# ---------------------------------------------------------------------------
# Social cards (1080 x 1080)
# ---------------------------------------------------------------------------
def social_header(fig, title, subtitle, header_h=0.300, title_size=56):
    fig.patches.append(FancyBboxPatch(
        (0, 1 - header_h), 1, header_h, boxstyle="square,pad=0",
        transform=fig.transFigure, facecolor=DEEP_NAVY, edgecolor="none",
        zorder=0))
    fig.text(0.06, 1 - header_h * 0.42, title, fontsize=title_size,
             fontweight="bold", color=WHITE, va="center", ha="left",
             linespacing=1.1)
    fig.text(0.06, 1 - header_h * 0.86, subtitle, fontsize=26,
             color=WARM_GLOW, va="center", ha="left")


def make_social_square():
    fig, ax = blank_axes((13, 13))
    social_header(fig, "AI helped build it.\nAI does not have to run it.",
                  "Build time vs. run time, for accounting workflows")
    rows = [
        ("BUILD TIME", "AI explains, drafts, and tests\nwith mock data. Once.", LIGHT_GRAY),
        ("RUN TIME", "The approved script runs.\nEvery month. Same rules.", DEEP_NAVY),
    ]
    top, h, gap = 0.650, 0.205, 0.035
    for i, (label, text, fill) in enumerate(rows):
        y = top - i * (h + gap) - h
        edge = OCEAN_TEAL if fill == LIGHT_GRAY else None
        box(ax, (0.06, y), 0.88, h, fill, edge=edge, lw=2.5, rounding=0.02)
        dark = fill == LIGHT_GRAY
        ax.text(0.10, y + h - 0.050, label, fontsize=30, fontweight="bold",
                color=OCEAN_TEAL if dark else WARM_GLOW, ha="left",
                va="center", zorder=4)
        ax.text(0.10, y + 0.075, text, fontsize=33,
                color=DEEP_NAVY if dark else WHITE, ha="left", va="center",
                linespacing=1.2, zorder=4)
    box(ax, (0.06, 0.085), 0.88, 0.090, GOLDEN_YELLOW)
    ax.text(0.5, 0.130, "Then the model goes home.", fontsize=36,
            fontweight="bold", color=DEEP_NAVY, ha="center", va="center",
            zorder=4)
    footer(fig, y=0.040, size=20)
    save_square(fig, "42_social_square.png")


def make_social_rule_of_thumb():
    fig, ax = blank_axes((13, 13))
    social_header(fig, "The Rule of Thumb",
                  "Which method belongs in each step?", header_h=0.220,
                  title_size=60)
    rules = [
        ("Rule is known?", "Encode the rule.", DEEP_NAVY),
        ("Language to interpret?", "Consider an LLM. Validate it.", SEA_GREEN),
        ("Pattern you can't write?", "Machine learning may fit.", OCEAN_TEAL),
        ("Needs accountability?", "Keep a person responsible.", GOLDEN_YELLOW),
    ]
    top, h, gap = 0.745, 0.142, 0.022
    for i, (q, a, fill) in enumerate(rules):
        y = top - i * (h + gap) - h
        box(ax, (0.06, y), 0.88, h, fill, rounding=0.02)
        dark = fill == GOLDEN_YELLOW
        ax.text(0.095, y + h * 0.68, q, fontsize=29, fontweight="bold",
                color=DEEP_NAVY if dark else WARM_GLOW, ha="left",
                va="center", zorder=4)
        ax.text(0.095, y + h * 0.30, a, fontsize=33, fontweight="bold",
                color=DEEP_NAVY if dark else WHITE, ha="left", va="center",
                zorder=4)
    footer(fig, y=0.040, size=20)
    save_square(fig, "42_social_rule_of_thumb.png")


def make_social_wrong_rule():
    fig, ax = blank_axes((13, 13))
    box(ax, (0.05, 0.110), 0.90, 0.840, DEEP_NAVY, rounding=0.03)
    ax.text(0.130, 0.835, "“", fontsize=170, color=GOLDEN_YELLOW,
            ha="center", va="center", fontweight="bold", zorder=4)
    ax.text(0.5, 0.590,
            "A script can apply\nthe wrong rule\nperfectly.",
            fontsize=58, fontweight="bold", color=WHITE, ha="center",
            va="center", linespacing=1.2, zorder=4)
    ax.text(0.5, 0.370, "Every month. Forever.", fontsize=44,
            fontweight="bold", color=GOLDEN_YELLOW, ha="center",
            va="center", zorder=4)
    ax.text(0.5, 0.230,
            "Deterministic does not mean correct.\nTest it with data built to break it.",
            fontsize=28, color=WARM_GLOW, style="italic", ha="center",
            va="center", linespacing=1.3, zorder=4)
    footer(fig, y=0.060, size=20)
    save_square(fig, "42_social_wrong_rule.png")


# ---------------------------------------------------------------------------
# Slide-ready variants (13.333 x 7.5 in; the point size set here is the point
# size on the slide). One idea per slide, no header or footer bars, no outlines.
# Rules: .claude/skills/pythonmuse-slide-visuals/SKILL.md. save_slide() raises
# if any text is under 22pt or runs off the edge.
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from slide_kit import blank_slide, save_slide, SLIDE_TARGET_PT  # noqa: E402

SLIDES_OUT = OUT / "slides"
HEAD_PT = 32      # headings and focal words
BODY_PT = SLIDE_TARGET_PT


def slide_box(ax, x, y, w, h, fill, zorder=2):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.002,rounding_size=0.02",
        facecolor=fill, edgecolor="none", zorder=zorder))


def slide_arrow(ax, start, end, color=SEA_GREEN):
    ax.annotate("", xy=end, xytext=start,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=6,
                                mutation_scale=40, shrinkA=0, shrinkB=0),
                zorder=5)


def slide_card(ax, x, y, w, h, fill, head, lines, head_col, body_col,
               head_size=HEAD_PT, body_size=BODY_PT, bold_last=False,
               first_off=0.200, step=0.140):
    """Heading at the top of a filled card, body lines spread beneath it.
    first_off is the first body line's distance below the card's top edge."""
    slide_box(ax, x, y, w, h, fill)
    pad = 0.025
    ax.text(x + pad, y + h - 0.085, head, fontsize=head_size,
            fontweight="bold", color=head_col, ha="left", va="center",
            zorder=4)
    for i, line in enumerate(lines):
        last = bold_last and i == len(lines) - 1
        ax.text(x + pad, y + h - first_off - i * step, line,
                fontsize=body_size, fontweight="bold" if last else "normal",
                color=body_col, ha="left", va="center", zorder=4)


def slide_band(ax, text, y=0.060, h=0.130, size=HEAD_PT):
    slide_box(ax, 0.03, y, 0.94, h, GOLDEN_YELLOW)
    ax.text(0.5, y + h / 2, text, fontsize=size, fontweight="bold",
            color=DEEP_NAVY, ha="center", va="center", zorder=4)


def make_hero_slide():
    fig, ax = blank_slide()
    lx, rx, w = 0.03, 0.60, 0.37
    y, h = 0.250, 0.690
    slide_card(ax, lx, y, w, h, LIGHT_GRAY, "BUILD TIME",
               ["AI explains the steps", "Drafts the script",
                "Tests on mock data"], OCEAN_TEAL, DEEP_NAVY)
    slide_card(ax, rx, y, w, h, DEEP_NAVY, "RUN TIME",
               ["Same approved rules", "Data stays put",
                "You review exceptions"], WARM_GLOW, WHITE)
    mid = (lx + w + rx) / 2
    slide_arrow(ax, (lx + w + 0.015, y + h * 0.42), (rx - 0.015, y + h * 0.42))
    ax.text(mid, y + h * 0.42 + 0.105, "Tested.\nApproved.", fontsize=BODY_PT,
            fontweight="bold", color=DEEP_NAVY, ha="center", va="center",
            linespacing=1.2)
    slide_band(ax, "Then the model goes home.", y=0.060, h=0.140, size=36)
    save_slide(fig, str(SLIDES_OUT / "42_hero_slide.png"))


def make_chatbot_vs_build_slide():
    fig, ax = blank_slide()
    w, y, h = 0.455, 0.250, 0.690
    slide_card(ax, 0.03, y, w, h, LIGHT_GRAY, "ASK THE CHATBOT",
               ["Data goes to the model", "The approach may shift",
                "Evidence: a transcript"], OCEAN_TEAL, DEEP_NAVY)
    slide_card(ax, 0.515, y, w, h, DEEP_NAVY, "BUILD IT ONCE",
               ["Mock data at build time", "Same rules every run",
                "Evidence: run log, report"], WARM_GLOW, WHITE)
    slide_band(ax, "Same task. Different evidence.", y=0.060, h=0.140)
    save_slide(fig, str(SLIDES_OUT / "42_chatbot_vs_build_slide.png"))


def make_four_kinds_slide():
    fig, ax = blank_slide()
    kinds = [
        ("RULES", "Can we write the rule?", "Excel, SQL, Python",
         DEEP_NAVY, WARM_GLOW, WHITE),
        ("PATTERNS", "History holds a pattern?", "Machine learning",
         OCEAN_TEAL, WARM_GLOW, WHITE),
        ("LANGUAGE", "Must it read text?", "An LLM, validated",
         BRIGHT_TEAL, DEEP_NAVY, DEEP_NAVY),
        ("JUDGMENT", "Needs accountability?", "A qualified person",
         GOLDEN_YELLOW, DEEP_NAVY, DEEP_NAVY),
    ]
    w, h = 0.455, 0.320
    for idx, (name, question, tool, fill, head_col, body_col) in enumerate(kinds):
        r, c = divmod(idx, 2)
        x = 0.03 + c * 0.485
        y = 0.620 - r * 0.350
        slide_card(ax, x, y, w, h, fill, name, [question, tool], head_col,
                   body_col, bold_last=True, first_off=0.165, step=0.085)
    slide_band(ax, "AI helps build all four. Judgment stays human.", y=0.060,
               h=0.130, size=30)
    save_slide(fig, str(SLIDES_OUT / "42_four_kinds_slide.png"))


def make_decision_tree_slide():
    """Questions 2-4 of the per-step tree, as the Rule of Thumb."""
    fig, ax = blank_slide()
    rows = [
        ("Rule is known?", "Encode the rule.", DEEP_NAVY, WARM_GLOW, WHITE),
        ("Language to read?", "LLM, then validate it.", OCEAN_TEAL, WARM_GLOW,
         WHITE),
        ("Pattern, no rule?", "Machine learning may fit.", BRIGHT_TEAL,
         DEEP_NAVY, DEEP_NAVY),
        ("Needs accountability?", "Keep a person responsible.", GOLDEN_YELLOW,
         DEEP_NAVY, DEEP_NAVY),
    ]
    h, gap, top = 0.190, 0.030, 0.940
    for i, (q, a, fill, qcol, acol) in enumerate(rows):
        y = top - i * (h + gap) - h
        slide_box(ax, 0.03, y, 0.94, h, fill)
        ax.text(0.060, y + h / 2, q, fontsize=BODY_PT, color=qcol,
                ha="left", va="center", zorder=4)
        ax.text(0.400, y + h / 2, a, fontsize=28, fontweight="bold",
                color=acol, ha="left", va="center", zorder=4)
    save_slide(fig, str(SLIDES_OUT / "42_decision_tree_slide.png"))


def make_control_questions_slide():
    """Questions 5 and 6 of the per-step tree: they apply to every option."""
    fig, ax = blank_slide()
    ax.text(0.03, 0.915, "Then, for every option:", fontsize=HEAD_PT,
            fontweight="bold", color=DEEP_NAVY, ha="left", va="center")
    slide_card(ax, 0.03, 0.470, 0.94, 0.360, DEEP_NAVY,
               "5.  Judgment, approval, or limits?",
               ["A qualified person stays responsible,",
                "whatever technology prepared the work."],
               WARM_GLOW, WHITE)
    slide_card(ax, 0.03, 0.070, 0.94, 0.360, OCEAN_TEAL,
               "6.  What evidence shows it worked?",
               ["Define validation, logging, exceptions,",
                "and sign-off before you build."],
               WARM_GLOW, WHITE)
    save_slide(fig, str(SLIDES_OUT / "42_control_questions_slide.png"))


def make_swimlane_slide():
    fig, ax = blank_slide()
    lanes = [
        ("SCRIPT", ["Calculates the", "27 percent"], DEEP_NAVY, WARM_GLOW,
         WHITE),
        ("LLM", ["Suggests", "questions", "(if permitted)"], BRIGHT_TEAL,
         DEEP_NAVY, DEEP_NAVY),
        ("ACCOUNTANT", ["Finds, supports,", "and owns the", "explanation"],
         GOLDEN_YELLOW, DEEP_NAVY, DEEP_NAVY),
    ]
    w, gap, y, h = 0.292, 0.032, 0.270, 0.670
    for i, (name, lines, fill, head_col, body_col) in enumerate(lanes):
        x = 0.03 + i * (w + gap)
        slide_card(ax, x, y, w, h, fill, name, lines, head_col, body_col,
                   head_size=30, step=0.115)
        if i < len(lanes) - 1:
            slide_arrow(ax, (x + w + 0.002, y + h / 2),
                        (x + w + gap - 0.002, y + h / 2))
    slide_band(ax, "Python calculates. AI suggests. You decide.", y=0.060,
               h=0.140, size=30)
    save_slide(fig, str(SLIDES_OUT / "42_variance_swimlane_slide.png"))


def make_control_or_request_slide():
    fig, ax = blank_slide()
    w, y, h = 0.455, 0.250, 0.690
    panel_y, panel_h = y + 0.215, 0.250
    # Left: polite request.
    slide_box(ax, 0.03, y, w, h, LIGHT_GRAY)
    ax.text(0.055, y + h - 0.085, "POLITE REQUEST", fontsize=HEAD_PT,
            fontweight="bold", color=OCEAN_TEAL, ha="left", va="center",
            zorder=4)
    ax.text(0.055, y + h - 0.185, "Written in the agent file",
            fontsize=BODY_PT, color=DEEP_NAVY, ha="left", va="center",
            zorder=4)
    slide_box(ax, 0.055, panel_y, w - 0.050, panel_h, MIDNIGHT_TEAL, zorder=3)
    ax.text(0.080, panel_y + panel_h / 2, "Do not touch the\npayroll folder.",
            fontsize=BODY_PT, family="monospace", color=WHITE, ha="left",
            va="center", linespacing=1.4, zorder=4)
    ax.text(0.055, y + 0.080, "The model is asked.", fontsize=28,
            fontweight="bold", color=DEEP_NAVY, ha="left", va="center",
            zorder=4)
    # Right: control.
    rx = 0.515
    slide_box(ax, rx, y, w, h, DEEP_NAVY)
    ax.text(rx + 0.025, y + h - 0.085, "CONTROL", fontsize=HEAD_PT,
            fontweight="bold", color=WARM_GLOW, ha="left", va="center",
            zorder=4)
    ax.text(rx + 0.025, y + h - 0.185, "Claude Code settings.json",
            fontsize=BODY_PT, color=WHITE, ha="left", va="center", zorder=4)
    slide_box(ax, rx + 0.025, panel_y, w - 0.050, panel_h, MIDNIGHT_TEAL,
              zorder=3)
    ax.text(rx + 0.050, panel_y + panel_h / 2, "deny:\nRead(./payroll/**)",
            fontsize=BODY_PT, family="monospace", color=WHITE, ha="left",
            va="center", linespacing=1.4, zorder=4)
    ax.text(rx + 0.025, y + 0.080, "The harness blocks it.", fontsize=28,
            fontweight="bold", color=WHITE, ha="left", va="center", zorder=4)
    slide_band(ax, "Know which is which.", y=0.060, h=0.140)
    save_slide(fig, str(SLIDES_OUT / "42_control_or_request_slide.png"))


def make_slides():
    make_hero_slide()
    make_chatbot_vs_build_slide()
    make_four_kinds_slide()
    make_decision_tree_slide()
    make_control_questions_slide()
    make_swimlane_slide()
    make_control_or_request_slide()


if __name__ == "__main__":
    make_hero()
    make_chatbot_vs_build()
    make_four_kinds()
    make_decision_tree()
    make_variance_swimlane()
    make_control_or_request()
    make_social_square()
    make_social_rule_of_thumb()
    make_social_wrong_rule()
    make_slides()
    print("Generated 9 visuals and 7 slide-ready visuals for Article 42.")
