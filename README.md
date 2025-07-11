# Traffic Studies

A comprehensive traffic analysis dashboard for Crystal, Minnesota, built with [Observable Framework](https://observablehq.com/framework/). This project processes and visualizes traffic data collected from [PicoCount 2500](https://vehiclecounts.com/picocount-2500.html) traffic counters across 13 monitoring locations, providing detailed insights into traffic patterns, speed compliance, and vehicle classifications.

**Note**: This project has been transitioned from Streamlit to Observable Framework. Legacy Streamlit files are maintained for reference.

## 🌟 Features

- **Interactive Dashboard**: Real-time filtering by location, date range, and time periods
- **Core Metrics**: 6 essential key performance indicators including speed compliance, peak hour analysis, and traffic volume
- **Chart Explanations**: Interactive "See explanation" expanders under each visualization with detailed reading guides
- **Print-Friendly Design**: Clean location display, organized sections, and professional layout optimized for reporting
- **Vehicle Classification**: Detailed analysis of 6 vehicle classes from motorcycles to heavy trucks
- **Speed Analysis**: Compliance monitoring, violation severity tracking, and 85th percentile calculations
- **Temporal Patterns**: Hourly, daily, and weekly traffic pattern visualization
- **Professional Visualizations**: Matplotlib charts with consistent styling, clear presentation, and organized grouping
- **Enhanced Data Processing**: Advanced validation, vectorized operations, and zero-traffic filtering
- **Performance Optimization**: Memory-efficient processing for large datasets with chunked loading
- **Data Quality Monitoring**: Comprehensive validation with detailed error reporting and statistics

## 🏗️ Project Structure

### Observable Framework Implementation (Primary)

```text
traffic-studies/
├── src/
│   ├── index.md           # Main Observable Framework dashboard
│   ├── traffic-volume.md  # Detailed traffic volume analysis page
│   ├── test.md            # Test suite for Observable Framework
│   ├── lib/
│   │   ├── data-loader.js # CSV parsing and data preprocessing
│   │   └── metrics.js     # Traffic metrics calculations
│   └── data/              # 13 CSV files for monitoring locations
├── observablehq.config.js # Observable Framework configuration
├── package.json           # Node.js dependencies and scripts
├── CLAUDE.md              # AI assistant guidance file
└── README.md              # This file
```

### Legacy Streamlit Implementation (Secondary)

```text
├── main.py                # Streamlit dashboard (archived)
├── utils/
│   ├── data_loader.py     # Enhanced data loading with validation
│   ├── metrics.py         # Traffic metrics and KPI calculations
│   ├── visualizations.py  # Chart generation and plotting functions
│   └── styles.css         # Custom CSS styling
├── tests/                 # Test suite
│   ├── conftest.py        # Test fixtures and sample data
│   ├── test_metrics.py    # Tests for metrics calculations
│   ├── test_data_loader.py # Tests for data loading
│   └── test_visualizations.py # Tests for chart generation
├── .streamlit/
│   └── config.toml        # Streamlit configuration settings
├── pyproject.toml         # Python dependencies and metadata
```

## 🚀 Getting Started

### Prerequisites

- Node.js 18 or higher
- [pnpm](https://pnpm.io/) - Fast, disk space efficient package manager

### Installation

1. **Clone the repository**

   ```shell
   git clone https://github.com/semanticdata/traffic-studies.git
   cd traffic-studies
   ```

2. **Install dependencies**

   ```shell
   pnpm install
   ```

3. **Add your data files**

   Place your CSV files from TrafficViewer Pro in the `src/data/` directory

4. **Run the development server**

   ```shell
   pnpm run dev
   ```

The dashboard will open in your web browser at `http://localhost:3000`

### Additional Commands

```shell
# Build for production
pnpm run build

# Deploy to Observable
pnpm run deploy

# Clean cache
pnpm run clean
```

### Legacy Streamlit Version

To run the legacy Streamlit version:

```shell
# Create virtual environment
uv venv
source .venv/bin/activate  # Unix/MacOS

# Install dependencies
uv sync

# Run Streamlit dashboard
uv run streamlit run main.py
```

### Supported Locations

The Observable Framework dashboard supports 13 different traffic monitoring locations in Crystal, Minnesota:

- 2809 Hampshire Ave, 2941 Hampshire Ave, 3528 Noble Ave
- 3618 Adair Ave, 3624 Welcome Ave, 4017 Jersey Ave
- 4848 Nevada Ave N, 5240 Maryland Ave N, 5336 Kentucky Ave N
- 5716 Elmhurst Ave, 6420 41st Ave, 6702 45th Ave N, 7206 58th Ave

Each location has its own CSV file in the `src/data/` directory with interactive location selection in the dashboard.

## 📊 Core Metrics Dashboard

### 6 Essential Key Performance Indicators

- **Total Vehicle Count**: Aggregate count of all vehicles detected
- **Average Speed**: Combined directional speed analysis
- **Speed Compliance Rate**: Percentage of vehicles adhering to speed limits
- **85th Percentile Speed**: Critical speed measurement for traffic engineering
- **Peak Hour Statistics**: Busiest hour identification and vehicle counts
- **Dominant Direction Analysis**: Traffic flow direction preferences with percentages

### Traffic Analysis Visualizations

The dashboard features well-organized visualization sections with interactive explanations to help users understand and interpret the data effectively.

#### 📊 Traffic Volume Analysis

- **Hourly Traffic Volume**: Stacked bar chart showing average vehicles per hour by direction, ideal for identifying peak commute periods
- **Daily Traffic Patterns**: Bar chart displaying traffic volume by day of week, useful for understanding weekly cycles and planning maintenance schedules

#### 🚗 Speed Analysis

- **Speed Violation Severity**: Categorizes speeding violations by severity levels (0-5, 5-10, 10-15, 15+ mph over limit) to prioritize enforcement efforts
- **Speed Distribution by Direction**: Dual charts showing vehicle speed distributions for each direction, helping identify speeding patterns
- **Speed Compliance Analysis**: Compares compliant vs. non-compliant vehicles by direction using green/red color coding
- **Speeding Patterns by Hour**: Dual-axis charts combining total vehicle count with speeding percentage to optimize enforcement timing

#### 🚛 Vehicle Classification

- **Vehicle Distribution**: Bar chart showing the distribution of 6 FHWA vehicle classes by direction, supporting infrastructure planning and traffic composition analysis

#### 📖 Interactive Chart Explanations

Each visualization includes an expandable "See explanation" section that provides:

- **How to read this chart**: Step-by-step guidance for interpreting the visualization
- **Key patterns to look for**: Important indicators and what they mean
- **Practical applications**: How to use the data for traffic management decisions
- **Color coding explanations**: What different colors and elements represent

#### 🖨️ Print-Friendly Design

- **Clean location display**: Professional formatting with location name and analysis period prominently shown
- **Organized sections**: Logical grouping with clear headers and dividers
- **Professional layout**: Optimized for generating reports and presentations
- **Consistent styling**: Uniform appearance across all visualizations

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

- **Traffic Engineering**: Speed limit assessment and road safety analysis with detailed compliance metrics
- **Urban Planning**: Peak hour identification and capacity planning using temporal pattern analysis
- **Policy Making**: Data-driven traffic management decisions with comprehensive KPI dashboard
- **Research**: Academic traffic pattern studies with interactive explanations for methodology understanding
- **Compliance Monitoring**: Speed enforcement effectiveness evaluation with violation severity tracking
- **Report Generation**: Print-friendly dashboard layout perfect for creating professional traffic reports
- **Public Presentations**: Clear visualizations with explanations suitable for community meetings and stakeholder presentations

## 🧪 Development and Testing

### Observable Framework Development

```bash
# Start development server with hot reload
pnpm run dev

# Build and test production build
pnpm run build

# Clean cache if needed
pnpm run clean

# Test page at src/test.md
open http://localhost:3000/test
```

### Legacy Streamlit Testing

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
# Run linting and formatting (Python)
uv run ruff check .
uv run ruff format .
```

### Test Coverage

The test suite includes comprehensive tests for:

- **Metrics calculations**: All 6 core KPIs and helper functions with real data validation
- **Calculation accuracy**: Tests using actual traffic data files with known expected results
- **Enhanced data loading**: CSV parsing, structure detection, validation framework, and error handling
- **Data validation**: Traffic data quality checks, negative value detection, and temporal validation
- **Memory efficiency**: Memory usage monitoring and chunked processing
- **Performance optimization**: Vectorized operations and speed compliance calculations
- **Visualizations**: Chart generation and matplotlib figure validation
- **Real-world validation**: Tests against 11 actual traffic data files from Crystal, Minnesota
- **Edge case handling**: Zero traffic periods, single data points, and boundary conditions
- **Cross-file consistency**: Ensures calculations are consistent across different data sources

## 🔧 Technical Details

### Dependencies

#### Observable Framework (Primary)

- **Observable Framework**: Modern web application framework for data visualization
- **D3.js**: Data visualization library (integrated with Observable)
- **Plot**: Observable's grammar of graphics for data visualization
- **JavaScript ES6+**: Modern JavaScript features and syntax

#### Legacy Streamlit (Secondary)

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
- **Interactive explanations**: Expandable "See explanation" sections for each visualization
- **Print-friendly design**: Professional layout optimized for report generation and presentations
- **Clean location formatting**: Automatic removal of quotes, commas, and extra whitespace from location names

## 📝 Data Sources

Traffic data is collected using [PicoCount 2500](https://vehiclecounts.com/picocount-2500.html) traffic counters and processed through [TrafficViewer Pro](https://vehiclecounts.com/trafficviewerpro.html) software. The dashboard provides a user-friendly interface for analyzing this data, making it accessible for traffic planning and decision-making purposes.

## 📜 License

This project is licensed under the [MIT License](LICENSE).
