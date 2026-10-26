"""Tests for the Article 43 cost workbook.

Run from the article folder:
    python -m pytest test_cost_workbook.py -q

Every expected figure below was worked out by hand BEFORE these assertions
were written.

  Cost per acceptable decision (10,000 items, $60/hour, $50 per uncaught error):
    Decision model + bands: 0.50 + 8,000 + 3,500 = 11,500.50 / 9,930 = 1.1582
    Cheapest model, half to a person: 0.25 + 30,000 + 5,000 = 35,000.25 / 9,900
                                      = 3.5354
    LLM paragraph, every item read: 40 + 15,000 + 0 = 15,040 / 10,000 = 1.504
    All manual: 30,000 / 10,000 = 3.00
"""

import sys
from pathlib import Path

import pytest

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import generate_worksheet as gw  # noqa: E402


@pytest.mark.parametrize("name, total, acceptable, per_decision", [
    ("Decision model + bands", 11500.50, 9930, 1.1582),
    ("Cheapest model, loose bands", 35000.25, 9900, 3.5354),
    ("LLM paragraph, every item read", 15040.00, 10000, 1.5040),
    ("All manual", 30000.00, 10000, 3.0000),
])
def test_cost_per_acceptable_decision(name, total, acceptable, per_decision):
    scenario = next(s for s in gw.SCENARIOS if s["name"] == name)
    r = gw.cost_per_acceptable_decision(scenario)
    assert r["total_cost"] == pytest.approx(total)
    assert r["acceptable"] == pytest.approx(acceptable)
    assert r["per_decision"] == pytest.approx(per_decision, abs=1e-4)


def test_cheapest_model_builds_the_most_expensive_process():
    per = {s["name"]: gw.cost_per_acceptable_decision(s)["per_decision"]
           for s in gw.SCENARIOS}
    assert max(per, key=per.get) == "Cheapest model, loose bands"


def test_workbook_has_live_formulas(tmp_path):
    from openpyxl import load_workbook
    gw.build(tmp_path)
    cost = load_workbook(tmp_path / "cost_per_acceptable_decision.xlsx")["Compare"]
    formulas = [c.value for row in cost.iter_rows() for c in row
                if isinstance(c.value, str) and c.value.startswith("=")]
    assert len(formulas) >= 24      # 6 calculated rows x 4 scenarios
    assert cost["B26"].value == "=B24/B25"
