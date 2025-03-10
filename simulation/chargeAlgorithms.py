from datetime import time
import math

def round_up_to_charging_speed(surplus, step_size, min_speed):
    return max(math.ceil(max(surplus, min_speed) / step_size) * step_size, min_speed)

def round_down_to_charging_speed(surplus, step_size, min_speed):
    rounded_value = (surplus // step_size) * step_size
    return rounded_value if rounded_value >= min_speed else 0

def round_to_charging_speed(surplus, step_size, min_speed):
    up = round_up_to_charging_speed(surplus, step_size, min_speed)
    down = round_down_to_charging_speed(surplus, step_size, min_speed)
    return up if abs(up - surplus) < abs(down - surplus) else down

def round_to_step_size(surplus, step_size, min_speed, charge_mode):
    rounding_functions = {
        "round_down": round_down_to_charging_speed,
        "round_up": round_up_to_charging_speed,
        "balanced": round_to_charging_speed
    }
    return rounding_functions.get(charge_mode, lambda x, y, z: x)(surplus, step_size, min_speed)

class BaseAlgorithm:
    def step(self, time_left, current_charge, current_time, solar_output, consumption):
        raise NotImplementedError("Subclasses must implement step method")

class UncontrolledCharging(BaseAlgorithm):
    def __init__(self, max_charging_speed, calls_per_hour, maximum_charge):
        self.max_charging_speed = max_charging_speed
        self.calls_per_hour = calls_per_hour
        self.maximum_charge = maximum_charge

    def step(self, time_left, current_charge, current_time, solar_output, consumption):
        max_charge_in_interval = self.max_charging_speed / self.calls_per_hour
        if current_charge >= self.maximum_charge:
            return 0
        remaining_charge = self.maximum_charge - current_charge
        return min(remaining_charge, max_charge_in_interval) * self.calls_per_hour

class PresetCharging(BaseAlgorithm):
    def __init__(self, calls_per_hour, maximum_charge, preset_charging_speed, preset_start_time, preset_end_time):
        self.calls_per_hour = calls_per_hour
        self.maximum_charge = maximum_charge
        self.preset_charging_speed = preset_charging_speed
        self.start_time = preset_start_time
        self.end_time = preset_end_time

    def step(self, time_left, current_charge, current_time, solar_output, consumption):
        if current_time < self.start_time or current_time > self.end_time or current_charge >= self.maximum_charge:
            return 0
        max_charge_in_interval = self.preset_charging_speed / self.calls_per_hour
        remaining_charge = self.maximum_charge - current_charge
        return min(remaining_charge, max_charge_in_interval) * self.calls_per_hour

class SurplusChargingBase(BaseAlgorithm):
    def __init__(self, max_charging_speed, calls_per_hour, minimum_charge, maximum_charge, delayed, min_speed, step_size, charge_mode):
        self.max_charging_speed = max_charging_speed
        self.calls_per_hour = calls_per_hour
        self.minimum_charge = minimum_charge
        self.maximum_charge = maximum_charge
        self.delayed = delayed
        self.min_speed = min_speed
        self.step_size = step_size
        self.charge_mode = charge_mode
        self.last_surplus = 0

    def calculate_surplus(self, solar_output, consumption):
        surplus = self.last_surplus if self.delayed else (solar_output - consumption)
        self.last_surplus = solar_output - consumption
        return surplus

    def charge_to_minimum(self, time_left, current_charge):
        required_hours = (self.minimum_charge - current_charge) / self.max_charging_speed
        if time_left <= required_hours * 60:
            max_charge_in_interval = self.max_charging_speed / self.calls_per_hour
            remaining_charge = max(self.maximum_charge - current_charge, 0)
            return min(remaining_charge, max_charge_in_interval) * self.calls_per_hour
        return None

    def charge_surplus(self, surplus, current_charge):
        if surplus > 0:
            charge_in_interval = surplus / self.calls_per_hour
            remaining_charge = self.maximum_charge - current_charge
            if remaining_charge < charge_in_interval:
                return remaining_charge * self.calls_per_hour
            rounded_surplus = round_to_step_size(surplus, self.step_size, self.min_speed, self.charge_mode)
            return min(rounded_surplus, self.max_charging_speed)
        return 0

class SurplusChargingAllInformation(SurplusChargingBase):
    def step(self, time_left, current_charge, current_time, solar_output, consumption):
        if current_charge >= self.maximum_charge:
            return 0
        surplus = self.calculate_surplus(solar_output, consumption)
        charge_rate = self.charge_to_minimum(time_left, current_charge)
        return charge_rate if charge_rate is not None else self.charge_surplus(surplus, current_charge)

class SurplusChargingNoSocInformation(SurplusChargingBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.minimum_charge_set = False

    def step(self, time_left, current_charge, current_time, solar_output, consumption):
        if self.minimum_charge_set == False:
            self.minimum_charge = min(current_charge + self.minimum_charge, self.maximum_charge)
            self.minimum_charge_set = True
        if current_charge >= self.maximum_charge:
            return 0
        surplus = self.calculate_surplus(solar_output, consumption)
        charge_rate = self.charge_to_minimum(time_left, current_charge)
        return charge_rate if charge_rate is not None else self.charge_surplus(surplus, current_charge)
