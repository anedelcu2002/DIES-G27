from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from ramp import User, UseCase


REQUIRED_INPUT_COLUMNS = ["households", "electricity_per_household_kwh"]


def deep_merge(default: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge two dictionaries without mutating the inputs."""
    result = deepcopy(default)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def load_residential_inputs(csv_path: str | Path, row_index: int = 0) -> dict[str, Any]:
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Input CSV not found: {csv_path}. Put the CSV next to main.py or update input_csv."
        )

    df = pd.read_csv(csv_path)

    missing = [col for col in REQUIRED_INPUT_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(
            f"Input CSV is missing required columns: {missing}. Found: {list(df.columns)}"
        )

    if row_index >= len(df):
        raise IndexError(
            f"row_index={row_index} is out of range. CSV has {len(df)} row(s)."
        )

    row = df.loc[row_index]
    return {
        "df": df,
        "households_real": int(row["households"]),
        "electricity_per_household_kwh": float(row["electricity_per_household_kwh"]),
    }


def validate_config(config: dict[str, Any], appliances: dict[str, Any]) -> None:
    if config["households_simulated"] <= 0:
        raise ValueError("households_simulated must be > 0")
    if config["num_days"] <= 0:
        raise ValueError("num_days must be > 0")
    if not 0 <= config["washing_user_share"] <= 1:
        raise ValueError("washing_user_share must be between 0 and 1")

    for name, params in appliances.items():
        if not params.get("enabled", True):
            continue
        if "user" not in params:
            raise ValueError(f"Appliance '{name}' is missing the 'user' field.")
        if params.get("number", 1) <= 0:
            raise ValueError(f"Appliance '{name}' must have number > 0")
        if params.get("power", 0) < 0:
            raise ValueError(f"Appliance '{name}' must have power >= 0")


def build_users(config: dict[str, Any]) -> dict[str, User]:
    households_simulated = int(config["households_simulated"])
    washing_users = int(round(config["washing_user_share"] * households_simulated))
    washing_users = max(washing_users, 1) if config["washing_user_share"] > 0 else 0

    users = {
        "households": User("households", households_simulated),
    }
    if washing_users > 0:
        users["washing_users"] = User("washing_users", washing_users)

    return users


ALLOWED_APPLIANCE_KEYS = {
    "name",
    "number",
    "power",
    "func_time",
    "window_1",
    "window_2",
    "window_3",
    "fixed",
    "fixed_cycle",
    "occasional_use",
    "flat",
    "thermal_p_var",
    "pref_index",
    "wd_we_type",
    "func_cycle",
    "time_fraction_random_variability",
    "num_windows",
    "continuous_duty_cycle",
}


def add_appliances(users: dict[str, User], appliances: dict[str, Any]) -> None:
    for appliance_name, params in appliances.items():
        if not params.get("enabled", True):
            continue

        user_key = params["user"]
        if user_key not in users:
            raise KeyError(
                f"Appliance '{appliance_name}' points to unknown user group '{user_key}'. "
                f"Available user groups: {list(users)}"
            )

        ramp_kwargs = {"name": appliance_name}
        for key, value in params.items():
            if key in {"enabled", "user"}:
                continue
            if key in ALLOWED_APPLIANCE_KEYS:
                ramp_kwargs[key] = value

        users[user_key].add_appliance(**ramp_kwargs)


def run_ramp(config: dict[str, Any], appliances: dict[str, Any]) -> dict[str, Any]:
    validate_config(config, appliances)

    input_data = load_residential_inputs(config["input_csv"], config["row_index"])
    households_real = input_data["households_real"]
    electricity_per_household_kwh = input_data["electricity_per_household_kwh"]

    users = build_users(config)
    add_appliances(users, appliances)

    case = UseCase(users=list(users.values()))
    case.initialize(num_days=int(config["num_days"]))

    profiles = case.generate_daily_load_profiles(flat=True, verbose=False)
    profile = np.array(profiles)

    weight = households_real / config["households_simulated"]
    profile_real = profile * weight
    profile_kw = profile_real / 1000.0

    output = {"residential_kw": profile_kw}
    for column_name, load_kw in config["dc_loads_kw"].items():
        output[column_name] = np.ones_like(profile_kw) * float(load_kw)

    output_df = pd.DataFrame(output)

    annual_energy = profile_kw.sum() / 60
    daily_energy = annual_energy / 365

    return {
        "input_summary": {
            "households_real": households_real,
            "electricity_per_household_kwh": electricity_per_household_kwh,
            "households_simulated": config["households_simulated"],
            "weight": weight,
            "num_days": config["num_days"],
        },
        "profile_kw": profile_kw,
        "output_df": output_df,
        "peak_kw": float(profile_kw.max()),
        "annual_energy_kwh": float(annual_energy),
        "average_daily_energy_kwh": float(daily_energy),
    }


def save_outputs(results: dict[str, Any], output_csv: str | Path) -> Path:
    output_csv = Path(output_csv)
    results["output_df"].to_csv(output_csv, index=False)
    return output_csv


def plot_first_day(profile_kw: np.ndarray, rolling_window: int = 5) -> None:
    smoothed = pd.Series(profile_kw).rolling(rolling_window, min_periods=1).mean()
    plt.figure(figsize=(10, 4))
    plt.plot(smoothed[:1440])
    plt.xlabel("Minute of day")
    plt.ylabel("Load (kW)")
    plt.title("Residential electricity demand")
    plt.tight_layout()
    plt.show()
