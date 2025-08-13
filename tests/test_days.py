import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date
import pytest
import reimbursement_calculator as rc

def test_get_project_duration():
    # Test valid date range
    start = date(2023, 1, 1)
    end = date(2023, 1, 10)
    assert rc.get_project_duration(start, end) == 10

    # Test single day duration
    start = date(2023, 1, 5)
    end = date(2023, 1, 5)
    assert rc.get_project_duration(start, end) == 1

    # Test invalid date range (end before start)
    with pytest.raises(ValueError):
        rc.get_project_duration(date(2023, 1, 10), date(2023, 1, 1))

def test_each_day():
    # Test valid date range
    start = date(2023, 1, 1)
    end = date(2023, 1, 5)
    days = list(rc.each_day(start, end))
    assert days == [date(2023, 1, i) for i in range(1, 6)]

    # Test single day
    start = date(2023, 1, 10)
    end = date(2023, 1, 10)
    days = list(rc.each_day(start, end))
    assert days == [date(2023, 1, 10)]

def test_middle_days():
    # Test valid date range with middle days
    start = date(2023, 1, 1)
    end = date(2023, 1, 5)
    days = list(rc.middle_days(start, end))
    assert days == [date(2023, 1, 2), date(2023, 1, 3), date(2023, 1, 4)]

    # Test single day (no middle days)
    start = date(2023, 1, 10)
    end = date(2023, 1, 10)
    days = list(rc.middle_days(start, end))
    assert days == []

    # Test two-day range (no middle days)
    start = date(2023, 1, 10)
    end = date(2023, 1, 11)
    days = list(rc.middle_days(start, end))
    assert days == []