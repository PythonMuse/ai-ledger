"""Generate branded visuals for Article 39 -- Buy the Platform. Own the
Accounting Logic.

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

LIGHT_GRAY = "#F5F5F5"

plt.rcParams["font.family"] = "sans-serif"

# ---------------------------------------------------------------------------
# PowerPoint-readability pass (trial for the house SKILL.md rule): every
# visual in this article was originally tuned with a 18pt floor. These are
# meant to be dropped onto a slide, not just viewed full-screen as a PNG, so
# the floor is raised to 22pt and every other size in the set is scaled up
# by the same ratio -- not just the smallest text, or the small text would
# end up closer in size to everything around it than it started.
#
# `pt()` wraps every *design* font size (the number tuned by eye in each
# call below) so the original value stays visible for reference. `canvas()`
# scales each figure's physical inches by the same factor -- since every box
# position and gap in this file is a fraction of the figure (0-1), enlarging
# the canvas by the same ratio as the text keeps every box the same size
# *relative to its text* as before. Nothing needs to be repositioned; the
# whole layout grows like a photograph enlargement. Footer branding
# ("PythonMuse LLC | www.pythonmuse.com") is exempted and keeps its
# original size, per instruction.
FONT_SCALE = 22 / 18


def pt(size):
    """Scale a design font size by FONT_SCALE, rounded to the nearest point."""
    return round(size * FONT_SCALE)


def canvas(w, h):
    """Scale a figure's inches by FONT_SCALE so boxes keep the same size
    relative to the now-larger text instead of fighting it."""
    return (round(w * FONT_SCALE, 1), round(h * FONT_SCALE, 1))


def lw(width):
    """Scale a line weight (points) by FONT_SCALE, to one decimal place."""
    return round(width * FONT_SCALE, 1)


def add_header_bar(fig, title, subtitle, height=0.13, title_size=29,
                    subtitle_size=16, brand_size=10.5, brand=True):
    bar = FancyBboxPatch(
        (0, 1 - height), 1, height,
        boxstyle="square,pad=0", transform=fig.transFigure,
        facecolor=DEEP_NAVY, edgecolor="none", zorder=0,
    )
    fig.patches.append(bar)
    fig.text(0.03, 1 - height / 2 + 0.018, title, fontsize=pt(title_size),
             fontweight="bold", color=WHITE, va="center", ha="left")
    fig.text(0.03, 1 - height / 2 - 0.032, subtitle, fontsize=pt(subtitle_size),
             color=WARM_GLOW, va="center", ha="left", alpha=1.0)
    if brand:
        fig.text(0.97, 1 - height / 2, "PythonMuse LLC", fontsize=pt(brand_size),
                 color=WHITE, va="center", ha="right", alpha=0.70)


# FancyBboxPatch inflates each box by `pad` on every side. Keep this small so
# that the gaps computed in each layout below survive and the connector arrows
# stay visible -- a larger pad silently eats them. This is a fractional
# (data-space) value, not a font size, so it does not scale with FONT_SCALE.
BOX_PAD = 0.004


def rounded_box(ax, xy, w, h, color, text_color=WHITE, text="", fontsize=12,
                sub="", subsize=10.5, sub_color=None, bold=True, title_offset=0.18,
                sub_offset=0.26, linespacing=1.4, edge=None, lw=0, ha="center",
                text_x=None, zorder=2):
    box = FancyBboxPatch(
        xy, w, h, boxstyle=f"round,pad={BOX_PAD},rounding_size=0.02",
        facecolor=color, edgecolor=edge or "none", linewidth=lw, zorder=zorder,
    )
    ax.add_patch(box)
    cx, cy = xy[0] + w / 2, xy[1] + h / 2
    tx = text_x if text_x is not None else cx
    if sub:
        ax.text(tx, cy + h * title_offset, text, fontsize=pt(fontsize),
                fontweight="bold" if bold else "normal",
                color=text_color, ha=ha, va="center", zorder=zorder + 1)
        ax.text(tx, cy - h * sub_offset, sub, fontsize=pt(subsize),
                color=sub_color or text_color, ha=ha, va="center",
                zorder=zorder + 1, alpha=1.0, linespacing=linespacing)
    else:
        ax.text(tx, cy, text, fontsize=pt(fontsize),
                fontweight="bold" if bold else "normal",
                color=text_color, ha=ha, va="center", zorder=zorder + 1,
                linespacing=linespacing)


def arrow_v(ax, x, y1, y2, color=OCEAN_TEAL, width=2.4):
    ax.annotate("", xy=(x, y2), xytext=(x, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw(width),
                                mutation_scale=round(17 * FONT_SCALE)), zorder=1)


# Anything at or lighter than Bright Teal takes dark text -- white on Bright
# Teal is the contrast violation that is easiest to ship without noticing.
LIGHT_FILLS = (BRIGHT_TEAL, GOLDEN_YELLOW, WARM_GLOW, SOFT_SAGE, LIGHT_GRAY, WHITE)

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


def blank_axes(figsize):
    fig, ax = plt.subplots(figsize=figsize, facecolor=WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_position([0, 0, 1, 1])
    return fig, ax


def save(fig, name):
    fig.savefig(f"visuals/{name}", dpi=180, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)


# ---------------------------------------------------------------------------
# 1. Hero -- the dividing line runs between plumbing and accounting logic,
#    not between "build" and "buy"
# ---------------------------------------------------------------------------
PLUMBING = [
    "Authentication and identity",
    "Model gateways",
    "System connectors",
    "Orchestration platform",
    "Monitoring and logging",
]

ACCOUNTING_LOGIC = [
    "Why the reconciliation\nworks this way",
    "What counts as an exception",
    "What the auditor expects to see",
    "When an entry needs approval",
    "When the agent must stop",
]


def make_hero():
    # Row items are the focal text (32-36pt design-size benchmark, before the
    # PowerPoint pass), so every supporting element -- header, column
    # headers, divider label, banner, footer -- is sized a step up to match
    # rather than left behind. The canvas grows by the same FONT_SCALE
    # factor as the text, so every box keeps its size relative to the text
    # it holds.
    fig, ax = blank_axes(canvas(17.4, 17.4))
    add_header_bar(fig, "The Line Is Not Between Build and Buy",
                   "It runs between the plumbing and the accounting logic.",
                   height=0.212, title_size=48, subtitle_size=22, brand=False)

    col_w = 0.42
    left_x, right_x = 0.03, 0.55
    head_bottom, head_h = 0.700, 0.062
    box_h, gap = 0.082, 0.010
    pitch = box_h + gap

    rounded_box(ax, (left_x, head_bottom), col_w, head_h, OCEAN_TEAL,
                text_color=WHITE, text="BUY THE PLUMBING", fontsize=23)
    rounded_box(ax, (right_x, head_bottom), col_w, head_h, DEEP_NAVY,
                text_color=GOLDEN_YELLOW, text="OWN THE ACCOUNTING LOGIC",
                fontsize=23)

    for i, label in enumerate(PLUMBING):
        y = head_bottom - gap - i * pitch - box_h
        rounded_box(ax, (left_x, y), col_w, box_h, LIGHT_GRAY,
                    text_color=DEEP_NAVY, text=label, fontsize=26, bold=False,
                    linespacing=1.25, edge=OCEAN_TEAL, lw=lw(1.1))

    for i, label in enumerate(ACCOUNTING_LOGIC):
        y = head_bottom - gap - i * pitch - box_h
        rounded_box(ax, (right_x, y), col_w, box_h, MIDNIGHT_TEAL,
                    text_color=WHITE, text=label, fontsize=25, bold=False,
                    linespacing=1.2)

    rows_bottom = head_bottom - gap - (len(PLUMBING) - 1) * pitch - box_h
    header_top = head_bottom + head_h

    # The dividing line itself.
    ax.plot([0.50, 0.50], [0.168, header_top + 0.007], linestyle=(0, (5, 4)),
            color=OCEAN_TEAL, linewidth=lw(2.2), zorder=1)
    ax.text(0.50, 0.400, "THE  REAL  DIVIDING  LINE", rotation=90,
            fontsize=pt(19), fontweight="bold", color=ALERT_ORANGE,
            ha="center", va="center", zorder=4,
            bbox=dict(facecolor=WHITE, edgecolor="none", pad=round(5 * FONT_SCALE)))

    wf_bottom, wf_h = 0.058, 0.106
    label_y = rows_bottom - 0.024
    arrow_top = label_y - 0.024
    ax.text(left_x + col_w / 2, label_y,
            "somebody else builds this well", fontsize=pt(19), fontweight="bold",
            color=OCEAN_TEAL, ha="center", va="center")
    ax.text(right_x + col_w / 2, label_y,
            "nobody else knows this", fontsize=pt(19), fontweight="bold",
            color=SEA_GREEN, ha="center", va="center")
    arrow_v(ax, left_x + col_w / 2, arrow_top, wf_bottom + wf_h + 0.009,
            color=OCEAN_TEAL)
    arrow_v(ax, right_x + col_w / 2, arrow_top, wf_bottom + wf_h + 0.009,
            color=SEA_GREEN)

    rounded_box(ax, (0.03, wf_bottom), 0.94, wf_h, GOLDEN_YELLOW,
                text_color=DEEP_NAVY, text="BUY THE PLUMBING. OWN THE ACCOUNTING LOGIC.",
                fontsize=26,
                sub="The question is not who writes the code. It is where the accounting knowledge lives.",
                subsize=19, sub_color=OCEAN_TEAL,
                title_offset=0.19, sub_offset=0.24)

    # This line has to point at the two columns above it and add a beat the
    # banner has not already made -- accountability. An earlier version
    # ("build or buy is a budgeting question; this is a control question")
    # had no referent for "this" and contradicted the article's own point
    # that internal building carries real cost too.
    fig.text(0.5, 0.027,
             "You can buy the left column. You still have to answer for the right one.",
             fontsize=pt(19), color=DEEP_NAVY, ha="center", va="center",
             style="italic")
    # Footer branding keeps its original size -- exempt from the scale pass.
    fig.text(0.5, 0.006, "PythonMuse LLC  |  www.pythonmuse.com",
             fontsize=20, color=OCEAN_TEAL, ha="center", va="center", alpha=0.78)

    save(fig, "39_hero.png")


# ---------------------------------------------------------------------------
# 2. SOC scope -- what SOC 2 answers, what SOC 1 answers, what neither does
# ---------------------------------------------------------------------------
SOC_PANELS = [
    ("SOC 2", MIDNIGHT_TEAL, "ANSWERS",
     "Are the vendor's controls over security, availability,\n"
     "processing integrity, confidentiality and privacy\n"
     "suitably designed — and, in a Type 2, operating?",
     "An examination and a report.\nThere is no such thing as\n\"SOC 2 certified.\""),
    ("SOC 1", OCEAN_TEAL, "ANSWERS",
     "Are the vendor's controls relevant to your internal\n"
     "control over financial reporting designed and\n"
     "operating as described?",
     "The right question once an agent\ntouches journal entries — whatever\nthe marketing page says."),
    ("NEITHER", GOLDEN_YELLOW, "ANSWERS",
     "Does this agent correctly perform\n"
     "YOUR reconciliation, with YOUR exceptions,\n"
     "to YOUR evidence standard?",
     "This one does not arrive as a PDF.\nYou test it, or nobody does."),
]


def make_soc_scope():
    # The SOC 2 / SOC 1 / NEITHER chip is the category label for each row --
    # it was badly under-filling its box (~16% of box height) at the old
    # fontsize=30. Tripling it to 90 brings the fill ratio to the ~50-65%
    # SKILL.md target, so it now reads as a real badge instead of a caption.
    #
    # The italic note under each body paragraph -- the quotable punchline
    # ("There is no such thing as 'SOC 2 certified.'", "You test it, or
    # nobody does.") -- and the header subtitle are the actual "context"
    # text that needed the 3x treatment; an earlier pass enlarged the chip
    # and body instead and left these alone. Note fontsize triples from the
    # article's original 18pt baseline to 54 (up from this file's
    # intermediate 22). The header subtitle gets a real but smaller bump
    # (21 -> 28) -- tripling it too would put it at 63, larger than the
    # 44pt title above it, which is its own kind of broken.
    #
    # Because the note block is now the tallest thing in the card, the
    # vertical stack is rebuilt around it instead of the other way around:
    # verb + body + chip keep their old relative grouping in the upper
    # portion of a taller card, and the note gets its own, much larger
    # share of the card below them. Canvas grows to give all of this room
    # without touching a single coordinate in the other five visuals.
    # Round 4: the title, the "ANSWERS" label, the body paragraph, and the
    # closing line are pulled up into the same visual family as the chip and
    # note instead of the token +15% the previous pass gave them, which was
    # invisible next to 110pt chips and 66pt notes. They land just under the
    # note (the smaller of the two "large" elements) rather than above it,
    # so the chip > note > title ordering still holds. Chip (90) and note
    # (54) are untouched.
    #
    # The body at this size needs a much wider text column than it had, so
    # the canvas widens AND the chip box narrows (it was 8.8in wide holding
    # a word that needs under 6in) to hand that width back to the body.
    fig, ax = blank_axes(canvas(28.0, 31.8))
    add_header_bar(fig, "Three Reports. Three Different Questions.",
                   "Asking SOC 2 whether the agent reconciles your bank account is asking the wrong document.",
                   height=0.129, title_size=62, subtitle_size=40, brand=False)

    top = 0.859
    card_h = 0.244
    gap = 0.015
    x, w = 0.03, 0.94

    # Chip box narrowed from 0.30 -- "NEITHER" at fontsize=90 needs under
    # 6in and had 8.8in, and the body column needs that space more than the
    # chip does. The chip's text size does not change.
    chip_w = 0.25
    chip_h = 0.051

    # Vertical anchors as fractions of card_h, top to bottom: verb, then
    # body (chip aligns with body), then a real gap, then the note block.
    verb_y, body_y, note_y = 0.914, 0.658, 0.237

    for i, (name, fill, verb, body, note) in enumerate(SOC_PANELS):
        y = top - i * (card_h + gap) - card_h
        rounded_box(ax, (x, y), w, card_h, fill)

        title_col, note_col = text_colors(fill)
        # On Golden Yellow the body must not be white -- text_colors handles
        # the pairing, but the body line is set explicitly for clarity.
        body_col = DEEP_NAVY if fill in LIGHT_FILLS else WHITE

        chip_fill = WHITE if fill in LIGHT_FILLS else WARM_GLOW
        rounded_box(ax, (x + 0.022, y + card_h * body_y - chip_h / 2), chip_w, chip_h,
                    chip_fill, text_color=DEEP_NAVY, text=name, fontsize=90)

        text_left = x + 0.022 + chip_w + 0.030
        ax.text(text_left, y + card_h * verb_y, verb, fontsize=pt(44),
                fontweight="bold", color=note_col, ha="left", va="center",
                zorder=4)
        ax.text(text_left, y + card_h * body_y, body, fontsize=pt(46),
                color=body_col, ha="left", va="center", zorder=4,
                linespacing=1.42)
        ax.text(text_left, y + card_h * note_y, note, fontsize=pt(54),
                color=note_col, ha="left", va="center", zorder=4,
                style="italic", linespacing=1.38)

    # Wrapped to two lines -- as one line at this size it ran the full width
    # of the canvas and clipped at both edges.
    fig.text(0.5, 0.050,
             "Read the report, not the badge —\nthen ask for the complementary user entity controls.",
             fontsize=pt(44), color=DEEP_NAVY, ha="center", va="center",
             fontweight="bold", linespacing=1.4)
    fig.text(0.5, 0.010, "PythonMuse LLC  |  www.pythonmuse.com",
             fontsize=19, color=OCEAN_TEAL, ha="center", va="center", alpha=0.78)

    save(fig, "39_soc_scope.png")


# ---------------------------------------------------------------------------
# 3. Agent questions -- the accounting control question and its agent form
# ---------------------------------------------------------------------------
# The right column's longest lines are wrapped by hand: at design-size 24pt in
# a 0.455-wide column they overrun the card and collide with the incoming
# connector arrow. Wrapping keeps the wording intact rather than shrinking
# the font to fit.
AGENT_ROWS = [
    ("Who can perform the action?",
     "Which tools and systems\nmay the agent call?"),
    ("Who authorized it?",
     "Whose authority is the\nagent acting under?"),
    ("What access was granted?",
     "What is in scope — and\nwhat is deliberately not?"),
    ("What evidence exists?",
     "What does the agent log,\nand for how long?"),
    ("Can it be traced to the approver?",
     "Does the agent's identity\nappear in the audit trail?"),
    ("What happens when it goes wrong?",
     "What makes the agent stop\ninstead of continuing?"),
]


def make_agent_questions():
    fig, ax = blank_axes(canvas(19.0, 18.0))
    add_header_bar(fig, "The Questions Did Not Change. The Actor Did.",
                   "Accounting has asked all six of these since long before anyone said \"agentic.\"",
                   height=0.130, title_size=44, subtitle_size=21, brand=False)

    # Row geometry is sized so that the closing banner still clears the footer:
    # the first pass put banner_y below zero and the banner ran off the canvas.
    head_bottom, head_h = 0.790, 0.055
    left_x, right_x = 0.03, 0.515
    col_w = 0.455
    row_h, gap = 0.085, 0.013
    pitch = row_h + gap

    rounded_box(ax, (left_x, head_bottom), col_w, head_h, OCEAN_TEAL,
                text_color=WHITE, text="THE CONTROL QUESTION", fontsize=22)
    rounded_box(ax, (right_x, head_bottom), col_w, head_h, DEEP_NAVY,
                text_color=GOLDEN_YELLOW, text="ITS AGENT FORM", fontsize=22)

    for i, (classic, agentic) in enumerate(AGENT_ROWS):
        y = head_bottom - gap - i * pitch - row_h
        rounded_box(ax, (left_x, y), col_w, row_h, LIGHT_GRAY,
                    text_color=DEEP_NAVY, text=classic, fontsize=24,
                    bold=False, linespacing=1.25, edge=OCEAN_TEAL, lw=lw(1.1))
        rounded_box(ax, (right_x, y), col_w, row_h, MIDNIGHT_TEAL,
                    text_color=WHITE, text=agentic, fontsize=24,
                    bold=False, linespacing=1.25)
        # Connector between the two columns for this row.
        ax.annotate("", xy=(right_x - 0.004, y + row_h / 2),
                    xytext=(left_x + col_w + 0.004, y + row_h / 2),
                    arrowprops=dict(arrowstyle="-|>", color=SEA_GREEN, lw=lw(2.2),
                                    mutation_scale=round(16 * FONT_SCALE)), zorder=1)

    rows_bottom = head_bottom - gap - (len(AGENT_ROWS) - 1) * pitch - row_h

    banner_h = 0.100
    banner_y = rows_bottom - 0.048 - banner_h
    rounded_box(ax, (0.03, banner_y), 0.94, banner_h, GOLDEN_YELLOW,
                text_color=DEEP_NAVY,
                text="THE NOUNS CHANGED. THE QUESTIONS DID NOT.",
                fontsize=27,
                # This subtitle was the other 18pt floor -- also lands at
                # exactly 22pt now.
                sub="NIST is working on agent identity and authorization. Accounting has been working on it for a century.",
                subsize=18, sub_color=OCEAN_TEAL,
                title_offset=0.19, sub_offset=0.25)

    fig.text(0.5, 0.008, "PythonMuse LLC  |  www.pythonmuse.com",
             fontsize=19, color=OCEAN_TEAL, ha="center", va="center", alpha=0.78)

    save(fig, "39_agent_questions.png")


# ---------------------------------------------------------------------------
# 4. Exit test -- what you can walk out with
# ---------------------------------------------------------------------------
EXIT_ITEMS = [
    ("THE WORKFLOW", "Can it be exported in any usable form?"),
    ("THE INSTRUCTIONS", "Prompts, rules, thresholds and mappings your team wrote."),
    ("YOUR TEST CASES", "Real hours of accounting judgment. Who keeps them?"),
    ("LOGS AND EVIDENCE", "Especially for periods already audited."),
    ("OWNERSHIP", "Who owns what was built during implementation?"),
    ("THE ABILITY TO RUN IT", "Could your team operate this somewhere else?"),
]


def make_exit_test():
    fig, ax = blank_axes(canvas(17.0, 18.0))
    add_header_bar(fig, "The Exit Test",
                   "If the relationship ends tomorrow, what do you actually walk out with?",
                   height=0.128, title_size=50, subtitle_size=21, brand=False)

    # Card pitch is sized so the closing banner and the italic note both clear
    # the footer -- the first pass computed a negative banner_y and the banner,
    # the note and the footer all printed on top of each other.
    top = 0.824
    card_h = 0.088
    gap = 0.015
    x, w = 0.03, 0.94
    num_fills = [MIDNIGHT_TEAL, OCEAN_TEAL, SEA_GREEN,
                 MIDNIGHT_TEAL, OCEAN_TEAL, SEA_GREEN]

    for i, (label, detail) in enumerate(EXIT_ITEMS):
        y = top - i * (card_h + gap) - card_h
        rounded_box(ax, (x, y), w, card_h, LIGHT_GRAY, edge=OCEAN_TEAL, lw=lw(1.1))

        # Numbered badge, sized to sit inside the shorter card with margin.
        rounded_box(ax, (x + 0.020, y + card_h / 2 - 0.030), 0.068, 0.060,
                    num_fills[i], text_color=WHITE, text=str(i + 1), fontsize=28)

        text_left = x + 0.020 + 0.068 + 0.028
        ax.text(text_left, y + card_h * 0.680, label, fontsize=pt(25),
                fontweight="bold", color=DEEP_NAVY, ha="left", va="center",
                zorder=4)
        ax.text(text_left, y + card_h * 0.280, detail, fontsize=pt(21),
                color=OCEAN_TEAL, ha="left", va="center", zorder=4)

    rows_bottom = top - (len(EXIT_ITEMS) - 1) * (card_h + gap) - card_h

    # Both banner lines go through `text` so they render at the same weight --
    # passing the second as `sub` leaves it un-bolded beside a bold first line.
    banner_h = 0.108
    banner_y = rows_bottom - 0.045 - banner_h
    rounded_box(ax, (0.03, banner_y), 0.94, banner_h, GOLDEN_YELLOW,
                text_color=DEEP_NAVY,
                text="IF INDEPENDENCE IS IN THE SALES PITCH,\nIT BELONGS IN ACCEPTANCE TESTING.",
                fontsize=27, linespacing=1.6)

    fig.text(0.5, 0.038,
             "Run this before you sign — not the week you need it.",
             fontsize=pt(20), color=DEEP_NAVY, ha="center", va="center",
             style="italic")
    fig.text(0.5, 0.010, "PythonMuse LLC  |  www.pythonmuse.com",
             fontsize=19, color=OCEAN_TEAL, ha="center", va="center", alpha=0.78)

    save(fig, "39_exit_test.png")


# ---------------------------------------------------------------------------
# 5. Three questions -- and who owns the answer to each
# ---------------------------------------------------------------------------
TRUST_QUESTIONS = [
    ("1", "CAN I TRUST THE COMPANY?", MIDNIGHT_TEAL,
     "Security, privacy, contractual protections, financial\n"
     "viability, subservice organizations, business continuity,\n"
     "and the relevant SOC reports — read, not collected.",
     "VENDOR RISK MANAGEMENT"),
    ("2", "CAN I TRUST THE AGENT ENVIRONMENT?", OCEAN_TEAL,
     "Models, permissions, identity, authorization, tool access,\n"
     "logging, model-change notification, human intervention,\n"
     "and what happens when the agent fails.",
     "AI GOVERNANCE"),
    ("3", "CAN I TRUST THIS AGENT TO DO THIS WORK?", GOLDEN_YELLOW,
     "Your own testing. Your own exceptions. Your own control\n"
     "requirements. Your own evidence. There is no report\n"
     "from anybody else that answers this one.",
     "ACCOUNTING"),
]


def make_three_questions():
    # The header subtitle and the three-card body paragraph double here --
    # design 21 -> 42, exactly the "at least 2x" asked for. The question
    # heading, number badge, and owner chip are NOT part of this ask and
    # keep their old absolute size; because canvas width/height both have
    # to grow to give the doubled body room, the badge and owner-chip boxes
    # (sized as canvas fractions) are recomputed so their PHYSICAL size
    # stays put rather than growing along with the canvas by accident.
    fig, ax = blank_axes(canvas(22.0, 17.9))
    add_header_bar(fig, "Three Questions Before You Approve an Agent",
                   "Built it or bought it — the third one never leaves the department.",
                   height=0.183, title_size=43, subtitle_size=42, brand=False)

    top = 0.799
    card_h = 0.231
    gap = 0.023
    x, w = 0.03, 0.94

    # Badge and owner-chip boxes, re-expressed for the new canvas so their
    # absolute (inch) size matches what they were before this edit.
    badge_w, badge_h = 0.058, 0.077
    owner_chip_h = 0.050

    # Vertical anchors as fractions of card_h -- rebuilt from scratch around
    # the doubled body block rather than reusing the old fractions, which
    # were sized for a body block less than half this height.
    heading_y, body_y, owner_y = 0.876, 0.485, 0.089

    for i, (num, question, fill, body, owner) in enumerate(TRUST_QUESTIONS):
        y = top - i * (card_h + gap) - card_h
        rounded_box(ax, (x, y), w, card_h, fill)

        on_light = fill in LIGHT_FILLS
        head_col = DEEP_NAVY if on_light else WHITE
        body_col = DEEP_NAVY if on_light else WHITE
        note_col = OCEAN_TEAL if on_light else WARM_GLOW

        # Number badge, aligned with the body block it labels.
        badge_fill = WHITE if on_light else WARM_GLOW
        rounded_box(ax, (x + 0.022, y + card_h * body_y - badge_h / 2), badge_w, badge_h,
                    badge_fill, text_color=DEEP_NAVY, text=num, fontsize=30)

        text_left = x + 0.022 + badge_w + 0.028
        ax.text(text_left, y + card_h * heading_y, question, fontsize=pt(27),
                fontweight="bold", color=head_col, ha="left", va="center",
                zorder=4)
        ax.text(text_left, y + card_h * body_y, body, fontsize=pt(42),
                color=body_col, ha="left", va="center", zorder=4,
                linespacing=1.40)

        # Owner chip, bottom-left under the body, widened for its label.
        chip_w = 0.243 if len(owner) > 16 else 0.162
        rounded_box(ax, (text_left, y + card_h * owner_y - owner_chip_h / 2), chip_w, owner_chip_h,
                    DEEP_NAVY if on_light else WHITE,
                    text_color=GOLDEN_YELLOW if on_light else DEEP_NAVY,
                    text=owner, fontsize=19)

        if i == 2:
            ax.text(x + w - 0.028, y + card_h * owner_y,
                    "does not outsource", fontsize=pt(20), fontweight="bold",
                    color=OCEAN_TEAL, ha="right", va="center", zorder=4,
                    style="italic")

    fig.text(0.5, 0.032,
             "\"How do you know this works?\" is not a question the vendor can answer for you.",
             fontsize=pt(21), color=DEEP_NAVY, ha="center", va="center",
             fontweight="bold")
    fig.text(0.5, 0.009, "PythonMuse LLC  |  www.pythonmuse.com",
             fontsize=19, color=OCEAN_TEAL, ha="center", va="center", alpha=0.78)

    save(fig, "39_three_questions.png")


# ---------------------------------------------------------------------------
# 6. Social square
# ---------------------------------------------------------------------------
def make_social_square():
    # Narrow canvas (8in), so the title wraps to two lines to stay dominant --
    # add_header_bar's offsets assume one line, so the bar is built by hand.
    fig, ax = blank_axes(canvas(8, 12.4))
    header_h = 0.230
    bar = FancyBboxPatch(
        (0, 1 - header_h), 1, header_h,
        boxstyle="square,pad=0", transform=fig.transFigure,
        facecolor=DEEP_NAVY, edgecolor="none", zorder=0,
    )
    fig.patches.append(bar)
    fig.text(0.05, 0.975, "Buy the Platform.\nOwn the Logic.", fontsize=pt(42),
             fontweight="bold", color=WHITE, va="top", ha="left",
             linespacing=1.1)
    fig.text(0.05, 0.818, "Build or buy is the wrong question.",
             fontsize=pt(21), color=WARM_GLOW, va="top", ha="left")

    rounded_box(ax, (0.06, 0.584), 0.88, 0.173, MIDNIGHT_TEAL,
                text_color=WHITE, text="A SOC 2 REPORT TELLS YOU",
                fontsize=21,
                sub="THE VENDOR'S CONTROLS\nWERE EXAMINED",
                subsize=24, sub_color=WARM_GLOW, linespacing=1.3,
                title_offset=0.26, sub_offset=0.18)

    rounded_box(ax, (0.06, 0.390), 0.88, 0.173, OCEAN_TEAL,
                text_color=WHITE, text="IT DOES NOT TELL YOU",
                fontsize=21,
                sub="THAT THE AGENT RECONCILES\nYOUR BANK ACCOUNT",
                subsize=24, sub_color=WARM_GLOW, linespacing=1.3,
                title_offset=0.26, sub_offset=0.18)

    rounded_box(ax, (0.06, 0.199), 0.88, 0.168, GOLDEN_YELLOW,
                text_color=DEEP_NAVY,
                text="THAT PART IS\nSTILL YOURS",
                fontsize=28, linespacing=1.7)

    # This closing line was the third 18pt floor in the set -- also now 22pt.
    fig.text(0.5, 0.120,
             "Buy the plumbing.\nOwn the accounting logic.",
             fontsize=pt(18), color=DEEP_NAVY, ha="center", va="center",
             fontweight="bold", linespacing=1.6)
    fig.text(0.5, 0.025, "PythonMuse LLC  |  www.pythonmuse.com", fontsize=18,
             color=OCEAN_TEAL, ha="center", va="center", alpha=0.85)

    save(fig, "39_social_square.png")


if __name__ == "__main__":
    make_hero()
    make_soc_scope()
    make_agent_questions()
    make_exit_test()
    make_three_questions()
    make_social_square()
    print("Generated 6 visuals for Article 39.")
