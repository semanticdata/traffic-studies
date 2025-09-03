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

from typing import Dict, Tuple

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


def clean_location_name(location_name: str) -> str:
    """Clean location name by removing quotes, commas, and extra whitespace."""
    return location_name.strip().strip('"').strip("'").strip(",").strip()


def setup_sidebar_filters() -> Tuple[str, Dict[str, str]]:
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
        format_func=clean_location_name,
    )

    return selected_location, locations


def load_and_filter_data(selected_location: str, locations: Dict[str, str]) -> Tuple[pd.DataFrame, Dict[str, str]]:
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

    # Apply filters - handle both tuple and single date cases
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = end_date = date_range

    mask = (
        (df["Date/Time"].dt.date >= start_date)
        & (df["Date/Time"].dt.date <= end_date)
        & (df["Hour"].between(hour_range[0], hour_range[1]))
    )
    filtered_df = df[mask].copy()

    # Add derived columns
    filtered_df["Hour"] = filtered_df["Date/Time"].dt.hour
    filtered_df["DayOfWeek"] = filtered_df["Date/Time"].dt.day_name()

    return filtered_df, structure


def display_core_metrics(filtered_df: pd.DataFrame, structure: Dict[str, str], selected_location: str) -> None:
    """Display the 6 core metrics in a clean layout."""
    st.subheader(f"Core Metrics - {selected_location}")
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

    date_min = filtered_df["Date/Time"].min().strftime("%B %d, %Y")
    date_max = filtered_df["Date/Time"].max().strftime("%B %d, %Y")
    st.info(f"📅 **Analysis Period:** {date_min} to {date_max}")


    st.divider()


def display_visualizations(filtered_df: pd.DataFrame, structure: Dict[str, str]) -> None:
    """Display all visualizations in organized sections."""

    # Traffic Volume Section
    st.subheader("📊 Traffic Volume Analysis")

    # Hourly Traffic Volume
    st.markdown("##### Hourly Traffic Volume")
    fig1 = plot_traffic_volume(filtered_df, structure)
    st.pyplot(fig1)

    with st.expander("See explanation"):
        st.markdown("""
        **How to read this chart:**
        - This stacked bar chart shows the average hourly traffic volume throughout the day
        - Each bar represents one hour (0-23), with the height showing total vehicles per hour
        - The two colors represent traffic in each direction (typically N/S or E/W)
        - **Peak hours** appear as the tallest bars, usually during morning and evening commutes
        - **Off-peak hours** (late night/early morning) show lower traffic volumes
        - Use this to identify busy periods and plan accordingly for traffic management
        """)

    # Daily Traffic Patterns
    st.markdown("##### Daily Traffic Patterns")
    temporal_fig = plot_temporal_patterns(filtered_df, structure)
    st.pyplot(temporal_fig)

    with st.expander("See explanation"):
        st.markdown("""
        **How to read this chart:**
        - This bar chart shows total traffic volume for each day of the week
        - Each bar represents one day, with separate colors for each traffic direction
        - **Weekday patterns** typically show higher volumes Monday-Friday
        - **Weekend patterns** may show different traffic distributions
        - Compare bar heights to identify the busiest and quietest days
        - Useful for understanding weekly traffic cycles and planning maintenance schedules
        """)

    st.divider()

    # Speed Analysis Section
    st.subheader("🚗 Speed Analysis")

    # Speed Violation Severity
    severity_fig = plot_speed_violation_severity(filtered_df, structure)
    if severity_fig:
        st.markdown("##### Speed Violation Severity")
        st.pyplot(severity_fig)

        with st.expander("See explanation"):
            st.markdown("""
            **How to read this chart:**
            - This chart categorizes speeding violations by severity level
            - **0-5 mph over**: Minor speeding, typically considered acceptable tolerance
            - **5-10 mph over**: Moderate speeding, may warrant attention
            - **10-15 mph over**: Significant speeding, safety concern
            - **15+ mph over**: Severe speeding, major safety risk
            - Colors progress from light to dark indicating increasing severity
            - Use this to prioritize enforcement efforts and identify dangerous speeding patterns
            """)

    # Speed Distribution
    st.markdown("##### Speed Distribution by Direction")
    fig2 = plot_speed_distribution(filtered_df, structure)
    st.pyplot(fig2)

    with st.expander("See explanation"):
        st.markdown("""
        **How to read this chart:**
        - These charts show the distribution of vehicle speeds in each direction
        - Each bar represents a speed range (e.g., 25-30 MPH, 30-35 MPH)
        - Bar height indicates the average number of vehicles in that speed range
        - **Normal distribution** typically peaks around the speed limit
        - **Right-skewed distribution** may indicate speeding issues
        - Compare the two directions to identify if one has more speeding than the other
        - Use this to understand overall speed compliance patterns
        """)

    # Speed Compliance
    st.markdown("##### Speed Compliance Analysis")
    fig3 = plot_speed_compliance(filtered_df, structure)
    st.pyplot(fig3)

    with st.expander("See explanation"):
        st.markdown("""
        **How to read this chart:**
        - This chart compares compliant vs. non-compliant vehicles by direction
        - **Green bars** represent vehicles traveling at or below the speed limit
        - **Red bars** represent vehicles exceeding the speed limit
        - Compare bar heights to see the compliance rate for each direction
        - Higher green bars indicate better speed compliance
        - Use this to quickly assess overall speed compliance and identify problem directions
        """)

    # Speeding by Hour
    st.markdown("##### Speeding Patterns by Hour")
    speeding_fig = plot_speeding_by_hour(filtered_df, structure)
    st.pyplot(speeding_fig)

    with st.expander("See explanation"):
        st.markdown("""
        **How to read this chart:**
        - This dual-axis chart shows when speeding occurs throughout the day
        - **Gray bars** (left axis) show total vehicle count by hour
        - **Red line with dots** (right axis) shows percentage of vehicles speeding
        - **High percentage + high volume** indicates peak enforcement opportunities
        - **High percentage + low volume** may indicate off-peak speeding patterns
        - Compare the two directions to identify directional speeding patterns
        - Use this to optimize enforcement timing and identify when speeding is most problematic
        """)

    st.divider()


def display_vehicle_classification(filtered_df: pd.DataFrame, structure: Dict[str, str]) -> None:
    """Display vehicle classification with chart and legend."""
    st.subheader("🚛 Vehicle Classification")

    # Display the chart
    classification_fig = plot_vehicle_classification_distribution(filtered_df, structure)
    st.pyplot(classification_fig)

    with st.expander("See explanation"):
        st.markdown("""
        **How to read this chart:**
        - This chart shows the distribution of different vehicle types in each direction
        - Each bar represents a vehicle classification based on the Federal Highway Administration (FHWA) system
        - **Class 2 (Passenger Cars)** typically dominates traffic in residential areas
        - **Class 3 (Pickups, Vans)** represents light commercial and personal vehicles
        - **Classes 4-6** represent larger commercial vehicles (buses, trucks)
        - Compare the two directions to identify if one has more commercial traffic
        - Use this data for infrastructure planning and understanding traffic composition
        """)

    # Display vehicle class legend
    st.markdown("##### Vehicle Class Legend")
    st.markdown("""
    - 🏍️ **Class 1**: Motorcycles  
    - 🚗 **Class 2**: Passenger Cars  
    - 🚐 **Class 3**: Pickups, Vans  
    - 🚌 **Class 4**: Buses  
    - 🚛 **Class 5**: 2 Axles, 6 Tires  
    - 🚛 **Class 6**: 3 Axles  
    """)


def display_optional_data(filtered_df: pd.DataFrame) -> None:
    """Display optional raw data section."""
    show_raw_data = st.checkbox("Show Raw Data")
    if show_raw_data:
        st.subheader("Raw Data")
        st.dataframe(filtered_df, use_container_width=True)


def main() -> None:
    """Main application function."""
    # Page configuration
    st.set_page_config(
        page_title="Traffic Analysis Dashboard",
        page_icon="🚗",
        layout="centered",
        menu_items={
            "About": (
                "Built for the [City of Crystal](https://www.crystalmn.gov/) by Miguel Pimentel. "
                "Data sourced from a pair of [PicoCount 2500](https://vehiclecounts.com/picocount-2500.html), "
                "and exported using [TrafficViewer Pro](https://vehiclecounts.com/trafficviewerpro.html)."
            ),
            "Get help": "mailto:miguel.pimentel@crystalmn.gov",
        },
    )

    # Apply custom CSS
    css_file_path = "styles.css"
    st.markdown(load_custom_css(css_file_path), unsafe_allow_html=True)

    # Header
    st.title("🚸 Traffic Analysis Dashboard")
    st.markdown(
        "Comprehensive traffic analysis for the City of Crystal, Minnesota. "
        "This dashboard analyzes traffic patterns, speed compliance, and vehicle classifications "
        "to support data-driven traffic management decisions."
    )
    # st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)
    # st.divider()

    # Setup sidebar and load data
    selected_location, locations = setup_sidebar_filters()
    filtered_df, structure = load_and_filter_data(selected_location, locations)

    # Clean the location name for display
    clean_location = clean_location_name(selected_location)

    # Display dashboard sections
    display_core_metrics(filtered_df, structure, clean_location)
    display_visualizations(filtered_df, structure)
    display_vehicle_classification(filtered_df, structure)
    display_optional_data(filtered_df)


if __name__ == "__main__":
    main()
