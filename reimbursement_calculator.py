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