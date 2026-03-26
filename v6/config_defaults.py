"""Default assumptions for the RAMP residential model.

Edit this file only if you want to change the baseline assumptions.
Most users should put scenario-specific changes in user_overrides.py instead.
"""

DEFAULT_CONFIG = {
    "input_csv": "residential_input.csv",
    "row_index": 0,
    "households_simulated": 50,
    "num_days": 366,
    "output_csv": "load_profiles_PC1098.csv",
    "save_csv": True,
    "plot_first_day": True,
    "rolling_window": 5,
    "dc_loads_kw": {
        "dc_campus_1_kw": 5000,
        "dc_campus_2_kw": 8000,
        "dc_campus_3_kw": 12000,
    },
    # Share of simulated households that own/use a washing machine user profile
    "washing_user_share": 0.30,
}

DEFAULT_APPLIANCES = {
    "Fridge": {
        "enabled": True,
        "user": "households",
        "number": 1,
        "power": 120,
        "func_time": 1440,
        "window_1": [0, 1440],
    },
    "Lighting": {
        "enabled": True,
        "user": "households",
        "number": 5,
        "power": 10,
        "func_time": 120,
        "window_1": [360, 540],
        "window_2": [1080, 1380],
    },
    "Electronics": {
        "enabled": True,
        "user": "households",
        "number": 2,
        "power": 70,
        "func_time": 180,
        "window_1": [500, 900],
        "window_2": [1080, 1320],
    },
    "Cooking": {
        "enabled": True,
        "user": "households",
        "number": 1,
        "power": 800,
        "func_time": 60,
        "window_1": [1020, 1380],
    },
    "WashingMachine": {
        "enabled": True,
        "user": "washing_users",
        "number": 1,
        "power": 500,
        "func_time": 60,
        "window_1": [600, 1200],
    },
    "BaseLoad": {
        "enabled": True,
        "user": "households",
        "number": 1,
        "power": 150,
        "func_time": 1440,
        "window_1": [0, 1440],
    },
}
