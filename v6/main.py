from config_defaults import DEFAULT_APPLIANCES, DEFAULT_CONFIG
from ramp_runner import deep_merge, plot_first_day, run_ramp, save_outputs
from user_overrides import USER_APPLIANCES, USER_CONFIG


def main() -> None:
    config = deep_merge(DEFAULT_CONFIG, USER_CONFIG)
    appliances = deep_merge(DEFAULT_APPLIANCES, USER_APPLIANCES)

    results = run_ramp(config, appliances)
    summary = results["input_summary"]

    print("=== INPUT SUMMARY ===")
    print(f"Real households: {summary['households_real']}")
    print(f"Electricity per household (kWh): {summary['electricity_per_household_kwh']}")
    print(f"Simulated households: {summary['households_simulated']}")
    print(f"Scaling factor: {summary['weight']:.2f}")
    print(f"Days simulated: {summary['num_days']}")

    print("\n=== RESULTS ===")
    print(f"Peak load (kW): {results['peak_kw']:.2f}")
    print(f"Annual energy (kWh): {results['annual_energy_kwh']:.2f}")
    print(f"Average daily energy (kWh): {results['average_daily_energy_kwh']:.2f}")

    if config.get("save_csv", True):
        output_path = save_outputs(results, config["output_csv"])
        print(f"\nSaved output to: {output_path}")

    if config.get("plot_first_day", True):
        plot_first_day(results["profile_kw"], rolling_window=config.get("rolling_window", 5))


if __name__ == "__main__":
    main()
