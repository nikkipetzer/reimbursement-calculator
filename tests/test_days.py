import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date, datetime
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

def test_get_project_duration_datetime_handling():
    # Test with datetime objects
    start = datetime(2023, 1, 1, 12, 0)
    end = datetime(2023, 1, 10, 12, 0)
    assert rc.get_project_duration(start, end) == 10

    # Test with mixed date and datetime inputs
    start = date(2023, 1, 5)
    end = datetime(2023, 1, 5, 15, 30)
    assert rc.get_project_duration(start, end) == 1

    # Test invalid types
    with pytest.raises(TypeError):
        rc.get_project_duration("2023-01-01", "2023-01-10")

def test_get_project_duration_invalid_types():
    with pytest.raises(TypeError):
        rc.get_project_duration("2024-10-01", date(2024,10,4)) #invalid start date type
    with pytest.raises(TypeError):
        rc.get_project_duration(date(2024, 10, 1), 999) #invalid end date type

def test_each_day_datetime_handling():
    days = list(rc.each_day(datetime(2023, 1, 1), datetime(2023, 1, 5)))
    assert [day == date(2023, 1, i) for i, day in enumerate(days, start=1)]
    
def test_middle_days_datetime_handling():
    days = list(rc.middle_days(datetime(2023, 1, 1), datetime(2023, 1, 5)))
    assert days == [date(2023, 1, 2), date(2023, 1, 3), date(2023, 1, 4)]

    # Test with mixed date and datetime inputs
    days = list(rc.middle_days(date(2023, 1, 10), datetime(2023, 1, 12)))
    assert days == [date(2023, 1, 11)]
