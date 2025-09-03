"""
Tests for posted speed extraction and integration functionality.

This test suite validates the posted speed extraction from Total-SPD.csv files
and integration with the traffic analysis system.
"""

import tempfile

from utils.data_loader import load_data
from utils.parsers.traffic_parser import detect_file_structure, extract_posted_speed


class TestPostedSpeedExtraction:
    """Test posted speed extraction from Total-SPD.csv files."""

    def test_extract_posted_speed_valid_csv(self):
        """Test posted speed extraction from valid Total-SPD.csv file."""
        csv_content = """
"Unit Type:","PicoCount 2500 V2.41"
"Serial Number:","24071598"
"ID:",""
"Location:","Test Location"
"Comments:","Test comment"
"Dwell:","90 ms"
"Measurements:","English"
"Start Date:","11/4/2024"
"Start Time:","00:00"
"Export Version:","Speed V2.10"
"Posted Speed:","35"
"Interval:","60 Min"
"Title:","Total Speeds"
"Date/Time","5-15 MPH","16-20 MPH","21-25 MPH"
11/04/2024 14:00 - 14:59,0,1,5
""".strip()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write(csv_content)
            f.flush()

            result = extract_posted_speed(f.name)
            assert result == 35

    def test_extract_posted_speed_different_values(self):
        """Test posted speed extraction with different speed values."""
        test_cases = [
            ("25", 25),
            ("30", 30),
            ("35", 35),
            ("45", 45),
        ]

        for speed_str, expected_speed in test_cases:
            csv_content = f'''
"Unit Type:","PicoCount 2500 V2.41"
"Posted Speed:","{speed_str}"
"Date/Time","5-15 MPH"
11/04/2024 14:00 - 14:59,0
'''.strip()

            with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
                f.write(csv_content)
                f.flush()

                result = extract_posted_speed(f.name)
                assert result == expected_speed, f"Expected {expected_speed}, got {result} for input '{speed_str}'"

    def test_extract_posted_speed_no_posted_speed_line(self):
        """Test posted speed extraction when no Posted Speed line exists."""
        csv_content = """
"Unit Type:","PicoCount 2500 V2.41"
"Location:","Test Location"
"Date/Time","5-15 MPH"
11/04/2024 14:00 - 14:59,0
""".strip()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write(csv_content)
            f.flush()

            result = extract_posted_speed(f.name)
            assert result is None

    def test_extract_posted_speed_invalid_speed_value(self):
        """Test posted speed extraction with invalid speed values."""
        csv_content = """
"Posted Speed:","invalid"
"Date/Time","5-15 MPH"
11/04/2024 14:00 - 14:59,0
""".strip()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write(csv_content)
            f.flush()

            result = extract_posted_speed(f.name)
            assert result is None

    def test_extract_posted_speed_nonexistent_file(self):
        """Test posted speed extraction with nonexistent file."""
        result = extract_posted_speed("nonexistent_file.csv")
        assert result is None

    def test_extract_posted_speed_none_input(self):
        """Test posted speed extraction with None input."""
        result = extract_posted_speed(None)
        assert result is None


class TestPostedSpeedIntegration:
    """Test integration of posted speed with data loading and metrics."""

    def test_posted_speed_in_structure(self):
        """Test that posted speed is included in the structure after loading data."""
        # Use a real data file that we know has posted speed
        df, location, structure = load_data("data/2809_Hampshire_Ave_N-ALL.csv")

        # Verify posted speed is in structure
        assert "posted_speed" in structure
        assert structure["posted_speed"] == 30  # Known value for this location

    def test_posted_speed_used_in_metrics(self):
        """Test that posted speed from CSV is used in metrics calculations."""
        from utils.metrics import get_core_metrics

        # Load data from location with 35 mph posted speed
        df, location, structure = load_data("data/4825_Douglas_Dr_N-ALL.csv")

        # Get metrics
        metrics = get_core_metrics(df, structure)

        # Verify the posted speed from CSV is used
        assert metrics["posted_speed"] == 35

        # Verify compliance calculation uses the correct speed limit
        # (We know this location should have reasonable compliance, not 17.2%)
        assert 50 <= metrics["compliance_rate"] <= 80  # Reasonable range

    def test_different_posted_speeds_different_locations(self):
        """Test that different locations have different posted speeds."""
        # Test 30 mph location
        df1, _, structure1 = load_data("data/2809_Hampshire_Ave_N-ALL.csv")
        assert structure1["posted_speed"] == 30

        # Test 35 mph location
        df2, _, structure2 = load_data("data/4825_Douglas_Dr_N-ALL.csv")
        assert structure2["posted_speed"] == 35

        # Verify they're different
        assert structure1["posted_speed"] != structure2["posted_speed"]


class TestReferenceFileDetection:
    """Test reference file detection for posted speed extraction."""

    def test_reference_files_detected(self):
        """Test that reference SPD files are detected correctly."""
        # Use a location where we know SPD files exist
        structure = detect_file_structure("data/2809_Hampshire_Ave_N-ALL.csv")

        assert "reference_files" in structure
        ref_files = structure["reference_files"]

        # Check that Total-SPD file is detected
        assert ref_files["total_spd_file"] is not None
        assert "2809_Hampshire_Ave_N-Total-SPD.csv" in ref_files["total_spd_file"]

        # Check that directional SPD files are detected
        assert ref_files["northbound_spd_file"] is not None
        assert ref_files["southbound_spd_file"] is not None

    def test_reference_files_different_directions(self):
        """Test that E/W locations have correct directional reference files."""
        # Use a location with E/W directions
        structure = detect_file_structure("data/4701_Louisiana_Ave_N-ALL.csv")

        ref_files = structure["reference_files"]

        # Should have E/W files, not N/S
        assert ref_files["eastbound_spd_file"] is not None
        assert ref_files["westbound_spd_file"] is not None
        assert ref_files["northbound_spd_file"] is None
        assert ref_files["southbound_spd_file"] is None
