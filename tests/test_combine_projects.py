import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date, datetime
import pytest
import reimbursement_calculator as rc


def test_combine_projects_empty_and_single():
    # Empty
    assert rc.combine_projects([]) == []

    # Single project -> one (start, end) tuple
    project = ("low", date(2023, 1, 1), date(2023, 1, 10))
    assert rc.combine_projects([project]) == [(date(2023, 1, 1), date(2023, 1, 10))]


def test_combine_projects_overlapping_or_contiguous():
    # Overlapping: 1–5 and 4–10 => merged 1–10
    projects = [
        ("low", date(2023, 1, 1), date(2023, 1, 5)),
        ("low", date(2023, 1, 4), date(2023, 1, 10)),
    ]
    assert rc.combine_projects(projects) == [(date(2023, 1, 1), date(2023, 1, 10))]

    # Contiguous: 1–5 and 6–10 => merged 1–10
    projects = [
        ("low", date(2023, 1, 1), date(2023, 1, 5)),
        ("low", date(2023, 1, 6), date(2023, 1, 10)),
    ]
    assert rc.combine_projects(projects) == [(date(2023, 1, 1), date(2023, 1, 10))]


def test_combine_projects_non_overlapping():
    # Non-overlapping: projects are all not overlapping and not contiguous
    projects = [
        ("low",  date(2023, 1, 1), date(2023, 1, 5)),   # ends 5th
        ("low",  date(2023, 1, 7), date(2023, 1, 10)),  # gap day 6th -> NOT contiguous
        ("high", date(2023, 1, 15), date(2023, 1, 15)),
    ]
    combined = rc.combine_projects(projects)
    assert combined == [
        (date(2023, 1, 1), date(2023, 1, 5)),
        (date(2023, 1, 7), date(2023, 1, 10)),
        (date(2023, 1, 15), date(2023, 1, 15)),
    ]
