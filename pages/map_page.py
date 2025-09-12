"""
Traffic Study Locations Map Page

Interactive map showing all traffic study locations in Crystal, Minnesota.
Users can view and select locations to navigate to detailed analysis.
"""

import pandas as pd
import streamlit as st

from utils.data_loader import get_available_locations


def load_location_data() -> pd.DataFrame:
    """Load and process location data from Locations.csv."""
    try:
        locations_df = pd.read_csv("data/Locations.csv")
        # Filter out rows with missing lat/lon
        locations_df = locations_df.dropna(subset=['Latitude', 'Longitude'])
        return locations_df
    except FileNotFoundError:
        return pd.DataFrame()
    except Exception:
        return pd.DataFrame()


def match_traffic_study_locations(locations_df: pd.DataFrame, available_locations: dict) -> pd.DataFrame:
    """Match location data with available traffic studies."""
    if locations_df.empty:
        return pd.DataFrame()
    
    matched_locations = []
    
    for _, row in locations_df.iterrows():
        address = str(row['Address']).strip()
        if address and address != 'nan':
            # Try to find a matching traffic study
            for study_name in available_locations.keys():
                # Clean the study name for comparison
                clean_study = study_name.replace('_', ' ').replace('-ALL', '').strip()
                if address.lower() in clean_study.lower() or clean_study.lower() in address.lower():
                    # Determine color based on notes (school zones get different color)
                    notes = str(row.get('Notes', '')).strip()
                    is_school = 'SCHOOL' in notes.upper()
                    color = '#FF6B6B' if is_school else '#4ECDC4'  # Red for schools, teal for regular
                    
                    # Size based on site ID (higher IDs = larger dots for visibility)
                    site_id = str(row.get('Site', '0'))
                    try:
                        size = min(60, max(30, int(site_id) // 1000)) if site_id.isdigit() else 40
                    except:
                        size = 40
                    
                    matched_locations.append({
                        'lat': row['Latitude'],
                        'lon': row['Longitude'], 
                        'address': address,
                        'study_location': study_name,
                        'site_id': site_id,
                        'notes': notes,
                        'color': color,
                        'size': size,
                        'type': 'School Zone' if is_school else 'Regular Traffic Study'
                    })
                    break
    
    return pd.DataFrame(matched_locations)


def main():
    """Main function for the map page."""
    st.title("🗺️ Traffic Study Locations")
    st.markdown(
        "Explore traffic study locations across Crystal, Minnesota. "
        "Select a location to view detailed analysis and reports."
    )
    
    # Load location data
    available_locations = get_available_locations()
    locations_df = load_location_data()
    matched_locations = match_traffic_study_locations(locations_df, available_locations)
    
    # Display map if we have locations with coordinates
    if not matched_locations.empty:
        # Display the map with color coding and variable sizes
        st.map(
            matched_locations[['lat', 'lon', 'color', 'size']], 
            color='color',    # Use color column for dot colors
            size='size',      # Use size column for dot sizes  
            zoom=13,          # Adjustable zoom level
            height=600,       # Adjustable map height
        )
        
        # Add legend
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**🎯 Map Legend:**")
            st.markdown("🔴 **Red dots**: School zone traffic studies")
            st.markdown("🔵 **Teal dots**: Regular traffic studies")
            st.markdown("📏 **Dot size**: Varies by site ID")
        
        with col2:
            school_count = len(matched_locations[matched_locations['type'] == 'School Zone'])
            regular_count = len(matched_locations[matched_locations['type'] == 'Regular Traffic Study'])
            st.metric("🏫 School Zones", school_count)
            st.metric("🚗 Regular Studies", regular_count)
        
        st.info(f"📊 Showing {len(matched_locations)} traffic study locations with coordinate data on map")
    else:
        st.warning("📍 No traffic study locations found with coordinate data for map display")
        st.info("Locations without coordinates are still available for analysis in the selection below.")
    
    st.divider()
    
    # Location Selection Section (always show this)
    st.subheader("📍 Select Location for Analysis")
    
    # Create location options including ALL available locations
    location_options = {}
    
    # First add locations with coordinates (from matched_locations)
    if not matched_locations.empty:
        for _, row in matched_locations.iterrows():
            display_name = f"{row['address']}"
            if row['notes'] and row['notes'] != 'nan':
                display_name += f" ({row['notes']})"
            location_options[display_name] = row['study_location']
    
    # Then add locations without coordinates (from available_locations but not in matched_locations)
    matched_study_names = set(matched_locations['study_location'].tolist()) if not matched_locations.empty else set()
    for study_name in available_locations.keys():
        if study_name not in matched_study_names:
            # Clean name for display
            clean_name = study_name.replace('_', ' ').replace('-ALL', '').strip()
            display_name = f"{clean_name} (No map coordinates)"
            location_options[display_name] = study_name
    
    selected_display = st.selectbox(
        "Choose a location to analyze:",
        options=list(location_options.keys()),
        index=None,
        placeholder="Select a traffic study location..."
    )
    
    if selected_display:
        selected_location = location_options[selected_display]
        
        # Store selected location in session state
        st.session_state['selected_location'] = selected_location
        
        # Check if location has coordinates (is in matched_locations)
        location_has_coords = selected_location in matched_locations['study_location'].values if not matched_locations.empty else False
        
        if not location_has_coords:
            st.warning("⚠️ This location doesn't have latitude/longitude coordinates and cannot be displayed on the map.")
        
        # Load and display core metrics for selected location
        try:
            from utils.data_loader import load_data
            from utils.metrics import get_core_metrics
            
            # Load data for the selected location
            df, location_name, structure = load_data(available_locations[selected_location])
            
            # Get core metrics
            metrics = get_core_metrics(df, structure)
            
            # Display key metrics
            st.markdown("##### 📈 Quick Traffic Overview")
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            
            with metric_col1:
                st.metric(
                    "📅 Average Daily Traffic", 
                    f"{metrics['adt']:,.0f}",
                    help="Total vehicles per day on average"
                )
            
            with metric_col2:
                st.metric(
                    "🎯 85th Percentile Speed", 
                    f"{metrics['percentile_85th']:.1f} mph",
                    help="Speed that 85% of vehicles travel at or below"
                )
            
            with metric_col3:
                st.metric(
                    "🚦 Speed Compliance", 
                    f"{metrics['compliance_rate']:.1f}%",
                    help="Percentage of vehicles traveling at or below speed limit"
                )
                
        except Exception as e:
            st.warning(f"Unable to load metrics for this location: {str(e)}")
        
        # Navigation button
        if st.button("📊 View Detailed Analysis", type="primary", width="stretch"):
            st.switch_page("pages/location_analysis.py")
    
    # Show total count info
    total_locations = len(available_locations)
    locations_with_coords = len(matched_locations) if not matched_locations.empty else 0
    locations_without_coords = total_locations - locations_with_coords
    
    if locations_without_coords > 0:
        st.info(f"📊 Total locations: {total_locations} ({locations_with_coords} with map coordinates, {locations_without_coords} without coordinates)")
    else:
        st.info(f"📊 All {total_locations} traffic study locations have coordinate data")


if __name__ == "__main__":
    main()