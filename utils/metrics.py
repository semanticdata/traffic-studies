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
    calculate_adt(df) -> float: Calculate Average Daily Traffic
    get_core_metrics(df, structure, speed_limit) -> Dict: Calculate all core metrics
"""

import os
from typing import Dict, List, Tuple

import pandas as pd
import streamlit as st


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
            # For compliance with new speed bins: ranges that include the speed limit are compliant
            # e.g., "26-30 MPH" includes 30 MPH, so it should be compliant for 30 MPH speed limit
            if "+" in speed_part:
                # For "45+" format, if the lower bound exceeds speed limit, it's non-compliant
                if speed > speed_limit:
                    pass  # non-compliant
                else:
                    compliant += count
            else:
                # For "26-30" format, extract upper bound and check if speed limit falls within range
                speed_range_parts = speed_part.split("-")
                if len(speed_range_parts) == 2:
                    lower_bound = float(speed_range_parts[0].strip())
                    upper_bound = float(speed_range_parts[1].strip())
                    # If speed limit falls within or below the range, it's compliant
                    if speed_limit >= lower_bound and speed_limit <= upper_bound:
                        compliant += count
                    elif upper_bound < speed_limit:
                        compliant += count
                    # else: upper_bound > speed_limit, so non-compliant
                else:
                    # Single number, use original logic
                    if speed <= speed_limit:
                        compliant += count
            total += count
        except (ValueError, IndexError):
            # Skip columns that don't have valid speed format
            continue
    return compliant, total


def load_mean_speed_from_speed_csv(structure: Dict[str, str]) -> float:
    """
    Load the mean speed from the pre-calculated values in Total-SPD.csv file.

    Uses the existing load_reference_speed_data function to properly handle
    malformed CSV headers (Total""Mean Speed -> Total, Mean Speed).

    Args:
        structure: Data structure containing reference file paths

    Returns:
        The average mean speed from the speed CSV, or 0 if unavailable
    """
    try:
        from utils.parsers.traffic_parser import load_reference_speed_data

        speed_file = structure.get("reference_files", {}).get("total_spd_file")
        if not speed_file or not os.path.exists(speed_file):
            return 0

        # Load the speed CSV file with proper header parsing
        speed_df = load_reference_speed_data(speed_file)

        if speed_df is not None and "Mean Speed" in speed_df.columns:
            valid_speeds = speed_df[speed_df["Mean Speed"] > 0]["Mean Speed"]
            if len(valid_speeds) > 0:
                return valid_speeds.mean()

        return 0
    except Exception:
        return 0


def load_85th_percentile_from_speed_csv(structure: Dict[str, str]) -> float:
    """
    Load the 85th percentile speed from the pre-calculated values in Total-SPD.csv file.

    Uses the existing load_reference_speed_data function to properly handle
    malformed CSV headers (Total""Mean Speed -> Total, Mean Speed).

    Args:
        structure: Data structure containing reference file paths

    Returns:
        The 85th percentile speed from the speed CSV, or 0 if unavailable
    """
    try:
        from utils.parsers.traffic_parser import load_reference_speed_data

        speed_file = structure.get("reference_files", {}).get("total_spd_file")
        if not speed_file or not os.path.exists(speed_file):
            return 0

        # Load the speed CSV file with proper header parsing
        speed_df = load_reference_speed_data(speed_file)

        if speed_df is not None and "85th Percentile" in speed_df.columns:
            valid_percentiles = speed_df[speed_df["85th Percentile"] > 0]["85th Percentile"]
            if len(valid_percentiles) > 0:
                # Return the average of hourly 85th percentile values
                return valid_percentiles.mean()

        return 0
    except Exception:
        return 0


def calculate_85th_percentile_speed(df: pd.DataFrame, speed_cols: List[str]) -> float:
    """
    Calculate the 85th percentile speed using proper interpolation within speed ranges.

    Note: This fallback method is used when pre-calculated values are not available.
    It may be inaccurate due to potential data corruption in speed range columns.
    """
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


def calculate_adt(df: pd.DataFrame) -> float:
    """
    Calculate the Average Daily Traffic (ADT) excluding partial days.

    Partial days (with less than 20 hours of data) are excluded to provide
    more accurate representation of typical daily traffic patterns.

    Args:
        df: DataFrame containing traffic data with a "Date/Time" and "Total" column.

    Returns:
        The calculated ADT value, or 0 if data is insufficient.
    """
    if df.empty:
        return 0

    # Group by date and calculate daily totals and hour counts
    df_copy = df.copy()
    df_copy["Date"] = pd.to_datetime(df_copy["Date/Time"]).dt.date

    daily_totals = df_copy.groupby("Date")["Total"].sum()
    daily_hour_counts = df_copy.groupby("Date").size()

    if daily_totals.empty:
        return 0

    # Filter to only include complete days (≥20 hours of data)
    # This excludes partial days that would skew the average
    complete_days = daily_totals[daily_hour_counts >= 20]

    if complete_days.empty:
        # Fall back to all days if no complete days found
        return daily_totals.mean()

    return complete_days.mean()


def _get_core_metrics_impl(df: pd.DataFrame, structure: Dict[str, str], speed_limit: int = None) -> Dict[str, float]:
    """
    Calculate all core metrics for the dashboard.

    Args:
        df: Filtered DataFrame containing traffic data
        structure: Dictionary containing data structure information
        speed_limit: Speed limit in MPH (uses posted_speed from structure if None)

    Returns:
        Dictionary containing all calculated metrics
    """
    # Use posted speed from structure if speed_limit not provided
    if speed_limit is None:
        speed_limit = structure.get("posted_speed", 30)
    # Basic counts
    total_vehicles = df["Total"].sum()
    dir1_volume = df[structure["dir1_volume_col"]].sum()
    dir2_volume = df[structure["dir2_volume_col"]].sum()

    # ADT Calculation
    adt = calculate_adt(df)

    # Speed calculations - prefer pre-calculated mean speed from speed CSV
    combined_avg_speed = load_mean_speed_from_speed_csv(structure)
    if combined_avg_speed == 0:
        # Fallback to calculation from speed range data (may be inaccurate due to corruption)
        combined_speed_cols = structure["dir1_speed_cols"] + structure["dir2_speed_cols"]
        combined_avg_speed = calculate_weighted_speed(df, combined_speed_cols)

    # Compliance calculations - use speed range data from the main CSV
    if "Dir1_Compliant" in df.columns and "Dir2_Compliant" in df.columns:
        # Use pre-calculated compliance columns if available
        total_compliant = df["Dir1_Compliant"].sum() + df["Dir2_Compliant"].sum()
        total_non_compliant = df["Dir1_Non_Compliant"].sum() + df["Dir2_Non_Compliant"].sum()
        total_speed_readings = total_compliant + total_non_compliant
    else:
        # Calculate compliance from speed range columns
        dir1_compliant, dir1_total = calculate_compliance(df, structure["dir1_speed_cols"], speed_limit)
        dir2_compliant, dir2_total = calculate_compliance(df, structure["dir2_speed_cols"], speed_limit)
        total_compliant = dir1_compliant + dir2_compliant
        total_speed_readings = dir1_total + dir2_total

    compliance_rate = (total_compliant / total_speed_readings * 100) if total_speed_readings > 0 else 0

    # 85th percentile speed - prefer pre-calculated values from speed CSV
    percentile_85th = load_85th_percentile_from_speed_csv(structure)
    if percentile_85th == 0:
        # Fallback to calculation from speed range data (may be inaccurate)
        combined_speed_cols = structure["dir1_speed_cols"] + structure["dir2_speed_cols"]
        percentile_85th = calculate_85th_percentile_speed(df, combined_speed_cols)

    # Peak hour analysis
    if not df.empty:
        hourly_volumes = df.groupby([df["Date/Time"].dt.date, df["Date/Time"].dt.hour])["Total"].sum()
        if not hourly_volumes.empty:
            peak_hour_idx = hourly_volumes.idxmax()
            peak_hour = peak_hour_idx[1]
            peak_vehicles = hourly_volumes.max()
        else:
            peak_hour = "N/A"
            peak_vehicles = 0
    else:
        peak_hour = "N/A"
        peak_vehicles = 0

    # Dominant direction
    dominant_direction = structure["dir1_name"] if dir1_volume > dir2_volume else structure["dir2_name"]
    dominant_pct = (
        max(dir1_volume, dir2_volume) / (dir1_volume + dir2_volume) * 100 if (dir1_volume + dir2_volume) > 0 else 0
    )

    return {
        "total_vehicles": total_vehicles,
        "adt": adt,
        "posted_speed": speed_limit,
        "combined_avg_speed": combined_avg_speed,
        "compliance_rate": compliance_rate,
        "percentile_85th": percentile_85th,
        "peak_hour": peak_hour,
        "peak_vehicles": peak_vehicles,
        "dominant_direction": dominant_direction,
        "dominant_pct": dominant_pct,
    }


@st.cache_data
def _get_core_metrics_cached(df: pd.DataFrame, structure: Dict[str, str], speed_limit: int = None) -> Dict[str, float]:
    """Cached version of get_core_metrics."""
    return _get_core_metrics_impl(df, structure, speed_limit)


def get_core_metrics(df: pd.DataFrame, structure: Dict[str, str], speed_limit: int = None) -> Dict[str, float]:
    """Calculate all core metrics for the dashboard."""
    # Check if we're in a test environment by looking for pytest in sys.modules
    import sys

    if "pytest" in sys.modules:
        # Don't use caching during tests to avoid cache interference
        return _get_core_metrics_impl(df, structure, speed_limit)
    else:
        # Use caching in normal runtime
        return _get_core_metrics_cached(df, structure, speed_limit)
