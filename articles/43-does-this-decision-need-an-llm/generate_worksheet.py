"""Build the Article 43 cost workbook -- "Does This Decision Actually Need a
Large Language Model?"

Run from anywhere:
    python generate_worksheet.py

Writes ./templates/cost_per_acceptable_decision.xlsx: four scenarios side by
side, every calculated cell a visible formula.

Styling follows docs/PythonMuse_BrandSample.xlsx: Deep Navy header row with
white bold text, thin Ocean Teal borders, #EDF5F5 alternating rows, Midnight
Teal total row with Golden Yellow text.
All content is synthetic. Prices are illustrative, not any provider's.
"""

from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

DEEP_NAVY = "002639"
MIDNIGHT_TEAL = "003144"
BRIGHT_TEAL = "3ABFB9"
GOLDEN_YELLOW = "FFD75E"
OCEAN_TEAL = "005F6F"
ALT_ROW = "EDF5F5"
WHITE = "FFFFFF"

HERE = Path(__file__).parent
TEMPLATES = HERE / "templates"
FOOTER = "PythonMuse LLC  |  www.pythonmuse.com"

thin = Side(style="thin", color=OCEAN_TEAL)
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
HEADER_FILL = PatternFill("solid", fgColor=DEEP_NAVY)
ALT_FILL = PatternFill("solid", fgColor=ALT_ROW)
TOTAL_FILL = PatternFill("solid", fgColor=MIDNIGHT_TEAL)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="top")


# ---------------------------------------------------------------------------
# Cost per acceptable decision: inputs, and a Python mirror of the formulas
# ---------------------------------------------------------------------------
INPUT_ROWS = [
    ("volume", "Items per month", "#,##0"),
    ("in_tokens", "Input tokens per item", "#,##0"),
    ("out_tokens", "Output tokens per item", "#,##0"),
    ("in_price", "Input price per million tokens ($, illustrative)", "$#,##0.00"),
    ("out_price", "Output price per million tokens ($, illustrative)", "$#,##0.00"),
    ("auto", "Share auto-routed (no person)", "0%"),
    ("confirm", "Share a person confirms", "0%"),
    ("escalate", "Share escalated to a person", "0%"),
    ("min_confirm", "Minutes per confirmation", "0.0"),
    ("min_escalate", "Minutes per escalation", "0.0"),
    ("rate", "Reviewer cost per hour ($)", "$#,##0"),
    ("auto_error", "Error rate on auto-routed items", "0.0%"),
    ("error_cost", "Cost of one uncaught error ($)", "$#,##0"),
]

SCENARIOS = [
    {"name": "Decision model + bands", "volume": 10000, "in_tokens": 500,
     "out_tokens": 0, "in_price": 0.10, "out_price": 0.0, "auto": 0.70,
     "confirm": 0.20, "escalate": 0.10, "min_confirm": 1.0, "min_escalate": 6.0,
     "rate": 60, "auto_error": 0.01, "error_cost": 50},
    {"name": "Cheapest model, loose bands", "volume": 10000, "in_tokens": 500,
     "out_tokens": 0, "in_price": 0.05, "out_price": 0.0, "auto": 0.50,
     "confirm": 0.0, "escalate": 0.50, "min_confirm": 1.0, "min_escalate": 6.0,
     "rate": 60, "auto_error": 0.02, "error_cost": 50},
    {"name": "LLM paragraph, every item read", "volume": 10000, "in_tokens": 500,
     "out_tokens": 300, "in_price": 2.00, "out_price": 10.00, "auto": 0.0,
     "confirm": 1.0, "escalate": 0.0, "min_confirm": 1.5, "min_escalate": 6.0,
     "rate": 60, "auto_error": 0.0, "error_cost": 50},
    {"name": "All manual", "volume": 10000, "in_tokens": 0, "out_tokens": 0,
     "in_price": 0.0, "out_price": 0.0, "auto": 0.0, "confirm": 1.0,
     "escalate": 0.0, "min_confirm": 3.0, "min_escalate": 6.0, "rate": 60,
     "auto_error": 0.0, "error_cost": 50},
]


def cost_per_acceptable_decision(s):
    """Python mirror of the workbook formulas (tested in test_cost_workbook.py)."""
    model = s["volume"] * (s["in_tokens"] * s["in_price"]
                           + s["out_tokens"] * s["out_price"]) / 1_000_000
    review = s["volume"] * (s["confirm"] * s["min_confirm"]
                            + s["escalate"] * s["min_escalate"]) * s["rate"] / 60
    uncaught = s["volume"] * s["auto"] * s["auto_error"]
    error_cost = uncaught * s["error_cost"]
    total = model + review + error_cost
    acceptable = s["volume"] - uncaught
    return {"model_cost": model, "review_cost": review, "uncaught": uncaught,
            "error_cost": error_cost, "total_cost": total,
            "acceptable": acceptable, "per_decision": total / acceptable}


# ---------------------------------------------------------------------------
# Shared styling helpers
# ---------------------------------------------------------------------------
def title_block(ws, title, subtitle):
    ws["A1"] = title
    ws["A1"].font = Font(name="Calibri", size=16, bold=True, color=DEEP_NAVY)
    ws["A2"] = subtitle
    ws["A2"].font = Font(name="Calibri", size=12, bold=True, color=BRIGHT_TEAL)
    ws.sheet_view.showGridLines = False


def header_row(ws, row, names_widths):
    for c, (name, width) in enumerate(names_widths, start=1):
        cell = ws.cell(row=row, column=c, value=name)
        cell.font = Font(name="Calibri", size=11, bold=True, color=WHITE)
        cell.fill = HEADER_FILL
        cell.border = BORDER
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        if width:
            ws.column_dimensions[get_column_letter(c)].width = width
    ws.row_dimensions[row].height = 32


def body_cell(ws, r, c, value, alt, bold=False, fmt=None, align=WRAP):
    cell = ws.cell(row=r, column=c, value=value)
    cell.font = Font(name="Calibri", size=11, color=DEEP_NAVY, bold=bold)
    cell.border = BORDER
    cell.alignment = align
    if alt:
        cell.fill = ALT_FILL
    if fmt:
        cell.number_format = fmt
    return cell


def footer(ws, row):
    ws.cell(row=row, column=1, value=FOOTER).font = Font(
        name="Calibri", size=10, italic=True, color=OCEAN_TEAL)


def landscape(ws):
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True


# ---------------------------------------------------------------------------
# Cost per acceptable decision workbook
# ---------------------------------------------------------------------------
CALC_ROWS = [
    ("Model cost ($)", "={c}5*({c}6*{c}8+{c}7*{c}9)/1000000", "$#,##0.00"),
    ("Review cost ($)", "={c}5*({c}11*{c}13+{c}12*{c}14)*{c}15/60", "$#,##0.00"),
    ("Uncaught errors (items)", "={c}5*{c}10*{c}16", "#,##0"),
    ("Cost of uncaught errors ($)", "={c}22*{c}17", "$#,##0.00"),
    ("Total cost ($)", "={c}20+{c}21+{c}23", "$#,##0.00"),
    ("Acceptable decisions (items)", "={c}5-{c}22", "#,##0"),
    ("Shares add to 100%?", '=IF(ROUND({c}10+{c}11+{c}12,6)=1,"OK","Fix shares")', None),
]

COST_NOTES = [
    "How to read this",
    "",
    "Cost per acceptable decision = (model cost + review cost + cost of uncaught errors) / decisions that ended up right.",
    "An item a person confirms or escalates is assumed to end up right; only auto-routed errors slip through.",
    "Every number in the yellow-headed input block is a placeholder. Replace it with your own volumes, minutes, rates, and error costs.",
    "Prices are illustrative, not any provider's list price. Check each provider's current pricing page.",
    "Notice which line moves the answer. In this example it is almost never the model price.",
    "",
    "Educational purposes only; not professional advice. Synthetic numbers.",
]


def build_cost(out_dir):
    wb = Workbook()
    ws = wb.active
    ws.title = "Compare"
    ws.sheet_properties.tabColor = GOLDEN_YELLOW
    title_block(ws, "Cost per Acceptable Decision",
                "The cheapest model is not automatically the cheapest process")
    header_row(ws, 4, [("Inputs", 48)] + [(s["name"], 22) for s in SCENARIOS])
    for i, (key, label, fmt) in enumerate(INPUT_ROWS):
        r = 5 + i
        body_cell(ws, r, 1, label, i % 2 == 1)
        for j, s in enumerate(SCENARIOS):
            body_cell(ws, r, 2 + j, s[key], i % 2 == 1, fmt=fmt, align=CENTER)

    header_row(ws, 19, [("Calculated (formulas)", None)] + [(s["name"], None) for s in SCENARIOS])
    for i, (label, formula, fmt) in enumerate(CALC_ROWS):
        r = 20 + i
        target = 27 if label.startswith("Shares") else r
        body_cell(ws, target, 1, label, i % 2 == 1)
        for j in range(len(SCENARIOS)):
            col = get_column_letter(2 + j)
            body_cell(ws, target, 2 + j, formula.format(c=col), i % 2 == 1, fmt=fmt,
                      align=CENTER)

    # The answer row, styled as the total row.
    for c in range(1, 2 + len(SCENARIOS)):
        col = get_column_letter(c)
        value = "Cost per acceptable decision ($)" if c == 1 else f"={col}24/{col}25"
        cell = ws.cell(row=26, column=c, value=value)
        cell.font = Font(name="Calibri", size=12, bold=True, color=GOLDEN_YELLOW)
        cell.fill = TOTAL_FILL
        cell.border = BORDER
        cell.alignment = CENTER if c > 1 else WRAP
        if c > 1:
            cell.number_format = "$#,##0.00"

    for i, line in enumerate(COST_NOTES, start=29):
        cell = ws.cell(row=i, column=1, value=line)
        heading = i == 29
        cell.font = Font(name="Calibri", size=12 if heading else 11, bold=heading,
                         color=OCEAN_TEAL if heading else DEEP_NAVY)
    footer(ws, 29 + len(COST_NOTES) + 1)
    ws.freeze_panes = "B5"
    landscape(ws)
    wb.save(out_dir / "cost_per_acceptable_decision.xlsx")


def build(out_dir=TEMPLATES):
    out_dir = Path(out_dir)
    out_dir.mkdir(exist_ok=True)
    build_cost(out_dir)


if __name__ == "__main__":
    build()
    for s in SCENARIOS:
        r = cost_per_acceptable_decision(s)
        print(f"{s['name']:<34} total ${r['total_cost']:>10,.2f}  "
              f"per acceptable decision ${r['per_decision']:.2f}")
    print("Wrote templates/cost_per_acceptable_decision.xlsx")
