"""
Visualization utilities for Traffic Studies dashboard.

This module contains functions to create various charts and visualizations for
traffic data analysis. All functions return matplotlib Figure objects that can
be displayed in the Streamlit dashboard.

Functions:
    plot_traffic_volume(filtered_df, structure) -> plt.Figure: Hourly volume charts
    plot_speed_distribution(filtered_df, structure) -> plt.Figure: Speed range analysis
    plot_speed_compliance(filtered_df, structure, speed_limit=30) -> plt.Figure: Compliance charts
    plot_temporal_patterns(filtered_df, structure) -> plt.Figure: Daily/weekly patterns
    plot_speed_violation_severity(filtered_df, structure, speed_limit=30) -> Optional[plt.Figure]: Violation analysis
    plot_vehicle_classification_distribution(filtered_df, structure) -> plt.Figure: Vehicle class charts
"""

from typing import Dict, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def plot_traffic_volume(filtered_df: pd.DataFrame, structure: Dict[str, str]) -> plt.Figure:
    """Create traffic volume visualizations."""
    hourly_volumes = (
        filtered_df.groupby("Hour")
        .agg({structure["dir1_volume_col"]: "mean", structure["dir2_volume_col"]: "mean"})
        .reset_index()
    )

    fig1, ax1 = plt.subplots(figsize=(15, 8))
    ax1.bar(
        hourly_volumes["Hour"],
        hourly_volumes[structure["dir1_volume_col"]],
        label=structure["dir1_name"],
        alpha=0.7,
        color="skyblue",
    )
    ax1.bar(
        hourly_volumes["Hour"],
        hourly_volumes[structure["dir2_volume_col"]],
        bottom=hourly_volumes[structure["dir1_volume_col"]],
        label=structure["dir2_name"],
        alpha=0.7,
        color="lightgreen",
    )
    ax1.set_title("Hourly Traffic Volume Distribution", pad=20, fontsize=14)
    ax1.set_xlabel("Hour of Day", fontsize=12)
    ax1.set_ylabel("Average Vehicles per Hour", fontsize=12)
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(range(24))
    return fig1


def plot_speed_distribution(filtered_df: pd.DataFrame, structure: Dict[str, str]) -> plt.Figure:
    """Create speed distribution visualizations."""
    dir1_speeds = filtered_df[structure["dir1_speed_cols"]].mean()
    dir2_speeds = filtered_df[structure["dir2_speed_cols"]].mean()

    fig2, (ax2a, ax2b) = plt.subplots(2, 1, figsize=(15, 12))

    # Direction 1 speeds
    sns.barplot(
        x=[col.split("-")[0].strip() for col in structure["dir1_speed_cols"]],
        y=dir1_speeds,
        color="skyblue",
        ax=ax2a,
    )
    ax2a.set_title(f"{structure['dir1_name']} Speed Distribution")
    ax2a.set_xlabel("Speed Range (MPH)")
    ax2a.set_ylabel("Average Vehicle Count")
    ax2a.tick_params(axis="x", rotation=45)

    # Direction 2 speeds
    sns.barplot(
        x=[col.split("-")[0].strip() for col in structure["dir2_speed_cols"]],
        y=dir2_speeds,
        color="lightgreen",
        ax=ax2b,
    )
    ax2b.set_title(f"{structure['dir2_name']} Speed Distribution")
    ax2b.set_xlabel("Speed Range (MPH)")
    ax2b.set_ylabel("Average Vehicle Count")
    ax2b.tick_params(axis="x", rotation=45)

    plt.tight_layout()
    return fig2


def plot_speed_compliance(filtered_df: pd.DataFrame, structure: Dict[str, str], speed_limit: int = 30) -> plt.Figure:
    """Create speed compliance visualizations."""
    # Calculate compliance directly from speed columns
    dir1_compliant = (
        filtered_df[structure["dir1_speed_cols"]]
        .apply(
            lambda row: sum(int(col.split("-")[0].strip()) <= speed_limit for col, count in row.items() if count > 0),
            axis=1,
        )
        .sum()
    )

    dir1_non_compliant = (
        filtered_df[structure["dir1_speed_cols"]]
        .apply(
            lambda row: sum(int(col.split("-")[0].strip()) > speed_limit for col, count in row.items() if count > 0),
            axis=1,
        )
        .sum()
    )

    dir2_compliant = (
        filtered_df[structure["dir2_speed_cols"]]
        .apply(
            lambda row: sum(int(col.split("-")[0].strip()) <= speed_limit for col, count in row.items() if count > 0),
            axis=1,
        )
        .sum()
    )

    dir2_non_compliant = (
        filtered_df[structure["dir2_speed_cols"]]
        .apply(
            lambda row: sum(int(col.split("-")[0].strip()) > speed_limit for col, count in row.items() if count > 0),
            axis=1,
        )
        .sum()
    )

    compliance_data = pd.DataFrame(
        {
            "Direction": [
                structure["dir1_name"],
                structure["dir1_name"],
                structure["dir2_name"],
                structure["dir2_name"],
            ],
            "Compliance": ["Compliant", "Non-Compliant", "Compliant", "Non-Compliant"],
            "Count": [
                dir1_compliant,
                dir1_non_compliant,
                dir2_compliant,
                dir2_non_compliant,
            ],
        }
    )

    fig3, ax3 = plt.subplots(figsize=(15, 8))
    sns.barplot(
        data=compliance_data,
        x="Direction",
        y="Count",
        hue="Compliance",
        palette=["lightgreen", "salmon"],
        ax=ax3,
    )
    ax3.set_title("Speed Compliance Analysis by Direction", pad=20, fontsize=14)
    ax3.set_xlabel("Direction", fontsize=12)
    ax3.set_ylabel("Vehicle Count", fontsize=12)
    ax3.legend(fontsize=10)
    ax3.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig3


def plot_temporal_patterns(filtered_df: pd.DataFrame, structure: Dict[str, str]) -> plt.Figure:
    """Create visualizations for temporal traffic patterns."""
    # Add day of week column using Date/Time instead of Date
    filtered_df["DayOfWeek"] = filtered_df["Date/Time"].dt.day_name()

    # Daily patterns
    daily_volumes = (
        filtered_df.groupby("DayOfWeek")
        .agg({structure["dir1_volume_col"]: "sum", structure["dir2_volume_col"]: "sum"})
        .reindex(
            [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ]
        )
    )

    fig, ax = plt.subplots(figsize=(15, 8))
    daily_volumes.plot(kind="bar", ax=ax)
    ax.set_title("Daily Traffic Volume Patterns", pad=20, fontsize=14)
    ax.set_xlabel("Day of Week", fontsize=12)
    ax.set_ylabel("Total Vehicle Count", fontsize=12)
    ax.legend(labels=[structure["dir1_name"], structure["dir2_name"]], fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


def plot_speed_violation_severity(
    filtered_df: pd.DataFrame, structure: Dict[str, str], speed_limit: int = 30
) -> Optional[plt.Figure]:
    """Create visualization for speed violation severity."""
    # Calculate speed ranges and their frequencies
    speed_ranges = {
        "0-5 mph over": (0, 5),
        "5-10 mph over": (5, 10),
        "10-15 mph over": (10, 15),
        "15+ mph over": (15, float("inf")),
    }

    violation_data = []
    for direction, speed_cols in [
        (structure["dir1_name"], structure["dir1_speed_cols"]),
        (structure["dir2_name"], structure["dir2_speed_cols"]),
    ]:
        for col in speed_cols:
            # Extract the lower speed bound from column name (e.g., "35-39 MPH" -> 35)
            speed = int(col.split("-")[0].strip())
            if speed > speed_limit:
                over_limit = speed - speed_limit
                for range_name, (min_over, max_over) in speed_ranges.items():
                    if min_over <= over_limit < max_over:
                        violation_data.append(
                            {
                                "Direction": direction,
                                "Violation Range": range_name,
                                # Changed from mean() to sum()
                                "Count": filtered_df[col].sum(),
                            }
                        )

    violation_df = pd.DataFrame(violation_data)

    # Only create visualization if there are violations
    if not violation_df.empty:
        fig, ax = plt.subplots(figsize=(15, 8))
        sns.barplot(
            data=violation_df,
            x="Direction",
            y="Count",
            hue="Violation Range",
            palette="YlOrRd",
            ax=ax,
        )
        ax.set_title("Speed Violation Severity Analysis", pad=20, fontsize=14)
        ax.set_xlabel("Direction", fontsize=12)
        ax.set_ylabel("Number of Vehicles", fontsize=12)
        ax.legend(title="Speed Over Limit", fontsize=10)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig
    else:
        return None


def plot_speeding_by_hour(filtered_df: pd.DataFrame, structure: Dict[str, str], speed_limit: int = 30) -> plt.Figure:
    """
    Create a visualization showing when speeding occurs throughout the day.

    Args:
        filtered_df: Filtered DataFrame containing the traffic data
        structure: Dictionary containing data structure information
        speed_limit: Speed limit in MPH (default: 30)

    Returns:
        matplotlib.figure.Figure: Figure containing the speeding by hour visualization
    """
    # Create a copy to avoid modifying the original DataFrame
    df = filtered_df.copy()

    # Get speed columns for both directions
    speed_cols_dir1 = structure["dir1_speed_cols"]
    speed_cols_dir2 = structure["dir2_speed_cols"]

    # Initialize DataFrames to store speeding data by hour
    hours = range(24)
    dir1_speeding = pd.Series(0, index=hours, dtype=float)
    dir2_speeding = pd.Series(0, index=hours, dtype=float)
    dir1_total = pd.Series(0, index=hours, dtype=float)
    dir2_total = pd.Series(0, index=hours, dtype=float)

    # Process each speed column for direction 1
    for col in speed_cols_dir1:
        # Extract speed range (e.g., '30-35' -> 30)
        try:
            speed = int(col.split("-")[0].strip().split()[0])
            is_speeding = speed > speed_limit

            # Add to appropriate series based on whether it's speeding
            for hour in hours:
                hour_data = df[df["Hour"] == hour][col].sum()
                dir1_total[hour] += hour_data
                if is_speeding:
                    dir1_speeding[hour] += hour_data
        except (ValueError, IndexError):
            continue

    # Process each speed column for direction 2
    for col in speed_cols_dir2:
        try:
            speed = int(col.split("-")[0].strip().split()[0])
            is_speeding = speed > speed_limit

            for hour in hours:
                hour_data = df[df["Hour"] == hour][col].sum()
                dir2_total[hour] += hour_data
                if is_speeding:
                    dir2_speeding[hour] += hour_data
        except (ValueError, IndexError):
            continue

    # Calculate percentage of speeding vehicles by hour
    dir1_percent = (dir1_speeding / dir1_total.replace(0, np.nan)) * 100
    dir2_percent = (dir2_speeding / dir2_total.replace(0, np.nan)) * 100

    # Create the figure
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))

    # Plot direction 1
    ax1.bar(hours, dir1_total, color="lightgray", alpha=0.5, label="Total Vehicles")
    ax1_twin = ax1.twinx()
    ax1_twin.plot(hours, dir1_percent, "r-", marker="o", label="% Speeding")

    ax1.set_title(f"{structure['dir1_name']} - Speeding by Hour of Day", pad=20, fontsize=14)
    ax1.set_xlabel("Hour of Day", fontsize=12)
    ax1.set_ylabel("Number of Vehicles", fontsize=12)
    ax1_twin.set_ylabel("% of Vehicles Speeding", fontsize=12, color="r")
    ax1_twin.tick_params(axis="y", labelcolor="r")
    ax1.set_xticks(hours)
    ax1.grid(True, alpha=0.3)

    # Add legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax1_twin.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

    # Plot direction 2
    ax2.bar(hours, dir2_total, color="lightgray", alpha=0.5, label="Total Vehicles")
    ax2_twin = ax2.twinx()
    ax2_twin.plot(hours, dir2_percent, "r-", marker="o", label="% Speeding")

    ax2.set_title(f"{structure['dir2_name']} - Speeding by Hour of Day", pad=20, fontsize=14)
    ax2.set_xlabel("Hour of Day", fontsize=12)
    ax2.set_ylabel("Number of Vehicles", fontsize=12)
    ax2_twin.set_ylabel("% of Vehicles Speeding", fontsize=12, color="r")
    ax2_twin.tick_params(axis="y", labelcolor="r")
    ax2.set_xticks(hours)
    ax2.grid(True, alpha=0.3)

    # Add legend
    lines1, labels1 = ax2.get_legend_handles_labels()
    lines2, labels2 = ax2_twin.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

    plt.tight_layout()
    return fig


def plot_vehicle_classification_distribution(filtered_df: pd.DataFrame, structure: Dict[str, str]) -> plt.Figure:
    """Create vehicle classification distribution visualizations."""
    class_counts_dir1 = [filtered_df[col].sum() for col in structure["dir1_class_cols"]]
    class_counts_dir2 = [filtered_df[col].sum() for col in structure["dir2_class_cols"]]

    class_data = pd.DataFrame(
        {
            "Vehicle Type": [
                "Class 1 - Motorcycles",
                "Class 2 - Passenger Cars",
                "Class 3 - Pickups, Vans",
                "Class 4 - Buses",
                "Class 5 - 2 Axles, 6 Tires",
                "Class 6 - 3 Axles",
            ],
            structure["dir1_name"]: class_counts_dir1,
            structure["dir2_name"]: class_counts_dir2,
        }
    )

    fig, ax = plt.subplots(figsize=(15, 8))
    class_data.plot(kind="bar", x="Vehicle Type", ax=ax)
    ax.set_title("Vehicle Classification Distribution", pad=20, fontsize=14)
    ax.set_xlabel("Vehicle Type", fontsize=12)
    ax.set_ylabel("Count", fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig
