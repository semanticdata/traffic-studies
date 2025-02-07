# This is the main dashboard for the traffic analysis project.
# It will display the data and allow for filtering and visualization.

import streamlit as st
from datetime import datetime
from utils.data_loader import load_data, get_available_locations
from utils.visualizations import (
    plot_traffic_volume,
    plot_speed_distribution,
    plot_speed_compliance,
    plot_temporal_patterns,
    plot_speed_violation_severity,
)
from utils.styles import CUSTOM_CSS
import numpy as np


# Set page config
st.set_page_config(
    page_title="Traffic Analysis Dashboard", page_icon="🚗", layout="wide"
)

# Apply custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Sidebar
# st.sidebar.header("Traffic Analysis Dashboard")
# st.sidebar.markdown(
#     """Please select a location and set your desired date and hour filters to analyze the traffic data."""
# )
st.sidebar.header("Location and Filters")

# Main dashboard layout
locations = get_available_locations()

if not locations:
    st.error("❌ No data files found. Please add CSV files to the 'data' directory.")
    st.stop()

# Location selector
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
    st.error(f"❌ Error: Could not find the data file for {selected_location}")
    st.stop()
except Exception as e:
    st.error(f"❌ Error loading data: {str(e)}")
    st.stop()

# Date range filter
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df["Date/Time"].min().date(), df["Date/Time"].max().date()),
    min_value=df["Date/Time"].min().date(),
    max_value=df["Date/Time"].max().date(),
)

# Hour range filter
hour_range = st.sidebar.slider(
    "Hour Range", min_value=0, max_value=23, value=(0, 23))

# Filter the data
mask = (
    (df["Date/Time"].dt.date >= date_range[0])
    & (df["Date/Time"].dt.date <= date_range[1])
    & (df["Hour"].between(hour_range[0], hour_range[1]))
)
filtered_df = df[mask]

# Location Info
st.markdown(
    f"""
    <h1 style='text-align: center;'>
        📍 {location_name} - Traffic Study
    </h1>
""",
    unsafe_allow_html=True,
)

# Display key metrics with enhanced styling
st.markdown("<div style='margin: 2rem 0;'>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_vehicles = filtered_df['Total'].sum()
    st.metric("📊 Total Vehicles", f"{total_vehicles:,}")

with col2:
    dir1_volume = filtered_df[structure["dir1_volume_col"]].sum()
    dir2_volume = filtered_df[structure["dir2_volume_col"]].sum()
    dominant_direction = structure["dir1_name"] if dir1_volume > dir2_volume else structure["dir2_name"]
    dominant_pct = max(dir1_volume, dir2_volume) / (dir1_volume +
                                                    dir2_volume) * 100 if (dir1_volume + dir2_volume) > 0 else 0
    st.metric("🔄 Dominant Direction",
              f"{dominant_direction}",
              f"{dominant_pct:.1f}%")

with col3:
    hourly_totals = filtered_df.groupby('Hour')['Total'].sum()
    peak_hour = hourly_totals.idxmax()
    peak_vehicles = hourly_totals.max()
    st.metric("⏰ Peak Hour",
              f"{peak_hour:02d}:00",
              f"{peak_vehicles:,} vehicles")

with col4:
    # Calculate compliance directly from speed columns
    def calculate_compliance(df, speed_cols, speed_limit=25):
        compliant = 0
        total = 0
        for col in speed_cols:
            speed = int(col.split('-')[0].strip())
            count = df[col].sum()
            if speed <= speed_limit:
                compliant += count
            total += count
        return compliant, total

    dir1_compliant, dir1_total = calculate_compliance(
        filtered_df, structure["dir1_speed_cols"])
    dir2_compliant, dir2_total = calculate_compliance(
        filtered_df, structure["dir2_speed_cols"])

    total_compliant = dir1_compliant + dir2_compliant
    total_speed_readings = dir1_total + dir2_total
    compliance_rate = (total_compliant / total_speed_readings *
                       100) if total_speed_readings > 0 else 0
    st.metric("🚦 Speed Compliance", f"{compliance_rate:.1f}%")

# Second row of metrics
col5, col6, col7, col8 = st.columns(4)

with col5:
    daily_traffic = filtered_df.groupby(
        filtered_df["Date/Time"].dt.date)["Total"].sum()
    avg_daily_traffic = daily_traffic.mean()
    max_daily_traffic = daily_traffic.max()
    st.metric(
        "📅 Daily Traffic",
        f"Avg: {avg_daily_traffic:,.0f}",
        f"Max: {max_daily_traffic:,.0f}"
    )

with col6:
    # Calculate average speeds using weighted average
    def calculate_weighted_speed(df, speed_cols):
        total_count = 0
        weighted_sum = 0
        for col in speed_cols:
            speed = int(col.split('-')[0].strip())
            count = df[col].sum()
            weighted_sum += speed * count
            total_count += count
        return weighted_sum / total_count if total_count > 0 else 0

    dir1_avg_speed = calculate_weighted_speed(
        filtered_df, structure["dir1_speed_cols"])
    st.metric(
        "🏎️ Average Speed ({})".format(structure["dir1_name"]),
        f"{dir1_avg_speed:.1f} mph"
    )

with col7:
    dir2_avg_speed = calculate_weighted_speed(
        filtered_df, structure["dir2_speed_cols"])
    st.metric(
        "🏎️ Average Speed ({})".format(structure["dir2_name"]),
        f"{dir2_avg_speed:.1f} mph"
    )

with col8:
    weekday_mask = filtered_df["Date/Time"].dt.weekday < 5
    weekday_avg = filtered_df[weekday_mask]["Total"].mean()
    weekend_avg = filtered_df[~weekday_mask]["Total"].mean()
    ratio = weekday_avg / weekend_avg if weekend_avg > 0 else 0
    st.metric(
        "📊 Weekday/Weekend Ratio",
        f"{weekday_avg:.1f} / {weekend_avg:.1f} = {ratio:.1f}"
    )


# Add a third row of metrics for additional insights
col9, col10, col11, col12 = st.columns(4)

with col9:
    # Calculate 85th percentile speed
    def calculate_85th_percentile_speed(df, speed_cols):
        speeds = []
        for col in speed_cols:
            speed = int(col.split('-')[0].strip())
            count = df[col].sum()
            speeds.extend([speed] * int(count))
        return np.percentile(speeds, 85) if speeds else 0

    dir1_85th = calculate_85th_percentile_speed(
        filtered_df, structure["dir1_speed_cols"])
    dir2_85th = calculate_85th_percentile_speed(
        filtered_df, structure["dir2_speed_cols"])
    st.metric("🎯 85th Percentile Speed",
              f"{max(dir1_85th, dir2_85th):.1f} mph")

with col10:
    # Peak hour factor (PHF)
    def calculate_phf(df):
        hourly_volumes = df.groupby('Hour')['Total'].sum()
        peak_hour_volume = hourly_volumes.max()
        if peak_hour_volume == 0:
            return 0
        peak_hour_idx = hourly_volumes.idxmax()
        peak_15min = df[df['Hour'] == peak_hour_idx]['Total'].max() * 4
        return peak_hour_volume / peak_15min if peak_15min > 0 else 0

    phf = calculate_phf(filtered_df)
    st.metric("📈 Peak Hour Factor", f"{phf:.2f}")

with col11:
    # High speed violations (15+ mph over limit)
    def count_high_speeders(df, speed_cols, speed_limit=25):
        high_speeders = 0
        for col in speed_cols:
            speed = int(col.split('-')[0].strip())
            if speed >= speed_limit + 15:
                high_speeders += df[col].sum()
        return high_speeders

    total_high_speeders = (
        count_high_speeders(filtered_df, structure["dir1_speed_cols"]) +
        count_high_speeders(filtered_df, structure["dir2_speed_cols"])
    )
    high_speeder_pct = (total_high_speeders /
                        total_vehicles * 100) if total_vehicles > 0 else 0
    st.metric("⚠️ High Speed Violations",
              f"{total_high_speeders:,} ({high_speeder_pct:.1f}%)")

with col12:
    # Busiest day of week
    dow_volumes = filtered_df.groupby(
        filtered_df['Date/Time'].dt.day_name())['Total'].mean()
    busiest_day = dow_volumes.idxmax()
    busiest_volume = dow_volumes.max()
    st.metric("📆 Busiest Day", f"{busiest_day}",
              f"Avg: {busiest_volume:.0f} vehicles")

st.markdown("</div>", unsafe_allow_html=True)

# Create tabs for visualizations
tab1, tab2, tab3 = st.tabs(
    ["📈 Traffic Volume", "🚗 Speed Analysis", "📊 Raw Data"])

with tab1:
    # st.subheader("Directional Traffic Volume by Hour")
    fig1 = plot_traffic_volume(filtered_df, structure)
    st.pyplot(fig1)

    # st.subheader("Daily Traffic Volume Patterns")
    temporal_fig = plot_temporal_patterns(filtered_df, structure)
    st.pyplot(temporal_fig)


with tab2:
    # st.subheader("Speed Violation Severity")
    severity_fig = plot_speed_violation_severity(filtered_df, structure)
    st.pyplot(severity_fig)

    # st.subheader("Speed Distribution by Direction")
    fig2 = plot_speed_distribution(filtered_df, structure)
    st.pyplot(fig2)

    # st.subheader("Speed Compliance by Direction")
    fig3 = plot_speed_compliance(filtered_df, structure)
    st.pyplot(fig3)

with tab3:
    # st.subheader("Data Summary")
    st.dataframe(filtered_df, use_container_width=True)

# Enhanced footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; padding: 1rem; background-color: rgba(128, 128, 128, 0.1); border-radius: 0.5rem;'>
        <p style='color: var(--text-color);'>Dashboard created with ❤️ using Streamlit | Data refreshed on: {}</p>
    </div>
""".format(
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ),
    unsafe_allow_html=True,
)
