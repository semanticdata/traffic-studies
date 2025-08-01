"""
Traffic data transformation and enrichment utilities.

This module handles data transformations specific to traffic analysis,
including speed compliance calculations, data enrichment, and derived metrics.
"""

from typing import Any, Dict

import pandas as pd


def calculate_speed_compliance(df: pd.DataFrame, structure: Dict[str, Any], speed_limit: int) -> pd.DataFrame:
    """Calculate speed compliance for both directions and add compliance columns to DataFrame."""
    # Get speed columns for both directions
    dir1_speed_cols = structure["dir1_speed_cols"]
    dir2_speed_cols = structure["dir2_speed_cols"]

    # Initialize compliance columns for direction 1
    df["Dir1_Compliant"] = 0
    df["Dir1_Non_Compliant"] = 0

    for col in dir1_speed_cols:
        if col in df.columns:
            try:
                # Extract speed from column name
                speed_part = col.split("MPH")[0].strip()
                if "+" in speed_part:
                    # Handle "45+" format - use the number as-is
                    speed = float(speed_part.replace("+", "").strip())
                else:
                    # Handle "25-29" format - use lower bound
                    speed = float(speed_part.split("-")[0].strip())

                # Add vehicle counts to appropriate compliance category
                if speed <= speed_limit:
                    df["Dir1_Compliant"] += df[col]
                else:
                    df["Dir1_Non_Compliant"] += df[col]
            except (ValueError, IndexError):
                # Skip columns that don't have valid speed format
                continue

    # Initialize compliance columns for direction 2
    df["Dir2_Compliant"] = 0
    df["Dir2_Non_Compliant"] = 0

    for col in dir2_speed_cols:
        if col in df.columns:
            try:
                # Extract speed from column name
                speed_part = col.split("MPH")[0].strip()
                if "+" in speed_part:
                    # Handle "45+" format - use the number as-is
                    speed = float(speed_part.replace("+", "").strip())
                else:
                    # Handle "25-29" format - use lower bound
                    speed = float(speed_part.split("-")[0].strip())

                # Add vehicle counts to appropriate compliance category
                if speed <= speed_limit:
                    df["Dir2_Compliant"] += df[col]
                else:
                    df["Dir2_Non_Compliant"] += df[col]
            except (ValueError, IndexError):
                # Skip columns that don't have valid speed format
                continue

    return df


def add_basic_enrichments(df: pd.DataFrame, structure: Dict[str, Any]) -> pd.DataFrame:
    """Add basic data enrichments like hour extraction and total calculations."""
    # Process datetime and add hour column
    if "Date/Time" in df.columns:
        df["Date/Time"] = pd.to_datetime(df["Date/Time"], errors="coerce")
        df["Hour"] = df["Date/Time"].dt.hour

    # Vectorized total calculation
    if structure["dir1_volume_col"] and structure["dir2_volume_col"]:
        df["Total"] = df[structure["dir1_volume_col"]] + df[structure["dir2_volume_col"]]

    return df


def filter_zero_traffic(df: pd.DataFrame, structure: Dict[str, Any]) -> tuple[pd.DataFrame, Dict[str, Any]]:
    """Filter out rows where both volume columns are 0 and return filtering statistics."""
    original_row_count = len(df)

    # Filter out rows where both volume columns are 0 (no traffic activity)
    dir1_col = structure["dir1_volume_col"]
    dir2_col = structure["dir2_volume_col"]

    if dir1_col and dir2_col:
        df = df[(df[dir1_col] > 0) | (df[dir2_col] > 0)]

    # Calculate filtering statistics
    filtered_row_count = len(df)
    filtering_stats = {
        "original_rows": original_row_count,
        "filtered_rows": filtered_row_count,
        "removed_rows": original_row_count - filtered_row_count,
        "removal_percentage": (
            ((original_row_count - filtered_row_count) / original_row_count) * 100 if original_row_count > 0 else 0
        ),
        "date_range": (
            {"start": df["Date/Time"].min(), "end": df["Date/Time"].max()}
            if len(df) > 0 and "Date/Time" in df.columns
            else None
        ),
        "active_hours": filtered_row_count,
        "inactive_hours": original_row_count - filtered_row_count,
    }

    return df, filtering_stats
