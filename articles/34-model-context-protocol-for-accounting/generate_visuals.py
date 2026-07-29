"""Generate branded visuals for Article 34 — From Reports to Requests.

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


def add_header_bar(fig, title, subtitle, height=0.14):
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
                 sub="", subsize=10, sub_color=None, bold=True, title_offset=0.14,
                 sub_offset=0.22, linespacing=1.4, edge=None, lw=0):
    box = FancyBboxPatch(
        xy, w, h, boxstyle=f"round,pad={BOX_PAD},rounding_size=0.03",
        facecolor=color, edgecolor=edge or "none", linewidth=lw, zorder=2,
    )
    ax.add_patch(box)
    cx, cy = xy[0] + w / 2, xy[1] + h / 2
    if sub:
        ax.text(cx, cy + h * title_offset, text, fontsize=fontsize,
                 fontweight="bold" if bold else "normal",
                 color=text_color, ha="center", va="center", zorder=3)
        ax.text(cx, cy - h * sub_offset, sub, fontsize=subsize, color=sub_color or text_color,
                 ha="center", va="center", zorder=3, alpha=1.0, linespacing=linespacing)
    else:
        ax.text(cx, cy, text, fontsize=fontsize, fontweight="bold" if bold else "normal",
                 color=text_color, ha="center", va="center", zorder=3, linespacing=linespacing)


def arrow_h(ax, x1, y, x2, color=OCEAN_TEAL, lw=2.4):
    ax.annotate("", xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                shrinkA=2, shrinkB=2, mutation_scale=18), zorder=1)


def arrow_v(ax, x, y1, y2, color=OCEAN_TEAL, lw=2.2):
    ax.annotate("", xy=(x, y2), xytext=(x, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                mutation_scale=16), zorder=1)


# ---------------------------------------------------------------------------
# 1. Hero — One Question, Three Accounting Eras
# ---------------------------------------------------------------------------
def make_hero():
    fig, ax = plt.subplots(figsize=(14, 7.2), facecolor=WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_position([0, 0, 1, 1])

    add_header_bar(fig, "One Question, Three Accounting Eras",
                    "The objective has not changed. The path to the answer has.", height=0.13)

    # Shared business question banner
    rounded_box(ax, (0.06, 0.685), 0.88, 0.10, MIDNIGHT_TEAL, text_color=WHITE,
                text='"Compare customer revenue and gross margin across all systems."',
                fontsize=14)
    fig.text(0.5, 0.665, "The same request, asked three ways",
              fontsize=10.5, color=OCEAN_TEAL, ha="center", va="top", style="italic")

    eras = [
        ("TRADITIONAL\nACCOUNTANT", OCEAN_TEAL,
         "Reports\n↓\nExports\n↓\nLookups\n↓\nReconciliation",
         "2–3 hours"),
        ("AI-ENABLED\nBUILDER", SEA_GREEN,
         "Prompt\n↓\nSQL / Python\n↓\nValidation",
         "10–30 minutes"),
        ("CONVERSATIONAL\nMCP USER", GOLDEN_YELLOW,
         "Natural-language\nrequest\n↓\nApproved workflow\n↓\nReview",
         "5–15 minutes"),
    ]

    n = len(eras)
    box_w = 0.26
    gap = (1 - n * box_w - 0.12) / (n - 1)
    x_start = 0.06
    col_top = 0.60
    col_h = 0.40

    for i, (title, color, steps, timing) in enumerate(eras):
        x = x_start + i * (box_w + gap)
        text_color = OCEAN_TEAL if color in (GOLDEN_YELLOW, WARM_GLOW) else WHITE

        # Header block
        rounded_box(ax, (x, col_top - 0.10), box_w, 0.10, color,
                    text_color=text_color, text=title, fontsize=13, linespacing=1.3)

        # Steps panel
        panel_h = col_h - 0.10 - 0.075
        rounded_box(ax, (x, col_top - 0.10 - panel_h - 0.012), box_w, panel_h, "#F5F5F5",
                    text_color=DEEP_NAVY, text=steps, fontsize=11.5, bold=False,
                    linespacing=1.55)

        # Timing chip
        rounded_box(ax, (x + box_w * 0.18, 0.115), box_w * 0.64, 0.062, color,
                    text_color=text_color, text=timing, fontsize=12)

    fig.text(0.5, 0.055,
              "Illustrative times only — actual effort depends on data quality, system access, workflow complexity, and required controls.",
              fontsize=10.5, color=OCEAN_TEAL, ha="center", va="center", style="italic", alpha=1.0)

    fig.savefig("visuals/34_hero.png", dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


# ---------------------------------------------------------------------------
# 2. APIs/SQL/ETL versus MCP — split screen
# ---------------------------------------------------------------------------
def make_api_vs_mcp():
    fig, ax = plt.subplots(figsize=(13, 7.4), facecolor=WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_position([0, 0, 1, 1])

    add_header_bar(fig, "APIs and SQL vs. MCP",
                    "Complementary layers — not competing solutions", height=0.13)

    panels = [
        (0.055, "APIs, SQL, and ETL", SEA_GREEN,
         ["Systems", "Data connection", "Structured data", "Calculation"],
         "Moves and transforms data reliably."),
        (0.545, "MCP", GOLDEN_YELLOW,
         ["Accountant's request", "AI co-pilot", "Approved tool selection", "API, SQL, report, or script"],
         "Connects human intent to approved capabilities."),
    ]

    panel_w = 0.40
    for x0, title, color, steps, caption in panels:
        text_color = OCEAN_TEAL if color in (GOLDEN_YELLOW, WARM_GLOW) else WHITE
        rounded_box(ax, (x0, 0.685), panel_w, 0.085, color,
                    text_color=text_color, text=title, fontsize=15)

        step_h = 0.088
        step_gap = 0.038
        top = 0.635
        centers = []
        for i, step in enumerate(steps):
            y = top - i * (step_h + step_gap) - step_h
            centers.append(y + step_h / 2)
            rounded_box(ax, (x0, y), panel_w, step_h, "#F5F5F5",
                        text_color=DEEP_NAVY, text=step, fontsize=12, bold=False)
        for i in range(len(steps) - 1):
            arrow_v(ax, x0 + panel_w / 2,
                    centers[i] - step_h / 2 - 0.004,
                    centers[i + 1] + step_h / 2 + 0.004)

        fig.text(x0 + panel_w / 2, 0.105, caption, fontsize=11.5, color=OCEAN_TEAL,
                  ha="center", va="center", style="italic", alpha=1.0)

    # Center divider
    ax.plot([0.5, 0.5], [0.09, 0.79], color=OCEAN_TEAL, lw=1.4, alpha=0.35, zorder=0)

    fig.text(0.5, 0.045,
              "MCP does not carry the water. It directs the request to the correct pipe.",
              fontsize=11, color=DEEP_NAVY, ha="center", va="center", fontweight="bold")

    fig.savefig("visuals/34_api_vs_mcp.png", dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


# ---------------------------------------------------------------------------
# 3. Builder-to-MCP progression (validation step emphasized)
# ---------------------------------------------------------------------------
def make_builder_to_mcp():
    fig, ax = plt.subplots(figsize=(13, 5.6), facecolor=WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_position([0, 0, 1, 1])

    add_header_bar(fig, "The Builder Creates the Road; MCP Adds the Signs",
                    "Conversational access depends on work someone did first", height=0.15)

    stages = [
        ("Accounting\nrequirement", OCEAN_TEAL, False),
        ("Builder creates\nworkflow", SEA_GREEN, False),
        ("Tested and\nvalidated", GOLDEN_YELLOW, True),
        ("Approved\nMCP tool", BRIGHT_TEAL, False),
        ("Used\nconversationally", SOFT_SAGE, False),
    ]

    n = len(stages)
    box_w = 0.15
    gap = (1 - n * box_w - 0.08) / (n - 1)
    x_start = 0.04
    y = 0.36
    box_h = 0.28

    xs = []
    for i, (title, color, emphasize) in enumerate(stages):
        x = x_start + i * (box_w + gap)
        xs.append(x)
        text_color = OCEAN_TEAL if color in (GOLDEN_YELLOW, WARM_GLOW, SOFT_SAGE) else WHITE
        if emphasize:
            rounded_box(ax, (x - 0.012, y - 0.045), box_w + 0.024, box_h + 0.09, color,
                        text_color=text_color, text=title, fontsize=13.5,
                        linespacing=1.4, edge=DEEP_NAVY, lw=2.4)
        else:
            rounded_box(ax, (x, y), box_w, box_h, color, text_color=text_color,
                        text=title, fontsize=12.5, linespacing=1.4)

    for i in range(n - 1):
        pad_a = 0.012 if stages[i][2] else 0
        pad_b = 0.012 if stages[i + 1][2] else 0
        arrow_h(ax, xs[i] + box_w + pad_a + 0.004, y + box_h / 2, xs[i + 1] - pad_b - 0.004)

    fig.text(0.5, 0.14,
              "The validation step is where a clever prototype becomes an accounting capability.",
              fontsize=11.5, color=DEEP_NAVY, ha="center", va="center", fontweight="bold")
    fig.text(0.5, 0.075,
              "Skip it and you have automated a guess.",
              fontsize=10.5, color=OCEAN_TEAL, ha="center", va="center", style="italic")

    fig.savefig("visuals/34_builder_to_mcp.png", dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


# ---------------------------------------------------------------------------
# 4. Future accounting technology stack, with governance running alongside
# ---------------------------------------------------------------------------
def make_tech_stack():
    fig, ax = plt.subplots(figsize=(12, 8.4), facecolor=WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_position([0, 0, 1, 1])

    add_header_bar(fig, "The Future Accounting Technology Stack",
                    "Governance runs the full height — not bolted on at the end", height=0.13)

    layers = [
        ("Accountant", "Defines the question, owns the conclusion", OCEAN_TEAL, WHITE),
        ("AI co-pilot or accounting agent", "Interprets intent, selects approved tools", SEA_GREEN, WHITE),
        ("Accounting instructions and approval rules", "Policies, mappings, materiality, escalation", BRIGHT_TEAL, WHITE),
        ("MCP tools", "Discoverable, permissioned capabilities", GOLDEN_YELLOW, OCEAN_TEAL),
        ("APIs | SQL | Reports | Python workflows", "Where the data moves and the math happens", MIDNIGHT_TEAL, WHITE),
        ("ERP | CRM | Payroll | Operational systems", "Systems of record", DEEP_NAVY, WHITE),
    ]

    stack_x, stack_w = 0.06, 0.62
    gov_x, gov_w = 0.72, 0.22
    box_h = 0.092
    gap = 0.034
    top = 0.80

    centers = []
    for i, (title, sub, color, text_color) in enumerate(layers):
        y = top - i * (box_h + gap) - box_h
        centers.append(y + box_h / 2)
        rounded_box(ax, (stack_x, y), stack_w, box_h, color, text_color=text_color,
                    text=title, fontsize=12.5, sub=sub, subsize=10.5, sub_color=text_color)

    for i in range(len(layers) - 1):
        arrow_v(ax, stack_x + stack_w / 2,
                centers[i] - box_h / 2 - 0.005,
                centers[i + 1] + box_h / 2 + 0.005)

    # Governance column spanning the full stack height
    gov_top = top
    gov_bottom = centers[-1] - box_h / 2
    gov_height = gov_top - gov_bottom
    box = FancyBboxPatch(
        (gov_x, gov_bottom), gov_w, gov_height,
        boxstyle="round,pad=0.012,rounding_size=0.02",
        facecolor="#F5F5F5", edgecolor=OCEAN_TEAL, linewidth=2.0, zorder=2,
    )
    ax.add_patch(box)
    ax.text(gov_x + gov_w / 2, gov_top - 0.045, "GOVERNANCE", fontsize=13,
             fontweight="bold", color=OCEAN_TEAL, ha="center", va="center", zorder=3)
    gov_items = ["Identity", "Permissions", "Validation", "Logging", "Approval", "Monitoring"]
    item_top = gov_top - 0.115
    item_step = (gov_height - 0.16) / (len(gov_items) - 1)
    for i, item in enumerate(gov_items):
        ax.text(gov_x + gov_w / 2, item_top - i * item_step, item, fontsize=11.5,
                 color=DEEP_NAVY, ha="center", va="center", zorder=3)

    fig.savefig("visuals/34_tech_stack.png", dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


# ---------------------------------------------------------------------------
# 5. Anatomy of an MCP accounting workflow (for builders)
# ---------------------------------------------------------------------------
def make_mcp_anatomy():
    fig, ax = plt.subplots(figsize=(12, 9.2), facecolor=WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_position([0, 0, 1, 1])

    add_header_bar(fig, "Anatomy of an MCP Accounting Workflow",
                    "What sits behind a one-sentence request", height=0.12)

    layers = [
        ("ACCOUNTANT", "Asks the business question in natural language", OCEAN_TEAL, WHITE),
        ("AI HOST", "The application in which the conversation occurs", SEA_GREEN, WHITE),
        ("MCP CLIENT", "Maintains the connection with the MCP server", BRIGHT_TEAL, WHITE),
        ("MCP SERVER", "Describes approved tools, resources, and prompts", GOLDEN_YELLOW, OCEAN_TEAL),
        ("TOOLS", "Invoke reports, SQL queries, APIs, or Python workflows", WARM_GLOW, OCEAN_TEAL),
        ("ACCOUNTING WORKFLOW", "Cleans, maps, calculates, reconciles, validates", MIDNIGHT_TEAL, WHITE),
        ("BUSINESS SYSTEMS", "ERP | CRM | Payroll | Project Mgmt | Warehouse", DEEP_NAVY, WHITE),
    ]

    x0, w = 0.05, 0.60
    box_h = 0.082
    gap = 0.030
    top = 0.83

    centers = []
    for i, (title, sub, color, text_color) in enumerate(layers):
        y = top - i * (box_h + gap) - box_h
        centers.append(y + box_h / 2)
        rounded_box(ax, (x0, y), w, box_h, color, text_color=text_color,
                    text=title, fontsize=12.5, sub=sub, subsize=10, sub_color=text_color)

    for i in range(len(layers) - 1):
        arrow_v(ax, x0 + w / 2,
                centers[i] - box_h / 2 - 0.004,
                centers[i + 1] + box_h / 2 + 0.004)

    # Governance sidebar
    gov_x, gov_w = 0.69, 0.26
    gov_top = top
    gov_bottom = centers[-1] - box_h / 2
    gov_height = gov_top - gov_bottom
    box = FancyBboxPatch(
        (gov_x, gov_bottom), gov_w, gov_height,
        boxstyle="round,pad=0.012,rounding_size=0.02",
        facecolor="#F5F5F5", edgecolor=OCEAN_TEAL, linewidth=2.0, zorder=2,
    )
    ax.add_patch(box)
    ax.text(gov_x + gov_w / 2, gov_top - 0.042, "GOVERNANCE", fontsize=12.5,
             fontweight="bold", color=OCEAN_TEAL, ha="center", va="center", zorder=3)
    ax.text(gov_x + gov_w / 2, gov_top - 0.075, "operates at every layer", fontsize=10,
             color=OCEAN_TEAL, ha="center", va="center", style="italic", zorder=3)
    gov_items = ["Identity", "Permissions", "Input validation", "Logging",
                 "Testing", "Approvals", "Source reconciliation", "Human review"]
    item_top = gov_top - 0.135
    item_step = (gov_height - 0.185) / (len(gov_items) - 1)
    for i, item in enumerate(gov_items):
        ax.text(gov_x + gov_w / 2, item_top - i * item_step, item, fontsize=11,
                 color=DEEP_NAVY, ha="center", va="center", zorder=3)

    fig.text(0.5, 0.032,
              "The server describes the capability. The workflow still does the accounting.",
              fontsize=11, color=DEEP_NAVY, ha="center", va="center", fontweight="bold")

    fig.savefig("visuals/34_mcp_anatomy.png", dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


# ---------------------------------------------------------------------------
# 6. Three complementary team roles
# ---------------------------------------------------------------------------
def make_team_roles():
    fig, ax = plt.subplots(figsize=(13, 6.0), facecolor=WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_position([0, 0, 1, 1])

    add_header_bar(fig, "Three Complementary Roles",
                    "One person may hold all three in a small team", height=0.15)

    roles = [
        ("WORKFLOW\nBUILDER", SEA_GREEN,
         "Converts requirements into\nscripts, tools, and\nautomated processes"),
        ("ACCOUNTING\nSUBJECT-MATTER EXPERT", GOLDEN_YELLOW,
         "Defines policies, mappings,\ncalculations, materiality,\nand controls"),
        ("CONVERSATIONAL USER\nAND REVIEWER", BRIGHT_TEAL,
         "Requests analysis, evaluates\nresults, applies\nprofessional judgment"),
    ]

    n = len(roles)
    box_w = 0.28
    gap = (1 - n * box_w - 0.08) / (n - 1)
    x_start = 0.04
    y = 0.22
    box_h = 0.46

    for i, (title, color, desc) in enumerate(roles):
        x = x_start + i * (box_w + gap)
        text_color = OCEAN_TEAL if color in (GOLDEN_YELLOW, WARM_GLOW) else WHITE
        rounded_box(ax, (x, y + box_h - 0.155), box_w, 0.155, color,
                    text_color=text_color, text=title, fontsize=12.5, linespacing=1.35)
        rounded_box(ax, (x, y), box_w, box_h - 0.168, "#F5F5F5",
                    text_color=DEEP_NAVY, text=desc, fontsize=11.5, bold=False,
                    linespacing=1.6)

    fig.text(0.5, 0.115,
              "The requirement is not that every accountant learns to code.",
              fontsize=11.5, color=OCEAN_TEAL, ha="center", va="center", style="italic")
    fig.text(0.5, 0.06,
              "It is that accounting knowledge becomes explicit enough to be built into a governed workflow.",
              fontsize=11.5, color=DEEP_NAVY, ha="center", va="center", fontweight="bold")

    fig.savefig("visuals/34_team_roles.png", dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


# ---------------------------------------------------------------------------
# 7. Maturity stages: Retrieve -> Execute  (retained from the first pass)
# ---------------------------------------------------------------------------
def make_maturity_stages():
    fig, ax = plt.subplots(figsize=(13, 4.6), facecolor=WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    add_header_bar(fig, "The Safest Progression",
                    "Resist the temptation to skip straight to “Execute”")

    stages = [
        ("Retrieve", SEA_GREEN),
        ("Analyze", BRIGHT_TEAL),
        ("Recommend", GOLDEN_YELLOW),
        ("Prepare", WARM_GLOW),
        ("Approve", ALERT_ORANGE),
        ("Execute", ALERT_RED),
    ]
    n = len(stages)
    box_w, box_h = 0.135, 0.30
    gap = (1 - n * box_w) / (n + 1)
    y = 0.33

    xs = []
    for i, (title, color) in enumerate(stages):
        x = gap + i * (box_w + gap)
        xs.append(x)
        text_color = OCEAN_TEAL if color in (GOLDEN_YELLOW, WARM_GLOW) else WHITE
        rounded_box(ax, (x, y), box_w, box_h, color, text_color=text_color, text=title, fontsize=13)

    for i in range(n - 1):
        arrow_h(ax, xs[i] + box_w + 0.004, y + box_h / 2, xs[i + 1] - 0.004)

    fig.text(0.5, 0.11,
              "Most accounting workflows should live comfortably in the first three stages for a long time.",
              fontsize=11, color=OCEAN_TEAL, ha="center", va="center", style="italic", alpha=1.0)

    fig.savefig("visuals/34_maturity_stages.png", dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


# ---------------------------------------------------------------------------
# 8. Social square: condensed three-eras graphic for LinkedIn / X
# ---------------------------------------------------------------------------
def make_social_square():
    fig, ax = plt.subplots(figsize=(8, 8), facecolor=WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_position([0, 0, 1, 1])

    header_h = 0.22
    add_header_bar(fig, "From Reports to Requests",
                    "One question, three accounting eras", height=header_h)

    fig.text(0.5, 0.705, '"Compare customer revenue and gross\nmargin across all systems."',
              fontsize=12.5, color=DEEP_NAVY, ha="center", va="center",
              style="italic", linespacing=1.5)

    eras = [
        ("TRADITIONAL ACCOUNTANT", "Reports → Exports → Lookups", "2–3 hours", OCEAN_TEAL),
        ("AI-ENABLED BUILDER", "Prompt → SQL / Python → Validate", "10–30 min", SEA_GREEN),
        ("CONVERSATIONAL MCP USER", "Ask → Approved workflow → Review", "5–15 min", GOLDEN_YELLOW),
    ]

    n = len(eras)
    box_h = 0.145
    region_top = 0.645
    region_bottom = 0.13
    gap = ((region_top - region_bottom) - n * box_h) / (n - 1)
    x0, w = 0.07, 0.86

    for i, (title, steps, timing, color) in enumerate(eras):
        y = region_top - i * (box_h + gap) - box_h
        text_color = OCEAN_TEAL if color in (GOLDEN_YELLOW, WARM_GLOW) else WHITE
        rounded_box(ax, (x0, y), w, box_h, color, text_color=text_color,
                    text=title, fontsize=13,
                    sub=f"{steps}\n{timing}", subsize=11, sub_color=text_color,
                    title_offset=0.26, sub_offset=0.18, linespacing=1.5)

    fig.text(0.5, 0.06, "PythonMuse LLC · pythonmuse.com", fontsize=10,
              color=OCEAN_TEAL, ha="center", va="center", alpha=0.85)

    fig.savefig("visuals/34_social_square.png", dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


if __name__ == "__main__":
    make_hero()
    make_api_vs_mcp()
    make_builder_to_mcp()
    make_tech_stack()
    make_mcp_anatomy()
    make_team_roles()
    make_maturity_stages()
    make_social_square()
    print("Generated 8 visuals for Article 34.")
