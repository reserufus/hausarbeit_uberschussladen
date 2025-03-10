# charging simulation using solarlog data

Simulation for the four described charging algorithms using data from solarlog.

Adjust file `config.json`:
```
{
    "daily_usage": "Daily energy requirement to be charged, measured in watt-hours (Wh).",
    "min_soc": "Minimum state of charge (SoC) percentage that the vehicle battery must reach by the end time.",
    "max_soc": "Maximum state of charge (SoC) percentage; charging stops when this level is reached.",
    "capacity": "Total battery capacity of the vehicle, expressed in watt-hours (Wh).",
    "start": "Start time of the charging process, formatted as 'HH:MM:SS' (e.g., '08:00:00').",
    "weekend_start": "Specific start time for charging on weekends (Saturday and Sunday), formatted as 'HH:MM:SS'.",
    "end": "End time of the charging process, formatted as 'HH:MM:SS'.",
    "weekend_end": "End time of the charging process on weekend days (Saturday and Sunday), formatted as 'HH:MM:SS'.",
    "max_charging_speed": "Maximum charging power the vehicle can accept, measured in watts (W).",
    "preset_charging_speed": "Predefined charging power used for scheduled charging, measured in watts (W).",
    "preset_start_time": "Start time for preset charging, formatted as 'HH:MM:SS'.",
    "preset_end_time": "End time for preset charging, formatted as 'HH:MM:SS'.",
    "calls_per_hour": "Frequency of algorithm execution per hour (e.g., 12 calls per hour for 5-minute intervals).",
    "starting_soc": "Initial state of charge (SoC) percentage of the vehicle battery at the start of the simulation.",
    "start_date": "Start date of the simulation, formatted as 'YYYY-MM-DD' (e.g., '2024-01-01'); data must be available for this date.",
    "end_date": "End date of the simulation, formatted as 'YYYY-MM-DD'; data must be available up to this date.",
    "surplus_charging_delayed": "Flag to use data from the previous interval for surplus charging algorithms, simulating component delays.",
    "minimum_charge_speed": "Minimum charging power the vehicle can accept, measured in watts (W).",
    "charge_step_size": "Increment by which charging power can be adjusted, measured in watts (W).",
    "step_mode": "Method for adjusting charging speed to the nearest step: 'round_down' (rounds down to the nearest step), 'round_up' (rounds up to the nearest step), or 'balanced' (rounds to the closest step)."
}
``` 

Then run

```
python solarlog.py data --first 20241225 --last 20241226 --datafile mydata.csv --config config.json
```

Find data in file `mydata.csv`.
