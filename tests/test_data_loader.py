"""
Tests for utils/data_loader.py module.
"""

from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest

from utils.data_loader import (
    detect_file_structure,
    get_available_locations,
    get_data_directory,
    get_location_from_file,
    load_data,
)


class TestGetDataDirectory:
    """Test get_data_directory function."""

    def test_get_data_directory_returns_path(self):
        """Test that get_data_directory returns a Path object."""
        result = get_data_directory()
        assert isinstance(result, Path)
        assert result.name == "data"

    def test_get_data_directory_relative_to_utils(self):
        """Test that data directory is correctly relative to utils directory."""
        result = get_data_directory()
        # Should be parent of utils directory + data
        expected_parts = ["traffic-studies", "data"]
        assert all(part in str(result) for part in expected_parts)


class TestGetLocationFromFile:
    """Test get_location_from_file function."""

    def test_get_location_from_file_success(self, mock_csv_file):
        """Test successful location extraction from CSV file."""
        result = get_location_from_file(mock_csv_file)
        assert result == "Hampshire Ave between Noble Ave and Adair Ave"

    def test_get_location_from_file_no_location_row(self, tmp_path):
        """Test location extraction when no location row exists."""
        csv_content = "Comments,Test file\nTitle,Test title\n"
        csv_file = tmp_path / "no_location.csv"
        csv_file.write_text(csv_content)

        result = get_location_from_file(str(csv_file))
        assert result == "Unknown Location"

    def test_get_location_from_file_nonexistent(self):
        """Test location extraction from nonexistent file."""
        result = get_location_from_file("nonexistent_file.csv")
        assert result == "Unknown Location"

    def test_get_location_from_file_empty_location(self, tmp_path):
        """Test location extraction when location field is empty."""
        csv_content = "Location,\nComments,Test file\n"
        csv_file = tmp_path / "empty_location.csv"
        csv_file.write_text(csv_content)

        result = get_location_from_file(str(csv_file))
        assert result == "Unknown Location"


class TestDetectFileStructure:
    """Test detect_file_structure function."""

    def test_detect_file_structure_success(self, mock_csv_file):
        """Test successful file structure detection."""
        result = detect_file_structure(mock_csv_file)

        assert result is not None
        assert isinstance(result, dict)

        # Check required keys
        required_keys = [
            "dir1_name",
            "dir2_name",
            "dir1_volume_col",
            "dir2_volume_col",
            "dir1_speed_cols",
            "dir2_speed_cols",
            "dir1_class_cols",
            "dir2_class_cols",
        ]

        for key in required_keys:
            assert key in result

        # Check directional names
        assert result["dir1_name"] == "Northbound"
        assert result["dir2_name"] == "Southbound"

        # Check volume columns
        assert result["dir1_volume_col"] == "Northbound"
        assert result["dir2_volume_col"] == "Southbound"

        # Check speed columns are lists and not empty
        assert isinstance(result["dir1_speed_cols"], list)
        assert isinstance(result["dir2_speed_cols"], list)
        assert len(result["dir1_speed_cols"]) > 0
        assert len(result["dir2_speed_cols"]) > 0

        # Check class columns are lists
        assert isinstance(result["dir1_class_cols"], list)
        assert isinstance(result["dir2_class_cols"], list)

    def test_detect_file_structure_eastwest(self, tmp_path):
        """Test file structure detection for East/West directions."""
        header = (
            "Date/Time,Eastbound,Westbound,"
            "25-29 MPH - Eastbound,30-34 MPH - Eastbound,"
            "25-29 MPH - Westbound,30-34 MPH - Westbound,"
            "Class 2 - Eastbound,Class 2 - Westbound"
        )
        csv_content = f"""Location,Test Location
{header}
1/1/2024 0:00,15,12,10,5,8,4,12,10
"""
        csv_file = tmp_path / "eastwest.csv"
        csv_file.write_text(csv_content)

        result = detect_file_structure(str(csv_file))

        assert result is not None
        assert result["dir1_name"] == "Eastbound"
        assert result["dir2_name"] == "Westbound"

    def test_detect_file_structure_nonexistent_file(self):
        """Test file structure detection for nonexistent file."""
        result = detect_file_structure("nonexistent_file.csv")
        assert result is None

    def test_detect_file_structure_invalid_csv(self, tmp_path):
        """Test file structure detection for invalid CSV."""
        csv_content = "Not a valid CSV format\nMissing proper headers"
        csv_file = tmp_path / "invalid.csv"
        csv_file.write_text(csv_content)

        result = detect_file_structure(str(csv_file))
        assert result is None


class TestLoadData:
    """Test load_data function."""

    def test_load_data_success(self, mock_csv_file):
        """Test successful data loading."""
        df, location, structure = load_data(mock_csv_file)

        # Check DataFrame
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert "Date/Time" in df.columns
        assert "Hour" in df.columns
        assert "Total" in df.columns

        # Check that Date/Time is datetime
        assert pd.api.types.is_datetime64_any_dtype(df["Date/Time"])

        # Check location
        assert location == "Hampshire Ave between Noble Ave and Adair Ave"

        # Check structure
        assert structure is not None
        assert isinstance(structure, dict)

    def test_load_data_with_speed_limit(self, mock_csv_file):
        """Test data loading with custom speed limit."""
        df, location, structure = load_data(mock_csv_file, speed_limit=25)

        assert isinstance(df, pd.DataFrame)
        assert location == "Hampshire Ave between Noble Ave and Adair Ave"
        assert structure is not None

    def test_load_data_nonexistent_file(self):
        """Test data loading for nonexistent file."""
        from utils.data_loader import FileStructureError

        with pytest.raises((FileNotFoundError, ValueError, FileStructureError)):
            load_data("nonexistent_file.csv")

    def test_load_data_invalid_structure(self, tmp_path):
        """Test data loading when structure detection fails."""
        csv_content = "Invalid CSV content without proper structure"
        csv_file = tmp_path / "invalid_structure.csv"
        csv_file.write_text(csv_content)

        with pytest.raises(Exception):  # Should raise an exception for invalid structure
            load_data(str(csv_file))

    def test_load_data_total_column_calculation(self, mock_csv_file):
        """Test that Total column is correctly calculated."""
        df, location, structure = load_data(mock_csv_file)

        # Total should equal sum of directional volumes
        calculated_total = df[structure["dir1_volume_col"]] + df[structure["dir2_volume_col"]]
        pd.testing.assert_series_equal(df["Total"], calculated_total, check_names=False)

    def test_load_data_hour_column_extraction(self, mock_csv_file):
        """Test that Hour column is correctly extracted."""
        df, location, structure = load_data(mock_csv_file)

        # Hour should match hour from Date/Time
        expected_hours = df["Date/Time"].dt.hour
        pd.testing.assert_series_equal(df["Hour"], expected_hours, check_names=False)


class TestValidateTrafficData:
    """Test suite for validate_traffic_data function."""

    def test_validate_traffic_data_valid_data(self):
        """Test validation with valid data."""
        from utils.data_loader import validate_traffic_data

        # Create sample valid data
        df = pd.DataFrame(
            {
                "Date/Time": pd.date_range("2024-01-01", periods=24, freq="h"),
                "Volume - Northbound": [10, 20, 30, 40] * 6,
                "Volume - Southbound": [15, 25, 35, 45] * 6,
                "Total": [25, 45, 65, 85] * 6,
                "20-25 MPH - Northbound": [5, 10, 15, 20] * 6,
                "20-25 MPH - Southbound": [8, 12, 18, 22] * 6,
                "Class #1 - Northbound": [8, 15, 22, 30] * 6,
                "Class #1 - Southbound": [12, 20, 28, 35] * 6,
            }
        )

        structure = {
            "dir1_volume_col": "Volume - Northbound",
            "dir2_volume_col": "Volume - Southbound",
            "dir1_speed_cols": ["20-25 MPH - Northbound"],
            "dir2_speed_cols": ["20-25 MPH - Southbound"],
            "dir1_class_cols": ["Class #1 - Northbound"],
            "dir2_class_cols": ["Class #1 - Southbound"],
        }

        result = validate_traffic_data(df, structure)
        assert result["is_valid"] is True
        assert len(result["errors"]) == 0
        assert "Volume - Northbound_max" in result["stats"]
        assert "Volume - Southbound_max" in result["stats"]

    def test_validate_traffic_data_negative_values(self):
        """Test validation with negative values."""
        from utils.data_loader import validate_traffic_data

        # Create sample data with negative values
        df = pd.DataFrame(
            {
                "Date/Time": pd.date_range("2024-01-01", periods=5, freq="h"),
                "Volume - Northbound": [10, -5, 30, 40, 50],  # Negative value
                "Volume - Southbound": [15, 25, 35, 45, 55],
                "Total": [25, 20, 65, 85, 105],
                "20-25 MPH - Northbound": [5, 10, 15, 20, 25],
                "20-25 MPH - Southbound": [8, 12, 18, 22, 28],
            }
        )

        structure = {
            "dir1_volume_col": "Volume - Northbound",
            "dir2_volume_col": "Volume - Southbound",
            "dir1_speed_cols": ["20-25 MPH - Northbound"],
            "dir2_speed_cols": ["20-25 MPH - Southbound"],
            "dir1_class_cols": [],
            "dir2_class_cols": [],
        }

        result = validate_traffic_data(df, structure)
        assert result["is_valid"] is False
        assert len(result["errors"]) > 0
        assert any("negative values" in error for error in result["errors"])


class TestMemoryUsage:
    """Test suite for memory usage functions."""

    def test_get_memory_usage(self):
        """Test memory usage calculation."""
        from utils.data_loader import get_memory_usage

        df = pd.DataFrame(
            {
                "col1": [1, 2, 3, 4, 5],
                "col2": ["a", "b", "c", "d", "e"],
                "col3": [1.1, 2.2, 3.3, 4.4, 5.5],
            }
        )

        result = get_memory_usage(df)
        assert "total_memory" in result
        assert "rows" in result
        assert "columns" in result
        assert "memory_per_row" in result
        assert result["rows"] == 5
        assert result["columns"] == 3
        assert "MB" in result["total_memory"]
        assert "bytes" in result["memory_per_row"]

    def test_get_memory_usage_empty_dataframe(self):
        """Test memory usage calculation with empty dataframe."""
        from utils.data_loader import get_memory_usage

        df = pd.DataFrame()
        result = get_memory_usage(df)
        assert result["rows"] == 0
        assert result["memory_per_row"] == "0 bytes"


class TestEnhancedLoadData:
    """Test suite for enhanced load_data functionality."""

    def test_load_data_with_filtering_stats(self):
        """Test that filtering statistics are included in enhanced structure."""
        # Using actual data file
        df, location, structure = load_data("data/2809_Hampshire_Ave_N-ALL.csv")

        assert "filtering_stats" in structure
        stats = structure["filtering_stats"]
        assert "original_rows" in stats
        assert "filtered_rows" in stats
        assert "removed_rows" in stats
        assert "removal_percentage" in stats
        assert "active_hours" in stats
        assert "inactive_hours" in stats
        assert stats["original_rows"] >= stats["filtered_rows"]

    def test_load_data_with_validation_results(self):
        """Test that data quality validation results are included."""
        df, location, structure = load_data("data/2809_Hampshire_Ave_N-ALL.csv")

        assert "data_quality" in structure
        quality = structure["data_quality"]
        assert "is_valid" in quality
        assert "warnings" in quality
        assert "errors" in quality
        assert "stats" in quality
        assert isinstance(quality["is_valid"], bool)
        assert isinstance(quality["warnings"], list)
        assert isinstance(quality["errors"], list)


class TestGetAvailableLocations:
    """Test get_available_locations function."""

    def test_get_available_locations_empty_directory(self, tmp_path):
        """Test get_available_locations with empty directory."""
        with patch("utils.data_loader.get_data_directory", return_value=tmp_path):
            result = get_available_locations()
            assert result == {}

    def test_get_available_locations_with_csv_files(self, tmp_path, sample_csv_content):
        """Test get_available_locations with CSV files."""
        # Create test CSV files with -ALL.csv suffix (required by get_available_locations)
        csv1 = tmp_path / "location1-ALL.csv"
        csv1.write_text(sample_csv_content)

        csv2_content = sample_csv_content.replace(
            "Hampshire Ave between Noble Ave and Adair Ave",
            "Main Street between 1st and 2nd",
        )
        csv2 = tmp_path / "location2-ALL.csv"
        csv2.write_text(csv2_content)

        with patch("utils.data_loader.get_data_directory", return_value=tmp_path):
            result = get_available_locations()

            assert len(result) == 2
            assert "Hampshire Ave between Noble Ave and Adair Ave" in result
            assert "Main Street between 1st and 2nd" in result

            # Check file paths
            assert result["Hampshire Ave between Noble Ave and Adair Ave"] == str(csv1)
            assert result["Main Street between 1st and 2nd"] == str(csv2)

    def test_get_available_locations_nonexistent_directory(self):
        """Test get_available_locations with nonexistent directory."""
        nonexistent_path = Path("/nonexistent/directory")
        with patch("utils.data_loader.get_data_directory", return_value=nonexistent_path):
            result = get_available_locations()
            assert result == {}

    def test_get_available_locations_ignores_non_csv(self, tmp_path):
        """Test that get_available_locations ignores non-CSV files."""
        # Create a CSV file with proper header and -ALL.csv suffix
        csv_file = tmp_path / "valid-ALL.csv"
        csv_file.write_text("Location,Test Location\nComments,Test\nDate/Time,Volume\n1/1/2024,100\n")

        # Create non-CSV files
        txt_file = tmp_path / "readme.txt"
        txt_file.write_text("Some text")

        py_file = tmp_path / "script.py"
        py_file.write_text("print('hello')")

        with patch("utils.data_loader.get_data_directory", return_value=tmp_path):
            result = get_available_locations()

            assert len(result) == 1
            assert "Test Location" in result

    def test_get_available_locations_handles_invalid_csv(self, tmp_path):
        """Test that get_available_locations handles invalid CSV files gracefully."""
        # Create valid CSV with proper header and -ALL.csv suffix
        valid_csv = tmp_path / "valid-ALL.csv"
        valid_csv.write_text("Location,Valid Location\nComments,Test\nDate/Time,Volume\n1/1/2024,100\n")

        # Create invalid CSV with -ALL.csv suffix
        invalid_csv = tmp_path / "invalid-ALL.csv"
        invalid_csv.write_text("Invalid content without location")

        with patch("utils.data_loader.get_data_directory", return_value=tmp_path):
            result = get_available_locations()

            # Should include valid file and derive location name from invalid file
            assert len(result) == 2
            assert "Valid Location" in result
            assert "All" in result  # Derived from filename: "invalid-ALL.csv" -> "ALL" -> "All"
