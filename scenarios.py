# scenarios.py
from datetime import date

# Scenario with a single low cost project
scenario_1 = [("low",  date(2024, 10, 1), date(2024, 10, 4))]
    
# Scenario with overlapping projects where high cost overrides low cost
scenario_2 = [("low",  date(2024, 10, 1), date(2024, 10, 1)),
            ("high", date(2024, 10, 2), date(2024, 10, 6)),
            ("low",  date(2024, 10, 6), date(2024, 10, 9))]

# Scenario with multiple projects, some overlapping and some not
scenario_3 = [("low",  date(2024,  9, 30), date(2024, 10, 3)),
            ("high", date(2024, 10,  5), date(2024, 10, 7)),
            ("high", date(2024, 10,  8), date(2024, 10, 8))]
    
    
# Scenario with a mix of low and high cost projects, some overlapping
scenario_4 = [("low",  date(2024, 10, 1), date(2024, 10, 1)),
            ("low",  date(2024, 10, 1), date(2024, 10, 1)),
            ("high", date(2024, 10, 2), date(2024, 10, 3)),
            ("high", date(2024, 10, 2), date(2024, 10, 6))]
     
#Combine scenarios
scenarios = (scenario_1,
             scenario_2,
            scenario_3,
            scenario_4)

