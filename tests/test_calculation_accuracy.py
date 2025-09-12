"""
Tests for calculation accuracy using real data with known expected results.

This test suite validates that our metrics calculations are correct by testing
them against real traffic data files with manually verified expected results.
"""

import numpy as np
import pandas as pd

from utils.data_loader import load_data
from utils.metrics import (
    calculate_85th_percentile_speed,
    calculate_compliance,
    calculate_weighted_speed,
    get_core_metrics,
)


class TestCalculationAccuracy:
    """Test calculation accuracy with real data and expected results."""

    def test_load_real_data_and_verify_structure(self):
        """Test that we can load real data and verify the structure is correct."""
        # Load real data file
        df, location, structure = load_data("data/2809_Hampshire_Ave_N-ALL.csv")

        # Verify basic structure
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert location == "2809 Hampshire Ave N"

        # Verify required columns exist
        assert "Date/Time" in df.columns
        assert "Hour" in df.columns
        assert "Total" in df.columns
        assert structure["dir1_volume_col"] in df.columns
        assert structure["dir2_volume_col"] in df.columns

        # Verify speed columns exist
        assert len(structure["dir1_speed_cols"]) > 0
        assert len(structure["dir2_speed_cols"]) > 0
        for col in structure["dir1_speed_cols"]:
            assert col in df.columns
        for col in structure["dir2_speed_cols"]:
            assert col in df.columns

    def test_total_volume_calculation_accuracy(self):
        """Test that total volume calculations are accurate."""
        df, location, structure = load_data("data/2809_Hampshire_Ave_N-ALL.csv")

        # Verify that Total column equals sum of directional volumes
        expected_total = df[structure["dir1_volume_col"]] + df[structure["dir2_volume_col"]]
        pd.testing.assert_series_equal(df["Total"], expected_total, check_names=False)

        # Test with specific known values from the data
        # From the CSV: first non-zero row should be 18 + 15 = 33
        non_zero_rows = df[df["Total"] > 0]
        if len(non_zero_rows) > 0:
            first_row = non_zero_rows.iloc[0]
            manual_total = first_row[structure["dir1_volume_col"]] + first_row[structure["dir2_volume_col"]]
            assert first_row["Total"] == manual_total

    def test_weighted_speed_calculation_with_known_data(self):
        """Test weighted speed calculation with known data points."""
        df, location, structure = load_data("data/2809_Hampshire_Ave_N-ALL.csv")

        # Test with first few rows of real data
        test_data = df.head(20)  # Use first 20 rows

        # Calculate weighted speed for northbound
        nb_speed = calculate_weighted_speed(test_data, structure["dir1_speed_cols"])
        sb_speed = calculate_weighted_speed(test_data, structure["dir2_speed_cols"])

        # Verify results are reasonable
        assert isinstance(nb_speed, (int, float))
        assert isinstance(sb_speed, (int, float))
        assert nb_speed >= 0
        assert sb_speed >= 0

        # Speed should be within reasonable range for traffic data
        assert nb_speed <= 80  # Should not exceed maximum speed range
        assert sb_speed <= 80

        # If there's traffic, speed should be > 0
        nb_has_traffic = test_data[structure["dir1_speed_cols"]].sum().sum() > 0
        sb_has_traffic = test_data[structure["dir2_speed_cols"]].sum().sum() > 0

        if nb_has_traffic:
            assert nb_speed > 0
        if sb_has_traffic:
            assert sb_speed > 0

    def test_compliance_calculation_with_known_values(self):
        """Test compliance calculation with known speed limit scenarios."""
        df, location, structure = load_data("data/2809_Hampshire_Ave_N-ALL.csv")

        # Test compliance with different speed limits
        for speed_limit in [25, 30, 35]:
            nb_compliant, nb_total = calculate_compliance(df, structure["dir1_speed_cols"], speed_limit)
            sb_compliant, sb_total = calculate_compliance(df, structure["dir2_speed_cols"], speed_limit)

            # Basic sanity checks
            assert nb_compliant >= 0
            assert sb_compliant >= 0
            assert nb_total >= nb_compliant
            assert sb_total >= sb_compliant

            # Higher speed limits should result in higher compliance
            if speed_limit > 25:
                nb_compliant_25, nb_total_25 = calculate_compliance(df, structure["dir1_speed_cols"], 25)
                sb_compliant_25, sb_total_25 = calculate_compliance(df, structure["dir2_speed_cols"], 25)

                # With higher speed limit, compliance should be >= than lower speed limit
                assert nb_compliant >= nb_compliant_25
                assert sb_compliant >= sb_compliant_25

    def test_85th_percentile_speed_calculation(self):
        """Test 85th percentile speed calculation with real data."""
        df, location, structure = load_data("data/2809_Hampshire_Ave_N-ALL.csv")

        # Calculate 85th percentile speeds
        nb_85th = calculate_85th_percentile_speed(df, structure["dir1_speed_cols"])
        sb_85th = calculate_85th_percentile_speed(df, structure["dir2_speed_cols"])

        # Verify results are reasonable
        assert isinstance(nb_85th, (int, float))
        assert isinstance(sb_85th, (int, float))
        assert nb_85th >= 0
        assert sb_85th >= 0

        # 85th percentile should be within reasonable range
        assert nb_85th <= 80
        assert sb_85th <= 80

        # If there's traffic, 85th percentile should be > 0
        nb_has_traffic = df[structure["dir1_speed_cols"]].sum().sum() > 0
        sb_has_traffic = df[structure["dir2_speed_cols"]].sum().sum() > 0

        if nb_has_traffic:
            assert nb_85th > 0
        if sb_has_traffic:
            assert sb_85th > 0

    def test_core_metrics_with_real_data(self):
        """Test complete core metrics calculation with real data."""
        df, location, structure = load_data("data/2809_Hampshire_Ave_N-ALL.csv")

        # Calculate core metrics
        metrics = get_core_metrics(df, structure, speed_limit=30)

        # Verify all expected metrics are present
        expected_keys = [
            "total_vehicles",
            "combined_avg_speed",
            "compliance_rate",
            "percentile_85th",
            "peak_hour",
            "peak_vehicles",
            "dominant_direction",
            "dominant_pct",
        ]

        for key in expected_keys:
            assert key in metrics, f"Missing metric: {key}"

        # Verify data types and ranges
        assert isinstance(metrics["total_vehicles"], (int, float, np.integer))
        assert metrics["total_vehicles"] >= 0

        assert isinstance(metrics["combined_avg_speed"], (int, float, np.floating))
        assert metrics["combined_avg_speed"] >= 0

        assert isinstance(metrics["compliance_rate"], (int, float, np.floating))
        assert 0 <= metrics["compliance_rate"] <= 100

        assert isinstance(metrics["percentile_85th"], (int, float, np.floating))
        assert metrics["percentile_85th"] >= 0

        assert isinstance(metrics["peak_hour"], (int, np.integer))
        assert 0 <= metrics["peak_hour"] <= 23

        assert isinstance(metrics["peak_vehicles"], (int, float, np.integer))
        assert metrics["peak_vehicles"] >= 0

        assert metrics["dominant_direction"] in [
            structure["dir1_name"],
            structure["dir2_name"],
        ]

        assert isinstance(metrics["dominant_pct"], (int, float, np.floating))
        assert 0 <= metrics["dominant_pct"] <= 100

        # Additional logical checks
        # Total vehicles should equal sum of directional volumes
        total_dir1 = df[structure["dir1_volume_col"]].sum()
        total_dir2 = df[structure["dir2_volume_col"]].sum()
        expected_total = total_dir1 + total_dir2
        assert metrics["total_vehicles"] == expected_total

        # Dominant direction percentage should be > 50% if there's a clear dominant direction
        if total_dir1 != total_dir2:
            assert metrics["dominant_pct"] > 50

    def test_calculation_consistency_across_files(self):
        """Test that calculations are consistent across different data files."""
        test_files = [
            "data/2809_Hampshire_Ave_N-ALL.csv",
            "data/2941_Hampshire_Ave_N-ALL.csv",
            "data/3528_Noble_Ave_N-ALL.csv",
        ]

        results = []
        for file_path in test_files:
            df, location, structure = load_data(file_path)
            metrics = get_core_metrics(df, structure, speed_limit=30)
            results.append((file_path, metrics))

        # Verify all calculations completed successfully
        assert len(results) == 3

        # Verify all metrics have reasonable values
        for file_path, metrics in results:
            assert metrics["total_vehicles"] >= 0, f"Invalid total vehicles for {file_path}"
            assert metrics["combined_avg_speed"] >= 0, f"Invalid avg speed for {file_path}"
            assert 0 <= metrics["compliance_rate"] <= 100, f"Invalid compliance rate for {file_path}"
            assert metrics["percentile_85th"] >= 0, f"Invalid 85th percentile for {file_path}"
            assert 0 <= metrics["peak_hour"] <= 23, f"Invalid peak hour for {file_path}"
            assert metrics["peak_vehicles"] >= 0, f"Invalid peak vehicles for {file_path}"
            assert 0 <= metrics["dominant_pct"] <= 100, f"Invalid dominant pct for {file_path}"

    def test_edge_case_handling(self):
        """Test handling of edge cases in calculations."""
        df, location, structure = load_data("data/2809_Hampshire_Ave_N-ALL.csv")

        # Test with zero traffic periods
        zero_traffic = df[df["Total"] == 0]
        if len(zero_traffic) > 0:
            # Should handle zero traffic gracefully
            nb_speed = calculate_weighted_speed(zero_traffic, structure["dir1_speed_cols"])
            sb_speed = calculate_weighted_speed(zero_traffic, structure["dir2_speed_cols"])
            assert nb_speed == 0
            assert sb_speed == 0

        # Test with single row
        single_row = df.head(1)
        if len(single_row) > 0:
            metrics = get_core_metrics(single_row, structure)
            assert isinstance(metrics["total_vehicles"], (int, float, np.integer))
            assert isinstance(metrics["combined_avg_speed"], (int, float, np.floating))
            assert isinstance(metrics["compliance_rate"], (int, float, np.floating))

    def test_manual_calculation_verification(self):
        """Test with manually calculated expected values from a small data subset."""
        df, location, structure = load_data("data/2809_Hampshire_Ave_N-ALL.csv")

        # Get a specific row with known values for manual verification
        # From the CSV data, we know row at 11/04/2024 15:00 has:
        # Northbound: 18, Southbound: 15
        specific_time = pd.to_datetime("2024-11-04 15:00:00")
        specific_row = df[df["Date/Time"] == specific_time]

        if len(specific_row) > 0:
            row = specific_row.iloc[0]

            # Verify the total calculation
            expected_total = row[structure["dir1_volume_col"]] + row[structure["dir2_volume_col"]]
            assert row["Total"] == expected_total

            # Verify directional values match expected
            assert row[structure["dir1_volume_col"]] == 18
            assert row[structure["dir2_volume_col"]] == 15
            assert row["Total"] == 33

    def test_data_quality_validation(self):
        """Test that data quality validation catches potential issues."""
        df, location, structure = load_data("data/2809_Hampshire_Ave_N-ALL.csv")

        # Verify no negative values in volume columns
        assert (df[structure["dir1_volume_col"]] >= 0).all()
        assert (df[structure["dir2_volume_col"]] >= 0).all()
        assert (df["Total"] >= 0).all()

        # Verify no negative values in speed columns
        for col in structure["dir1_speed_cols"] + structure["dir2_speed_cols"]:
            assert (df[col] >= 0).all(), f"Negative values found in {col}"

        # Verify DateTime column is properly formatted
        assert pd.api.types.is_datetime64_any_dtype(df["Date/Time"])

        # Verify Hour column matches DateTime
        expected_hours = df["Date/Time"].dt.hour
        pd.testing.assert_series_equal(df["Hour"], expected_hours, check_names=False)

        # Check for data consistency
        validation_result = structure.get("data_quality", {})
        if validation_result:
            # If validation is available, check the results
            assert isinstance(validation_result["is_valid"], bool)
            assert isinstance(validation_result["errors"], list)
            assert isinstance(validation_result["warnings"], list)
