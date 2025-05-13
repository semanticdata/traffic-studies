# Traffic Studies

A comprehensive traffic analysis dashboard for Crystal, Minnesota, built with Streamlit. This project processes and visualizes traffic data collected from [PicoCount 2500](https://vehiclecounts.com/picocount-2500.html) traffic counters, providing detailed insights into traffic patterns, speed compliance, and vehicle classifications.

## 🌟 Features

- Interactive dashboard with real-time filtering by location, date, and time
- Comprehensive traffic metrics and visualizations
- Vehicle classification analysis
- Speed compliance monitoring
- Temporal traffic pattern analysis

## 🚀 Getting Started

### Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer and resolver

### Installation

1. Clone the repository

    ```shell
    git clone https://github.com/semanticdata/traffic-studies.git
    cd traffic-studies
    ```

2. Create and activate a virtual environment using uv

    ```shell
    uv venv
    .venv/Scripts/activate  # On Windows
    source .venv/bin/activate  # On Unix or MacOS
    ```

3. Install dependencies

    ```shell
    uv pip install -r requirements.txt
    ```

4. Run the dashboard

    ```shell
    streamlit run main.py
    ```

## 📊 Available Metrics

### Key Performance Indicators

- Total Vehicle Count
- Average Speed (Northbound/Eastbound and Southbound/Westbound)
- Speed Compliance Rate
- Daily Traffic (Average and Maximum)
- Peak Hour Statistics
- Dominant Direction Analysis
- 85th Percentile Speed
- Peak Hour Factor (PHF)
- High Speed Violation Tracking
- Weekday/Weekend Traffic Ratio

### Traffic Analysis

- Hourly Volume Distribution (by direction)
- Daily Traffic Patterns
- Speed Distribution Analysis
- Speed Violation Severity (+5, +10, +15 mph over limit)
- Directional Speed Compliance

### Vehicle Classifications

- 🏍️ Class 1: Motorcycles
- 🚗 Class 2: Passenger Cars
- 🚐 Class 3: Pickups, Vans
- 🚌 Class 4: Buses
- 🚛 Class 5: 2 Axles, 6 Tires
- 🚛 Class 6: 3 Axles

## 📝 Data Sources

Traffic data is collected using PicoCount 2500 traffic counters and processed through TrafficViewer Pro software. The dashboard provides a user-friendly interface for analyzing this data, making it accessible for traffic planning and decision-making purposes.

## 📜 License

This project is licensed under the [MIT License](LICENSE).
