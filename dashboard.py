import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="Traffic Analysis Dashboard",
    page_icon="🚗",
    layout="wide"
)

# Title and description
st.title("🚗 Traffic Analysis Dashboard")
st.markdown("""
This dashboard provides insights into traffic patterns and speed compliance data across multiple locations.
Select a location from the sidebar and use the filters to customize the view.
""")

def get_location_from_file(file_path):
    """Extract location name from the CSV file metadata."""
    try:
        # Read the first few lines to get the metadata
        with open(file_path, 'r') as f:
            header_lines = [next(f) for _ in range(6)]
        
        # Look for the location line (typically first line)
        for line in header_lines:
            if 'Location:' in line:
                # Extract the location name from the line containing 'Location:'
                # Split the line by commas and take the second value as the location
                parts = [part.strip() for part in line.split('Location:')[1].split(',') if part.strip()]
                if len(parts) > 1:
                    return parts[1]
                elif len(parts) == 1:
                    return parts[0]
                return "Unknown Location"
    except Exception:
        pass
    
    # Fallback to filename if location not found in metadata
    return Path(file_path).stem.split('-')[0].replace('_', ' ').title()

# Load and process data
@st.cache_data
def load_data(file_path):
    # Get the location name first
    location_name = get_location_from_file(file_path)
    
    # Load the actual data
    df = pd.read_csv(file_path, skiprows=6)
    df['Date/Time'] = pd.to_datetime(df['Date/Time'].str.split(' - ').str[0])
    df['Hour'] = df['Date/Time'].dt.hour
    
    # Calculate speed compliance
    speed_columns = [col for col in df.columns if col not in ['Date/Time', 'Hour', 'Total']]
    
    # Calculate compliant speeds (0-30 mph)
    df['Compliant'] = df[['0-20'] + [str(i) for i in range(21, 31) if str(i) in df.columns]].sum(axis=1)
    
    # Calculate non-compliant speeds (31+ mph)
    non_compliant_cols = [col for col in speed_columns 
                         if col not in ['0-20'] and 
                         (col != '45-99') and 
                         (col.isdigit() and int(col) > 30 if col.isdigit() else False)]
    if '45-99' in df.columns:
        non_compliant_cols.append('45-99')
    df['Non_Compliant'] = df[non_compliant_cols].sum(axis=1)
    
    return df, location_name

def get_available_locations():
    """Get list of available data files and their locations."""
    data_dir = Path('data')
    if not data_dir.exists():
        return {}
    
    locations = {}
    for file in data_dir.glob('*.csv'):
        location_name = get_location_from_file(str(file))
        locations[location_name] = str(file)
    
    return locations

# Sidebar
st.sidebar.header("Location and Filters")

# Get available locations
locations = get_available_locations()

if not locations:
    st.error("❌ No data files found. Please add CSV files to the 'data' directory.")
    st.stop()

# Location selector
selected_location = st.sidebar.selectbox(
    "Select Location",
    options=sorted(list(locations.keys())),
    index=0
)

# Load the data for selected location
try:
    df, location_name = load_data(locations[selected_location])
    # st.sidebar.success(f"📍 Showing data for {location_name}")
except FileNotFoundError:
    st.error(f"❌ Error: Could not find the data file for {selected_location}")
    st.stop()
except Exception as e:
    st.error(f"❌ Error loading data: {str(e)}")
    st.stop()

# Date range filter
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df['Date/Time'].min().date(), df['Date/Time'].max().date()),
    min_value=df['Date/Time'].min().date(),
    max_value=df['Date/Time'].max().date()
)

# Hour range filter
hour_range = st.sidebar.slider(
    "Hour Range",
    min_value=0,
    max_value=23,
    value=(0, 23)
)

# Filter the data
mask = (
    (df['Date/Time'].dt.date >= date_range[0]) &
    (df['Date/Time'].dt.date <= date_range[1]) &
    (df['Hour'].between(hour_range[0], hour_range[1]))
)
filtered_df = df[mask]

# Location Info
st.header(f"📍 {location_name} Traffic Analysis")
st.markdown(f"Analyzing traffic data from {date_range[0]} to {date_range[1]}")

# Display key metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Vehicles", f"{filtered_df['Total'].sum():,}")
    
with col2:
    avg_vehicles = filtered_df['Total'].mean()
    st.metric("Avg Vehicles/Hour", f"{avg_vehicles:.1f}")
    
with col3:
    peak_hour = filtered_df.loc[filtered_df['Total'].idxmax(), 'Hour']
    peak_vehicles = filtered_df['Total'].max()
    st.metric("Peak Hour", f"{peak_hour:02d}:00 ({peak_vehicles} vehicles)")
    
with col4:
    compliance_rate = (filtered_df['Compliant'].sum() / filtered_df['Total'].sum() * 100)
    st.metric("Speed Compliance", f"{compliance_rate:.1f}%")

# Create visualizations
st.header("📊 Detailed Analysis")

# 1. Traffic Volume by Hour
col1, col2 = st.columns(2)

with col1:
    st.subheader("Traffic Volume by Hour")
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=filtered_df, x='Hour', y='Total', color='skyblue', ax=ax1)
    ax1.set_xlabel('Hour of Day')
    ax1.set_ylabel('Total Vehicles')
    ax1.grid(True, alpha=0.3)
    st.pyplot(fig1)

# 2. Speed Distribution
with col2:
    st.subheader("Average Speed Distribution")
    speed_columns = [col for col in filtered_df.columns if col not in ['Date/Time', 'Hour', 'Total', 'Compliant', 'Non_Compliant']]
    speed_dist = filtered_df[speed_columns].mean()
    if '0-20' in speed_dist.index:
        speed_dist = speed_dist.drop('0-20')

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.barplot(x=speed_dist.index, y=speed_dist.values, color='lightgreen', ax=ax2)
    plt.xticks(rotation=45)
    ax2.set_xlabel('Speed (mph)')
    ax2.set_ylabel('Average Vehicle Count')
    ax2.grid(True, alpha=0.3)
    st.pyplot(fig2)

# 3. Speed Compliance by Hour
col3, col4 = st.columns(2)

with col3:
    st.subheader("Speed Compliance by Hour")
    compliance_data = pd.DataFrame({
        'Hour': filtered_df['Hour'],
        'Compliant': filtered_df['Compliant'],
        'Non-Compliant': filtered_df['Non_Compliant']
    })
    compliance_data_melted = pd.melt(compliance_data, id_vars=['Hour'], var_name='Compliance', value_name='Count')

    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=compliance_data_melted, x='Hour', y='Count', hue='Compliance', 
                palette=['lightgreen', 'salmon'], ax=ax3)
    ax3.set_xlabel('Hour of Day')
    ax3.set_ylabel('Vehicle Count')
    ax3.grid(True, alpha=0.3)
    st.pyplot(fig3)

# 4. Traffic Volume Over Time
with col4:
    st.subheader("Traffic Volume Over Time")
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    filtered_df.groupby('Date/Time')['Total'].sum().plot(ax=ax4, color='purple')
    ax4.set_xlabel('Date/Time')
    ax4.set_ylabel('Total Vehicles')
    ax4.grid(True, alpha=0.3)
    st.pyplot(fig4)

# Data Summary
st.header("📋 Data Summary")
if st.checkbox("Show Raw Data"):
    st.dataframe(filtered_df)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Dashboard created with Streamlit | Data refreshed on: {}</p>
</div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True) 