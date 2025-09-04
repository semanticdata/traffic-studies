"""
Traffic Studies Dashboard - Main Application

A comprehensive traffic analysis dashboard for Crystal, Minnesota, built with Streamlit.
This application processes and visualizes traffic data collected from PicoCount 2500
traffic counters, providing detailed insights into traffic patterns, speed compliance,
and vehicle classifications.

Features:
- Interactive filtering by location, date range, and time periods
- Core key performance indicators and metrics
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
    plot_traffic_volume_plotly,
    plot_speed_distribution_plotly,
    plot_speed_compliance_plotly,
    plot_temporal_patterns_plotly,
    plot_speed_violation_severity_plotly,
    plot_speeding_by_hour_plotly,
    plot_vehicle_classification_distribution_plotly,
)


def load_custom_css(file_path: str) -> str:
    """Load custom CSS from an external file."""
    with open(file_path, "r") as f:
        return f"<style>{f.read()}</style>"


def clean_location_name(location_name: str) -> str:
    """Clean location name by removing quotes, commas, and extra whitespace."""
    return location_name.strip().strip('"').strip("'").strip(",").strip()


def setup_sidebar_filters() -> Tuple[str, Dict[str, str], str]:
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

    viz_library = st.sidebar.radio("Choose visualization library", ["Matplotlib", "Plotly"], index=1)

    return selected_location, locations, viz_library


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
    """Display the 8 core metrics in a clean layout."""
    st.subheader(f"Core Metrics - {selected_location}")
    metrics = get_core_metrics(filtered_df, structure)

    # First row - Volume and patterns
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📊 Total Vehicles", f"{metrics['total_vehicles']:,}", border=True, height="stretch")

    with col2:
        st.metric("📅 Average Daily Traffic", f"{metrics['adt']:,.0f}", border=True, height="stretch")

    with col3:
        peak_hour_display = (
            f"{metrics['peak_hour']:02d}:00" if isinstance(metrics["peak_hour"], int) else metrics["peak_hour"]
        )
        st.metric("⏰ Peak Hour", peak_hour_display, f"{metrics['peak_vehicles']:,} vehicles", border=True)

    with col4:
        st.metric(
            "🔄 Dominant Direction", metrics["dominant_direction"], f"{metrics['dominant_pct']:.1f}%", border=True
        )

    # Second row - Speed analysis
    col5, col6, col7, col8 = st.columns(4)

    with col5:
        st.metric("📝 Posted Speed", f"{metrics['posted_speed']} mph", border=True)

    with col6:
        st.metric("🏎️ Average Speed", f"{metrics['combined_avg_speed']:.1f} mph", border=True)

    with col7:
        st.metric("🎯 85th Percentile Speed", f"{metrics['percentile_85th']:.1f} mph", border=True)

    with col8:
        st.metric("🚦 Speed Compliance", f"{metrics['compliance_rate']:.1f}%", border=True)

    if not filtered_df.empty:
        date_min = filtered_df["Date/Time"].min().strftime("%B %d, %Y")
        date_max = filtered_df["Date/Time"].max().strftime("%B %d, %Y")
        st.info(f"📅 **Analysis Period:** {date_min} to {date_max}")

    st.divider()


def display_visualizations(filtered_df: pd.DataFrame, structure: Dict[str, str], viz_library: str) -> None:
    """Display all visualizations in organized sections."""

    # Traffic Volume Section
    st.subheader("📊 Traffic Volume Analysis")

    # Hourly Traffic Volume
    st.markdown("##### Hourly Traffic Volume")
    if viz_library == "Matplotlib":
        fig1 = plot_traffic_volume(filtered_df, structure)
        st.pyplot(fig1)
    else:
        fig1 = plot_traffic_volume_plotly(filtered_df, structure)
        st.plotly_chart(fig1, use_container_width=True)

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
    if viz_library == "Matplotlib":
        temporal_fig = plot_temporal_patterns(filtered_df, structure)
        st.pyplot(temporal_fig)
    else:
        temporal_fig = plot_temporal_patterns_plotly(filtered_df, structure)
        st.plotly_chart(temporal_fig, use_container_width=True)

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
    if viz_library == "Matplotlib":
        severity_fig = plot_speed_violation_severity(filtered_df, structure)
        if severity_fig:
            st.markdown("##### Speed Violation Severity")
            st.pyplot(severity_fig)
    else:
        severity_fig = plot_speed_violation_severity_plotly(filtered_df, structure)
        if severity_fig:
            st.markdown("##### Speed Violation Severity")
            st.plotly_chart(severity_fig, use_container_width=True)

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
    if viz_library == "Matplotlib":
        fig2 = plot_speed_distribution(filtered_df, structure)
        st.pyplot(fig2)
    else:
        fig2 = plot_speed_distribution_plotly(filtered_df, structure)
        st.plotly_chart(fig2, use_container_width=True)

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
    if viz_library == "Matplotlib":
        fig3 = plot_speed_compliance(filtered_df, structure)
        st.pyplot(fig3)
    else:
        fig3 = plot_speed_compliance_plotly(filtered_df, structure)
        st.plotly_chart(fig3, use_container_width=True)

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
    if viz_library == "Matplotlib":
        speeding_fig = plot_speeding_by_hour(filtered_df, structure)
        st.pyplot(speeding_fig)
    else:
        speeding_fig = plot_speeding_by_hour_plotly(filtered_df, structure)
        st.plotly_chart(speeding_fig, use_container_width=True)

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


def display_vehicle_classification(filtered_df: pd.DataFrame, structure: Dict[str, str], viz_library: str) -> None:
    """Display vehicle classification with chart and legend."""
    st.subheader("🚛 Vehicle Classification")

    # Display the chart
    if viz_library == "Matplotlib":
        classification_fig = plot_vehicle_classification_distribution(filtered_df, structure)
        st.pyplot(classification_fig)
    else:
        classification_fig = plot_vehicle_classification_distribution_plotly(filtered_df, structure)
        st.plotly_chart(classification_fig, use_container_width=True)

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


def display_pdf_report(clean_location: str) -> None:
    """Display PDF source data report section."""
    import os

    st.subheader("📄 PDF Source Data Report")

    pdf_dir = os.path.join("data", "reports")
    pdf_filename = f"{clean_location}.pdf"
    pdf_path = os.path.join(pdf_dir, pdf_filename)
    alt_pdf_filename = f"{clean_location.replace('_', ' ')}.pdf"
    alt_pdf_path = os.path.join(pdf_dir, alt_pdf_filename)

    # Check for PDF file existence
    if os.path.exists(pdf_path):
        current_pdf_path = pdf_path
    elif os.path.exists(alt_pdf_path):
        current_pdf_path = alt_pdf_path
    else:
        current_pdf_path = None

    if current_pdf_path:
        show_pdf = st.checkbox("Display PDF Report", help="View the original traffic counter report for this location")

        if show_pdf:
            st.info("📋 This report contains the raw data and additional analysis from the traffic counter.")

            # Display PDF
            st.pdf(current_pdf_path, height=600)

            # Add download button
            with open(current_pdf_path, "rb") as pdf_file:
                pdf_data = pdf_file.read()
                st.download_button(
                    label="📥 Download PDF Report",
                    data=pdf_data,
                    file_name=f"{clean_location}_Traffic_Report.pdf",
                    mime="application/pdf",
                    help="Download the complete traffic analysis report",
                    use_container_width=True,
                )
    else:
        st.warning(f"📄 No PDF report available for {clean_location}.")


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
                "Data sourced from [PicoCount 2500](https://vehiclecounts.com/picocount-2500.html) traffic counters, "
                "and exported using [TrafficViewer Pro](https://vehiclecounts.com/trafficviewerpro.html). "
                "Find the source code on [GitHub](https://github.com/semanticdata/traffic-studies)."
            ),
            "Report a bug": "https://github.com/semanticdata/traffic-studies/issues",
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

    # Setup sidebar and load data
    selected_location, locations, viz_library = setup_sidebar_filters()
    filtered_df, structure = load_and_filter_data(selected_location, locations)

    # Clean the location name for display
    clean_location = clean_location_name(selected_location)

    # Display dashboard sections
    display_core_metrics(filtered_df, structure, clean_location)
    display_visualizations(filtered_df, structure, viz_library)
    display_vehicle_classification(filtered_df, structure, viz_library)

    # Display PDF report section
    display_pdf_report(clean_location)


if __name__ == "__main__":
    main()
