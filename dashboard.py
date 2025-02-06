# This is the main dashboard for the traffic analysis project.
# It will display the data and allow for filtering and visualization.

import streamlit as st
from datetime import datetime
from utils.data_loader import load_data, get_available_locations
from utils.visualizations import (
    plot_traffic_volume,
    plot_speed_distribution,
    plot_speed_compliance,
)
from utils.styles import CUSTOM_CSS

# Set page config
st.set_page_config(
    page_title="Traffic Analysis Dashboard", page_icon="🚗", layout="wide"
)

# Apply custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Sidebar
st.sidebar.header("Traffic Analysis Dashboard")
st.sidebar.markdown(
    """Please select a location and set your desired date and hour filters to analyze the traffic data."""
)
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
hour_range = st.sidebar.slider("Hour Range", min_value=0, max_value=23, value=(0, 23))

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
    <h1 style='text-align: center; margin-bottom: 2rem;'>
        📍 {location_name} - Traffic Study
    </h1>
    <p style='text-align: center; font-size: 1.2rem; color: var(--text-color);'>
        Analyzing traffic data from <b>{date_range[0]}</b> to <b>{date_range[1]}</b>
    </p>
""",
    unsafe_allow_html=True,
)

# Display key metrics with enhanced styling
st.markdown("<div style='margin: 2rem 0;'>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📊 Total Vehicles", f"{filtered_df['Total'].sum():,}")

with col2:
    dir1_volume = filtered_df[structure["dir1_volume_col"]].sum()
    dir2_volume = filtered_df[structure["dir2_volume_col"]].sum()
    dominant_direction = (
        structure["dir1_name"] if dir1_volume > dir2_volume else structure["dir2_name"]
    )
    dominant_pct = max(dir1_volume, dir2_volume) / (dir1_volume + dir2_volume) * 100
    st.metric("🔄 Dominant Direction", f"{dominant_direction} ({dominant_pct:.1f}%)")

with col3:
    peak_hour = filtered_df.loc[filtered_df["Total"].idxmax(), "Hour"]
    peak_vehicles = filtered_df["Total"].max()
    st.metric("⏰ Peak Hour", f"{peak_hour:02d}:00 ({peak_vehicles} vehicles)")

with col4:
    total_compliant = (
        filtered_df["Dir1_Compliant"].sum() + filtered_df["Dir2_Compliant"].sum()
    )
    total_volume = filtered_df["Total"].sum()
    compliance_rate = (total_compliant / total_volume * 100) if total_volume > 0 else 0
    st.metric("🚦 Speed Compliance", f"{compliance_rate:.1f}%")

# Add a second row of metrics
col5, col6, col7, col8 = st.columns(4)

with col5:
    avg_daily_traffic = (
        filtered_df.groupby(filtered_df["Date/Time"].dt.date)["Total"].sum().mean()
    )
    st.metric("📅 Average Daily Traffic", f"{avg_daily_traffic:,.0f}")

with col6:
    # Calculate average speeds using the speed columns from structure
    dir1_speeds = filtered_df[structure["dir1_speed_cols"]].mean().mean()
    st.metric(
        "🏎️ Average Speed ({})".format(structure["dir1_name"]), f"{dir1_speeds:.1f} mph"
    )

with col7:
    dir2_speeds = filtered_df[structure["dir2_speed_cols"]].mean().mean()
    st.metric(
        "🏎️ Average Speed ({})".format(structure["dir2_name"]), f"{dir2_speeds:.1f} mph"
    )
with col8:
    weekday_avg = filtered_df[filtered_df["Date/Time"].dt.weekday < 5]["Total"].mean()
    weekend_avg = filtered_df[filtered_df["Date/Time"].dt.weekday >= 5]["Total"].mean()
    ratio = weekday_avg / weekend_avg if weekend_avg > 0 else 0
    st.metric("📊 Weekday/Weekend Ratio", f"{ratio:.2f}")

st.markdown("</div>", unsafe_allow_html=True)

# Create tabs for visualizations
tab1, tab2, tab3 = st.tabs(["📈 Traffic Volume", "🚗 Speed Analysis", "📊 Raw Data"])

with tab1:
    st.subheader("Directional Traffic Volume by Hour")
    fig1 = plot_traffic_volume(filtered_df, structure)
    st.pyplot(fig1)

    st.subheader("Traffic Volume Over Time")
    fig4 = plot_traffic_volume(filtered_df, structure)
    st.pyplot(fig4)

with tab2:
    st.subheader("Speed Distribution by Direction")
    fig2 = plot_speed_distribution(filtered_df, structure)
    st.pyplot(fig2)

    st.subheader("Speed Compliance by Direction")
    fig3 = plot_speed_compliance(filtered_df, structure)
    st.pyplot(fig3)

with tab3:
    st.subheader("Data Summary")
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
