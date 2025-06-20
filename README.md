# Traffic Studies

A comprehensive traffic analysis dashboard for Crystal, Minnesota, built with Streamlit. This project processes and visualizes traffic data collected from [PicoCount 2500](https://vehiclecounts.com/picocount-2500.html) traffic counters, providing detailed insights into traffic patterns, speed compliance, and vehicle classifications.

## 🌟 Features

- **Interactive Dashboard**: Real-time filtering by location, date range, and time periods
- **Comprehensive Metrics**: 12+ key performance indicators including speed compliance, peak hour analysis, and traffic volume
- **Vehicle Classification**: Detailed analysis of 6 vehicle classes from motorcycles to heavy trucks
- **Speed Analysis**: Compliance monitoring, violation severity tracking, and 85th percentile calculations
- **Temporal Patterns**: Hourly, daily, and weekly traffic pattern visualization
- **Multi-format Visualizations**: Both Matplotlib and Plotly charts for different analysis needs

## 🏗️ Project Structure

```text
traffic-studies/
├── main.py                 # Main Streamlit dashboard application
├── utils/
│   ├── data_loader.py     # Data loading and CSV parsing utilities
│   ├── visualizations.py # Chart generation and plotting functions
│   └── styles.css         # Custom CSS styling for the dashboard
├── data/                  # Directory for CSV data files
├── pyproject.toml         # Project dependencies and metadata
└── README.md              # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer and resolver

### Installation

1. **Clone the repository**

   ```shell
   git clone https://github.com/semanticdata/traffic-studies.git
   cd traffic-studies
   ```

2. **Create and activate a virtual environment**

   ```shell
   uv venv
   .venv/Scripts/activate  # On Windows
   source .venv/bin/activate  # On Unix or MacOS
   ```

3. **Install dependencies**

   ```shell
   uv sync
   ```

4. **Add your data files**

   Place your CSV files from TrafficViewer Pro in the `data/` directory

5. **Run the dashboard**

   ```shell
   streamlit run main.py
   ```

The dashboard will open in your web browser at `http://localhost:8501`

## 📊 Available Metrics

### Key Performance Indicators

- **Total Vehicle Count**: Aggregate count of all vehicles detected
- **Average Speed**: Directional speed analysis (Northbound/Eastbound and Southbound/Westbound)
- **Speed Compliance Rate**: Percentage of vehicles adhering to speed limits
- **Daily Traffic**: Average and maximum daily vehicle counts
- **Peak Hour Statistics**: Busiest hour identification and vehicle counts
- **Dominant Direction Analysis**: Traffic flow direction preferences
- **85th Percentile Speed**: Critical speed measurement for traffic engineering
- **Peak Hour Factor (PHF)**: Traffic flow consistency measurement
- **High Speed Violation Tracking**: Vehicles exceeding speed limits by 15+ mph
- **Weekday/Weekend Traffic Ratio**: Temporal traffic pattern comparison

### Traffic Analysis Visualizations

#### 1. Hourly Volume Distribution

Displays the average number of vehicles per hour for each direction of traffic. The stacked bar chart shows the breakdown of traffic volume, making it easy to identify peak hours and directional traffic patterns throughout the day.

#### 2. Speed Distribution Analysis

Shows the distribution of vehicle speeds in different ranges for each direction. The bar charts help identify common speed patterns and compare speed distributions between different traffic directions.

#### 3. Speed Compliance Visualization

Presents the compliance rate with speed limits through a donut chart, showing the percentage of vehicles that were compliant versus non-compliant. This helps quickly assess overall speed limit adherence.

#### 4. Speed Violation Severity

Categorizes speeding violations by severity (+5, +10, +15 mph over the limit) using a bar chart. This helps identify the most common types of speed violations and their relative frequencies.

#### 5. Speeding by Hour of Day

Combines bar and line charts to show both the total number of vehicles and the percentage of vehicles speeding for each hour. This dual-axis visualization helps identify patterns in speeding behavior throughout the day.

#### 6. Temporal Traffic Patterns

Illustrates how traffic volume varies by day of week and hour of day using a heatmap. This helps identify weekly patterns, peak periods, and off-peak times.

#### 7. Vehicle Classification Distribution

Shows the distribution of different vehicle classes (from motorcycles to heavy trucks) using pie charts. This helps understand the composition of traffic in terms of vehicle types.

### Vehicle Classifications

The dashboard analyzes six FHWA vehicle classes:

- 🏍️ **Class 1**: Motorcycles
- 🚗 **Class 2**: Passenger Cars
- 🚐 **Class 3**: Pickups, Vans
- 🚌 **Class 4**: Buses
- 🚛 **Class 5**: 2 Axles, 6 Tires
- 🚛 **Class 6**: 3 Axles

## 📁 Data Format

The application expects CSV files exported from TrafficViewer Pro with the following structure:

- **Metadata rows**: Location, comments, and title information
- **Date/Time column**: Timestamp for each data point
- **Volume columns**: Directional traffic counts
- **Speed range columns**: Speed distribution data (e.g., "35-39 MPH - Northbound")
- **Classification columns**: Vehicle class counts by direction

## 🎯 Use Cases

- **Traffic Engineering**: Speed limit assessment and road safety analysis
- **Urban Planning**: Peak hour identification and capacity planning
- **Policy Making**: Data-driven traffic management decisions
- **Research**: Academic traffic pattern studies
- **Compliance Monitoring**: Speed enforcement effectiveness evaluation

## 🔧 Technical Details

### Dependencies

- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Matplotlib**: Static plotting and visualization
- **Plotly**: Interactive charting
- **Seaborn**: Statistical data visualization
- **NumPy**: Numerical computing

### Performance

- Handles large datasets efficiently through pandas optimization
- Interactive filtering with real-time updates
- Responsive design for desktop and tablet viewing

## 📝 Data Sources

Traffic data is collected using [PicoCount 2500](https://vehiclecounts.com/picocount-2500.html) traffic counters and processed through [TrafficViewer Pro](https://vehiclecounts.com/trafficviewerpro.html) software. The dashboard provides a user-friendly interface for analyzing this data, making it accessible for traffic planning and decision-making purposes.

## 📜 License

This project is licensed under the [MIT License](LICENSE).

## Common Issues

- Ensure CSV files have proper TrafficViewer Pro metadata rows
- Check that column names match expected patterns
- Verify Date/Time column format
- Large datasets may cause slow filtering - consider data sampling for very large files
- Caching can be added with `@st.cache_data` decorator for expensive operations
- Matplotlib figures should use `plt.tight_layout()` for proper spacing
- Always return Figure objects, not display them directly
