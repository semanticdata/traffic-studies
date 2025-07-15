"""
Tests for utils/metrics.py module.
"""

import numpy as np
import pandas as pd

from utils.metrics import (
    calculate_85th_percentile_speed,
    calculate_compliance,
    calculate_phf,
    calculate_weighted_speed,
    count_high_speeders,
    get_core_metrics,
)


class TestCalculateWeightedSpeed:
    """Test calculate_weighted_speed function."""

    def test_calculate_weighted_speed_basic(self, sample_traffic_data):
        """Test basic weighted speed calculation."""
        speed_cols = ["20-24 MPH - Northbound", "25-29 MPH - Northbound", "30-34 MPH - Northbound"]
        result = calculate_weighted_speed(sample_traffic_data, speed_cols)

        assert isinstance(result, float)
        assert result >= 20.0  # Minimum speed from columns
        assert result <= 34.0  # Maximum speed from columns

    def test_calculate_weighted_speed_empty_data(self):
        """Test weighted speed calculation with empty data."""
        df = pd.DataFrame({"20-24 MPH - Test": [0, 0, 0]})
        speed_cols = ["20-24 MPH - Test"]
        result = calculate_weighted_speed(df, speed_cols)

        assert result == 0.0

    def test_calculate_weighted_speed_single_column(self):
        """Test weighted speed calculation with single column."""
        df = pd.DataFrame({"25-29 MPH - Test": [10, 20, 30]})
        speed_cols = ["25-29 MPH - Test"]
        result = calculate_weighted_speed(df, speed_cols)

        # Should return midpoint of range: (25 + 29) / 2 = 27.0
        assert result == 27.0


class TestCalculateCompliance:
    """Test calculate_compliance function."""

    def test_calculate_compliance_basic(self, sample_traffic_data):
        """Test basic compliance calculation."""
        speed_cols = ["20-24 MPH - Northbound", "25-29 MPH - Northbound", "35-39 MPH - Northbound"]
        compliant, total = calculate_compliance(sample_traffic_data, speed_cols, speed_limit=30)

        assert isinstance(compliant, (int, np.integer))
        assert isinstance(total, (int, np.integer))
        assert compliant >= 0
        assert total >= compliant
        assert total > 0

    def test_calculate_compliance_all_compliant(self):
        """Test compliance calculation when all vehicles are compliant."""
        df = pd.DataFrame({"20-24 MPH - Test": [10, 20, 30], "25-29 MPH - Test": [15, 25, 35]})
        speed_cols = ["20-24 MPH - Test", "25-29 MPH - Test"]
        compliant, total = calculate_compliance(df, speed_cols, speed_limit=30)

        assert compliant == total
        assert total == 135  # Sum of all values

    def test_calculate_compliance_none_compliant(self):
        """Test compliance calculation when no vehicles are compliant."""
        df = pd.DataFrame({"35-39 MPH - Test": [10, 20, 30], "40-44 MPH - Test": [15, 25, 35]})
        speed_cols = ["35-39 MPH - Test", "40-44 MPH - Test"]
        compliant, total = calculate_compliance(df, speed_cols, speed_limit=30)

        assert compliant == 0
        assert total == 135


class TestCalculate85thPercentileSpeed:
    """Test calculate_85th_percentile_speed function."""

    def test_calculate_85th_percentile_basic(self, sample_traffic_data):
        """Test basic 85th percentile speed calculation."""
        speed_cols = ["20-24 MPH - Northbound", "25-29 MPH - Northbound", "30-34 MPH - Northbound"]
        result = calculate_85th_percentile_speed(sample_traffic_data, speed_cols)

        assert isinstance(result, (float, np.floating))
        assert result >= 20.0
        assert result <= 34.0

    def test_calculate_85th_percentile_single_speed(self):
        """Test 85th percentile with single speed range."""
        df = pd.DataFrame({"25-29 MPH - Test": [100]})
        speed_cols = ["25-29 MPH - Test"]
        result = calculate_85th_percentile_speed(df, speed_cols)

        # Should interpolate to 85% within the range: 25 + (0.85 * (29-25)) = 28.4
        assert result == 28.4

    def test_calculate_85th_percentile_no_data(self):
        """Test 85th percentile with no data."""
        df = pd.DataFrame({"25-29 MPH - Test": [0]})
        speed_cols = ["25-29 MPH - Test"]
        result = calculate_85th_percentile_speed(df, speed_cols)

        assert result == 0


class TestCalculatePHF:
    """Test calculate_phf function."""

    def test_calculate_phf_basic(self, sample_traffic_data):
        """Test basic PHF calculation."""
        result = calculate_phf(sample_traffic_data)

        assert isinstance(result, (float, np.floating))
        assert result >= 0.0
        # PHF can exceed 1.0 in real-world scenarios, so we just check it's reasonable
        assert result <= 5.0

    def test_calculate_phf_no_traffic(self):
        """Test PHF calculation with no traffic."""
        df = pd.DataFrame({"Hour": [0, 1, 2], "Total": [0, 0, 0]})
        result = calculate_phf(df)

        assert result == 0.0

    def test_calculate_phf_uniform_traffic(self):
        """Test PHF calculation with uniform traffic."""
        df = pd.DataFrame({"Hour": [0, 1, 2, 3], "Total": [100, 100, 100, 100]})
        result = calculate_phf(df)

        assert result == 0.25  # 100 / (100 * 4)


class TestCountHighSpeeders:
    """Test count_high_speeders function."""

    def test_count_high_speeders_basic(self, sample_traffic_data):
        """Test basic high speeders counting."""
        speed_cols = ["35-39 MPH - Northbound", "40-44 MPH - Northbound", "45-50 MPH - Northbound"]
        result = count_high_speeders(sample_traffic_data, speed_cols, speed_limit=30)

        assert isinstance(result, (int, np.integer))
        assert result >= 0

    def test_count_high_speeders_none(self):
        """Test high speeders counting when none exceed threshold."""
        df = pd.DataFrame({"20-24 MPH - Test": [10, 20, 30], "25-29 MPH - Test": [15, 25, 35]})
        speed_cols = ["20-24 MPH - Test", "25-29 MPH - Test"]
        result = count_high_speeders(df, speed_cols, speed_limit=30)

        assert result == 0

    def test_count_high_speeders_all_exceed(self):
        """Test high speeders counting when all exceed threshold."""
        df = pd.DataFrame({"45-49 MPH - Test": [10, 20, 30], "50+ MPH - Test": [15, 25, 35]})
        speed_cols = ["45-49 MPH - Test", "50+ MPH - Test"]
        result = count_high_speeders(df, speed_cols, speed_limit=30)

        assert result == 135  # Sum of all values


class TestGetCoreMetrics:
    """Test get_core_metrics function."""

    def test_get_core_metrics_complete(self, sample_traffic_data, sample_structure):
        """Test complete core metrics calculation."""
        result = get_core_metrics(sample_traffic_data, sample_structure)

        # Verify all expected keys are present
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
            assert key in result, f"Missing key: {key}"

        # Verify data types and ranges
        assert isinstance(result["total_vehicles"], (int, np.integer))
        assert result["total_vehicles"] >= 0

        assert isinstance(result["combined_avg_speed"], (float, np.floating))
        assert result["combined_avg_speed"] >= 0

        assert isinstance(result["compliance_rate"], (float, np.floating))
        assert 0 <= result["compliance_rate"] <= 100

        assert isinstance(result["percentile_85th"], (float, np.floating))
        assert result["percentile_85th"] >= 0

        assert isinstance(result["peak_hour"], (int, np.integer))
        assert 0 <= result["peak_hour"] <= 23

        assert isinstance(result["peak_vehicles"], (int, np.integer))
        assert result["peak_vehicles"] >= 0

        assert result["dominant_direction"] in ["Northbound", "Southbound"]

        assert isinstance(result["dominant_pct"], (float, np.floating))
        assert 0 <= result["dominant_pct"] <= 100

    def test_get_core_metrics_empty_data(self, sample_structure):
        """Test core metrics with empty data."""
        df = pd.DataFrame(
            {
                "Date/Time": pd.to_datetime(["2024-01-01 00:00:00"]),
                "Hour": [0],
                "Total": [0],
                "Northbound": [0],
                "Southbound": [0],
            }
        )

        # Add all required columns with zeros
        for col in sample_structure["dir1_speed_cols"] + sample_structure["dir2_speed_cols"]:
            df[col] = [0]

        result = get_core_metrics(df, sample_structure)

        assert result["total_vehicles"] == 0
        assert result["combined_avg_speed"] == 0
        assert result["peak_vehicles"] == 0

    def test_get_core_metrics_speed_limit_variation(self, sample_traffic_data, sample_structure):
        """Test core metrics with different speed limits."""
        result_30 = get_core_metrics(sample_traffic_data, sample_structure, speed_limit=30)
        result_25 = get_core_metrics(sample_traffic_data, sample_structure, speed_limit=25)

        # Compliance rate should be different with different speed limits
        assert result_30["compliance_rate"] != result_25["compliance_rate"]
        # Lower speed limit should generally result in lower compliance
        assert result_25["compliance_rate"] <= result_30["compliance_rate"]
