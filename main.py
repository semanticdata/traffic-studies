"""
Traffic Studies Dashboard - Main Application

A comprehensive traffic analysis dashboard for Crystal, Minnesota, built with Streamlit.
This application processes and visualizes traffic data collected from PicoCount 2500
traffic counters, providing detailed insights into traffic patterns, speed compliance,
and vehicle classifications.

Features:
- Interactive filtering by location, date range, and time periods
- 12+ key performance indicators and metrics
- Vehicle classification analysis (6 FHWA classes)
- Speed compliance monitoring and violation tracking
- Temporal traffic pattern analysis
- Multiple visualization formats (Matplotlib and Plotly)

Data Sources:
- PicoCount 2500 traffic counters
- TrafficViewer Pro software exports

Author: Miguel Pimentel
License: MIT
"""

from typing import Tuple

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from utils.data_loader import get_available_locations, load_data
from utils.visualizations import (
    plot_speed_compliance,
    plot_speed_distribution,
    plot_speed_violation_severity,
    plot_speeding_by_hour,
    plot_temporal_patterns,
    plot_traffic_volume,
    plot_vehicle_classification_distribution,
)


# Function to calculate weighted average speed
def calculate_weighted_speed(df: pd.DataFrame, speed_cols: list) -> float:
    """Calculate the weighted average speed."""
    total_count = 0
    weighted_sum = 0
    for col in speed_cols:
        speed = int(col.split("-")[0].strip())
        count = df[col].sum()
        weighted_sum += speed * count
        total_count += count
    return weighted_sum / total_count if total_count > 0 else 0


# Function to calculate compliance
def calculate_compliance(df: pd.DataFrame, speed_cols: list, speed_limit: int = 30) -> Tuple[int, int]:
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


# Function to calculate 85th percentile speed
def calculate_85th_percentile_speed(df: pd.DataFrame, speed_cols: list) -> float:
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


# Function to calculate peak hour factor (PHF)
def calculate_phf(df: pd.DataFrame) -> float:
    """Calculate the Peak Hour Factor (PHF)."""
    hourly_volumes = df.groupby("Hour")["Total"].sum()
    peak_hour_volume = hourly_volumes.max()
    if peak_hour_volume == 0:
        return 0
    peak_hour_idx = hourly_volumes.idxmax()
    peak_15min = df[df["Hour"] == peak_hour_idx]["Total"].max() * 4
    return peak_hour_volume / peak_15min if peak_15min > 0 else 0


# Function to count high-speed violators
def count_high_speeders(df: pd.DataFrame, speed_cols: list, speed_limit: int = 30) -> int:
    """Count the number of high-speed violators (15+ mph over limit)."""
    high_speeders = 0
    for col in speed_cols:
        speed = int(col.split("-")[0].strip())
        if speed >= speed_limit + 15:
            high_speeders += df[col].sum()
    return high_speeders


# Set page config
st.set_page_config(page_title="Traffic Analysis Dashboard", page_icon="🚗", layout="wide")

# Sidebar for filters
st.sidebar.title("Filters")
locations = get_available_locations()

if not locations:
    st.sidebar.error("❌ No data files found. Please add CSV files to the 'data' directory.")
    st.stop()

selected_location = st.sidebar.selectbox(
    "Select Location",
    options=sorted(list(locations.keys())),
    index=0,
    format_func=lambda x: x.strip().strip('"').strip("'").strip(",").strip(),
)

# Load the data for selected location
try:
    df, location_name, structure = load_data(locations[selected_location])
except FileNotFoundError:
    st.sidebar.error(f"❌ Error: Could not find the data file for {selected_location}")
    st.stop()
except Exception as e:
    st.sidebar.error(f"❌ Error loading data: {str(e)}")
    st.stop()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df["Date/Time"].min().date(), df["Date/Time"].max().date()),
    min_value=df["Date/Time"].min().date(),
    max_value=df["Date/Time"].max().date(),
)

hour_range = st.sidebar.slider("Hour Range", min_value=0, max_value=23, value=(0, 23))

# Filter the data
mask = (
    (df["Date/Time"].dt.date >= date_range[0])
    & (df["Date/Time"].dt.date <= date_range[1])
    & (df["Hour"].between(hour_range[0], hour_range[1]))
)
filtered_df = df[mask].copy()

# Then add any new columns
filtered_df["Hour"] = filtered_df["Date/Time"].dt.hour
filtered_df["DayOfWeek"] = filtered_df["Date/Time"].dt.day_name()


# Load custom CSS from an external file
def load_custom_css(file_path: str) -> str:
    with open(file_path, "r") as f:
        return f"<style>{f.read()}</style>"


# Apply custom CSS
css_file_path = "styles.css"
st.markdown(load_custom_css(css_file_path), unsafe_allow_html=True)

# Main dashboard layout
st.title("Traffic Analysis Dashboard")
st.markdown("This dashboard provides insights into traffic data, including volume, speed, and vehicle classification.")
st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

# Display key metrics with enhanced styling
col1, col2, col3 = st.columns(3)

with col1:
    total_vehicles = filtered_df["Total"].sum()
    st.metric("📊 Total Vehicles", f"{total_vehicles:,}")

with col2:
    dir2_avg_speed = calculate_weighted_speed(filtered_df, structure["dir2_speed_cols"])
    st.metric(
        "🏎️ Average Speed ({})".format(structure["dir2_name"]),
        f"{dir2_avg_speed:.1f} mph",
    )

with col3:
    dir1_avg_speed = calculate_weighted_speed(filtered_df, structure["dir1_speed_cols"])
    st.metric(
        "🏎️ Average Speed ({})".format(structure["dir1_name"]),
        f"{dir1_avg_speed:.1f} mph",
    )

# Second row of metrics
col4, col5, col6 = st.columns(3)

with col4:
    dir1_compliant, dir1_total = calculate_compliance(filtered_df, structure["dir1_speed_cols"])
    dir2_compliant, dir2_total = calculate_compliance(filtered_df, structure["dir2_speed_cols"])
    total_compliant = dir1_compliant + dir2_compliant
    total_speed_readings = dir1_total + dir2_total
    compliance_rate = (total_compliant / total_speed_readings * 100) if total_speed_readings > 0 else 0
    st.metric("🚦 Speed Compliance", f"{compliance_rate:.1f}%")

with col5:
    dir1_85th = calculate_85th_percentile_speed(filtered_df, structure["dir1_speed_cols"])
    dir2_85th = calculate_85th_percentile_speed(filtered_df, structure["dir2_speed_cols"])
    st.metric("🎯 85th Percentile Speed", f"{max(dir1_85th, dir2_85th):.1f} mph")

with col6:
    daily_traffic = filtered_df.groupby(filtered_df["Date/Time"].dt.date)["Total"].sum()
    avg_daily_traffic = daily_traffic.mean()
    max_daily_traffic = daily_traffic.max()
    st.metric("📅 Daily Traffic", f"Avg: {avg_daily_traffic:,.0f}")

# Third row of metrics
col7, col8, col9 = st.columns(3)

with col7:
    dir1_volume = filtered_df[structure["dir1_volume_col"]].sum()
    dir2_volume = filtered_df[structure["dir2_volume_col"]].sum()
    dominant_direction = structure["dir1_name"] if dir1_volume > dir2_volume else structure["dir2_name"]
    dominant_pct = (
        max(dir1_volume, dir2_volume) / (dir1_volume + dir2_volume) * 100 if (dir1_volume + dir2_volume) > 0 else 0
    )
    st.metric("🔄 Dominant Direction", f"{dominant_direction}", f"{dominant_pct:.1f}%")

with col8:
    # Group by both date and day name to get accurate daily totals
    daily_volumes = filtered_df.groupby([filtered_df["Date/Time"].dt.date, filtered_df["Date/Time"].dt.day_name()])[
        "Total"
    ].sum()

    # Calculate true average by day of week
    dow_averages = daily_volumes.groupby(level=1).mean()
    busiest_day = dow_averages.idxmax()
    busiest_volume = dow_averages.max()
    st.metric("📆 Busiest Day", f"{busiest_day}", f"Avg: {busiest_volume:.0f} vehicles")

with col9:
    # Group by date and hour to get unique peak hours
    hourly_volumes = filtered_df.groupby([filtered_df["Date/Time"].dt.date, filtered_df["Date/Time"].dt.hour])[
        "Total"
    ].sum()

    # Find the overall peak hour
    peak_hour_idx = hourly_volumes.idxmax()
    peak_hour = peak_hour_idx[1]  # Get hour from the multi-index
    peak_vehicles = hourly_volumes.max()
    st.metric("⏰ Peak Hour", f"{peak_hour:02d}:00", f"{peak_vehicles:,} vehicles")

# Fourth row of metrics
col10, col11, col12 = st.columns(3)

with col10:
    phf = calculate_phf(filtered_df)
    st.metric("📈 Peak Hour Factor", f"{phf:.2f}")

with col11:
    total_high_speeders = count_high_speeders(filtered_df, structure["dir1_speed_cols"]) + count_high_speeders(
        filtered_df, structure["dir2_speed_cols"]
    )
    high_speeder_pct = (total_high_speeders / total_vehicles * 100) if total_vehicles > 0 else 0
    st.metric("⚠️ High Speed Violations", f"{total_high_speeders:,} ({high_speeder_pct:.1f}%)")

with col12:
    weekday_mask = filtered_df["Date/Time"].dt.weekday < 5
    weekday_avg = filtered_df[weekday_mask]["Total"].mean()
    weekend_avg = filtered_df[~weekday_mask]["Total"].mean()
    ratio = weekday_avg / weekend_avg if weekend_avg > 0 else 0
    st.metric(
        "📊 Weekday/Weekend Ratio",
        f"{weekday_avg:.1f} / {weekend_avg:.1f} = {ratio:.1f}",
    )

# Visualizations
st.subheader("Traffic Volume")
fig1 = plot_traffic_volume(filtered_df, structure)
st.pyplot(fig1)

# Plotly Traffic Volume
plotly_fig1 = px.line(filtered_df, x="Date/Time", y="Total", title="Traffic Volume Over Time")
st.plotly_chart(plotly_fig1)

temporal_fig = plot_temporal_patterns(filtered_df, structure)
st.pyplot(temporal_fig)

# Plotly Temporal Patterns
plotly_temporal_fig = px.histogram(filtered_df, x="Hour", y="Total", title="Temporal Traffic Patterns", nbins=24)
st.plotly_chart(plotly_temporal_fig)

st.subheader("Speed Analysis")
severity_fig = plot_speed_violation_severity(filtered_df, structure)
st.pyplot(severity_fig)

fig2 = plot_speed_distribution(filtered_df, structure)
st.pyplot(fig2)

fig3 = plot_speed_compliance(filtered_df, structure)
st.pyplot(fig3)

# Add speeding by hour visualization
st.subheader("Speeding by Hour of Day")
st.markdown(
    "This visualization shows when speeding occurs throughout the day, with the total number of vehicles "
    "and the percentage of vehicles speeding for each hour."
)
speeding_fig = plot_speeding_by_hour(filtered_df, structure)
st.pyplot(speeding_fig)

st.subheader("Vehicle Classification")
classification_fig = plot_vehicle_classification_distribution(filtered_df, structure)
st.pyplot(classification_fig)

dir1_col, dir2_col = st.columns(2)

with dir1_col:
    st.markdown(f"#### {structure['dir1_name']}")
    try:
        class_counts_dir1 = []
        for i in range(6):
            if i < len(structure.get("dir1_class_cols", [])):
                class_counts_dir1.append(filtered_df[structure["dir1_class_cols"][i]].sum())
            else:
                class_counts_dir1.append(0)
        class_data_dir1 = pd.DataFrame(
            {
                "Vehicle Type": [
                    "🏍️ Class 1 - Motorcycles",
                    "🚗 Class 2 - Passenger Cars",
                    "🚐 Class 3 - Pickups, Vans",
                    "🚌 Class 4 - Buses",
                    "🚛 Class 5 - 2 Axles, 6 Tires",
                    "🚛 Class 6 - 3 Axles",
                ],
                "Count": class_counts_dir1,
            }
        )
        total_dir1 = class_data_dir1["Count"].sum()
        class_data_dir1["Percentage"] = (class_data_dir1["Count"] / total_dir1 * 100 if total_dir1 > 0 else 0).round(1)
        for _, row in class_data_dir1.iterrows():
            st.markdown(f"{row['Vehicle Type']}: **{row['Count']:,}** ({row['Percentage']}%)")
        st.markdown(f"**Total Vehicles: {total_dir1:,}**")
    except Exception as e:
        st.error(f"Error processing {structure['dir1_name']} classification data: {str(e)}")
        class_data_dir1 = pd.DataFrame({"Vehicle Type": [], "Count": []})

with dir2_col:
    st.markdown(f"#### {structure['dir2_name']}")
    try:
        class_counts_dir2 = []
        for i in range(6):
            if i < len(structure.get("dir2_class_cols", [])):
                class_counts_dir2.append(filtered_df[structure["dir2_class_cols"][i]].sum())
            else:
                class_counts_dir2.append(0)
        class_data_dir2 = pd.DataFrame(
            {
                "Vehicle Type": [
                    "🏍️ Class 1 - Motorcycles",
                    "🚗 Class 2 - Passenger Cars",
                    "🚐 Class 3 - Pickups, Vans",
                    "🚌 Class 4 - Buses",
                    "🚛 Class 5 - 2 Axles, 6 Tires",
                    "🚛 Class 6 - 3 Axles",
                ],
                "Count": class_counts_dir2,
            }
        )
        total_dir2 = class_data_dir2["Count"].sum()
        class_data_dir2["Percentage"] = (class_data_dir2["Count"] / total_dir2 * 100 if total_dir2 > 0 else 0).round(1)
        for _, row in class_data_dir2.iterrows():
            st.markdown(f"{row['Vehicle Type']}: **{row['Count']:,}** ({row['Percentage']}%)")
        st.markdown(f"**Total Vehicles: {total_dir2:,}**")
    except Exception as e:
        st.error(f"Error processing {structure['dir2_name']} classification data: {str(e)}")
        class_data_dir2 = pd.DataFrame({"Vehicle Type": [], "Count": []})

show_raw_data = st.checkbox("Show Raw Data")
if show_raw_data:
    st.subheader("Raw Data")
    st.dataframe(filtered_df, use_container_width=True)

st.markdown("---")
st.markdown(
    "Data sourced from a pair of [PicoCount 2500](https://vehiclecounts.com/picocount-2500.html), "
    "and exported from [TrafficViewer Pro](https://vehiclecounts.com/trafficviewerpro.html). "
    "Dashboard created with [Streamlit](https://streamlit.io)."
)
