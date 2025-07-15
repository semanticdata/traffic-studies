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
    """Calculate the weighted average speed using midpoint of speed ranges."""
    total_count = 0
    weighted_sum = 0
    for col in speed_cols:
        try:
            # Extract speed from column name, handle formats like "25-29 MPH" and "45+ MPH"
            speed_part = col.split("MPH")[0].strip()
            if "+" in speed_part:
                # Handle "45+" format - use the number plus 2.5 mph as estimate
                speed = float(speed_part.replace("+", "").strip()) + 2.5
            else:
                # Handle "25-29" format - use midpoint of range
                speed_range = speed_part.split("-")
                lower = float(speed_range[0].strip())
                upper = float(speed_range[1].strip()) if len(speed_range) > 1 else lower
                speed = (lower + upper) / 2

            count = df[col].sum()
            weighted_sum += speed * count
            total_count += count
        except (ValueError, IndexError):
            # Skip columns that don't have valid speed format
            continue
    return weighted_sum / total_count if total_count > 0 else 0


def calculate_compliance(df: pd.DataFrame, speed_cols: List[str], speed_limit: int = 30) -> Tuple[int, int]:
    """Calculate the number of compliant and non-compliant vehicles."""
    compliant = 0
    total = 0
    for col in speed_cols:
        try:
            # Extract speed from column name, handle formats like "25-29 MPH" and "45+ MPH"
            speed_part = col.split("MPH")[0].strip()
            if "+" in speed_part:
                # Handle "45+" format - use the number as-is
                speed = float(speed_part.replace("+", "").strip())
            else:
                # Handle "25-29" format - use lower bound
                speed = float(speed_part.split("-")[0].strip())

            count = df[col].sum()
            if speed <= speed_limit:
                compliant += count
            total += count
        except (ValueError, IndexError):
            # Skip columns that don't have valid speed format
            continue
    return compliant, total


def calculate_85th_percentile_speed(df: pd.DataFrame, speed_cols: List[str]) -> float:
    """Calculate the 85th percentile speed using proper interpolation within speed ranges."""
    if not speed_cols:
        return 0
    
    # Build cumulative distribution with proper speed ranges
    speed_ranges = []
    for col in speed_cols:
        try:
            speed_part = col.split("MPH")[0].strip()
            if "+" in speed_part:
                # Handle "45+" format - use the number plus 5 as upper bound
                lower = float(speed_part.replace("+", "").strip())
                upper = lower + 5  # Assume +5 mph range for "+" speeds
            else:
                # Handle "25-29" format
                speed_range = speed_part.split("-")
                lower = float(speed_range[0].strip())
                upper = float(speed_range[1].strip()) if len(speed_range) > 1 else lower

            count = df[col].sum()
            if count > 0:
                speed_ranges.append((lower, upper, count))
        except (ValueError, IndexError):
            # Skip columns that don't have valid speed format
            continue
    
    if not speed_ranges:
        return 0
    
    # Sort by lower bound of speed range
    speed_ranges.sort()
    
    # Calculate total vehicles and 85th percentile target
    total_vehicles = sum(count for _, _, count in speed_ranges)
    if total_vehicles == 0:
        return 0
    
    target_85th = total_vehicles * 0.85
    
    # Find the speed range containing the 85th percentile
    cumulative = 0
    for lower, upper, count in speed_ranges:
        if cumulative + count >= target_85th:
            # The 85th percentile falls in this range
            # Calculate position within the range
            vehicles_needed = target_85th - cumulative
            position_in_range = vehicles_needed / count if count > 0 else 0
            
            # Linear interpolation within the range
            percentile_speed = lower + (position_in_range * (upper - lower))
            return percentile_speed
        
        cumulative += count
    
    # If we get here, return the upper bound of the highest range
    return speed_ranges[-1][1] if speed_ranges else 0


def calculate_phf(df: pd.DataFrame) -> float:
    """
    Calculate the Peak Hour Factor (PHF).
    
    Note: PHF requires 15-minute interval data for proper calculation.
    Since our data is hourly, we cannot calculate traditional PHF.
    This function returns 0 to indicate PHF is not applicable.
    """
    # PHF = Peak Hour Volume / (Peak 15-minute flow rate * 4)
    # This requires sub-hourly data which we don't have
    return 0.0


def count_high_speeders(df: pd.DataFrame, speed_cols: List[str], speed_limit: int = 30) -> int:
    """Count the number of high-speed violators (15+ mph over limit)."""
    high_speeders = 0
    for col in speed_cols:
        try:
            # Extract speed from column name, handle formats like "25-29 MPH" and "45+ MPH"
            speed_part = col.split("MPH")[0].strip()
            if "+" in speed_part:
                # Handle "45+" format - use the number as-is
                speed = float(speed_part.replace("+", "").strip())
            else:
                # Handle "25-29" format - use lower bound
                speed = float(speed_part.split("-")[0].strip())

            if speed >= speed_limit + 15:
                high_speeders += df[col].sum()
        except (ValueError, IndexError):
            # Skip columns that don't have valid speed format
            continue
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

    # Speed calculations - use true weighted average across both directions
    combined_speed_cols = structure["dir1_speed_cols"] + structure["dir2_speed_cols"]
    combined_avg_speed = calculate_weighted_speed(df, combined_speed_cols)

    # Compliance calculations
    dir1_compliant, dir1_total = calculate_compliance(df, structure["dir1_speed_cols"], speed_limit)
    dir2_compliant, dir2_total = calculate_compliance(df, structure["dir2_speed_cols"], speed_limit)
    total_compliant = dir1_compliant + dir2_compliant
    total_speed_readings = dir1_total + dir2_total
    compliance_rate = (total_compliant / total_speed_readings * 100) if total_speed_readings > 0 else 0

    # 85th percentile speed - combine both directions for accurate calculation
    combined_speed_cols = structure["dir1_speed_cols"] + structure["dir2_speed_cols"]
    percentile_85th = calculate_85th_percentile_speed(df, combined_speed_cols)

    # Peak hour analysis
    hourly_volumes = df.groupby([df["Date/Time"].dt.date, df["Date/Time"].dt.hour])["Total"].sum()
    peak_hour_idx = hourly_volumes.idxmax()
    peak_hour = peak_hour_idx[1]
    peak_vehicles = hourly_volumes.max()

    # Dominant direction
    dominant_direction = structure["dir1_name"] if dir1_volume > dir2_volume else structure["dir2_name"]
    dominant_pct = (
        max(dir1_volume, dir2_volume) / (dir1_volume + dir2_volume) * 100 if (dir1_volume + dir2_volume) > 0 else 0
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
