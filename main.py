"""
Traffic Studies Dashboard - Main Application

A comprehensive traffic analysis dashboard for Crystal, Minnesota, built with Streamlit.
Multi-page application with navigation between map view and detailed location analysis.

Author: Miguel Pimentel
License: MIT
"""

import streamlit as st


def main() -> None:
    """Main application function with page navigation."""
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

    # Define pages
    map_page = st.Page("pages/map_page.py", title="Location Map", icon="🗺️", default=True)

    analysis_page = st.Page("pages/location_analysis.py", title="Traffic Analysis", icon="📊")

    # Create navigation
    pg = st.navigation([map_page, analysis_page], position="top")

    # Run the selected page
    pg.run()


if __name__ == "__main__":
    main()
