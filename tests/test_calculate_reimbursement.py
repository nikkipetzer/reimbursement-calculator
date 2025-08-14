import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date, datetime
import pytest
import reimbursement_calculator as rc


def test_calculate_empty_returns_zero():
    # Test that an empty list of projects returns zero reimbursement
    total, breakdown = rc.calculate_reimbursement([])
    assert total == 0
    assert breakdown == {}

def test_calculate_simple_low_range_total_and_breakdown():
    # One low-cost project: 10/01–10/04
    # travel(low)=45 on 10/01 & 10/04; full(low)=75 on 10/02 & 10/03 → total=240
    projects = [("low", date(2024,10,1), date(2024,10,4))]
    total, breakdown = rc.calculate_reimbursement(projects)
    assert total == 240
    # spot-check the breakdown
    assert breakdown[date(2024,10,1)] == ("low", "travel", 45)
    assert breakdown[date(2024,10,2)] == ("low", "full",   75)
    assert breakdown[date(2024,10,3)] == ("low", "full",   75)
    assert breakdown[date(2024,10,4)] == ("low", "travel", 45)


def test_calculate_overlap_high_wins_on_full_day():
    # low: 10/01–10/03, high: 10/02–10/02 overlaps in the middle
    # Day types for merged 10/01–10/03: travel, full, travel
    # Cities: 10/01 low, 10/02 high, 10/03 low
    # Rates: 45 + 85 + 45 = 175
    projects = [
        ("low",  date(2024,10,1), date(2024,10,3)),
        ("high", date(2024,10,2), date(2024,10,2)),
    ]
    total, breakdown = rc.calculate_reimbursement(projects)
    assert total == 175
    assert breakdown[date(2024,10,1)] == ("low",  "travel", 45)
    assert breakdown[date(2024,10,2)] == ("high", "full",   85)  # high wins on overlap
    assert breakdown[date(2024,10,3)] == ("low",  "travel", 45)
