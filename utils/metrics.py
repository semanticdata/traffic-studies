"""
Metrics calculation utilities for Traffic Studies dashboard.

This module contains functions to calculate various traffic metrics and KPIs
from the processed traffic data.

Functions:
    calculate_weighted_speed(df, speed_cols) -> float: Calculate weighted average speed
    calculate_compliance(df, speed_cols, speed_limit) -> Tuple[int, int]: Calculate compliance counts
    calculate_85th_percentile_speed(df, speed_cols) -> float: Calculate 85th percentile speed
    calculate_phf(df) -> float: Calculate Peak Hour Factor
    count_high_speeders(df, speed_cols, speed_limit) -> int: Count high-speed violators
    get_core_metrics(df, structure, speed_limit) -> Dict: Calculate all core metrics
"""

from typing import Dict, List, Tuple

import numpy as np
import pandas as pd


def calculate_weighted_speed(df: pd.DataFrame, speed_cols: List[str]) -> float:
    """Calculate the weighted average speed."""
    total_count = 0
    weighted_sum = 0
    for col in speed_cols:
        speed = int(col.split("-")[0].strip())
        count = df[col].sum()
        weighted_sum += speed * count
        total_count += count
    return weighted_sum / total_count if total_count > 0 else 0


def calculate_compliance(df: pd.DataFrame, speed_cols: List[str], speed_limit: int = 30) -> Tuple[int, int]:
    """Calculate the number of compliant and non-compliant vehicles."""
    compliant = 0
    total = 0
    for col in speed_cols:
        speed = int(col.split("-")[0].strip())
        count = df[col].sum()
        if speed <= speed_limit:
            compliant += count
        total += count
    return compliant, total


def calculate_85th_percentile_speed(df: pd.DataFrame, speed_cols: List[str]) -> float:
    """Calculate the 85th percentile speed."""
    speeds = []
    for col in speed_cols:
        speed_range = col.split("MPH")[0].strip().split("-")
        lower = float(speed_range[0].strip())
        upper = float(speed_range[1].strip()) if len(speed_range) > 1 else lower
        mid_speed = (lower + upper) / 2
        count = df[col].sum()
        speeds.extend([mid_speed] * int(count))
    return np.percentile(speeds, 85) if speeds else 0


def calculate_phf(df: pd.DataFrame) -> float:
    """Calculate the Peak Hour Factor (PHF)."""
    hourly_volumes = df.groupby("Hour")["Total"].sum()
    peak_hour_volume = hourly_volumes.max()
    if peak_hour_volume == 0:
        return 0
    peak_hour_idx = hourly_volumes.idxmax()
    peak_15min = df[df["Hour"] == peak_hour_idx]["Total"].max() * 4
    return peak_hour_volume / peak_15min if peak_15min > 0 else 0


def count_high_speeders(df: pd.DataFrame, speed_cols: List[str], speed_limit: int = 30) -> int:
    """Count the number of high-speed violators (15+ mph over limit)."""
    high_speeders = 0
    for col in speed_cols:
        speed = int(col.split("-")[0].strip())
        if speed >= speed_limit + 15:
            high_speeders += df[col].sum()
    return high_speeders


def get_core_metrics(df: pd.DataFrame, structure: Dict[str, str], speed_limit: int = 30) -> Dict:
    """
    Calculate all core metrics for the dashboard.
    
    Args:
        df: Filtered DataFrame containing traffic data
        structure: Dictionary containing data structure information
        speed_limit: Speed limit in MPH
        
    Returns:
        Dictionary containing all calculated metrics
    """
    # Basic counts
    total_vehicles = df["Total"].sum()
    dir1_volume = df[structure["dir1_volume_col"]].sum()
    dir2_volume = df[structure["dir2_volume_col"]].sum()
    
    # Speed calculations
    dir1_avg_speed = calculate_weighted_speed(df, structure["dir1_speed_cols"])
    dir2_avg_speed = calculate_weighted_speed(df, structure["dir2_speed_cols"])
    combined_avg_speed = (dir1_avg_speed + dir2_avg_speed) / 2
    
    # Compliance calculations
    dir1_compliant, dir1_total = calculate_compliance(df, structure["dir1_speed_cols"], speed_limit)
    dir2_compliant, dir2_total = calculate_compliance(df, structure["dir2_speed_cols"], speed_limit)
    total_compliant = dir1_compliant + dir2_compliant
    total_speed_readings = dir1_total + dir2_total
    compliance_rate = (total_compliant / total_speed_readings * 100) if total_speed_readings > 0 else 0
    
    # 85th percentile speed
    dir1_85th = calculate_85th_percentile_speed(df, structure["dir1_speed_cols"])
    dir2_85th = calculate_85th_percentile_speed(df, structure["dir2_speed_cols"])
    percentile_85th = max(dir1_85th, dir2_85th)
    
    # Peak hour analysis
    hourly_volumes = df.groupby([df["Date/Time"].dt.date, df["Date/Time"].dt.hour])["Total"].sum()
    peak_hour_idx = hourly_volumes.idxmax()
    peak_hour = peak_hour_idx[1]
    peak_vehicles = hourly_volumes.max()
    
    # Dominant direction
    dominant_direction = structure["dir1_name"] if dir1_volume > dir2_volume else structure["dir2_name"]
    dominant_pct = (
        max(dir1_volume, dir2_volume) / (dir1_volume + dir2_volume) * 100 
        if (dir1_volume + dir2_volume) > 0 else 0
    )
    
    return {
        "total_vehicles": total_vehicles,
        "combined_avg_speed": combined_avg_speed,
        "compliance_rate": compliance_rate,
        "percentile_85th": percentile_85th,
        "peak_hour": peak_hour,
        "peak_vehicles": peak_vehicles,
        "dominant_direction": dominant_direction,
        "dominant_pct": dominant_pct,
    }