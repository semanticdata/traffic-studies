"""
Pytest configuration and fixtures for traffic studies tests.
"""

from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def sample_traffic_data():
    """Create sample traffic data for testing."""
    # Create date range for 7 days
    start_date = datetime(2024, 1, 1, 0, 0, 0)
    dates = [start_date + timedelta(hours=i) for i in range(24 * 7)]  # 7 days of hourly data

    data = {
        "Date/Time": dates,
        "Hour": [d.hour for d in dates],
        "Total": np.random.randint(10, 100, len(dates)),
        # Northbound/Southbound columns
        "Northbound": np.random.randint(5, 50, len(dates)),
        "Southbound": np.random.randint(5, 50, len(dates)),
        # Speed columns for Northbound
        "5-14 MPH - Northbound": np.random.randint(0, 5, len(dates)),
        "15-19 MPH - Northbound": np.random.randint(0, 10, len(dates)),
        "20-24 MPH - Northbound": np.random.randint(5, 15, len(dates)),
        "25-29 MPH - Northbound": np.random.randint(10, 20, len(dates)),
        "30-34 MPH - Northbound": np.random.randint(5, 15, len(dates)),
        "35-39 MPH - Northbound": np.random.randint(3, 10, len(dates)),
        "40-44 MPH - Northbound": np.random.randint(1, 5, len(dates)),
        "45-50 MPH - Northbound": np.random.randint(0, 3, len(dates)),
        # Speed columns for Southbound
        "5-14 MPH - Southbound": np.random.randint(0, 5, len(dates)),
        "15-19 MPH - Southbound": np.random.randint(0, 10, len(dates)),
        "20-24 MPH - Southbound": np.random.randint(5, 15, len(dates)),
        "25-29 MPH - Southbound": np.random.randint(10, 20, len(dates)),
        "30-34 MPH - Southbound": np.random.randint(5, 15, len(dates)),
        "35-39 MPH - Southbound": np.random.randint(3, 10, len(dates)),
        "40-44 MPH - Southbound": np.random.randint(1, 5, len(dates)),
        "45-50 MPH - Southbound": np.random.randint(0, 3, len(dates)),
        # Vehicle classification columns
        "Class 1 - Northbound": np.random.randint(0, 2, len(dates)),
        "Class 2 - Northbound": np.random.randint(15, 35, len(dates)),
        "Class 3 - Northbound": np.random.randint(3, 8, len(dates)),
        "Class 4 - Northbound": np.random.randint(0, 2, len(dates)),
        "Class 5 - Northbound": np.random.randint(1, 4, len(dates)),
        "Class 6 - Northbound": np.random.randint(0, 2, len(dates)),
        "Class 1 - Southbound": np.random.randint(0, 2, len(dates)),
        "Class 2 - Southbound": np.random.randint(15, 35, len(dates)),
        "Class 3 - Southbound": np.random.randint(3, 8, len(dates)),
        "Class 4 - Southbound": np.random.randint(0, 2, len(dates)),
        "Class 5 - Southbound": np.random.randint(1, 4, len(dates)),
        "Class 6 - Southbound": np.random.randint(0, 2, len(dates)),
    }

    df = pd.DataFrame(data)
    df["Date/Time"] = pd.to_datetime(df["Date/Time"])
    return df


@pytest.fixture
def sample_structure():
    """Create sample data structure for testing."""
    return {
        "dir1_name": "Northbound",
        "dir2_name": "Southbound",
        "dir1_volume_col": "Northbound",
        "dir2_volume_col": "Southbound",
        "dir1_speed_cols": [
            "5-14 MPH - Northbound",
            "15-19 MPH - Northbound",
            "20-24 MPH - Northbound",
            "25-29 MPH - Northbound",
            "30-34 MPH - Northbound",
            "35-39 MPH - Northbound",
            "40-44 MPH - Northbound",
            "45-50 MPH - Northbound",
        ],
        "dir2_speed_cols": [
            "5-14 MPH - Southbound",
            "15-19 MPH - Southbound",
            "20-24 MPH - Southbound",
            "25-29 MPH - Southbound",
            "30-34 MPH - Southbound",
            "35-39 MPH - Southbound",
            "40-44 MPH - Southbound",
            "45-50 MPH - Southbound",
        ],
        "dir1_class_cols": [
            "Class 1 - Northbound",
            "Class 2 - Northbound",
            "Class 3 - Northbound",
            "Class 4 - Northbound",
            "Class 5 - Northbound",
            "Class 6 - Northbound",
        ],
        "dir2_class_cols": [
            "Class 1 - Southbound",
            "Class 2 - Southbound",
            "Class 3 - Southbound",
            "Class 4 - Southbound",
            "Class 5 - Southbound",
            "Class 6 - Southbound",
        ],
    }


@pytest.fixture
def sample_csv_content():
    """Create sample CSV content for testing data_loader."""
    header = (
        "Date/Time,Northbound,Southbound,"
        "5-14 MPH - Northbound,15-19 MPH - Northbound,20-24 MPH - Northbound,25-29 MPH - Northbound,"
        "30-34 MPH - Northbound,35-39 MPH - Northbound,40-44 MPH - Northbound,45-50 MPH - Northbound,"
        "5-14 MPH - Southbound,15-19 MPH - Southbound,20-24 MPH - Southbound,25-29 MPH - Southbound,"
        "30-34 MPH - Southbound,35-39 MPH - Southbound,40-44 MPH - Southbound,45-50 MPH - Southbound,"
        "Class 1 - Northbound,Class 2 - Northbound,Class 3 - Northbound,Class 4 - Northbound,"
        "Class 5 - Northbound,Class 6 - Northbound,Class 1 - Southbound,Class 2 - Southbound,"
        "Class 3 - Southbound,Class 4 - Southbound,Class 5 - Southbound,Class 6 - Southbound"
    )

    return f"""Location,Hampshire Ave between Noble Ave and Adair Ave
Comments,Crystal Traffic Study
Title,Hampshire Ave between Noble Ave and Adair Ave
Start Date,6/11/2024 0:00
End Date,6/18/2024 0:00
Study Duration,7 days
Created By,TrafficViewer Pro v1.0

{header}
6/11/2024 0:00,15,12,0,2,5,6,2,0,0,0,0,1,4,5,2,0,0,0,0,12,2,0,1,0,0,10,1,0,1,0
6/11/2024 1:00,8,5,0,1,2,4,1,0,0,0,0,0,1,3,1,0,0,0,0,6,1,0,1,0,0,4,1,0,0,0
6/11/2024 2:00,5,3,0,0,1,3,1,0,0,0,0,0,1,2,0,0,0,0,0,4,1,0,0,0,0,2,1,0,0,0
"""


@pytest.fixture
def mock_csv_file(tmp_path, sample_csv_content):
    """Create a temporary CSV file for testing."""
    csv_file = tmp_path / "test_data.csv"
    csv_file.write_text(sample_csv_content)
    return str(csv_file)
