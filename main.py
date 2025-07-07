"""
Traffic Studies Dashboard - Main Application

A comprehensive traffic analysis dashboard for Crystal, Minnesota, built with Streamlit.
This application processes and visualizes traffic data collected from PicoCount 2500
traffic counters, providing detailed insights into traffic patterns, speed compliance,
and vehicle classifications.

Features:
- Interactive filtering by location, date range, and time periods
- 6 core key performance indicators and metrics
- Vehicle classification analysis (6 FHWA classes)
- Speed compliance monitoring and violation tracking
- Temporal traffic pattern analysis
- Streamlined visualizations with Matplotlib

Data Sources:
- PicoCount 2500 traffic counters
- TrafficViewer Pro software exports

Author: Miguel Pimentel
License: MIT
"""

import pandas as pd
import streamlit as st

from utils.data_loader import get_available_locations, load_data
from utils.metrics import get_core_metrics
from utils.visualizations import (
    plot_speed_compliance,
    plot_speed_distribution,
    plot_speed_violation_severity,
    plot_speeding_by_hour,
    plot_temporal_patterns,
    plot_traffic_volume,
    plot_vehicle_classification_distribution,
)


def load_custom_css(file_path: str) -> str:
    """Load custom CSS from an external file."""
    with open(file_path, "r") as f:
        return f"<style>{f.read()}</style>"


def setup_sidebar_filters():
    """Set up sidebar filters and return selected values."""
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

    return selected_location, locations


def load_and_filter_data(selected_location: str, locations: dict):
    """Load and filter the traffic data."""
    try:
        df, location_name, structure = load_data(locations[selected_location])
    except FileNotFoundError:
        st.sidebar.error(f"❌ Error: Could not find the data file for {selected_location}")
        st.stop()
    except Exception as e:
        st.sidebar.error(f"❌ Error loading data: {str(e)}")
        st.stop()

    # Date and time filters
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(df["Date/Time"].min().date(), df["Date/Time"].max().date()),
        min_value=df["Date/Time"].min().date(),
        max_value=df["Date/Time"].max().date(),
    )

    hour_range = st.sidebar.slider("Hour Range", min_value=0, max_value=23, value=(0, 23))

    # Apply filters
    mask = (
        (df["Date/Time"].dt.date >= date_range[0])
        & (df["Date/Time"].dt.date <= date_range[1])
        & (df["Hour"].between(hour_range[0], hour_range[1]))
    )
    filtered_df = df[mask].copy()

    # Add derived columns
    filtered_df["Hour"] = filtered_df["Date/Time"].dt.hour
    filtered_df["DayOfWeek"] = filtered_df["Date/Time"].dt.day_name()

    return filtered_df, structure


def display_core_metrics(filtered_df: pd.DataFrame, structure: dict):
    """Display the 6 core metrics in a clean layout."""
    metrics = get_core_metrics(filtered_df, structure)

    # First row - Primary metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📊 Total Vehicles", f"{metrics['total_vehicles']:,}")

    with col2:
        st.metric("🏎️ Average Speed", f"{metrics['combined_avg_speed']:.1f} mph")

    with col3:
        st.metric("🚦 Speed Compliance", f"{metrics['compliance_rate']:.1f}%")

    # Second row - Analysis metrics
    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric("🎯 85th Percentile Speed", f"{metrics['percentile_85th']:.1f} mph")

    with col5:
        st.metric("⏰ Peak Hour", f"{metrics['peak_hour']:02d}:00", f"{metrics['peak_vehicles']:,} vehicles")

    with col6:
        st.metric("🔄 Dominant Direction", metrics["dominant_direction"], f"{metrics['dominant_pct']:.1f}%")


def display_visualizations(filtered_df: pd.DataFrame, structure: dict):
    """Display all visualizations in organized sections."""

    # Traffic Volume Section
    st.subheader("Traffic Volume Analysis")
    fig1 = plot_traffic_volume(filtered_df, structure)
    st.pyplot(fig1)

    temporal_fig = plot_temporal_patterns(filtered_df, structure)
    st.pyplot(temporal_fig)

    # Speed Analysis Section
    st.subheader("Speed Analysis")
    severity_fig = plot_speed_violation_severity(filtered_df, structure)
    if severity_fig:
        st.pyplot(severity_fig)

    fig2 = plot_speed_distribution(filtered_df, structure)
    st.pyplot(fig2)

    fig3 = plot_speed_compliance(filtered_df, structure)
    st.pyplot(fig3)

    # Speeding by Hour Section
    st.subheader("Speeding by Hour of Day")
    st.markdown(
        "This visualization shows when speeding occurs throughout the day, with the total number of vehicles "
        "and the percentage of vehicles speeding for each hour."
    )
    speeding_fig = plot_speeding_by_hour(filtered_df, structure)
    st.pyplot(speeding_fig)


def display_vehicle_classification(filtered_df: pd.DataFrame, structure: dict):
    """Display vehicle classification with chart and legend."""
    st.subheader("Vehicle Classification")

    # Display the chart
    classification_fig = plot_vehicle_classification_distribution(filtered_df, structure)
    st.pyplot(classification_fig)

    # Display vehicle class legend
    st.markdown("### Vehicle Class Legend")
    st.markdown("""
    - 🏍️ **Class 1**: Motorcycles  
    - 🚗 **Class 2**: Passenger Cars  
    - 🚐 **Class 3**: Pickups, Vans  
    - 🚌 **Class 4**: Buses  
    - 🚛 **Class 5**: 2 Axles, 6 Tires  
    - 🚛 **Class 6**: 3 Axles  
    """)


def display_optional_data(filtered_df: pd.DataFrame):
    """Display optional raw data section."""
    show_raw_data = st.checkbox("Show Raw Data")
    if show_raw_data:
        st.subheader("Raw Data")
        st.dataframe(filtered_df, use_container_width=True)


def main():
    """Main application function."""
    # Page configuration
    st.set_page_config(page_title="Traffic Analysis Dashboard", page_icon="🚗", layout="wide")

    # Apply custom CSS
    css_file_path = "styles.css"
    st.markdown(load_custom_css(css_file_path), unsafe_allow_html=True)

    # Header
    st.title("Traffic Analysis Dashboard")
    st.markdown(
        "This dashboard provides insights into traffic data, including volume, speed, and vehicle classification."
    )
    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

    # Setup sidebar and load data
    selected_location, locations = setup_sidebar_filters()
    filtered_df, structure = load_and_filter_data(selected_location, locations)

    # Display dashboard sections
    display_core_metrics(filtered_df, structure)
    display_visualizations(filtered_df, structure)
    display_vehicle_classification(filtered_df, structure)
    display_optional_data(filtered_df)

    # Footer
    st.markdown("---")
    st.markdown(
        "Data sourced from a pair of [PicoCount 2500](https://vehiclecounts.com/picocount-2500.html), "
        "and exported from [TrafficViewer Pro](https://vehiclecounts.com/trafficviewerpro.html). "
        "Dashboard created with [Streamlit](https://streamlit.io)."
    )


if __name__ == "__main__":
    main()
