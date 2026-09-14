"""Generate branded visuals for Article 38 -- Your AI Workflow Was Approved. Did
Anyone Read the Customer Contract?

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


def add_header_bar(fig, title, subtitle, height=0.13, title_size=29,
                    subtitle_size=16, brand_size=10.5, brand=True):
    bar = FancyBboxPatch(
        (0, 1 - height), 1, height,
        boxstyle="square,pad=0", transform=fig.transFigure,
        facecolor=DEEP_NAVY, edgecolor="none", zorder=0,
    )
    fig.patches.append(bar)
    fig.text(0.03, 1 - height / 2 + 0.018, title, fontsize=title_size,
             fontweight="bold", color=WHITE, va="center", ha="left")
    fig.text(0.03, 1 - height / 2 - 0.032, subtitle, fontsize=subtitle_size,
             color=WARM_GLOW, va="center", ha="left", alpha=1.0)
    if brand:
        fig.text(0.97, 1 - height / 2, "PythonMuse LLC", fontsize=brand_size,
                 color=WHITE, va="center", ha="right", alpha=0.70)


# FancyBboxPatch inflates each box by `pad` on every side. Keep this small so
# that the gaps computed in each layout below survive and the connector arrows
# stay visible -- a larger pad silently eats them.
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
        ax.text(tx, cy + h * title_offset, text, fontsize=fontsize,
                fontweight="bold" if bold else "normal",
                color=text_color, ha=ha, va="center", zorder=zorder + 1)
        ax.text(tx, cy - h * sub_offset, sub, fontsize=subsize,
                color=sub_color or text_color, ha=ha, va="center",
                zorder=zorder + 1, alpha=1.0, linespacing=linespacing)
    else:
        ax.text(tx, cy, text, fontsize=fontsize,
                fontweight="bold" if bold else "normal",
                color=text_color, ha=ha, va="center", zorder=zorder + 1,
                linespacing=linespacing)


def arrow_v(ax, x, y1, y2, color=OCEAN_TEAL, lw=2.4):
    ax.annotate("", xy=(x, y2), xytext=(x, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                mutation_scale=17), zorder=1)


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
# 1. Hero -- what our governance approved vs. what the customer's MSA says
# ---------------------------------------------------------------------------
APPROVED = [
    "Use case documented",
    "Access limited to what's needed",
    "Results tested and reviewed",
    "Human review built in",
    "Governance Lead signed off",
]

MSA_SAYS = [
    "Disclose AI use before deployment",
    "No training on our data",
    "Limits on automated decisions",
    "Requirements flow down to subcontractors",
    "Notify us when problems are known",
]


def make_hero():
    fig, ax = blank_axes((13.4, 10.6))
    add_header_bar(fig, "Approved by Us. Permitted by Them?",
                   "Both can be true about the same workflow at the same time.",
                   height=0.092)

    col_w = 0.40
    left_x, right_x = 0.04, 0.56
    head_bottom, head_h = 0.735, 0.080
    box_h, gap = 0.080, 0.014
    pitch = box_h + gap

    rounded_box(ax, (left_x, head_bottom), col_w, head_h, DEEP_NAVY,
                text_color=GOLDEN_YELLOW, text="OUR AI GOVERNANCE APPROVED",
                fontsize=18.5)
    rounded_box(ax, (right_x, head_bottom), col_w, head_h, OCEAN_TEAL,
                text_color=WHITE, text="THE CUSTOMER'S MSA SAYS", fontsize=18.5)

    for i, label in enumerate(APPROVED):
        y = head_bottom - gap - i * pitch - box_h
        rounded_box(ax, (left_x, y), col_w, box_h, MIDNIGHT_TEAL,
                    text_color=WHITE, text=label, fontsize=17, bold=False,
                    linespacing=1.3)

    for i, label in enumerate(MSA_SAYS):
        y = head_bottom - gap - i * pitch - box_h
        rounded_box(ax, (right_x, y), col_w, box_h, LIGHT_GRAY,
                    text_color=DEEP_NAVY, text=label, fontsize=17, bold=False,
                    linespacing=1.3, edge=OCEAN_TEAL, lw=1.1)

    rows_bottom = head_bottom - gap - (len(APPROVED) - 1) * pitch - box_h
    header_center = head_bottom + head_h / 2
    header_top = head_bottom + head_h

    # The control gap itself, sitting between two columns that can each be
    # entirely correct on their own.
    ax.plot([0.50, 0.50], [0.205, header_top + 0.010], linestyle=(0, (5, 4)),
            color=OCEAN_TEAL, linewidth=2.2, zorder=1)
    ax.text(0.50, 0.46, "THE  CONTROL  GAP", rotation=90, fontsize=16.5,
            fontweight="bold", color=ALERT_ORANGE, ha="center", va="center",
            zorder=4, bbox=dict(facecolor=WHITE, edgecolor="none", pad=5))

    # Neither column contradicts the other -- they just never compared notes.
    ax.text(0.50, header_center, "≠", fontsize=28, fontweight="bold",
            color=ALERT_ORANGE, ha="center", va="center", zorder=5,
            bbox=dict(facecolor=WHITE, edgecolor="none", pad=2))

    wf_bottom, wf_h = 0.095, 0.145
    arrow_v(ax, left_x + col_w / 2, rows_bottom - 0.018, wf_bottom + wf_h + 0.014,
            color=OCEAN_TEAL)
    arrow_v(ax, right_x + col_w / 2, rows_bottom - 0.018, wf_bottom + wf_h + 0.014,
            color=SEA_GREEN)
    ax.text(left_x + col_w / 2, rows_bottom - 0.050,
            "all true", fontsize=16, fontweight="bold", color=OCEAN_TEAL,
            ha="center", va="center")
    ax.text(right_x + col_w / 2, rows_bottom - 0.050,
            "also true", fontsize=16, fontweight="bold", color=SEA_GREEN,
            ha="center", va="center")

    rounded_box(ax, (0.04, wf_bottom), 0.92, wf_h, GOLDEN_YELLOW,
                text_color=DEEP_NAVY, text="THE WORKFLOW GOES LIVE",
                fontsize=20,
                sub="Nobody asked whether the applicable customer contract permitted it",
                subsize=16.5, sub_color=OCEAN_TEAL,
                title_offset=0.17, sub_offset=0.24)

    fig.text(0.5, 0.046,
             "Approved by internal governance is not the same question as permitted by contract.",
             fontsize=16.5, color=DEEP_NAVY, ha="center", va="center",
             style="italic")
    fig.text(0.5, 0.014, "PythonMuse LLC  |  www.pythonmuse.com",
             fontsize=11, color=OCEAN_TEAL, ha="center", va="center", alpha=0.78)

    save(fig, "38_hero.png")


# ---------------------------------------------------------------------------
# 2. Service layers -- direct service, supporting activities, internal use
# ---------------------------------------------------------------------------
LAYERS3 = [
    ("LAYER 1\nDIRECT\nSERVICE", MIDNIGHT_TEAL,
     "Inspect the vehicle. Change the oil. Replace the part.",
     "Everyone agrees the contract covers this.",
     "Clear."),
    ("LAYER 2\nSUPPORTING\nACTIVITIES", OCEAN_TEAL,
     "Schedule the appointment. Create the work order. Draft the invoice.",
     "This is where AI shows up first —\nand the AI never touches the oil filter.",
     "Depends how 'Services' is defined."),
    ("LAYER 3\nINTERNAL\nANALYSIS", SEA_GREEN,
     "Profitability analysis. Forecasting. Management reporting.",
     "Still uses the customer's information,\nseveral steps removed.",
     "Rarely what the drafter had in mind."),
]


def make_service_layers():
    fig, ax = blank_axes((13.4, 12.4))
    add_header_bar(fig, "Where Does the Service Actually End?",
                   "The same customer engagement, in three layers -- and AI doesn't stay in layer one.",
                   height=0.088)

    row_h, row_gap = 0.202, 0.030
    pitch = row_h + row_gap
    top = 0.868
    chip_x, chip_w = 0.05, 0.235
    body_x, body_w = 0.305, 0.660

    for i, (name, color, doing, note, clarity) in enumerate(LAYERS3):
        y = top - i * pitch - row_h
        rounded_box(ax, (chip_x, y), chip_w, row_h, color,
                    text_color=WHITE, text=name, fontsize=17.5,
                    linespacing=1.3)
        rounded_box(ax, (body_x, y), body_w, row_h, LIGHT_GRAY,
                    text_color=DEEP_NAVY, text="", edge=OCEAN_TEAL, lw=1.1)
        ax.text(body_x + 0.028, y + row_h * 0.83, doing, fontsize=17.5,
                color=DEEP_NAVY, ha="left", va="center", zorder=4)
        # The bolded "punchline" line -- enlarged per feedback, and the one
        # long enough (Layer 2) to need a manual line break to stay inside
        # the card at the larger size. The figure was made taller (12.4in,
        # up from 11.4in) rather than growing row_h, so this row keeps the
        # same fraction of the layout but gets more physical inches to work
        # with -- see the Standard Color Constants comment on BOX_PAD for
        # why growing figsize beats growing fractional coordinates here.
        ax.text(body_x + 0.028, y + row_h * 0.48, note, fontsize=19,
                fontweight="bold", color=OCEAN_TEAL, ha="left", va="center",
                zorder=4, linespacing=1.25)
        ax.text(body_x + 0.028, y + row_h * 0.12, "MSA reach: " + clarity,
                fontsize=17, color=DEEP_NAVY, ha="left", va="center",
                zorder=4, style="italic")

    bottom_row_y = top - (len(LAYERS3) - 1) * pitch - row_h
    ax.annotate("", xy=(0.022, bottom_row_y + 0.01), xytext=(0.022, top - 0.01),
                arrowprops=dict(arrowstyle="-|>", color=ALERT_ORANGE, lw=2.8,
                                mutation_scale=19), zorder=1)
    ax.text(0.011, (top + bottom_row_y) / 2, "HOW CLEARLY DOES THE MSA REACH?",
            rotation=90, fontsize=16, fontweight="bold", color=ALERT_ORANGE,
            ha="center", va="center")

    rounded_box(ax, (0.05, 0.038), 0.90, 0.155, DEEP_NAVY, text_color=WHITE,
                text="Which layers does “in connection with the Services” cover?",
                fontsize=18.5,
                sub="If nobody can answer confidently, resolve it before automating the layer beneath it.",
                subsize=16.5, sub_color=WARM_GLOW,
                title_offset=0.24, sub_offset=0.24)

    fig.text(0.5, 0.0125, "PythonMuse LLC  |  www.pythonmuse.com",
             fontsize=11, color=OCEAN_TEAL, ha="center", va="center", alpha=0.78)

    save(fig, "38_service_layers.png")


# ---------------------------------------------------------------------------
# 3. Processing vs. training -- two different questions, two different answers
# ---------------------------------------------------------------------------
def make_process_vs_train():
    fig, ax = blank_axes((13.4, 12.0))
    add_header_bar(fig, "Using the Data Is Not the Same as Training on It",
                   "Same document, two separate questions -- and the contract may answer them differently.",
                   height=0.100, subtitle_size=18.5)

    card_top, card_bottom = 0.845, 0.280
    card_h = card_top - card_bottom
    left_x, right_x, card_w = 0.04, 0.52, 0.44

    rounded_box(ax, (left_x, card_bottom), card_w, card_h, LIGHT_GRAY,
                text_color=DEEP_NAVY, text="", edge=OCEAN_TEAL, lw=1.2)
    ax.text(left_x + card_w / 2, card_top - 0.058, "PROCESSING THE DATA",
            fontsize=20, fontweight="bold", color=DEEP_NAVY,
            ha="center", va="center", zorder=4)

    left_rows = [
        ("What it means", "Reads records to draft the invoice"),
        ("Anthropic (Commercial Terms)", "Not used to train models"),
        ("Microsoft Copilot", "Graph data not used to train"),
        ("OpenAI API", "Not used to train, unless opted in"),
    ]
    row_top, row_pitch = card_top - 0.132, 0.122

    y = row_top
    for label, value in left_rows:
        ax.text(left_x + 0.032, y + 0.030, label, fontsize=18,
                color=OCEAN_TEAL, ha="left", va="center", zorder=4)
        ax.text(left_x + 0.032, y - 0.028, value, fontsize=17.5,
                fontweight="bold", color=DEEP_NAVY, ha="left", va="center",
                zorder=4)
        y -= row_pitch

    rounded_box(ax, (right_x, card_bottom), card_w, card_h, MIDNIGHT_TEAL,
                text_color=WHITE, text="", edge="none")
    ax.text(right_x + card_w / 2, card_top - 0.058, "TRAINING ON THE DATA",
            fontsize=20, fontweight="bold", color=GOLDEN_YELLOW,
            ha="center", va="center", zorder=4)

    right_rows = [
        ("What it means", "Used to improve the model"),
        ("Consumer Claude (Free / Pro / Max)", "Used unless you opt out"),
        ("Same vendor, different product", "The tier changes the answer"),
        ("Ask", "Retained? Disabled? Which tier?"),
    ]
    y = row_top
    for label, value in right_rows:
        ax.text(right_x + 0.032, y + 0.030, label, fontsize=18,
                color=WARM_GLOW, ha="left", va="center", zorder=4)
        ax.text(right_x + 0.032, y - 0.028, value, fontsize=17.5,
                fontweight="bold", color=WHITE, ha="left", va="center",
                zorder=4)
        y -= row_pitch

    rounded_box(ax, (0.04, 0.038), 0.92, 0.225, DEEP_NAVY,
                text_color=WHITE,
                text="Same vendor. Different tier. Different answer.",
                fontsize=20,
                sub="A contract can permit processing customer data as part of the service while\nseparately prohibiting the use of that data to train, fine-tune, or improve a\nmodel. Get the answer in writing, then match it to what the contract promised.",
                subsize=18, sub_color=WARM_GLOW, linespacing=1.42,
                title_offset=0.29, sub_offset=0.15)

    fig.text(0.5, 0.0115, "PythonMuse LLC  |  www.pythonmuse.com",
             fontsize=11, color=OCEAN_TEAL, ha="center", va="center", alpha=0.78)

    save(fig, "38_process_vs_train.png")


# ---------------------------------------------------------------------------
# 4. One approved tool, four customers, four different answers
# ---------------------------------------------------------------------------
CUSTOMERS = [
    ("CUSTOMER A", "Permitted", SOFT_SAGE,
     "No AI-specific\nrestrictions\nin the MSA."),
    ("CUSTOMER B", "Disclose First", GOLDEN_YELLOW,
     "MSA requires\nnotice before\nAI is used."),
    ("CUSTOMER C", "Additional\nReview", ALERT_ORANGE,
     "MSA restricts\nautomated\ndecisioning."),
    ("CUSTOMER D", "No AI\nLanguage", BRIGHT_TEAL,
     "Silent on AI --\nconfirm what\n“Services” covers."),
]


def make_customer_dimension():
    fig, ax = blank_axes((13.4, 11.2))
    add_header_bar(fig, "One Approved Tool. Four Different Answers.",
                   "The same AI-assisted billing workflow, evaluated against four real contracts.",
                   height=0.090)

    # Header bar occupies the top 0.090 of the figure (down to y=0.910), so
    # everything below has to clear that with room to spare.
    top_w, top_h = 0.64, 0.105
    top_x = 0.5 - top_w / 2
    top_y = 0.780
    rounded_box(ax, (top_x, top_y), top_w, top_h, DEEP_NAVY, text_color=WHITE,
                text="APPROVED: AI-ASSISTED INVOICE DRAFTING TOOL",
                fontsize=17.5,
                sub="Same tool. Same workflow. Same internal approval.",
                subsize=15, sub_color=WARM_GLOW,
                title_offset=0.20, sub_offset=0.26)

    col_w, col_gap = 0.220, 0.020
    total_w = 4 * col_w + 3 * col_gap
    start_x = 0.5 - total_w / 2
    card_h, card_y = 0.390, 0.225

    for i, (name, verdict, color, detail) in enumerate(CUSTOMERS):
        x = start_x + i * (col_w + col_gap)
        arrow_v(ax, x + col_w / 2, top_y - 0.012, card_y + card_h + 0.012,
                color=OCEAN_TEAL)
        title_color, sub_color = text_colors(color)
        # Drawn as a bare box, then three separate text calls -- rounded_box's
        # built-in title/sub placement auto-centers a multi-line block and
        # will not reliably keep three stacked labels inside a short card.
        rounded_box(ax, (x, card_y), col_w, card_h, color, text="")
        cx = x + col_w / 2
        ax.text(cx, card_y + card_h * 0.88, name, fontsize=16.5,
                fontweight="bold", color=title_color, ha="center",
                va="center", zorder=4)
        ax.text(cx, card_y + card_h * 0.63, verdict, fontsize=19,
                fontweight="bold", color=title_color, ha="center",
                va="center", zorder=4, linespacing=1.2)
        # The bottom section of the card -- the "so what does this contract
        # actually say" line -- enlarged per feedback; it now needs more
        # vertical room than the other two lines, hence the taller card.
        ax.text(cx, card_y + card_h * 0.22, detail, fontsize=18,
                color=sub_color, ha="center", va="center", zorder=4,
                linespacing=1.30)

    rounded_box(ax, (0.05, 0.038), 0.90, 0.170, MIDNIGHT_TEAL, text_color=WHITE,
                text="Is this tool approved for this workflow, using this data,\nfor this customer, under this contract?",
                fontsize=18.5,
                sub="“Approved for the organization” and “permitted for this customer”\nare two different questions -- and only one of them is usually being asked.",
                subsize=15.5, sub_color=WARM_GLOW, linespacing=1.35,
                title_offset=0.24, sub_offset=0.20)

    fig.text(0.5, 0.0115, "PythonMuse LLC  |  www.pythonmuse.com",
             fontsize=11, color=OCEAN_TEAL, ha="center", va="center", alpha=0.78)

    save(fig, "38_customer_dimension.png")


# ---------------------------------------------------------------------------
# 5. Six practical controls -- preventive vs. detective
# ---------------------------------------------------------------------------
CONTROLS = [
    ("Flag AI terms during contract review",
     "Record whether a new MSA restricts\nAI, ML, decisioning, or training.",
     "PREVENTIVE", MIDNIGHT_TEAL),
    ("Define the perimeter clearly",
     "Make definitions specific enough\nto separate delivery from support.",
     "PREVENTIVE", MIDNIGHT_TEAL),
    ("Add a contract checkpoint to AI approval",
     "Before deployment, determine\nwhether customer-specific\nrestrictions apply.",
     "PREVENTIVE", MIDNIGHT_TEAL),
    ("Understand what happens to the data",
     "Separate processing customer\ninformation from retaining or\ntraining on it.",
     "PREVENTIVE", MIDNIGHT_TEAL),
    ("Map the full workflow",
     "Follow customer data through\ndelivery, billing, collections,\nand reporting.",
     "DETECTIVE", OCEAN_TEAL),
    ("Establish re-review triggers",
     "New data, customers, models,\nor contract terms should\ntrigger a re-review.",
     "DETECTIVE", OCEAN_TEAL),
]


def make_controls():
    # Doubling the detail text (18pt -> 36pt) doesn't fit in the old
    # 13.4x13.5 layout at any reasonable line count, so this figure is both
    # wider (more usable width per line) and considerably taller (six rows,
    # each now sized for a 3-line block at 36pt) than the rest of the set.
    fig, ax = blank_axes((15.0, 25.5))
    # add_header_bar's title/subtitle offsets (+/-0.018, -0.032) are fixed
    # figure-fraction constants, not inches -- header height needs to stay
    # roughly >=0.08 regardless of how tall the overall figure is, or the
    # subtitle anchor falls outside the bar entirely. That's what clipped
    # the title and dropped the subtitle onto row 1 at height=0.041.
    add_header_bar(fig, "Six Controls, Not One Legal Review",
                   "You do not need to send every automation idea to Legal. You do need these.",
                   height=0.082)

    row_h, row_gap = 0.126, 0.010
    pitch = row_h + row_gap
    top = 0.905
    body_x, body_w = 0.035, 0.820
    chip_x, chip_w = 0.870, 0.095

    for i, (title, detail, kind, color) in enumerate(CONTROLS):
        y = top - i * pitch - row_h
        rounded_box(ax, (body_x, y), body_w, row_h, color, text_color=WHITE,
                    text=title, fontsize=20, sub=detail, subsize=36,
                    sub_color=WARM_GLOW, ha="left",
                    text_x=body_x + 0.022,
                    title_offset=0.39, sub_offset=0.0, linespacing=1.18)
        chip_fill = GOLDEN_YELLOW if kind == "PREVENTIVE" else BRIGHT_TEAL
        rounded_box(ax, (chip_x, y), chip_w, row_h, chip_fill,
                    text_color=DEEP_NAVY, text=kind, fontsize=14)

    rounded_box(ax, (0.035, 0.021), 0.930, 0.086, DEEP_NAVY, text_color=WHITE,
                text="The goal is the right question reaching the right person before launch.",
                fontsize=18.5,
                sub="Not more bureaucracy -- one field in a register and one flag in contract review.",
                subsize=16, sub_color=WARM_GLOW,
                title_offset=0.24, sub_offset=0.24)

    fig.text(0.5, 0.006,
             "PythonMuse LLC  |  www.pythonmuse.com",
             fontsize=11, color=OCEAN_TEAL, ha="center", va="center", alpha=0.78)

    save(fig, "38_controls.png")


# ---------------------------------------------------------------------------
# 6. Social square -- the punchline
# ---------------------------------------------------------------------------
def make_social_square():
    fig, ax = blank_axes((8, 10.8))
    header_h = 0.135
    add_header_bar(fig, "Did Anyone Read the Contract?",
                   "AI governance has a customer dimension.",
                   height=header_h, title_size=24, subtitle_size=15.5,
                   brand=False)

    # The second line in each box is now uppercase to match the title above
    # it (not lowercase, per feedback) and enlarged enough that it needs two
    # lines to stay inside the box.
    rounded_box(ax, (0.06, 0.660), 0.88, 0.195, MIDNIGHT_TEAL,
                text_color=WHITE, text="YOUR AI GOVERNANCE CAN SAY",
                fontsize=18,
                sub="DOCUMENTED, TESTED,\nREVIEWED, APPROVED",
                subsize=20, sub_color=WARM_GLOW, linespacing=1.3,
                title_offset=0.26, sub_offset=0.18)

    rounded_box(ax, (0.06, 0.440), 0.88, 0.195, OCEAN_TEAL,
                text_color=WHITE, text="THE MSA CAN STILL SAY",
                fontsize=18,
                sub="NOT WITHOUT DISCLOSURE.\nNOT FOR THIS DECISION.",
                subsize=20, sub_color=WARM_GLOW, linespacing=1.3,
                title_offset=0.26, sub_offset=0.18)

    # Both lines belong to `text` so they render at the same weight -- passing
    # the second as `sub` leaves it un-bolded next to a bold first line.
    rounded_box(ax, (0.06, 0.225), 0.88, 0.190, GOLDEN_YELLOW,
                text_color=DEEP_NAVY,
                text="APPROVED ISN'T\nPERMITTED",
                fontsize=25, linespacing=1.7)

    fig.text(0.5, 0.135,
             "Your AI register and your contract\nregister need to start talking.",
             fontsize=16.5, color=DEEP_NAVY, ha="center", va="center",
             fontweight="bold", linespacing=1.6)
    fig.text(0.5, 0.028, "PythonMuse LLC  |  www.pythonmuse.com", fontsize=11,
             color=OCEAN_TEAL, ha="center", va="center", alpha=0.85)

    save(fig, "38_social_square.png")


if __name__ == "__main__":
    make_hero()
    make_service_layers()
    make_process_vs_train()
    make_customer_dimension()
    make_controls()
    make_social_square()
    print("Generated 6 visuals for Article 38.")
