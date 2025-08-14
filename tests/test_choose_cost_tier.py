import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date, datetime
import pytest
import reimbursement_calculator as rc


def test_low_only_days():
    # Test a project with only low cost days
    projects = [("low", date(2023, 1, 1), date(2023, 1, 5))]
    mapping = rc.choose_cost_tier_per_day(projects)
    assert mapping == {
        date(2023, 1, 1): "low",
        date(2023, 1, 2): "low",
        date(2023, 1, 3): "low",
        date(2023, 1, 4): "low",
        date(2023, 1, 5): "low"
    }   

def test_high_only_days():
    # Test a project with only high cost days
    projects = [("high", date(2023, 1, 1), date(2023, 1, 5))]
    mapping = rc.choose_cost_tier_per_day(projects)
    assert mapping == {
        date(2023, 1, 1): "high",
        date(2023, 1, 2): "high",
        date(2023, 1, 3): "high",
        date(2023, 1, 4): "high",
        date(2023, 1, 5): "high"
    }

def test_overlap_high_overrides_low():
    # Test overlapping projects where high cost overrides low cost
    projects = [
        ("low", date(2023, 1, 1), date(2023, 1, 5)),
        ("high", date(2023, 1, 3), date(2023, 1, 7))
    ]
    mapping = rc.choose_cost_tier_per_day(projects)
    assert mapping == {
        date(2023, 1, 1): "low",
        date(2023, 1, 2): "low",
        date(2023, 1, 3): "high",
        date(2023, 1, 4): "high",
        date(2023, 1, 5): "high",
        date(2023, 1, 6): "high",
        date(2023, 1, 7): "high"
    }

def test_overlap_high_remains_if_low_first():
    # Test overlapping projects where high cost remains if low cost is first
    projects = [
        ("high", date(2023, 1, 1), date(2023, 1, 5)),
        ("low", date(2023, 1, 3), date(2023, 1, 7))
    ]
    mapping = rc.choose_cost_tier_per_day(projects)
    assert mapping == {
        date(2023, 1, 1): "high",
        date(2023, 1, 2): "high",
        date(2023, 1, 3): "high",
        date(2023, 1, 4): "high",
        date(2023, 1, 5): "high",
        date(2023, 1, 6): "low",
        date(2023, 1, 7): "low"
    }

def test_city_cost_tier_normalizaed():
    # Test that city cost tiers are normalized to 'low' and 'high'
    projects = [
        ("LOW", date(2023, 1, 1), date(2023, 1, 5)),
        (" High ", date(2023, 1, 6), date(2023, 1, 10))
    ]
    mapping = rc.choose_cost_tier_per_day(projects)
    assert mapping == {
        date(2023, 1, 1): "low",
        date(2023, 1, 2): "low",
        date(2023, 1, 3): "low",
        date(2023, 1, 4): "low",
        date(2023, 1, 5): "low",
        date(2023, 1, 6): "high",
        date(2023, 1, 7): "high",
        date(2023, 1, 8): "high",
        date(2023, 1, 9): "high",
        date(2023, 1, 10): "high"
    }

def test_raise_error_for_invalid_cost_tier():
    # Test that an error is raised for invalid cost tiers
    projects = [("medium", date(2023, 1, 1), date(2023, 1, 5))]
    with pytest.raises(ValueError):
        rc.choose_cost_tier_per_day(projects)   