"""Scenario accounting for the exploratory ULEZ notebook.

The notebook supplies its original emission-factor function. Values remain model
units: this module fixes trip and scenario accounting, not coefficient calibration.
"""
from __future__ import annotations

import math
import pandas as pd


def travel_profile(distance_km, start_hour, speeds, emission_factor):
    """Integrate hourly speed and emissions while preserving the trip distance."""
    if not math.isfinite(distance_km) or distance_km < 0:
        raise ValueError("Distance must be finite and nonnegative")
    if len(speeds) != 24 or any(not math.isfinite(float(v)) or v <= 0 for v in speeds):
        raise ValueError("Expected 24 finite positive hourly speeds")
    remaining = float(distance_km)
    duration = emissions = 0.0
    hour = int(start_hour) % 24
    while remaining > 1e-12:
        speed = float(speeds[hour])
        segment = min(remaining, speed)
        factor = float(emission_factor(speed))
        if not math.isfinite(factor) or factor < 0:
            raise ValueError("Emission factors must be finite and nonnegative")
        emissions += factor * segment
        duration += segment / speed * 60
        remaining -= segment
        hour = (hour + 1) % 24
    return {"distance_km": float(distance_km), "duration_minutes": duration, "emissions": emissions}


def restriction_applies(rule, hour, diesel, exempt):
    """Preserve notebook rules: all day, hours 7–19, or hours 7–10/16–19.

    Hours are discrete: an inclusive hour 19 restriction ends at 20:00.
    """
    if rule not in range(1, 10):
        raise ValueError("Restriction rule must be between 1 and 9")
    group, vehicle_rule = divmod(rule - 1, 3)
    hour = int(hour) % 24
    active = group == 0 or (group == 1 and 7 <= hour <= 19) or (group == 2 and (7 <= hour <= 10 or 16 <= hour <= 19))
    vehicle_affected = vehicle_rule == 0 or (vehicle_rule == 1 and not exempt) or (vehicle_rule == 2 and diesel)
    return bool(active and vehicle_affected)


def trip_outcome(case, rule, hour, diesel, exempt, max_wait_hours=2):
    """Return mutually exclusive proceed, cancel, or delay status per scenario."""
    if max_wait_hours < 0:
        raise ValueError("Maximum wait must be nonnegative")
    if case == 5 or not restriction_applies(rule, hour, diesel, exempt):
        return "proceed", 0
    for delay in range(1, min(int(max_wait_hours), 24) + 1):
        if not restriction_applies(rule, hour + delay, diesel, exempt):
            return "delay", delay
    return "cancel", 0


def evaluate_scenarios(trips, speeds, emission_function, max_wait_hours=2):
    """Evaluate all 27 alternatives without mutating the baseline trip dataset."""
    detail = []
    summary = []
    baseline = []
    for _, trip in trips.iterrows():
        factor = lambda speed, t=trip: emission_function(t["euro_class"], speed, t["vehicle_category"])
        baseline.append(travel_profile(trip["distance_km"], trip["time2"], speeds, factor)["emissions"])
    baseline_total = sum(baseline)
    for area in range(1, 4):
        for rule in range(1, 10):
            scenario = []
            for position, (_, trip) in enumerate(trips.iterrows()):
                status, delay = trip_outcome(trip[f"Area {area}_case"], rule, trip["time2"], bool(trip["Diesel"]), bool(trip["Lux"]), max_wait_hours)
                if status == "cancel":
                    emissions = 0.0
                elif status == "proceed":
                    emissions = baseline[position]
                else:
                    factor = lambda speed, t=trip: emission_function(t["euro_class"], speed, t["vehicle_category"])
                    emissions = travel_profile(trip["distance_km"], trip["time2"] + delay, speeds, factor)["emissions"]
                scenario.append({"trip_id": position, "area": f"Area {area}", "rule": rule, "status": status, "delay_hours": delay, "baseline_emissions": baseline[position], "scenario_emissions": emissions})
            counts = {status: sum(row["status"] == status for row in scenario) for status in ("proceed", "cancel", "delay")}
            total = sum(row["scenario_emissions"] for row in scenario)
            summary.append({"area": f"Area {area}", "rule": rule, **counts, "baseline_emissions": baseline_total, "scenario_emissions": total, "emission_change": total - baseline_total})
            detail.extend(scenario)
    return pd.DataFrame(summary), pd.DataFrame(detail), baseline
