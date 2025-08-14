import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import date
import scenarios as s
import reimbursement_calculator as rc


def test_totals_for_all_scenarios():
    expected = [240, 665, 520, 440]
    for projects, exp in zip(s.scenarios, expected):
        total, breakdown = rc.calculate_reimbursement(projects)
        assert total == exp

