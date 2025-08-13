import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import reimbursement_calculator as rc

def test_get_reimbursement_rate_valid_pairs():
    # Make sure the function returns correct values for valid city cost and day type combos
    assert rc.get_reimbursement_rate("low", "travel") == 45
    assert rc.get_reimbursement_rate("low", "full") == 75
    assert rc.get_reimbursement_rate("high", "travel") == 55
    assert rc.get_reimbursement_rate("high", "full") == 85

def test_get_reimbursement_rate_invalid_city_cost():
    #Make sure the function raises ValueError for invalid city cost tiers
    with pytest.raises(ValueError):
        rc.get_reimbursement_rate("medium", "travel")

def test_get_reimbursement_rate_invalid_day_type():
    # Make sure the function raises ValueError for invalid day types
    with pytest.raises(ValueError):
        rc.get_reimbursement_rate("low", "half")
    with pytest.raises(ValueError):
        rc.get_reimbursement_rate("high", "part-time")

def test_get_reimbursement_rate_cleans_inputs():
    # Make sure the function cleans inputs before processingf (removes whitespace, lowercases)
    assert rc.get_reimbursement_rate("  low  ", "  travel  ") == 45
    assert rc.get_reimbursement_rate("HIGH", "FULL") == 85
    assert rc.get_reimbursement_rate("Low", "Full") == 75


