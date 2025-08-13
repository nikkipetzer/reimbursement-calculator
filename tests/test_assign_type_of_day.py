import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date, datetime
import pytest
import reimbursement_calculator as rc

def test_assign_single_day_as_travel():
    # Test a single day project as travel
    type_of_day = rc.assign_type_of_day([(date(2023, 1, 1), date(2023, 1, 1))])
    assert type_of_day[date(2023,1,1)] == "travel"


def test_assign_range_travel_ends_full_middle():
    # Test a project with travel days at the start and end, and full days in the middle
    type_of_day = rc.assign_type_of_day([(date(2023, 1, 1), date(2023, 1, 5))])
    assert type_of_day[date(2023, 1, 1)] == "travel"
    assert type_of_day[date(2023, 1, 5)] == "travel"
    assert type_of_day[date(2023, 1, 2)] == "full"
    assert type_of_day[date(2023, 1, 3)] == "full"
    assert type_of_day[date(2023, 1, 4)] == "full"

def test_assign_accepts_datetimes():
    # Test that the function accepts datetime objects and classifies them correctly
    start = datetime(2023, 1, 1, 12, 0)
    end = datetime(2023, 1, 5, 12, 0)
    type_of_day = rc.assign_type_of_day([(start, end)])
    
    assert type_of_day[start.date()] == "travel"
    assert type_of_day[end.date()] == "travel"
    assert type_of_day[date(2023, 1, 2)] == "full"
    assert type_of_day[date(2023, 1, 3)] == "full"
    assert type_of_day[date(2023, 1, 4)] == "full"

def test_assign_noncontiguous_nonoverlap_periods():
    ranges = [
        (date(2023, 1, 1), date(2023, 1, 5)),
        (date(2023, 1, 7), date(2023, 1, 10)),
    ]
    dt = rc.assign_type_of_day(ranges)

    #first range
    assert dt[date(2023, 1, 1)] == "travel"
    assert dt[date(2023, 1, 5)] == "travel"
    assert dt[date(2023, 1, 2)] == "full"

    #second range
    assert dt[date(2023, 1, 7)] == "travel"
    assert dt[date(2023, 1, 10)] == "travel"
    assert dt[date(2023, 1, 8)] == "full"
    assert dt[date(2023, 1, 9)] == "full"

    #gap days not assigned
    assert date(2023, 1, 6) not in dt

    #only days in ranges are assigned
    assert set(dt.keys()) == {
        date(2023, 1, 1), date(2023, 1  , 2), date(2023, 1, 3),
        date(2023, 1, 4), date(2023, 1, 5),
        date(2023, 1, 7), date(2023, 1  , 8), date(2023, 1, 9),
        date(2023, 1, 10), }  