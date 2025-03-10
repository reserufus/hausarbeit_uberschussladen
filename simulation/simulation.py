from datetime import datetime, time, date
import json
import click
import pandas as pd
from pydantic import BaseModel
from typing import Dict

from chargeAlgorithms import BaseAlgorithm, UncontrolledCharging, PresetCharging, SurplusChargingAllInformation, SurplusChargingNoSocInformation

class Configuration(BaseModel):
    daily_usage: int
    min_soc: int
    max_soc: int
    capacity: int
    start: time
    weekend_start: time
    end: time
    weekend_end: time
    max_charging_speed: int
    preset_charging_speed: int
    preset_start_time: time
    preset_end_time: time
    calls_per_hour: int
    starting_soc: int
    start_date: date
    end_date: date
    surplus_charging_delayed: bool
    minimum_charge_speed: int
    charge_step_size: int
    step_mode: str

def load_config(config_path: str) -> Configuration:
    with open(config_path) as config_file:
        return Configuration(**json.load(config_file))

def calculate_remaining_minutes(current_time: time, end_time: time) -> float:
    date = datetime.today().date()
    dt1 = datetime.combine(date, current_time)
    dt2 = datetime.combine(date, end_time)
    return (dt2 - dt1).total_seconds() / 60

def create_simulators(config: Configuration) -> Dict[str, BaseAlgorithm]:
    min_charge = config.min_soc * config.capacity / 100
    max_charge = config.max_soc * config.capacity / 100
    common_params = {
        "max_charging_speed": config.max_charging_speed,
        "calls_per_hour": config.calls_per_hour,
        "maximum_charge": max_charge
    }
    surplus_params = {
        **common_params,
        "minimum_charge": min_charge,
        "delayed": config.surplus_charging_delayed,
        "min_speed": config.minimum_charge_speed,
        "step_size": config.charge_step_size,
        "charge_mode": config.step_mode
    }
    return {
        "uncontrolled": UncontrolledCharging(**common_params),
        "preset": PresetCharging(
            calls_per_hour=config.calls_per_hour,
            maximum_charge=max_charge,
            preset_charging_speed=config.preset_charging_speed,
            preset_start_time=config.preset_start_time,
            preset_end_time=config.preset_end_time
        ),
        "surplus_all": SurplusChargingAllInformation(**surplus_params),
        "surplus_no_soc": SurplusChargingNoSocInformation(**surplus_params)
    }

def process_day_data(day_data: pd.DataFrame, config: Configuration, simulators: Dict[str, BaseAlgorithm], current_charge: Dict[str, float]) -> list:
    results = []
    is_weekend = day_data.iloc[0]['time'].weekday() >= 5
    start_time = config.weekend_start if is_weekend else config.start
    end_time = config.weekend_end if is_weekend else config.end

    for _, row in day_data.iterrows():
        current_time = row['time'].time()
        if start_time <= current_time <= end_time:
            row_result = {'time': row['time'], 'surplus': max(row['output'] - row['consumption'], 0)}
            
            for name, simulator in simulators.items():
                charge_power = simulator.step(
                    calculate_remaining_minutes(current_time, config.end),
                    current_charge[name],
                    current_time,
                    row['output'],
                    row['consumption']
                )
                current_charge[name] += charge_power / config.calls_per_hour
                row_result[f'{name}_charging_power'] = charge_power
                row_result[f'{name}_charging_soc'] = (current_charge[name] / config.capacity) * 100
            
            results.append(row_result)

    return results

@click.group()
def cli():
    pass

@click.command()
@click.option("--datafile", default="data.csv", help="Data *.csv file")
@click.option("--configfile", default="config.json", help="JSON configuration file")
@click.option("--out", default="out.csv", help="Output *.csv file")
def simulation(datafile: str, configfile: str, out: str):
    config = load_config(configfile)
    df = pd.read_csv(datafile, parse_dates=['time'])

    df = df[(df['time'].dt.date >= pd.to_datetime(config.start_date).date()) & 
            (df['time'].dt.date <= pd.to_datetime(config.end_date).date())]

    if df.empty:
        print(f"No data available between {config.start_date} and {config.end_date}.")
        return
    
    df['date'] = df['time'].dt.date 
    results = []
    
    simulators = create_simulators(config)
    current_charge = {sim: config.capacity * config.starting_soc / 100 for sim in simulators}
    
    for _, day_data in df.groupby('date'):
        results.extend(process_day_data(day_data, config, simulators, current_charge))
        for sim in current_charge:
            current_charge[sim] -= config.daily_usage

    output_df = pd.DataFrame(results)
    output_df.to_csv(out, index=False)
    print(f"Simulation completed. Results saved in {out}")

cli.add_command(simulation)

if __name__ == '__main__':
    cli()
