"""
Traffic Study Locations Map Page

Interactive map showing all traffic study locations in Crystal, Minnesota.
Users can view and select locations to navigate to detailed analysis.
"""

import pandas as pd
import pydeck as pdk
import streamlit as st

from utils.data_loader import get_available_locations


def load_location_data() -> pd.DataFrame:
    """Load and process location data from Locations.csv."""
    try:
        locations_df = pd.read_csv("data/Locations.csv")
        # Filter out rows with missing lat/lon
        locations_df = locations_df.dropna(subset=["Latitude", "Longitude"])
        return locations_df
    except FileNotFoundError:
        return pd.DataFrame()
    except Exception:
        return pd.DataFrame()


def match_traffic_study_locations(locations_df: pd.DataFrame, available_locations: dict) -> pd.DataFrame:
    """Match location data with available traffic studies and include traffic metrics."""
    if locations_df.empty:
        return pd.DataFrame()

    matched_locations = []

    # Import here to avoid circular imports
    from utils.data_loader import load_data
    from utils.metrics import get_core_metrics

    for _, row in locations_df.iterrows():
        address = str(row["Address"]).strip()
        if address and address != "nan":
            # Try to find a matching traffic study
            for study_name in available_locations.keys():
                # Clean the study name for comparison
                clean_study = study_name.replace("_", " ").replace("-ALL", "").strip()
                if address.lower() in clean_study.lower() or clean_study.lower() in address.lower():
                    # Determine color based on notes (school zones get different color)
                    notes = str(row.get("Notes", "")).strip()
                    is_school = "SCHOOL" in notes.upper()

                    # PyDeck color format: [R, G, B] values 0-255
                    color = [255, 107, 107] if is_school else [78, 205, 196]  # Red for schools, teal for regular

                    # Size based on site ID (higher IDs = larger dots for visibility)
                    site_id = str(row.get("Site", "0"))
                    try:
                        radius = min(60, max(30, int(site_id) // 1000)) if site_id.isdigit() else 40
                    except (ValueError, TypeError, ZeroDivisionError):
                        radius = 40

                    # Load traffic metrics for tooltip
                    try:
                        df, _, structure = load_data(available_locations[study_name])
                        metrics = get_core_metrics(df, structure)
                        adt = f"{metrics['adt']:,.0f}"
                        percentile_85th = f"{metrics['percentile_85th']:.1f} mph"
                        compliance_rate = f"{metrics['compliance_rate']:.1f}%"
                        posted_speed = f"{metrics['posted_speed']} mph"
                    except Exception:
                        # Fallback values if metrics can't be loaded
                        adt = "N/A"
                        percentile_85th = "N/A"
                        compliance_rate = "N/A"
                        posted_speed = "N/A"

                    # Clean notes for display
                    display_notes = notes if notes and notes != "nan" else ""

                    matched_locations.append(
                        {
                            "lat": row["Latitude"],
                            "lon": row["Longitude"],
                            "address": address,
                            "study_location": study_name,
                            "site_id": site_id,
                            "notes": display_notes,
                            "color": color,
                            "radius": radius,
                            "type": "School Zone" if is_school else "Regular Traffic Study",
                            "adt": adt,
                            "percentile_85th": percentile_85th,
                            "compliance_rate": compliance_rate,
                            "posted_speed": posted_speed,
                            "location_name": clean_study,
                        }
                    )
                    break

    return pd.DataFrame(matched_locations)


def main():
    """Main function for the map page."""
    st.title("🗺️ Traffic Study Locations")
    st.markdown(
        "Explore traffic study locations across Crystal, Minnesota. "
        "Select a location to view detailed analysis and reports."
    )

    # Load location data with spinner
    with st.spinner("Loading traffic study locations..."):
        available_locations = get_available_locations()
        locations_df = load_location_data()
        matched_locations = match_traffic_study_locations(locations_df, available_locations)

    # Create location options including ALL available locations (before map display for click handling)
    location_options = {}

    # First add locations with coordinates (from matched_locations)
    if not matched_locations.empty:
        for _, row in matched_locations.iterrows():
            display_name = f"{row['address']}"
            if row["notes"] and row["notes"] != "nan":
                display_name += f" ({row['notes']})"
            location_options[display_name] = row["study_location"]

    # Then add locations without coordinates (from available_locations but not in matched_locations)
    matched_study_names = set(matched_locations["study_location"].tolist()) if not matched_locations.empty else set()
    for study_name in available_locations.keys():
        if study_name not in matched_study_names:
            # Clean name for display
            clean_name = study_name.replace("_", " ").replace("-ALL", "").strip()
            display_name = f"{clean_name} (No map coordinates)"
            location_options[display_name] = study_name

    # Display map if we have locations with coordinates
    if not matched_locations.empty:
        # Create PyDeck layer for interactive map with hover tooltips
        scatterplot_layer = pdk.Layer(
            "ScatterplotLayer",
            data=matched_locations,
            id="traffic-locations",
            get_position=["lon", "lat"],
            get_color="color",
            get_radius="radius",
            pickable=True,
            auto_highlight=True,
        )

        # Calculate center point for Crystal, Minnesota area
        center_lat = matched_locations["lat"].mean()
        center_lon = matched_locations["lon"].mean()

        # Create the view state
        view_state = pdk.ViewState(latitude=center_lat, longitude=center_lon, zoom=13, pitch=0, controller=True)

        # Create the deck with tooltip configuration
        deck = pdk.Deck(
            layers=[scatterplot_layer],
            initial_view_state=view_state,
            tooltip={
                "text": (
                    "{address}\nType: {type}\nADT: {adt}\n"
                    "85th Percentile: {percentile_85th}\nCompliance: {compliance_rate}\n"
                    "Posted Speed: {posted_speed}"
                )
            },
        )

        # Display the interactive map with event handling
        event = st.pydeck_chart(
            deck,
            use_container_width=True,
            height=600,
            on_select="rerun",
            selection_mode="single-object",
        )

        # Handle map click events - automatically select clicked location
        if event.selection:
            try:
                # Extract clicked object data from the PyDeck event structure
                if (
                    "objects" in event.selection
                    and "traffic-locations" in event.selection["objects"]
                    and len(event.selection["objects"]["traffic-locations"]) > 0
                ):
                    clicked_data = event.selection["objects"]["traffic-locations"][0]
                    clicked_study_location = clicked_data.get("study_location")

                    # Only process if this is a new selection (not already in session state)
                    current_selection = st.session_state.get("selected_location")
                    if clicked_study_location and clicked_study_location != current_selection:
                        # Store the clicked location in session state
                        st.session_state["selected_location"] = clicked_study_location

                        # Find the display name for the clicked location
                        clicked_display_name = None
                        for display_name, study_location in location_options.items():
                            if study_location == clicked_study_location:
                                clicked_display_name = display_name
                                break

                        if clicked_display_name:
                            st.success(f"📍 Selected: **{clicked_display_name}**")
                        else:
                            st.success(f"📍 Selected: **{clicked_study_location}**")

                        st.rerun()  # Rerun only once for new selections

            except Exception as e:
                st.error(f"Error processing click: {e}")
                st.info("Please try clicking directly on a location dot")

        # Add legend
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**🎯 Map Legend:**")
            st.markdown("🔴 **Red dots**: School zone traffic studies")
            st.markdown("🔵 **Teal dots**: Regular traffic studies")
            st.markdown("📏 **Dot size**: Varies by site ID")

        with col2:
            school_count = len(matched_locations[matched_locations["type"] == "School Zone"])
            regular_count = len(matched_locations[matched_locations["type"] == "Regular Traffic Study"])
            st.metric("🏫 School Zones", school_count)
            st.metric("🚗 Regular Studies", regular_count)

        st.info(f"📊 Showing {len(matched_locations)} traffic study locations with coordinate data on map")
    else:
        st.warning("📍 No traffic study locations found with coordinate data for map display")
        st.info("Locations without coordinates are still available for analysis in the selection below.")

    st.divider()

    # Location Selection Section (always show this)
    st.subheader("📍 Select Location for Analysis")

    # Show helpful message about map interaction (removed redundant tip)

    # Determine default selection based on session state or clicked location
    default_index = None
    selected_from_session = st.session_state.get("selected_location")
    if selected_from_session:
        # Find the display name for the session state location
        for display_name, study_location in location_options.items():
            if study_location == selected_from_session:
                # Find index in sorted list
                sorted_options = sorted(list(location_options.keys()))
                default_index = sorted_options.index(display_name)
                break

    selected_display = st.selectbox(
        "Choose a location to analyze:",
        options=sorted(list(location_options.keys())),
        index=default_index,
        placeholder="Select a traffic study location...",
    )

    if selected_display:
        selected_location = location_options[selected_display]

        # Store selected location in session state
        st.session_state["selected_location"] = selected_location

        # Check if location has coordinates (is in matched_locations)
        location_has_coords = (
            selected_location in matched_locations["study_location"].values if not matched_locations.empty else False
        )

        if not location_has_coords:
            st.warning(
                "⚠️ This location doesn't have latitude/longitude coordinates and cannot be displayed on the map."
            )

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
                    help="Total vehicles per day on average",
                )

            with metric_col2:
                st.metric(
                    "🎯 85th Percentile Speed",
                    f"{metrics['percentile_85th']:.1f} mph",
                    help="Speed that 85% of vehicles travel at or below",
                )

            with metric_col3:
                st.metric(
                    "🚦 Speed Compliance",
                    f"{metrics['compliance_rate']:.1f}%",
                    help="Percentage of vehicles traveling at or below speed limit",
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
        st.info(
            f"📊 Total locations: {total_locations} "
            f"({locations_with_coords} with map coordinates, {locations_without_coords} without coordinates)"
        )
    else:
        st.info(f"📊 All {total_locations} traffic study locations have coordinate data")


if __name__ == "__main__":
    main()
