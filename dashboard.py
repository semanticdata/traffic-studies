# This is the main dashboard for the traffic analysis project.
# It will display the data and allow for filtering and visualization.

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="Traffic Analysis Dashboard",
    page_icon="🚗",
    layout="wide"
)

# Load and process data
@st.cache_data
def load_data(file_path):
    # Detect file structure
    structure = detect_file_structure(file_path)
    if not structure:
        raise ValueError("Could not detect file structure")
    
    # Get the location name and ensure it's clean
    location_name = structure['location']
    if location_name and isinstance(location_name, str):
        location_name = location_name.strip().strip('"').strip("'").strip(',').strip()
    
    try:
        # Read the CSV with proper parameters
        df = pd.read_csv(file_path, skiprows=structure['metadata_rows'])
        
        # Convert Date/Time to datetime using the specific format from the file
        df['Date/Time'] = pd.to_datetime(df['Date/Time'], errors='coerce')
        df['Hour'] = df['Date/Time'].dt.hour
        
        # Calculate speed compliance for both directions
        dir1_speed_cols = structure['dir1_speed_cols']
        dir2_speed_cols = structure['dir2_speed_cols']
        
        df['Dir1_Compliant'] = df[dir1_speed_cols].apply(lambda x: (x <= 30).sum(), axis=1)
        df['Dir1_Non_Compliant'] = df[dir1_speed_cols].apply(lambda x: (x > 30).sum(), axis=1)
        
        df['Dir2_Compliant'] = df[dir2_speed_cols].apply(lambda x: (x <= 30).sum(), axis=1)
        df['Dir2_Non_Compliant'] = df[dir2_speed_cols].apply(lambda x: (x > 30).sum(), axis=1)
        
        # Calculate total volumes
        df['Total'] = df[structure['dir1_volume_col']] + df[structure['dir2_volume_col']]
        
        return df, location_name, structure
        
    except Exception as e:
        st.error(f"Error loading data: {e} (and I thought I was the only one with issues!)")
        raise

def get_location_from_file(file_path):
    """Extract location name from the CSV file metadata."""
    try:
        # Read the first few lines to get the metadata
        with open(file_path, 'r') as f:
            header_lines = [next(f) for _ in range(6)]
        
        # Look for the location line
        for line in header_lines:
            if 'Location:' in line:
                # Strip quotes, commas, and whitespace from both ends of the location string
                location = line.split('Location:')[1].strip().strip('"').strip("'").strip(',').strip()
                return location
        
        # Fallback to filename if location not found in metadata
        return Path(file_path).stem.split('-')[1].replace('_', ' ').strip().strip('"').strip("'").title()
    except Exception:
        return Path(file_path).stem.split('-')[1].replace('_', ' ').strip().strip('"').strip("'").title()

def detect_file_structure(file_path):
    """Detect the structure of the CSV file and return appropriate parsing parameters."""
    try:
        with open(file_path, 'r') as f:
            header_lines = [next(f) for _ in range(15)]
        
        # Extract metadata information
        location = None
        comments = None
        title = None
        
        for line in header_lines:
            if 'Location:' in line:
                # Handle CSV formatted line with quotes
                parts = line.strip().split('","')  # Split on CSV delimiter
                if len(parts) > 1:
                    # Remove remaining quotes and clean
                    location = parts[1].replace('"', '').strip()
                else:
                    # Fallback to original method
                    location = line.split('Location:')[1].strip().strip('"').strip("'").strip(',').strip()
            elif 'Comments:' in line:
                comments = line.split('Comments:')[1].strip().strip('"').strip(',')
            elif 'Title:' in line:
                title = line.split('Title:')[1].strip().strip('"').strip(',')
        
        # Find data columns
        column_line = None
        for i, line in enumerate(header_lines):
            if 'Date/Time' in line:
                column_line = line
                metadata_rows = i
                break
        
        if column_line:
            columns = [col.strip().strip('"') for col in column_line.split(',')]
            
            # Detect direction pairs based on column names
            dir1_speed_cols = [col for col in columns if 'MPH  - Northbound' in col]
            dir2_speed_cols = [col for col in columns if 'MPH  - Southbound' in col]
            
            # If no N/S columns found, try E/W
            if not (dir1_speed_cols and dir2_speed_cols):
                dir1_speed_cols = [col for col in columns if 'MPH  - Eastbound' in col]
                dir2_speed_cols = [col for col in columns if 'MPH  - Westbound' in col]
            
            # Determine the direction pairs
            if 'Northbound' in ''.join(columns):
                dir1_name = 'Northbound'
                dir2_name = 'Southbound'
            else:
                dir1_name = 'Eastbound'
                dir2_name = 'Westbound'
            
            return {
                'metadata_rows': metadata_rows,
                'columns': columns,
                'location': location,
                'comments': comments,
                'title': title,
                'dir1_name': dir1_name,
                'dir2_name': dir2_name,
                'dir1_speed_cols': dir1_speed_cols,
                'dir2_speed_cols': dir2_speed_cols,
                'dir1_volume_col': f'Volume - {dir1_name}',
                'dir2_volume_col': f'Volume - {dir2_name}'
            }
    except Exception as e:
        print(f"Error detecting file structure: {e}")
        return None

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
st.sidebar.header("Traffic Analysis Dashboard")
st.sidebar.markdown("""Please select a location and set your desired date and hour filters to analyze the traffic data.""") 
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
    index=0,
    format_func=lambda x: x.strip().strip('"').strip("'").strip(',').strip()
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
st.header(f"📍 {location_name} - Traffic Study")
st.markdown(f"Analyzing traffic data from _{date_range[0]}_ to _{date_range[1]}_.")

# Display key metrics
col1, col2 = st.columns(2)

with col1:
    st.metric("Total Vehicles", f"{filtered_df['Total'].sum():,}")

with col2:
    dir1_volume = filtered_df[structure['dir1_volume_col']].sum()
    dir2_volume = filtered_df[structure['dir2_volume_col']].sum()
    dominant_direction = structure['dir1_name'] if dir1_volume > dir2_volume else structure['dir2_name']
    dominant_pct = max(dir1_volume, dir2_volume) / (dir1_volume + dir2_volume) * 100
    st.metric("Dominant Direction", f"{dominant_direction} ({dominant_pct:.1f}%)")

# New row for the next two metrics
col3, col4 = st.columns(2)

with col3:
    peak_hour = filtered_df.loc[filtered_df['Total'].idxmax(), 'Hour']
    peak_vehicles = filtered_df['Total'].max()
    st.metric("Peak Hour", f"{peak_hour:02d}:00 ({peak_vehicles} vehicles)")

with col4:
    total_compliant = filtered_df['Dir1_Compliant'].sum() + filtered_df['Dir2_Compliant'].sum()
    total_volume = filtered_df['Total'].sum()
    compliance_rate = (total_compliant / total_volume * 100) if total_volume > 0 else 0
    st.metric("Speed Compliance", f"{compliance_rate:.1f}%")

# Create visualizations
st.header("📊 Detailed Analysis")

# 1. Directional Traffic Volume by Hour
st.subheader("Directional Traffic Volume by Hour")
hourly_volumes = filtered_df.groupby('Hour').agg({
    structure['dir1_volume_col']: 'mean',
    structure['dir2_volume_col']: 'mean'
}).reset_index()

fig1, ax1 = plt.subplots(figsize=(15, 8))
ax1.bar(hourly_volumes['Hour'], hourly_volumes[structure['dir1_volume_col']], 
        label=structure['dir1_name'], alpha=0.7, color='skyblue')
ax1.bar(hourly_volumes['Hour'], hourly_volumes[structure['dir2_volume_col']], 
        bottom=hourly_volumes[structure['dir1_volume_col']], 
        label=structure['dir2_name'], alpha=0.7, color='lightgreen')
ax1.set_xlabel('Hour of Day')
ax1.set_ylabel('Average Vehicles per Hour')
ax1.legend()
ax1.grid(True, alpha=0.3)
st.pyplot(fig1)

# 2. Speed Distribution by Direction
st.subheader("Speed Distribution by Direction")

# Calculate average speeds for both directions
dir1_speeds = filtered_df[structure['dir1_speed_cols']].mean()
dir2_speeds = filtered_df[structure['dir2_speed_cols']].mean()

fig2, (ax2a, ax2b) = plt.subplots(2, 1, figsize=(15, 12))

# Direction 1 speeds
sns.barplot(x=[col.split('-')[0].strip() for col in structure['dir1_speed_cols']], 
            y=dir1_speeds, color='skyblue', ax=ax2a)
ax2a.set_title(f'{structure["dir1_name"]} Speed Distribution')
ax2a.set_xlabel('Speed Range (MPH)')
ax2a.set_ylabel('Average Vehicle Count')
ax2a.tick_params(axis='x', rotation=45)

# Direction 2 speeds
sns.barplot(x=[col.split('-')[0].strip() for col in structure['dir2_speed_cols']], 
            y=dir2_speeds, color='lightgreen', ax=ax2b)
ax2b.set_title(f'{structure["dir2_name"]} Speed Distribution')
ax2b.set_xlabel('Speed Range (MPH)')
ax2b.set_ylabel('Average Vehicle Count')
ax2b.tick_params(axis='x', rotation=45)

plt.tight_layout()
st.pyplot(fig2)

# 3. Speed Compliance by Direction
st.subheader("Speed Compliance by Direction")
compliance_data = pd.DataFrame({
    'Direction': [structure['dir1_name'], structure['dir1_name'], structure['dir2_name'], structure['dir2_name']],
    'Compliance': ['Compliant', 'Non-Compliant', 'Compliant', 'Non-Compliant'],
    'Count': [
        filtered_df['Dir1_Compliant'].sum(),
        filtered_df['Dir1_Non_Compliant'].sum(),
        filtered_df['Dir2_Compliant'].sum(),
        filtered_df['Dir2_Non_Compliant'].sum()
    ]
})

fig3, ax3 = plt.subplots(figsize=(15, 8))
sns.barplot(data=compliance_data, x='Direction', y='Count', hue='Compliance',
            palette=['lightgreen', 'salmon'], ax=ax3)
ax3.set_ylabel('Vehicle Count')
ax3.grid(True, alpha=0.3)
st.pyplot(fig3)

# 4. Traffic Volume Over Time by Direction
st.subheader("Traffic Volume Over Time")
fig4, ax4 = plt.subplots(figsize=(15, 8))
ax4.plot(filtered_df['Date/Time'], filtered_df[structure['dir1_volume_col']], 
         label=structure['dir1_name'], color='skyblue', alpha=0.7)
ax4.plot(filtered_df['Date/Time'], filtered_df[structure['dir2_volume_col']], 
         label=structure['dir2_name'], color='lightgreen', alpha=0.7)
ax4.set_xlabel('Date/Time')
ax4.set_ylabel('Vehicles')
ax4.legend()
ax4.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
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
