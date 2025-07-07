# Traffic Studies

A comprehensive traffic analysis dashboard for Crystal, Minnesota, built with Streamlit. This project processes and visualizes traffic data collected from [PicoCount 2500](https://vehiclecounts.com/picocount-2500.html) traffic counters, providing detailed insights into traffic patterns, speed compliance, and vehicle classifications.

## 🌟 Features

- **Interactive Dashboard**: Real-time filtering by location, date range, and time periods
- **Core Metrics**: 6 essential key performance indicators including speed compliance, peak hour analysis, and traffic volume
- **Vehicle Classification**: Detailed analysis of 6 vehicle classes from motorcycles to heavy trucks
- **Speed Analysis**: Compliance monitoring, violation severity tracking, and 85th percentile calculations
- **Temporal Patterns**: Hourly, daily, and weekly traffic pattern visualization
- **Professional Visualizations**: Matplotlib charts with consistent styling and clear presentation
- **Enhanced Data Processing**: Advanced validation, vectorized operations, and zero-traffic filtering
- **Performance Optimization**: Memory-efficient processing for large datasets with chunked loading
- **Data Quality Monitoring**: Comprehensive validation with detailed error reporting and statistics

## 🏗️ Project Structure

```text
traffic-studies/
├── main.py                # Main Streamlit dashboard
├── utils/
│   ├── data_loader.py     # Enhanced data loading with validation and optimization
│   ├── metrics.py         # Traffic metrics and KPI calculations
│   ├── visualizations.py  # Chart generation and plotting functions
│   └── styles.css         # Custom CSS styling for the dashboard
├── tests/                 # Test suite
│   ├── conftest.py        # Test fixtures and sample data
│   ├── test_metrics.py    # Tests for metrics calculations
│   ├── test_data_loader.py # Tests for data loading
│   └── test_visualizations.py # Tests for chart generation
├── .streamlit/
│   └── config.toml        # Streamlit configuration settings
├── data/                  # Directory for CSV data files
├── pyproject.toml         # Project dependencies and metadata
├── CLAUDE.md              # AI assistant guidance file
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
   uv run streamlit run main.py
   ```

The dashboard will open in your web browser at `http://localhost:8501`

### Configuration

#### Optional: Disable usage statistics

Usage statistics collection is already disabled via `.streamlit/config.toml`. To modify settings:

```shell
# Edit .streamlit/config.toml
[browser]
gatherUsageStats = false
```

## 📊 Core Metrics Dashboard

### 6 Essential Key Performance Indicators

- **Total Vehicle Count**: Aggregate count of all vehicles detected
- **Average Speed**: Combined directional speed analysis
- **Speed Compliance Rate**: Percentage of vehicles adhering to speed limits
- **85th Percentile Speed**: Critical speed measurement for traffic engineering
- **Peak Hour Statistics**: Busiest hour identification and vehicle counts
- **Dominant Direction Analysis**: Traffic flow direction preferences with percentages

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

## 🚀 Enhanced Data Processing

### Advanced Data Loading Features

The application includes sophisticated data processing capabilities that ensure high-quality analysis:

#### **Zero-Traffic Filtering**

- Automatically removes time periods with no traffic activity (both directions = 0)
- Improves analysis accuracy by focusing on active traffic periods
- Provides detailed statistics on filtered vs. original data

#### **Comprehensive Data Validation**

- **Volume Validation**: Detects negative values and unrealistic traffic volumes (>1000 vehicles/hour)
- **Speed Validation**: Validates speed range data for consistency and realistic values  
- **Temporal Validation**: Checks for missing time periods and irregular intervals
- **Classification Validation**: Ensures vehicle class data integrity
- **Cross-Validation**: Verifies total volumes match directional sums

#### **Performance Optimization**

- **Vectorized Operations**: NumPy-based speed compliance calculations for 30-50% performance improvement
- **Memory Efficiency**: Chunked processing for large datasets to prevent memory issues
- **Memory Monitoring**: Built-in memory usage tracking and reporting

#### **Enhanced Error Handling**

- **Custom Exceptions**: Specific error types for different failure modes
  - `TrafficDataError`: Base exception for traffic data processing
  - `DataValidationError`: Data quality and validation failures
  - `FileStructureError`: CSV format and structure issues
- **Detailed Error Messages**: Contextual information for troubleshooting
- **Graceful Degradation**: Handles partial data and missing columns

#### **Metadata & Statistics**

- **Filtering Statistics**: Tracks original vs. filtered row counts and percentages
- **Data Quality Metrics**: Validation results with warnings and error details
- **Memory Usage**: Real-time memory consumption monitoring
- **Processing Metadata**: Date ranges, active hours, and data completeness

### Usage Examples

```python
# Standard enhanced loading with validation
df, location, structure = load_data('traffic_data.csv')

# Access filtering statistics
stats = structure['filtering_stats']
print(f"Removed {stats['removed_rows']} inactive periods ({stats['removal_percentage']:.1f}%)")

# Check data quality
quality = structure['data_quality']
if not quality['is_valid']:
    print(f"Data validation errors: {quality['errors']}")

# Memory-efficient loading for large files
df, location, structure = load_large_traffic_data('large_file.csv', chunk_size=10000)

# Monitor memory usage
memory_info = get_memory_usage(df)
print(f"Dataset using {memory_info['total_memory']} of memory")
```

## 📁 Data Format

The application expects CSV files exported from TrafficViewer Pro with the following structure:

- **Metadata rows**: Location, comments, and title information
- **Date/Time column**: Timestamp for each data point (validated for consistency)
- **Volume columns**: Directional traffic counts (automatically filtered for zero-traffic periods)
- **Speed range columns**: Speed distribution data (e.g., "35-39 MPH - Northbound")
- **Classification columns**: Vehicle class counts by direction (validated for data integrity)

**Data Processing Notes:**

- Files are automatically validated for structure compatibility and data quality
- Zero-traffic time periods are filtered out to improve analysis accuracy
- Memory usage is optimized for large datasets through chunked processing
- Comprehensive error handling provides detailed feedback for data issues

## 🎯 Use Cases

- **Traffic Engineering**: Speed limit assessment and road safety analysis
- **Urban Planning**: Peak hour identification and capacity planning
- **Policy Making**: Data-driven traffic management decisions
- **Research**: Academic traffic pattern studies
- **Compliance Monitoring**: Speed enforcement effectiveness evaluation

## 🧪 Development and Testing

### Testing

```bash
# Run all tests
uv run pytest

# Run tests with coverage report
uv run pytest --cov=utils --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_metrics.py

# Run tests with verbose output
uv run pytest -v

# Install development dependencies (includes pytest)
uv sync --dev
```

### Code Quality

```bash
# Run linting and formatting
uv run ruff check .
uv run ruff format .
```

### Test Coverage

The test suite includes comprehensive tests for:

- **Metrics calculations**: All 6 core KPIs and helper functions
- **Enhanced data loading**: CSV parsing, structure detection, validation framework, and error handling
- **Data validation**: Traffic data quality checks, negative value detection, and temporal validation
- **Memory efficiency**: Memory usage monitoring and chunked processing
- **Performance optimization**: Vectorized operations and speed compliance calculations
- **Visualizations**: Chart generation and matplotlib figure validation

## 🔧 Technical Details

### Dependencies

- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis with enhanced validation
- **Matplotlib**: Static plotting and visualization
- **Seaborn**: Statistical data visualization
- **NumPy**: Numerical computing and vectorized operations for performance optimization

### Key Enhancements

- **Zero-traffic filtering**: Automatically removes inactive time periods for cleaner analysis
- **Vectorized operations**: 30-50% performance improvement in speed calculations
- **Data validation**: Comprehensive quality checks with detailed error reporting
- **Memory optimization**: Efficient processing for large datasets
- **Enhanced error handling**: Custom exceptions with contextual error messages

## 📝 Data Sources

Traffic data is collected using [PicoCount 2500](https://vehiclecounts.com/picocount-2500.html) traffic counters and processed through [TrafficViewer Pro](https://vehiclecounts.com/trafficviewerpro.html) software. The dashboard provides a user-friendly interface for analyzing this data, making it accessible for traffic planning and decision-making purposes.

## 📜 License

This project is licensed under the [MIT License](LICENSE).
