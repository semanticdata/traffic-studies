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
        csv_content = """Location,Test Location
Date/Time,Eastbound,Westbound,25-29 MPH - Eastbound,30-34 MPH - Eastbound,25-29 MPH - Westbound,30-34 MPH - Westbound,Class 2 - Eastbound,Class 2 - Westbound
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
        with pytest.raises((FileNotFoundError, ValueError)):
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


class TestGetAvailableLocations:
    """Test get_available_locations function."""

    def test_get_available_locations_empty_directory(self, tmp_path):
        """Test get_available_locations with empty directory."""
        with patch("utils.data_loader.get_data_directory", return_value=tmp_path):
            result = get_available_locations()
            assert result == {}

    def test_get_available_locations_with_csv_files(self, tmp_path, sample_csv_content):
        """Test get_available_locations with CSV files."""
        # Create test CSV files
        csv1 = tmp_path / "location1.csv"
        csv1.write_text(sample_csv_content)

        csv2_content = sample_csv_content.replace(
            "Hampshire Ave between Noble Ave and Adair Ave", "Main Street between 1st and 2nd"
        )
        csv2 = tmp_path / "location2.csv"
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
        # Create a CSV file with proper header
        csv_file = tmp_path / "valid.csv"
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
        # Create valid CSV with proper header
        valid_csv = tmp_path / "valid.csv"
        valid_csv.write_text("Location,Valid Location\nComments,Test\nDate/Time,Volume\n1/1/2024,100\n")

        # Create invalid CSV
        invalid_csv = tmp_path / "invalid.csv"
        invalid_csv.write_text("Invalid content without location")

        with patch("utils.data_loader.get_data_directory", return_value=tmp_path):
            result = get_available_locations()

            # Should include valid file and unknown location for invalid file
            assert len(result) == 2
            assert "Valid Location" in result
            assert "Unknown Location" in result
