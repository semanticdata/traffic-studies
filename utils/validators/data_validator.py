"""
Data validation utilities for traffic data quality checks.

This module provides comprehensive validation functions to ensure data integrity
and quality for traffic analysis, including volume checks, temporal validation,
and cross-validation between related columns.
"""

from typing import Any, Dict

import pandas as pd


class DataValidationError(Exception):
    """Raised when data validation fails."""

    def __init__(self, message: str, validation_details: Dict[str, Any] = None) -> None:
        super().__init__(message)
        self.validation_details = validation_details or {}


def validate_traffic_data(df: pd.DataFrame, structure: Dict[str, Any]) -> Dict[str, Any]:
    """Comprehensive data validation with detailed reporting."""
    validation_results = {"is_valid": True, "warnings": [], "errors": [], "stats": {}}

    # Volume validation
    vol_cols = [structure["dir1_volume_col"], structure["dir2_volume_col"]]

    for col in vol_cols:
        if col in df.columns:
            # Check for negative values
            negative_count = (df[col] < 0).sum()
            if negative_count > 0:
                validation_results["errors"].append(f"Found {negative_count} negative values in {col}")
                validation_results["is_valid"] = False

            # Check for unrealistic maximum values (>1000 vehicles/hour)
            max_val = df[col].max()
            if max_val > 1000:
                validation_results["warnings"].append(
                    f"Unusually high traffic volume in {col}: {max_val} vehicles/hour"
                )

            # Store statistics
            validation_results["stats"][f"{col}_max"] = max_val
            validation_results["stats"][f"{col}_mean"] = df[col].mean()

    # Cross-check total vs sum of directional volumes
    if "Total" in df.columns and all(col in df.columns for col in vol_cols):
        total_diff = abs(df["Total"] - (df[vol_cols[0]] + df[vol_cols[1]])).sum()
        if total_diff > 0:
            validation_results["errors"].append(
                f"Total column doesn't match sum of directional volumes (difference: {total_diff})"
            )
            validation_results["is_valid"] = False

    # Speed validation
    speed_cols = structure["dir1_speed_cols"] + structure["dir2_speed_cols"]
    for col in speed_cols:
        if col in df.columns:
            # Check for negative values
            negative_count = (df[col] < 0).sum()
            if negative_count > 0:
                validation_results["errors"].append(f"Found {negative_count} negative values in speed column {col}")
                validation_results["is_valid"] = False

    # Temporal validation
    if "Date/Time" in df.columns:
        # Check for missing time periods (assuming hourly data)
        time_diffs = df["Date/Time"].diff().dropna()
        expected_diff = pd.Timedelta(hours=1)
        irregular_intervals = (time_diffs != expected_diff).sum()
        if irregular_intervals > 0:
            validation_results["warnings"].append(f"Found {irregular_intervals} irregular time intervals")

        # Store temporal statistics
        validation_results["stats"]["date_range"] = {
            "start": df["Date/Time"].min(),
            "end": df["Date/Time"].max(),
            "total_hours": len(df),
        }

    # Classification validation
    class_cols = structure["dir1_class_cols"] + structure["dir2_class_cols"]
    for col in class_cols:
        if col in df.columns:
            # Check for negative values
            negative_count = (df[col] < 0).sum()
            if negative_count > 0:
                validation_results["errors"].append(
                    f"Found {negative_count} negative values in classification column {col}"
                )
                validation_results["is_valid"] = False

    return validation_results
