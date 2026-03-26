"""Optional scenario-specific overrides.

Leave dictionaries empty to use all defaults.
Only add keys you want to change.
You can also add entirely new appliances here.
"""

USER_CONFIG = {
    # Example:
    # "households_simulated": 100,
    # "num_days": 365,
    # "output_csv": "scenario_A.csv",
}

USER_APPLIANCES = {
    # Example override of an existing appliance:
    # "Cooking": {"power": 1000},

    # Example of adding a new appliance:
    # "Laptop": {
    #     "enabled": True,
    #     "user": "households",
    #     "number": 1,
    #     "power": 60,
    #     "func_time": 240,
    #     "window_1": [1080, 1380],
    # },
}
