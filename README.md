# reimbursement_calculator
Python tool to compute travel reimbursement for sets of projects; handles overlapping or contiguous projects.

## Rules
- All projects have a start_date and end_date: the first day and last day of a project (or sequence of projects) are travel days.
- The first day of a project and the last day of a project are considered "travel" days. Days with no travel in the middle of a project are "full" days. 
    - If there are multiple projects on the same day, the high cost tier overwrites the low cost tier.
- There are two types of cities a project can be in, high cost cities and low cost cities.
- Any given day is only ever reimbursed once, even if multiple projects are on the same day.
- Projects that are contiguous or overlap, with no gap between the end of one and the start of the next, are considered a sequence of projects and should be treated similar to a single project, therefore affecting how day type is assigned.
- Any day in the middle of a project (or sequence of projects) is considered a full day.
- If there is a gap between projects, those gap days are not reimbursed and the days on either side of that gap are travel days.

- Reimbursement Rates are designated per day type and cost tier combination as designated in table:

|            | Low Cost Tier City | High Cost Tier City |
|------------|--------------------|---------------------|
| Travel Day | $45                 |$55 |
| Full Day   | $75                 |$85 |


## Assumptions
- Projects are inputted as tuples including: city_cost_tier ("low" or "high"), start_date, and end_date
    - Start and end dates can be dates or datetimes (normalized to dates)
    - End date of project can equal start date but can not come before start date
- If two projects are overlapping, any days with high cost will override days with low cost and are only reimbursed once
- If two projects are overlapping or contiguous, travel and full dates are determined based off of the combined date ranges
- Any days that are gaps between two projects (not contiguous) are not reimbursed.
- All calendar days are treated equally without special deference, ex: holidays/ weekends.
- If two projects within a given set are identical in day types and cost tiers, these are treated as dupliactes and only one is kept.
- A single day project is treated as a travel day.

## Repo Structure
- reimbursement_calculator.py: contains primary functions for calculating total and breakdown reimbursement and helper functions
- scenarios.py: the 4 scenario inputs (as lists)
- run_scenarios.py: scenario runner used to print reimbursement totals and per day breakdown 
- tests/: contains unit tests for each function or group of functions in reimbursement_calculator.py and run_scenarios.py
  - test_rate.py
  - test_dates.py
  - test_combine.py
  - test_classify_and_choose.py
  - test_scenarios.py
- README.md
- requirements.txt: pytest (for unit tests)



## How to run
### Quick Start: Run all 4 Scenarios

**Prereqs**
- Python 3.10+ and `pip`
- Install test deps: `pip install -r requirements.txt`

**Run all scenarios:**
`python run_scenarios.py`

### Custom Calculations
``` python
from datetime import date
from reimbursement_calculator import calculate_reimbursement
projects = [("low", date(2024,10,1), date(2024,10,4))]
total_reimbursement, reimbursement_breakdown = calculate_reimbursement(projects)
print(total_reimbursement)
for d in sorted(reimbursement_breakdown):
    print(d, reimbursement_breakdown[d])
```

### Expected Scenario Results
| Scenario | Total |
|----------|-------|
| 1 | $240 |
| 2 | $665 |
| 3 | $520 |
| 4 | $440 |

- Besides running all scenarios with `python run_scenarios.py`, you can also run the scenario validation with pytest installed: `pytest -q tests/test_scenarios.py::test_totals_for_all_scenarios`

## How the Code Works
- Examines project ranges within given set to determine if overlapping or contiguous. If so, these are merged into one duration.
- Days are classified as travel or full based on combined project duration
- Cost tiers per day are chosen with high values overwriting low if there is overlap.
- Reimbursement rates are calculated by looking up reimbursement rate for corresponding day type/ cost tier.
- A total reimbursement for each project set is returned based on these rules as well as a daily breakdown of reimbursement.

## Unit Testing
- `pytest -q` to run full unit tests
- `tests/test_scenarios.py` is most critical check, which validates the four scenario totals to be as follows:
    - [240, 665, 520, 440]
- Further unit tests are created for calculation and helper functions, such as the rate lookup, project combiner, day assignment, and cost tier choice

## Error Handling
- Invalid city cost tiers (not "high" or "low") return a ValueError
    - Note that the city cost tier is stripped of white space and lowercased in case of inconsistent input, allowing for inputs like 'HIGH' and ' Low '.
- Date or datetime type values are required for start_date and end_date and will return TypeError if not met
- If end_date < start_date, this will return a ValueError
