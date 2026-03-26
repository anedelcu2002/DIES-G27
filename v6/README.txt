How to use this refactor
========================

1. Put these four files in the same folder as your RAMP project:
   - config_defaults.py
   - user_overrides.py
   - ramp_runner.py
   - main.py

2. Make sure residential_input.csv is in the same folder, or change input_csv in config_defaults.py.

3. Run:
   python main.py

4. Normal workflow:
   - Keep baseline assumptions in config_defaults.py
   - Change only scenario-specific values in user_overrides.py
   - Leave user_overrides.py empty to fall back to all defaults

5. To add a new appliance:
   Add it inside USER_APPLIANCES in user_overrides.py, for example:

   "Laptop": {
       "enabled": True,
       "user": "households",
       "number": 1,
       "power": 60,
       "func_time": 240,
       "window_1": [1080, 1380]
   }

6. To disable an appliance:
   Example:
   "Cooking": {"enabled": False}

7. Current user groups supported by default:
   - households
   - washing_users
