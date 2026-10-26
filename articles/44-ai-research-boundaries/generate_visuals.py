"""Generate branded visuals for Article 44 -- Let AI Do the Research. You Set
the Boundaries.

Run from anywhere:
    python generate_visuals.py

Article visuals (./visuals/) are built at true slide size (13.333 x 7.5 in)
with scripts/slide_kit.py, so the point size set here is the point size when
the image is dropped on a PowerPoint slide: 24pt body, 28pt+ headings, nothing
under 22pt. Each drawing function is written once and used twice: framed
(header bar + footer) for the article, and header-less (./visuals/slides/) as
an optional slide variant. Three square social cards are exported at exactly
1080 x 1080 px; they are a separate format and not size-checked.

Rules: .claude/skills/pythonmuse-slide-visuals/SKILL.md. save_slide() raises
if any text is under 22pt or runs off the edge. On top of that, every label
placed inside a box is registered with fit() and checked against that box
before saving, because save_slide() cannot see text spilling out of a card.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyBboxPatch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from slide_kit import (  # noqa: E402
    FRAME_CONTENT_BOTTOM, FRAME_CONTENT_TOP, SLIDE_H_IN, SLIDE_TARGET_PT,
    SLIDE_W_IN, blank_slide, framed_slide, save_slide)

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
TEAL_TINT = "#EDF5F5"

plt.rcParams["font.family"] = "sans-serif"

FOOTER = "PythonMuse LLC  |  www.pythonmuse.com"
OUT = Path(__file__).parent / "visuals"
SLIDES_OUT = OUT / "slides"

HEAD_PT = 30      # card headings and focal words
BODY_PT = SLIDE_TARGET_PT
BOX_PAD = 0.002

# Slide variants use (almost) the whole canvas.
SLIDE_TOP, SLIDE_BOTTOM = 0.94, 0.06


# ---------------------------------------------------------------------------
# Containment check: text registered with fit() must stay inside its box.
# ---------------------------------------------------------------------------
_FITS = []


def fit(t, x0, x1, y0, y1):
    """Register text object t as belonging inside the box (figure fractions)."""
    _FITS.append((t, x0, x1, y0, y1))
    return t


def check_fits(fig):
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    inv = fig.transFigure.inverted()
    problems = []
    for t, x0, x1, y0, y1 in _FITS:
        if t.figure is not fig:
            continue
        bb = inv.transform_bbox(t.get_window_extent(r))
        # Require a visible inside margin left and right, not just "inside".
        if (bb.x0 < x0 + 0.008 or bb.x1 > x1 - 0.008
                or bb.y0 < y0 + 0.004 or bb.y1 > y1 - 0.004):
            problems.append(f"spills out of its box: '{t.get_text()[:40]}'")
    _FITS.clear()
    if problems:
        plt.close(fig)
        raise ValueError("Layout check failed:\n  - " + "\n  - ".join(problems))


def save(fig, path):
    check_fits(fig)
    save_slide(fig, str(path))


# ---------------------------------------------------------------------------
# Shared drawing helpers (all coordinates are 0-1 figure fractions)
# ---------------------------------------------------------------------------
def box(ax, x, y, w, h, fill, zorder=2, rounding=0.02):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad={BOX_PAD},rounding_size={rounding}",
        facecolor=fill, edgecolor="none", zorder=zorder))


def arrow(ax, start, end, color=SEA_GREEN):
    ax.annotate("", xy=end, xytext=start,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=6,
                                mutation_scale=40, shrinkA=0, shrinkB=0),
                zorder=5)


def label(ax, x, y, s, bounds, size=BODY_PT, color=DEEP_NAVY, weight="normal",
          ha="center", va="center", **kw):
    t = ax.text(x, y, s, fontsize=size, color=color, fontweight=weight,
                ha=ha, va=va, zorder=4, **kw)
    return fit(t, *bounds)


def band(ax, text, y, h, fill=GOLDEN_YELLOW, color=DEEP_NAVY, size=HEAD_PT):
    box(ax, 0.03, y, 0.94, h, fill)
    label(ax, 0.5, y + h / 2, text, (0.03, 0.97, y, y + h), size=size,
          color=color, weight="bold")


def split_area(top, bottom, band_frac=0.17, gap=0.03):
    """(band_y, band_h, content_y, content_h) with a takeaway band at the
    bottom of the content area."""
    band_h = (top - bottom) * band_frac
    cy = bottom + band_h + gap
    return bottom, band_h, cy, top - cy


def make_pair(draw, name, title, subtitle):
    """Article version (framed) and slide version (header-less)."""
    fig, ax = framed_slide(title, subtitle, FOOTER)
    draw(ax, FRAME_CONTENT_TOP, FRAME_CONTENT_BOTTOM)
    save(fig, OUT / f"44_{name}.png")
    fig, ax = blank_slide()
    draw(ax, SLIDE_TOP, SLIDE_BOTTOM)
    save(fig, SLIDES_OUT / f"44_{name}_slide.png")


# ---------------------------------------------------------------------------
# 1. Hero: the library and its four shelves
# ---------------------------------------------------------------------------
SHELVES = [
    ("Authoritative", "May support the conclusion", DEEP_NAVY, WARM_GLOW, WHITE),
    ("Interpretation", "May explain, never alone", OCEAN_TEAL, WARM_GLOW, WHITE),
    ("Discovery", "May point to the issue", BRIGHT_TEAL, DEEP_NAVY, DEEP_NAVY),
    ("Off-limits", "Do not access", LIGHT_GRAY, OCEAN_TEAL, DEEP_NAVY),
]
BOOK_COLORS = {DEEP_NAVY: [OCEAN_TEAL, SEA_GREEN, BRIGHT_TEAL, SOFT_SAGE],
               OCEAN_TEAL: [SEA_GREEN, BRIGHT_TEAL, SOFT_SAGE, TEAL_TINT],
               BRIGHT_TEAL: [SEA_GREEN, TEAL_TINT, OCEAN_TEAL, SOFT_SAGE],
               LIGHT_GRAY: ["#D9D9D9", "#C8C8C8", "#E3E3E3", "#BDBDBD"]}


def draw_hero(ax, top, bottom):
    by, bh, cy, ch = split_area(top, bottom, band_frac=0.16)
    gap = 0.018
    h = (ch - 3 * gap) / 4
    for i, (name, rule, fill, name_col, rule_col) in enumerate(SHELVES):
        y = cy + ch - (i + 1) * h - i * gap
        box(ax, 0.03, y, 0.94, h, fill)
        label(ax, 0.055, y + h / 2, name, (0.03, 0.33, y, y + h), size=28,
              color=name_col, weight="bold", ha="left")
        # A row of books (decoration only, no text).
        heights = [0.78, 0.62, 0.86, 0.70, 0.80, 0.58, 0.74]
        bx = 0.345
        for j, bh_frac in enumerate(heights):
            bw = 0.022 if j % 3 else 0.030
            ax.add_patch(FancyBboxPatch(
                (bx, y + h * 0.10), bw, h * bh_frac * 0.85,
                boxstyle="round,pad=0,rounding_size=0.004",
                facecolor=BOOK_COLORS[fill][j % 4], edgecolor="none",
                zorder=3))
            bx += bw + 0.006
        label(ax, 0.59, y + h / 2, rule, (0.575, 0.97, y, y + h),
              color=rule_col, ha="left")
    band(ax, "Tell it which shelves we trust.", by, bh)


# ---------------------------------------------------------------------------
# 2. Does the workflow need the internet?
# ---------------------------------------------------------------------------
def draw_does_it_need_web(ax, top, bottom):
    by, bh, cy, ch = split_area(top, bottom, band_frac=0.16)
    cols = [
        (0.03, 0.42, DEEP_NAVY, WARM_GLOW, WHITE, "No internet needed",
         ["Bank reconciliation", "Payroll reconciliation",
          "Fixed asset rollforward", "Journal entry review"]),
        (0.48, 0.49, TEAL_TINT, OCEAN_TEAL, DEEP_NAVY, "Research with a boundary",
         ["New guidance", "Disclosure comparison", "Tax updates"]),
    ]
    for x, w, fill, head_col, body_col, head, items in cols:
        box(ax, x, cy, w, ch, fill)
        bounds = (x, x + w, cy, cy + ch)
        label(ax, x + 0.025, cy + ch - 0.075, head, bounds, size=28,
              color=head_col, weight="bold", ha="left")
        step = (ch - 0.17) / 4
        for k, item in enumerate(items):
            label(ax, x + 0.035, cy + ch - 0.17 - k * step, "•  " + item,
                  bounds, color=body_col, ha="left")
    band(ax, "Access follows the purpose, not the tool.", by, bh)


# ---------------------------------------------------------------------------
# 3. Finding vs. relying: discovery lane and evidence lane
# ---------------------------------------------------------------------------
def draw_discovery_vs_reliance(ax, top, bottom):
    gap = 0.05
    lane_h = (top - bottom - gap) / 2
    lanes = [
        (bottom + lane_h + gap, "DISCOVERY: may point to the issue",
         ["LinkedIn", "Forums", "News", "Blogs"], LIGHT_GRAY, DEEP_NAVY,
         "Finds the\nissue", BRIGHT_TEAL, DEEP_NAVY),
        (bottom, "EVIDENCE: may support the conclusion",
         ["SEC", "IRS", "FASB", "IFRS", "Contract"], DEEP_NAVY, WHITE,
         "Supports the\nconclusion", GOLDEN_YELLOW, DEEP_NAVY),
    ]
    chip_x0, chip_x1 = 0.03, 0.665
    for y, title, chips, chip_fill, chip_col, dest, dest_fill, dest_col in lanes:
        n = len(chips)
        cgap = 0.012
        weights = [1.6 if len(c) > 6 else 1.0 for c in chips]
        unit = (chip_x1 - chip_x0 - (n - 1) * cgap) / sum(weights)
        chip_h = lane_h * 0.60
        cy = y + 0.01
        label(ax, chip_x0, cy + chip_h + 0.045, title,
              (0.0, chip_x1 + 0.08, y, y + lane_h), size=26,
              color=OCEAN_TEAL, weight="bold", ha="left")
        cx = chip_x0
        for k, c in enumerate(chips):
            cw = unit * weights[k]
            box(ax, cx, cy, cw, chip_h, chip_fill)
            label(ax, cx + cw / 2, cy + chip_h / 2, c, (cx, cx + cw, cy, cy + chip_h),
                  color=chip_col, weight="bold")
            cx += cw + cgap
        dx, dw = 0.745, 0.225
        box(ax, dx, cy, dw, chip_h, dest_fill)
        label(ax, dx + dw / 2, cy + chip_h / 2, dest, (dx, dx + dw, cy, cy + chip_h),
              size=26, color=dest_col, weight="bold", linespacing=1.15)
        arrow(ax, (chip_x1 + 0.012, cy + chip_h / 2), (dx - 0.012, cy + chip_h / 2))


# ---------------------------------------------------------------------------
# 4. The boundary should match the purpose and risk of the task
# ---------------------------------------------------------------------------
RINGS = [
    ("Explore", "Broad web is fine", BRIGHT_TEAL, DEEP_NAVY),
    ("Support a conclusion", "Authoritative and approved", OCEAN_TEAL, WHITE),
    ("Evaluate against policy", "Provided documents only, no web", DEEP_NAVY, WHITE),
]


def draw_boundary_matches_risk(ax, top, bottom):
    span_in = (top - bottom) * SLIDE_H_IN          # usable height, inches
    cx, cyy = 0.235, (top + bottom) / 2
    r0 = min(span_in / 2, (cx - 0.03) * SLIDE_W_IN)   # keep a side margin
    radii = [r0, r0 * 0.70, r0 * 0.40]
    for (name, _, fill, _), r in zip(RINGS, radii):
        ax.add_patch(Ellipse((cx, cyy), 2 * r / SLIDE_W_IN, 2 * r / SLIDE_H_IN,
                             facecolor=fill, edgecolor="none", zorder=2))
    # Ring numbers sit inside each ring, directly labeling it.
    num_y = [cyy + (radii[0] + radii[1]) / 2 / SLIDE_H_IN,
             cyy + (radii[1] + radii[2]) / 2 / SLIDE_H_IN, cyy]
    num_col = [DEEP_NAVY, WHITE, GOLDEN_YELLOW]
    for k in range(3):
        t = ax.text(cx, num_y[k], str(k + 1), fontsize=30, fontweight="bold",
                    color=num_col[k], ha="center", va="center", zorder=4)
        fit(t, 0.0, 0.5, bottom, top)
    # Right: one row per ring, same color, same number.
    rx, rw = 0.50, 0.47
    gap = 0.025
    h = (top - bottom - 2 * gap) / 3
    for k, (name, rule, fill, col) in enumerate(RINGS):
        y = top - (k + 1) * h - k * gap
        box(ax, rx, y, rw, h, fill)
        bounds = (rx, rx + rw, y, y + h)
        head_col = DEEP_NAVY if fill == BRIGHT_TEAL else WARM_GLOW
        label(ax, rx + 0.022, y + h * 0.67, f"{k + 1}. {name}", bounds,
              size=28, color=head_col, weight="bold", ha="left")
        label(ax, rx + 0.022, y + h * 0.30, rule, bounds, color=col, ha="left")


# ---------------------------------------------------------------------------
# 5. Trusted does not always mean permitted
# ---------------------------------------------------------------------------
def draw_trusted_vs_permitted(ax, top, bottom):
    gx0, gap = 0.12, 0.02
    head_h = 0.085
    cw = (0.97 - gx0 - gap) / 2
    ch = (top - bottom - head_h - 2 * gap) / 2
    cols = ["Permitted", "Not permitted"]
    rows = ["Trusted", "Untrusted"]
    cells = {
        (0, 0): ("SEC guidance,\nread and cited", SOFT_SAGE, DEEP_NAVY),
        (0, 1): ("A paid database\ncopied wholesale\nby an AI agent", GOLDEN_YELLOW, DEEP_NAVY),
        (1, 0): ("A public forum:\nfine to read,\nnot to rely on", LIGHT_GRAY, DEEP_NAVY),
        (1, 1): ("Scraping a site\nwhose terms\nforbid it", OCEAN_TEAL, WHITE),
    }
    for c, name in enumerate(cols):
        x = gx0 + c * (cw + gap)
        y = top - head_h
        box(ax, x, y, cw, head_h, DEEP_NAVY)
        label(ax, x + cw / 2, y + head_h / 2, name, (x, x + cw, y, top),
              size=28, color=WHITE, weight="bold")
    for r, name in enumerate(rows):
        y = top - head_h - gap - (r + 1) * ch - r * gap
        box(ax, 0.03, y, gx0 - 0.03 - gap / 2, ch, DEEP_NAVY)
        t = ax.text(0.03 + (gx0 - 0.03 - gap / 2) / 2, y + ch / 2, name,
                    fontsize=BODY_PT, fontweight="bold", color=WHITE, rotation=90,
                    ha="center", va="center", zorder=4)
        fit(t, 0.03, gx0, y, y + ch)
        for c in range(2):
            x = gx0 + c * (cw + gap)
            text, fill, col = cells[(r, c)]
            box(ax, x, y, cw, ch, fill)
            label(ax, x + cw / 2, y + ch / 2, text, (x, x + cw, y, y + ch),
                  size=26, color=col, weight="bold" if fill == GOLDEN_YELLOW
                  else "normal", linespacing=1.25)


# ---------------------------------------------------------------------------
# 6. "Research this." vs. a research boundary
# ---------------------------------------------------------------------------
BOUNDARY_LINES = [
    ("Rely on:", "SEC, IRS, FASB, IFRS"),
    ("Explain with:", "approved publications"),
    ("Never support:", "social media, forums"),
    ("Bring back:", "source, dates, link"),
]


def draw_research_this_vs_boundary(ax, top, bottom):
    by, bh, cy, ch = split_area(top, bottom, band_frac=0.16)
    lw = 0.31
    box(ax, 0.03, cy, lw, ch, LIGHT_GRAY)
    lb = (0.03, 0.03 + lw, cy, cy + ch)
    label(ax, 0.055, cy + ch - 0.07, "THE PROMPT", lb, size=26,
          color=OCEAN_TEAL, weight="bold", ha="left")
    label(ax, 0.03 + lw / 2, cy + ch * 0.42, "“Research\nthis.”", lb,
          size=44, color=DEEP_NAVY, weight="bold", linespacing=1.1)
    rx = 0.03 + lw + 0.03
    rw = 0.97 - rx
    box(ax, rx, cy, rw, ch, DEEP_NAVY)
    rb = (rx, rx + rw, cy, cy + ch)
    label(ax, rx + 0.025, cy + ch - 0.07, "THE BOUNDARY", rb, size=26,
          color=WARM_GLOW, weight="bold", ha="left")
    step = (ch - 0.16) / 4
    for k, (lead, rest) in enumerate(BOUNDARY_LINES):
        y = cy + ch - 0.165 - k * step
        t = ax.text(rx + 0.025, y, lead, fontsize=BODY_PT, fontweight="bold",
                    color=BRIGHT_TEAL, ha="left", va="center", zorder=4)
        fit(t, *rb)
        label(ax, rx + 0.27, y, rest, rb, color=WHITE, ha="left")
    band(ax, "Same AI. Same question. Very different research.", by, bh, size=28)


# ---------------------------------------------------------------------------
# 7. The evidence package (mock evidence log)
# ---------------------------------------------------------------------------
# Column widths in inches (they must add up to 0.94 of 13.333 in = 12.53 in).
# Measured at 24pt: "SAB 121 rescinded" 3.15 in, "Authoritative" 2.17 in.
LOG_COLS = [("Conclusion", 3.45), ("Source", 1.95), ("Published", 2.30),
            ("Retrieved", 2.30), ("Tier", 2.53)]
LOG_ROWS = [
    ("SAB 121 rescinded", "sec.gov", "2025-01-23", "2026-10-14", "Authoritative"),
    ("Loss contingency", "FASB ASC", "Current", "2026-10-14", "Authoritative"),
    ("How we found it", "LinkedIn", "2025-01-24", "2026-10-14", "Discovery"),
]


def draw_evidence_package(ax, top, bottom):
    by, bh, cy, ch = split_area(top, bottom, band_frac=0.16)
    gap = 0.012
    row_h = (ch - 3 * gap) / 4
    x0 = 0.03
    for r in range(4):
        y = cy + ch - (r + 1) * row_h - r * gap
        fill = DEEP_NAVY if r == 0 else (LIGHT_GRAY if r % 2 else TEAL_TINT)
        box(ax, x0, y, 0.94, row_h, fill, rounding=0.012)
        x = x0
        for c, (head, w) in enumerate(LOG_COLS):
            w = w / SLIDE_W_IN
            if r == 0:
                s, col, weight = head, WHITE, "bold"
            else:
                s = LOG_ROWS[r - 1][c]
                col = DEEP_NAVY
                weight = "normal"
                if c in (1, 3):
                    col = OCEAN_TEAL
                if c == 4 and s == "Discovery":
                    col = OCEAN_TEAL
            label(ax, x + 0.012, y + row_h / 2, s, (x, x + w, y, y + row_h),
                  color=col, weight=weight, ha="left")
            x += w
    band(ax, "Don't make the reviewer play detective.", by, bh)


# ---------------------------------------------------------------------------
# Social cards (1080 x 1080): a separate format, not size-checked
# ---------------------------------------------------------------------------
NL = "\n"


def social_footer(fig, y, size=20):
    fig.text(0.5, y, FOOTER, fontsize=size, color=OCEAN_TEAL, ha="center",
             va="center", alpha=0.80)


def blank_axes(figsize):
    fig, ax = plt.subplots(figsize=figsize, facecolor=WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_position([0, 0, 1, 1])
    return fig, ax


def save_square(fig, name, inches=13):
    """Exact 1080 x 1080 px, so no tight bbox (it would trim)."""
    check_fits(fig)
    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / name, dpi=1080 / inches, facecolor=fig.get_facecolor())
    plt.close(fig)


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


FIVE_QUESTIONS = [
    "Does it need external access at all?",
    "Where may it look?",
    "What may it rely on?",
    "Are we allowed to use it this way?",
    "What evidence must it bring back?",
]


def make_social_square():
    fig, ax = blank_axes((13, 13))
    social_header(fig, "Before AI starts" + NL + "researching",
                  "Five questions. Then let it search.")
    top, h, gap = 0.680, 0.085, 0.015
    for k, q in enumerate(FIVE_QUESTIONS):
        y = top - (k + 1) * h - k * gap
        box(ax, 0.06, y, 0.88, h, LIGHT_GRAY if k % 2 else TEAL_TINT)
        # Check box
        ax.add_patch(FancyBboxPatch((0.09, y + h * 0.22), 0.050, h * 0.56,
                                    boxstyle="round,pad=0,rounding_size=0.008",
                                    facecolor=DEEP_NAVY, edgecolor="none",
                                    zorder=3))
        ax.text(0.115, y + h / 2, "✓", fontsize=34, fontweight="bold",
                color=GOLDEN_YELLOW, ha="center", va="center", zorder=4)
        label(ax, 0.17, y + h / 2, q, (0.06, 0.94, y, y + h), size=31,
              color=DEEP_NAVY, weight="bold", ha="left")
    ax.text(0.5, 0.122, "Internet access should follow the purpose of the"
            + NL + "workflow, not the capability of the tool.", fontsize=25,
            style="italic", color=OCEAN_TEAL, ha="center", va="center",
            linespacing=1.3)
    social_footer(fig, y=0.030)
    save_square(fig, "44_social_square.png")


def quote_card(name, lines, sub, quote_pt=60):
    fig, ax = blank_axes((13, 13))
    box(ax, 0.05, 0.110, 0.90, 0.840, DEEP_NAVY, rounding=0.03)
    ax.text(0.130, 0.835, "“", fontsize=170, color=GOLDEN_YELLOW,
            ha="center", va="center", fontweight="bold", zorder=4)
    label(ax, 0.5, 0.560, lines, (0.05, 0.95, 0.30, 0.80), size=quote_pt,
          color=WHITE, weight="bold", linespacing=1.2)
    label(ax, 0.5, 0.215, sub, (0.05, 0.95, 0.12, 0.31), size=30,
          color=WARM_GLOW, style="italic", linespacing=1.3)
    social_footer(fig, y=0.060)
    save_square(fig, name)


def make_social_quote_purpose():
    quote_card("44_social_quote_purpose.png",
               "Internet access\nshould follow the\npurpose of the\nworkflow, not the\n"
               "capability of\nthe tool.",
               "Some workflows need no web at all.", quote_pt=54)


def make_social_bold_headings():
    quote_card("44_social_bold_headings.png",
               "Bold headings\nare not evidence.\n\nNeither is a\nconfident tone.",
               "Click the source. Read it. Then decide.", quote_pt=58)


if __name__ == "__main__":
    make_pair(draw_hero, "hero", "Let AI Do the Research",
              "You decide which shelves it may use.")
    make_pair(draw_does_it_need_web, "does_it_need_web",
              "Does the Workflow Need the Internet?",
              "Some steps never need to leave the building.")
    make_pair(draw_discovery_vs_reliance, "discovery_vs_reliance",
              "Finding Is Not Relying",
              "Where may AI look? What may AI rely on?")
    make_pair(draw_boundary_matches_risk, "boundary_matches_risk",
              "The Boundary Matches the Task",
              "Higher stakes, smaller research boundary.")
    make_pair(draw_trusted_vs_permitted, "trusted_vs_permitted",
              "Trusted Is Not the Same as Permitted",
              "Good content can still be off-limits.")
    make_pair(draw_research_this_vs_boundary, "research_this_vs_boundary",
              "Two Prompts, Two Research Processes",
              "Decide the boundary before it starts.")
    make_pair(draw_evidence_package, "evidence_package",
              "The Evidence Comes Back With the Answer",
              "Published date and retrieved date, side by side.")
    make_social_square()
    make_social_quote_purpose()
    make_social_bold_headings()
    print("Generated 7 article visuals, 7 slide variants, and 3 social cards "
          "for Article 44.")
