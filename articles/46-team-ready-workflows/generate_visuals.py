"""Generate branded visuals for Article 46 -- I Built the Workflow. Now How
Does My Team Use It? (the first PythonMuse Lab).

Run from anywhere:
    python generate_visuals.py

Article visuals (./visuals/) are built at true slide size (13.333 x 7.5 in)
with scripts/slide_kit.py, so the point size set here is the point size when
the image is dropped on a PowerPoint slide: 24pt body, 26pt+ headings, nothing
under 22pt. Each drawing function is written once and used twice: framed
(header bar + footer) for the article, and header-less (./visuals/slides/) as
an optional slide variant. Two square social cards are exported at exactly
1080 x 1080 px; they are a separate format and not size-checked.

The two screenshots in ./visuals/ (46_demo_desktop_check.png and
46_demo_desktop_stop.png) are NOT generated here: they are real captures of
the companion demo's desktop window running on its synthetic sample files.

Rules: .claude/skills/pythonmuse-slide-visuals/SKILL.md. save_slide() raises
if any text is under 22pt or runs off the edge. On top of that, every label
placed inside a box is registered with fit() and checked against that box
before saving, because save_slide() cannot see text spilling out of a card.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from slide_kit import (  # noqa: E402
    FRAME_CONTENT_BOTTOM, FRAME_CONTENT_TOP, SLIDE_TARGET_PT, blank_slide,
    framed_slide, save_slide)

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

HEAD_PT = 28      # card headings and focal words
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


def arrow(ax, start, end, color=SEA_GREEN, lw=6):
    ax.annotate("", xy=end, xytext=start,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                mutation_scale=40, shrinkA=0, shrinkB=0),
                zorder=5)


def label(ax, x, y, s, bounds, size=BODY_PT, color=DEEP_NAVY, weight="normal",
          ha="center", va="center", **kw):
    t = ax.text(x, y, s, fontsize=size, color=color, fontweight=weight,
                ha=ha, va=va, zorder=6, **kw)
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
    save(fig, OUT / f"46_{name}.png")
    fig, ax = blank_slide()
    draw(ax, SLIDE_TOP, SLIDE_BOTTOM)
    save(fig, SLIDES_OUT / f"46_{name}_slide.png")


def card_list(ax, x, y, w, h, fill, head, head_col, items, body_col,
              head_size=HEAD_PT):
    """A card with a heading and a short list, evenly spaced."""
    box(ax, x, y, w, h, fill)
    bounds = (x, x + w, y, y + h)
    label(ax, x + 0.025, y + h - 0.075, head, bounds, size=head_size,
          color=head_col, weight="bold", ha="left")
    # Spread the list under the heading, but never more than 0.12 apart,
    # and centre the block in the space left below the heading.
    area_top, area_bottom = y + h - 0.15, y + 0.03
    n = len(items)
    step = min((area_top - area_bottom - 0.06) / max(n - 1, 1), 0.12)
    mid = (area_top + area_bottom) / 2
    first = mid + step * (n - 1) / 2
    for k, item in enumerate(items):
        label(ax, x + 0.03, first - k * step, "•  " + item, bounds,
              color=body_col, ha="left")


# ---------------------------------------------------------------------------
# 1. Hero: "I built it" -> "My team can use it"
# ---------------------------------------------------------------------------
def draw_hero(ax, top, bottom):
    by, bh, cy, ch = split_area(top, bottom, band_frac=0.17)
    w = 0.40
    left_x, right_x = 0.03, 0.97 - w
    card_list(ax, left_x, cy, w, ch, LIGHT_GRAY, "I built it", OCEAN_TEAL,
              ["Code editor open", "Scripts and folders", "I know its quirks"],
              DEEP_NAVY, head_size=30)
    card_list(ax, right_x, cy, w, ch, DEEP_NAVY, "My team can use it",
              WARM_GLOW, ["Pick date and file", "Read the checks",
                          "Run, then review"], WHITE, head_size=30)
    mid = cy + ch / 2
    arrow(ax, (left_x + w + 0.03, mid), (right_x - 0.03, mid), lw=8)
    band(ax, "Same tested scripts. A better front door.", by, bh)


# ---------------------------------------------------------------------------
# 2. Five roles, shared accountability
# ---------------------------------------------------------------------------
ROLES = [
    ("Designer", "Logic and\ncontrols", TEAL_TINT, OCEAN_TEAL, DEEP_NAVY),
    ("Builder", "Code and\ntests", TEAL_TINT, OCEAN_TEAL, DEEP_NAVY),
    ("Operator", "Runs it,\nchecks it", DEEP_NAVY, WARM_GLOW, WHITE),
    ("Reviewer", "Judges,\nsigns off", GOLDEN_YELLOW, DEEP_NAVY, DEEP_NAVY),
    ("Maintainer", "Changes,\nrollback", TEAL_TINT, OCEAN_TEAL, DEEP_NAVY),
]


def draw_five_roles(ax, top, bottom):
    by, bh, cy, ch = split_area(top, bottom, band_frac=0.17)
    gap = 0.012
    w = (0.94 - 4 * gap) / 5
    for k, (name, what, fill, head_col, body_col) in enumerate(ROLES):
        x = 0.03 + k * (w + gap)
        box(ax, x, cy, w, ch, fill)
        bounds = (x, x + w, cy, cy + ch)
        label(ax, x + w / 2, cy + ch * 0.72, name, bounds, size=25,
              color=head_col, weight="bold")
        label(ax, x + w / 2, cy + ch * 0.36, what, bounds, color=body_col,
              linespacing=1.3)
    band(ax, "Wear several hats. Don't review your own run.", by, bh,
         fill=DEEP_NAVY, color=WARM_GLOW)


# ---------------------------------------------------------------------------
# 3. The operator journey, with the two places a person must stop
# ---------------------------------------------------------------------------
STEPS = [
    ("Pick file\nand date", TEAL_TINT, DEEP_NAVY, None),
    ("Read the\nchecks", TEAL_TINT, DEEP_NAVY, "Red?\nStop."),
    ("Confirm\nand run", TEAL_TINT, DEEP_NAVY, None),
    ("Check the\noutput", TEAL_TINT, DEEP_NAVY, "Doesn't tie?\nStop."),
    ("Reviewer\nsigns off", GOLDEN_YELLOW, DEEP_NAVY, None),
]


def draw_operator_journey(ax, top, bottom):
    span = top - bottom
    gap = 0.03
    w = (0.94 - 4 * gap) / 5
    card_h = span * 0.44
    card_y = top - card_h - span * 0.04
    chip_h = span * 0.32
    chip_y = bottom + span * 0.02
    for k, (text, fill, col, stop) in enumerate(STEPS):
        x = 0.03 + k * (w + gap)
        box(ax, x, card_y, w, card_h, fill)
        label(ax, x + w / 2, card_y + card_h / 2, text,
              (x, x + w, card_y, card_y + card_h), size=25, color=col,
              weight="bold", linespacing=1.25)
        if k < 4:
            arrow(ax, (x + w + 0.006, card_y + card_h / 2),
                  (x + w + gap - 0.006, card_y + card_h / 2), lw=5)
        if stop:
            arrow(ax, (x + w / 2, card_y - 0.008), (x + w / 2, chip_y + chip_h + 0.012),
                  color=ALERT_RED, lw=5)
            box(ax, x - 0.012, chip_y, w + 0.024, chip_h, ALERT_RED)
            label(ax, x + w / 2, chip_y + chip_h / 2, stop,
                  (x - 0.012, x + w + 0.012, chip_y, chip_y + chip_h),
                  color=WHITE, weight="bold", linespacing=1.25)


# ---------------------------------------------------------------------------
# 4. Architecture: the rules live outside the front door (appendix)
# ---------------------------------------------------------------------------
LAYERS = [
    ("Front door", "collects inputs", LIGHT_GRAY, DEEP_NAVY, OCEAN_TEAL),
    ("Checks", "stop or warn", TEAL_TINT, DEEP_NAVY, OCEAN_TEAL),
    ("Calculation", "tested script", DEEP_NAVY, WHITE, WARM_GLOW),
    ("Workpaper", "with run info", TEAL_TINT, DEEP_NAVY, OCEAN_TEAL),
]


def draw_architecture(ax, top, bottom):
    span = top - bottom
    gap = 0.04
    w = (0.94 - 3 * gap) / 4
    h = span * 0.40
    y = top - h - span * 0.02
    xs = [0.03 + k * (w + gap) for k in range(4)]
    for k, (name, sub, fill, head_col, sub_col) in enumerate(LAYERS):
        x = xs[k]
        box(ax, x, y, w, h, fill)
        b = (x, x + w, y, y + h)
        label(ax, x + w / 2, y + h * 0.63, name, b, size=26, color=head_col,
              weight="bold")
        label(ax, x + w / 2, y + h * 0.30, sub, b, color=sub_col)
        if k < 3:
            arrow(ax, (x + w + 0.006, y + h / 2), (x + w + gap - 0.006, y + h / 2),
                  lw=5)
    # Second row: who uses the door, where the rules live, who reviews.
    rh = span * 0.34
    ry = bottom + span * 0.02
    gap_v = (0.008, 0.012)

    def lower(x0, x1, text, fill, col, up=True, centers=None):
        box(ax, x0, ry, x1 - x0, rh, fill)
        label(ax, (x0 + x1) / 2, ry + rh / 2, text, (x0, x1, ry, ry + rh),
              color=col, weight="bold", linespacing=1.25)
        for cx in centers or [(x0 + x1) / 2]:
            if up:
                arrow(ax, (cx, ry + rh + gap_v[0]), (cx, y - gap_v[1]),
                      color=OCEAN_TEAL, lw=5)
            else:
                arrow(ax, (cx, y - gap_v[0]), (cx, ry + rh + gap_v[1]),
                      color=OCEAN_TEAL, lw=5)

    lower(xs[0], xs[0] + w, "Operator", TEAL_TINT, DEEP_NAVY)
    lower(xs[1], xs[2] + w, "Rules file: buckets,\nthresholds, tolerance",
          OCEAN_TEAL, WHITE, centers=[xs[1] + w / 2, xs[2] + w / 2])
    lower(xs[3], xs[3] + w, "Reviewer\nsigns off", GOLDEN_YELLOW, DEEP_NAVY,
          up=False)


# ---------------------------------------------------------------------------
# 5. Three front doors
# ---------------------------------------------------------------------------
DOORS = [
    ("Guided terminal", "A few users,\nfine with text", "Python, or a\npackaged app",
     TEAL_TINT, OCEAN_TEAL, DEEP_NAVY),
    ("Desktop window", "Point-and-click\noperators", "Install on each\nmachine",
     DEEP_NAVY, WARM_GLOW, WHITE),
    ("Internal web page", "Many users,\none shared copy", "Hosting, login,\nIT approval",
     TEAL_TINT, OCEAN_TEAL, DEEP_NAVY),
]


def draw_three_front_doors(ax, top, bottom):
    by, bh, cy, ch = split_area(top, bottom, band_frac=0.17)
    gap = 0.02
    w = (0.94 - 2 * gap) / 3
    for k, (name, good, needs, fill, head_col, body_col) in enumerate(DOORS):
        x = 0.03 + k * (w + gap)
        box(ax, x, cy, w, ch, fill)
        b = (x, x + w, cy, cy + ch)
        label(ax, x + w / 2, cy + ch * 0.87, name, b, size=25, color=head_col,
              weight="bold")
        label(ax, x + 0.025, cy + ch * 0.70, "Good for:", b, color=head_col,
              weight="bold", ha="left")
        label(ax, x + 0.025, cy + ch * 0.63, good, b, color=body_col, ha="left",
              linespacing=1.2, va="top")
        label(ax, x + 0.025, cy + ch * 0.35, "Needs:", b, color=head_col,
              weight="bold", ha="left")
        label(ax, x + 0.025, cy + ch * 0.28, needs, b, color=body_col, ha="left",
              linespacing=1.2, va="top")
    band(ax, "Choose for the operator, not the builder.", by, bh)


# ---------------------------------------------------------------------------
# 6. What a green check means (and doesn't)
# ---------------------------------------------------------------------------
def draw_green_check(ax, top, bottom):
    by, bh, cy, ch = split_area(top, bottom, band_frac=0.17)
    w = 0.43
    card_list(ax, 0.03, cy, w, ch, TEAL_TINT, "The checks confirm",
              OCEAN_TEAL, ["Every column is there", "Each invoice once",
                           "The total ties"], DEEP_NAVY)
    rx = 0.97 - w
    card_list(ax, rx, cy, w, ch, DEEP_NAVY, "A person still judges",
              WARM_GLOW, ["Was the export complete?", "Is the credit real?",
                          "Will they pay?"], WHITE)
    label(ax, 0.5, cy + ch / 2, "≠", (0.03 + w, rx, cy, cy + ch), size=54,
          color=OCEAN_TEAL, weight="bold")
    band(ax, "A green check is not a sign-off.", by, bh)


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


AFTER_THE_RUN = [
    "Tie the total to the GL",
    "Check the customer count",
    "Read every exception",
    "Spot-check unflagged items",
]


def make_social_square():
    fig, ax = blank_axes((13, 13))
    social_header(fig, "I built it." + NL + "Can my team run it?",
                  "What the operator checks after the run")
    top, h, gap = 0.660, 0.095, 0.018
    for k, q in enumerate(AFTER_THE_RUN):
        y = top - (k + 1) * h - k * gap
        box(ax, 0.06, y, 0.88, h, LIGHT_GRAY if k % 2 else TEAL_TINT)
        ax.add_patch(FancyBboxPatch((0.09, y + h * 0.22), 0.050, h * 0.56,
                                    boxstyle="round,pad=0,rounding_size=0.008",
                                    facecolor=DEEP_NAVY, edgecolor="none",
                                    zorder=3))
        ax.text(0.115, y + h / 2, "✓", fontsize=34, fontweight="bold",
                color=GOLDEN_YELLOW, ha="center", va="center", zorder=4)
        label(ax, 0.17, y + h / 2, q, (0.06, 0.94, y, y + h), size=34,
              color=DEEP_NAVY, weight="bold", ha="left")
    ax.text(0.5, 0.135, "A green check means the checks passed," + NL
            + "not that the accounting is right.", fontsize=28,
            style="italic", color=OCEAN_TEAL, ha="center", va="center",
            linespacing=1.3)
    social_footer(fig, y=0.030)
    save_square(fig, "46_social_square.png")


def make_social_quote():
    fig, ax = blank_axes((13, 13))
    box(ax, 0.05, 0.110, 0.90, 0.840, DEEP_NAVY, rounding=0.03)
    ax.text(0.130, 0.835, "“", fontsize=170, color=GOLDEN_YELLOW,
            ha="center", va="center", fontweight="bold", zorder=4)
    label(ax, 0.5, 0.555, "Your team doesn't\nneed to become\nprogrammers.\n"
          "Your workflow\nneeds a better\nfront door.",
          (0.05, 0.95, 0.30, 0.80), size=54, color=WHITE, weight="bold",
          linespacing=1.2)
    label(ax, 0.5, 0.205, "Build it once. Hand it over well.", (0.05, 0.95, 0.12, 0.30),
          size=32, color=WARM_GLOW, style="italic")
    social_footer(fig, y=0.060)
    save_square(fig, "46_social_quote.png")


if __name__ == "__main__":
    make_pair(draw_hero, "hero", "I Built It. Can My Team Use It?",
              "From the builder's desk to the operator's.")
    make_pair(draw_five_roles, "five_roles", "Five Roles, Shared Accountability",
              "One person may hold several of them.")
    make_pair(draw_operator_journey, "operator_journey",
              "The Operator's Journey", "Two places where a person must stop.")
    make_pair(draw_architecture, "architecture", "Keep the Rules Behind the Door",
              "The front door collects inputs. It holds no rules.")
    make_pair(draw_three_front_doors, "three_front_doors",
              "Three Kinds of Front Door", "The simplest one that fits wins.")
    make_pair(draw_green_check, "green_check", "What a Green Check Means",
              "Checks passed is not the same as correct.")
    make_social_square()
    make_social_quote()
    print("Generated 6 article visuals, 6 slide variants, and 2 social cards "
          "for Article 46.")
