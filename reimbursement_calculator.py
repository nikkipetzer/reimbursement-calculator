#Imports
from datetime import date, datetime, timedelta

#Define Reimbursement Rate Table
reimbursement_rates = {
    "low": {"travel": 45, "full": 75},
    "high": {"travel": 55, "full": 85}
}


def get_reimbursement_rate(city_cost: str, day_type: str):
    """Get the reimbursement rate based on city cost and day type."""
    city_cost_cleaned = str(city_cost).lower().strip()
    day_type_cleaned = str(day_type).lower().strip()

    if city_cost_cleaned not in reimbursement_rates:
        raise ValueError(f"Invalid city cost tier: {city_cost}. Valid options are: {list(reimbursement_rates)}")
    if day_type_cleaned not in reimbursement_rates[city_cost_cleaned]:
        raise ValueError(f"Invalid day type: {day_type}. Valid options are: {list(reimbursement_rates[city_cost_cleaned])}")
    
    return reimbursement_rates[city_cost_cleaned][day_type_cleaned]


def get_project_duration(start_date: date | datetime, end_date: date | datetime):
    """Calculate the day count between two project dates (inclusive). Converts datetime to date if inputted."""
    if isinstance(start_date, datetime):
        start_date = start_date.date()
    if isinstance(end_date, datetime):
        end_date = end_date.date()

    if not isinstance(start_date, date) or not isinstance(end_date, date):
        raise TypeError("Both start_date and end_date must be of type date or datetime.")

    if end_date < start_date:
        raise ValueError("End date cannot be before start date. It must equal or follow the start date.")
    
    return (end_date - start_date).days + 1


def each_day(start_date: date | datetime, end_date: date | datetime):
    """Return each day in a project period start_date to end_date (inclusive). Converts datetime to date if inputted."""
    start_date_cleaned = start_date.date() if isinstance(start_date, datetime) else start_date
    end_date_cleaned = end_date.date() if isinstance(end_date, datetime) else end_date

    for day in range(get_project_duration(start_date_cleaned, end_date_cleaned)):
        yield start_date_cleaned + timedelta(days=day)


def middle_days(start_date: date, end_date: date):
    """Return all days in a project period except the first and last day: the middle days in the period. Converts datetime to date if inputted."""
    start_date_cleaned = start_date.date() if isinstance(start_date, datetime) else start_date
    end_date_cleaned = end_date.date() if isinstance(end_date, datetime) else end_date
    
    for day in range(1, get_project_duration(start_date_cleaned, end_date_cleaned) - 1):
        yield start_date_cleaned + timedelta(days=day)
