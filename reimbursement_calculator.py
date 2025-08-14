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


def combine_projects(projects):
    """Combine multiple projects into a single project with a start and end date. if overlapping or contiguous projects in a set.
    Input: projects - a list of tuples containing the following (city_cost_tier, start_date, end_date)
    """
    if len(projects) == 0: #no projects provided
        return []
    if len(projects) == 1: #only one project provided
        return [(projects[0][1], projects[0][2])]
    
    elif len(projects) > 1: #if more than one project provided
    #extract the start and end dates from each project and sort by start date
        sorted_projects_dates = sorted([(p[1],p[2]) for p in projects])
        merged_project_dates = []

        curr_start_date = sorted_projects_dates[0][0]
        curr_end_date = sorted_projects_dates[0][1]

        for start, end in sorted_projects_dates[1:]: #iterate through remaining sorted projects
            #projects overlap or are contiguous
            if start <= curr_end_date or start <= curr_end_date + timedelta(days=1):
                curr_end_date = max(curr_end_date, end)
            #projects have no overlap or contiguity
            else:
                merged_project_dates.append((curr_start_date, curr_end_date))
                curr_start_date = start
                curr_end_date = end
    
        merged_project_dates.append((curr_start_date, curr_end_date))
        return merged_project_dates
    

def assign_type_of_day(project_dates):
    """Assign a type of day (full or travel) to combined project dates. Travel days are edge days and full days are interior days
    Input: project_dates - a list of project date pairs/ tuples (start_date, end_date)
    """
    type_of_day = {}
    
    for start_date, end_date in project_dates:
        #Handle datetimes
        if isinstance(start_date, datetime):
            start_date = start_date.date()
        if isinstance(end_date, datetime):
            end_date = end_date.date()

        if start_date == end_date: #one day travel
            type_of_day[start_date] = 'travel'
        else:
            type_of_day[start_date] = 'travel' #edge days
            type_of_day[end_date] = 'travel'
            for day in middle_days(start_date, end_date): #middle days
                type_of_day[day] = 'full'
    
    return type_of_day


def choose_cost_tier_per_day(projects):
    """Assign city cost tier to each date in a project duration. Possible cost tiers are 'low' and 'high'. If a date is covered by multiple projects, the highest cost tier is assigned.
    Input: projects - a list of tuples containing the following (city_cost_tier, start_date, end_date) """

    city_cost_tier_for_day = {}

    for cost_tier, start, end in projects:
        cost_tier_cleaned = str(cost_tier).lower().strip()
        #validate provided cost tier (cleaned)
        if cost_tier_cleaned not in reimbursement_rates:
            raise ValueError(f"Invalid city cost tier: {cost_tier}. Valid options are: {list(reimbursement_rates)}")
        
        for day in each_day(start,end):
            if cost_tier_cleaned == 'high':
                city_cost_tier_for_day[day] = 'high' #override with high cost tier if already set, or populate with high tier
            elif day not in city_cost_tier_for_day:
                city_cost_tier_for_day[day] = "low" #otherwise, low
    
    return city_cost_tier_for_day


            