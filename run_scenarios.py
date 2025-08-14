import scenarios as s
import reimbursement_calculator as rc

from reimbursement_calculator import calculate_reimbursement
import scenarios as sc


def run_scenarios():
    """Runs all provided scenarios and resulting total reimbursement as well as daily reimbursement breakdown."""
    for i, projects in enumerate(sc.scenarios, start=1):
        total, breakdown = calculate_reimbursement(projects)

        print(f"Scenario {i} total reimbursement amount: ${total}")
        for d in sorted(breakdown):
            city_tier, day_type, rate = breakdown[d]
            print(f"  {d.isoformat()} :  ${rate} (Day Type: {day_type}, City Cost Tier: {city_tier})")
        


run_scenarios()