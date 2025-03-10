# Charging Simulation Using Solarlog Data

This project simulates four distinct charging algorithms using Solarlog data to model vehicle charging behavior. The simulation output can then be analyzed to visualize charging curves and calculate associated costs.

## Configuration

Before running the simulation, configure the `config.json` file with the following parameters:

```
{
    "daily_usage": "Daily energy requirement for charging, in watt-hours (Wh).",
    "min_soc": "Minimum state of charge (SoC) percentage the battery must reach by the end time.",
    "max_soc": "Maximum SoC percentage; charging halts upon reaching this threshold.",
    "capacity": "Total battery capacity of the vehicle, in watt-hours (Wh).",
    "start": "Charging start time, in 'HH:MM:SS' format (e.g., '08:00:00').",
    "weekend_start": "Weekend-specific (Saturday/Sunday) charging start time, in 'HH:MM:SS' format.",
    "end": "Charging end time, in 'HH:MM:SS' format.",
    "weekend_end": "Weekend-specific (Saturday/Sunday) charging end time, in 'HH:MM:SS' format.",
    "max_charging_speed": "Maximum charging power supported by the vehicle, in watts (W).",
    "preset_charging_speed": "Fixed charging power for scheduled charging, in watts (W).",
    "preset_start_time": "Start time for preset charging, in 'HH:MM:SS' format.",
    "preset_end_time": "End time for preset charging, in 'HH:MM:SS' format.",
    "calls_per_hour": "Number of algorithm executions per hour (e.g., 12 for 5-minute intervals).",
    "starting_soc": "Initial SoC percentage of the battery at simulation start.",
    "start_date": "Simulation start date, in 'YYYY-MM-DD' format (e.g., '2024-01-01'); data must be available.",
    "end_date": "Simulation end date, in 'YYYY-MM-DD' format; data must be available through this date.",
    "surplus_charging_delayed": "Flag to use prior interval data for surplus charging, mimicking component delays.",
    "minimum_charge_speed": "Minimum charging power the vehicle accepts, in watts (W).",
    "charge_step_size": "Increment for adjusting charging power, in watts (W).",
    "step_mode": "Charging speed adjustment method: 'round_down' (to lower step), 'round_up' (to upper step), or 'balanced' (to nearest step)."
    "daily_usage": "Daily energy requirement for charging, in watt-hours (Wh).",
    "min_soc": "Minimum state of charge (SoC) percentage the battery must reach by the end time.",
    "max_soc": "Maximum SoC percentage; charging halts upon reaching this threshold.",
    "capacity": "Total battery capacity of the vehicle, in watt-hours (Wh).",
    "start": "Charging start time, in 'HH:MM:SS' format (e.g., '08:00:00').",
    "weekend_start": "Weekend-specific (Saturday/Sunday) charging start time, in 'HH:MM:SS' format.",
    "end": "Charging end time, in 'HH:MM:SS' format.",
    "weekend_end": "Weekend-specific (Saturday/Sunday) charging end time, in 'HH:MM:SS' format.",
    "max_charging_speed": "Maximum charging power supported by the vehicle, in watts (W).",
    "preset_charging_speed": "Fixed charging power for scheduled charging, in watts (W).",
    "preset_start_time": "Start time for preset charging, in 'HH:MM:SS' format.",
    "preset_end_time": "End time for preset charging, in 'HH:MM:SS' format.",
    "calls_per_hour": "Number of algorithm executions per hour (e.g., 12 for 5-minute intervals).",
    "starting_soc": "Initial SoC percentage of the battery at simulation start.",
    "start_date": "Simulation start date, in 'YYYY-MM-DD' format (e.g., '2024-01-01'); data must be available.",
    "end_date": "Simulation end date, in 'YYYY-MM-DD' format; data must be available through this date.",
    "surplus_charging_delayed": "Flag to use prior interval data for surplus charging, mimicking component delays.",
    "minimum_charge_speed": "Minimum charging power the vehicle accepts, in watts (W).",
    "charge_step_size": "Increment for adjusting charging power, in watts (W).",
    "step_mode": "Charging speed adjustment method: 'round_down' (to lower step), 'round_up' (to upper step), or 'balanced' (to nearest step)."
}
```

## Running the Simulation

First, ensure Solarlog data is retrieved using the `solarlog.py` script. Then, execute the simulation with:

```bash

## Running the Simulation

First, ensure Solarlog data is retrieved using the `solarlog.py` script. Then, execute the simulation with:

```bash
python simulation.py simulation --datafile entire_2024.csv --configfile config.json --out out.csv
```

This command generates a simulation output file, `out.csv`, containing the results for further analysis.

## Analyzing the Results
This command generates a simulation output file, `out.csv`, containing the results for further analysis.

## Analyzing the Results

The `evaluation.py` script processes the simulation output (`out.csv`) to visualize charging curves or compute costs. It supports two commands:
The `evaluation.py` script processes the simulation output (`out.csv`) to visualize charging curves or compute costs. It supports two commands:

### Plot Charging Curves
### Plot Charging Curves

To generate a charging curve diagram for a specific day, run:
To generate a charging curve diagram for a specific day, run:

```bash
```bash
python evaluation.py plot-charging-data --csv-file out.csv --selected-date 2024-07-12 --start-time 08:00 --end-time 23:00
```

This creates a Matplotlib plot of the charging curves for July 12, 2024, from 08:00 to 23:00.
This creates a Matplotlib plot of the charging curves for July 12, 2024, from 08:00 to 23:00.

### Calculate Charging Costs
### Calculate Charging Costs

To compute costs and energy metrics for the four algorithms, use:
To compute costs and energy metrics for the four algorithms, use:

```bash
python evaluation.py print-charging-costs --csv-file out.csv --solar-price 0.097 --grid-price 0.33
```bash
python evaluation.py print-charging-costs --csv-file out.csv --solar-price 0.097 --grid-price 0.33
```

This calculates costs assuming €0.097 per kWh for solar energy (e.g., feed-in tariff as opportunity cost) and €0.33 per kWh for grid energy, displaying the results in the console.