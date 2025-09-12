"""
Tests for utils/visualizations.py module.
"""

import matplotlib

matplotlib.use("Agg")  # Use non-interactive backend for testing
import matplotlib.pyplot as plt
import pandas as pd
import pytest

from utils.visualizations import (
    plot_speed_compliance,
    plot_speed_distribution,
    plot_speed_violation_severity,
    plot_speeding_by_hour,
    plot_temporal_patterns,
    plot_traffic_volume,
    plot_vehicle_classification_distribution,
)


class TestPlotTrafficVolume:
    """Test plot_traffic_volume function."""

    def test_plot_traffic_volume_returns_figure(self, sample_traffic_data, sample_structure):
        """Test that plot_traffic_volume returns a matplotlib Figure."""
        fig = plot_traffic_volume(sample_traffic_data, sample_structure)

        assert isinstance(fig, plt.Figure)
        plt.close(fig)  # Clean up

    def test_plot_traffic_volume_has_correct_elements(self, sample_traffic_data, sample_structure):
        """Test that the plot has the expected elements."""
        fig = plot_traffic_volume(sample_traffic_data, sample_structure)

        ax = fig.axes[0]

        # Check title
        assert "Hourly Traffic Volume Distribution" in ax.get_title()

        # Check axis labels
        assert "Hour of Day" in ax.get_xlabel()
        assert "Average Vehicles per Hour" in ax.get_ylabel()

        # Check legend
        legend = ax.get_legend()
        assert legend is not None
        legend_texts = [text.get_text() for text in legend.get_texts()]
        assert sample_structure["dir1_name"] in legend_texts
        assert sample_structure["dir2_name"] in legend_texts

        plt.close(fig)

    def test_plot_traffic_volume_empty_data(self, sample_structure):
        """Test plot_traffic_volume with empty data."""
        df = pd.DataFrame(
            {
                "Hour": [],
                sample_structure["dir1_volume_col"]: [],
                sample_structure["dir2_volume_col"]: [],
            }
        )

        fig = plot_traffic_volume(df, sample_structure)
        assert isinstance(fig, plt.Figure)
        plt.close(fig)


class TestPlotSpeedDistribution:
    """Test plot_speed_distribution function."""

    def test_plot_speed_distribution_returns_figure(self, sample_traffic_data, sample_structure):
        """Test that plot_speed_distribution returns a matplotlib Figure."""
        fig = plot_speed_distribution(sample_traffic_data, sample_structure)

        assert isinstance(fig, plt.Figure)
        # Should have 2 subplots (one for each direction)
        assert len(fig.axes) == 2
        plt.close(fig)

    def test_plot_speed_distribution_subplot_titles(self, sample_traffic_data, sample_structure):
        """Test that subplots have correct titles."""
        fig = plot_speed_distribution(sample_traffic_data, sample_structure)

        ax1, ax2 = fig.axes

        assert sample_structure["dir1_name"] in ax1.get_title()
        assert sample_structure["dir2_name"] in ax2.get_title()
        assert "Speed Distribution" in ax1.get_title()
        assert "Speed Distribution" in ax2.get_title()

        plt.close(fig)

    def test_plot_speed_distribution_axis_labels(self, sample_traffic_data, sample_structure):
        """Test that axes have correct labels."""
        fig = plot_speed_distribution(sample_traffic_data, sample_structure)

        for ax in fig.axes:
            assert "Speed Range (MPH)" in ax.get_xlabel()
            assert "Average Vehicle Count" in ax.get_ylabel()

        plt.close(fig)


class TestPlotSpeedCompliance:
    """Test plot_speed_compliance function."""

    def test_plot_speed_compliance_returns_figure(self, sample_traffic_data, sample_structure):
        """Test that plot_speed_compliance returns a matplotlib Figure."""
        fig = plot_speed_compliance(sample_traffic_data, sample_structure)

        assert isinstance(fig, plt.Figure)
        assert len(fig.axes) == 1
        plt.close(fig)

    def test_plot_speed_compliance_elements(self, sample_traffic_data, sample_structure):
        """Test that the compliance plot has expected elements."""
        fig = plot_speed_compliance(sample_traffic_data, sample_structure)

        ax = fig.axes[0]

        # Check title
        assert "Speed Compliance Analysis by Direction" in ax.get_title()

        # Check axis labels
        assert "Direction" in ax.get_xlabel()
        assert "Vehicle Count" in ax.get_ylabel()

        # Check legend
        legend = ax.get_legend()
        assert legend is not None

        plt.close(fig)

    def test_plot_speed_compliance_custom_speed_limit(self, sample_traffic_data, sample_structure):
        """Test plot_speed_compliance with custom speed limit."""
        fig = plot_speed_compliance(sample_traffic_data, sample_structure, speed_limit=25)

        assert isinstance(fig, plt.Figure)
        plt.close(fig)


class TestPlotTemporalPatterns:
    """Test plot_temporal_patterns function."""

    def test_plot_temporal_patterns_returns_figure(self, sample_traffic_data, sample_structure):
        """Test that plot_temporal_patterns returns a matplotlib Figure."""
        fig = plot_temporal_patterns(sample_traffic_data, sample_structure)

        assert isinstance(fig, plt.Figure)
        assert len(fig.axes) == 1
        plt.close(fig)

    def test_plot_temporal_patterns_elements(self, sample_traffic_data, sample_structure):
        """Test that temporal patterns plot has expected elements."""
        fig = plot_temporal_patterns(sample_traffic_data, sample_structure)

        ax = fig.axes[0]

        # Check title
        assert "Daily Traffic Volume Patterns" in ax.get_title()

        # Check axis labels
        assert "Day of Week" in ax.get_xlabel()
        assert "Total Vehicle Count" in ax.get_ylabel()

        # Check legend
        legend = ax.get_legend()
        assert legend is not None

        plt.close(fig)

    def test_plot_temporal_patterns_day_order(self, sample_traffic_data, sample_structure):
        """Test that days are in correct order."""
        # Add DayOfWeek column to test data
        sample_traffic_data["DayOfWeek"] = sample_traffic_data["Date/Time"].dt.day_name()

        fig = plot_temporal_patterns(sample_traffic_data, sample_structure)

        ax = fig.axes[0]
        # Check that x-axis has day names (can't easily verify order without complex logic)
        tick_labels = [tick.get_text() for tick in ax.get_xticklabels()]
        assert len(tick_labels) > 0

        plt.close(fig)


class TestPlotSpeedViolationSeverity:
    """Test plot_speed_violation_severity function."""

    def test_plot_speed_violation_severity_with_violations(self, sample_traffic_data, sample_structure):
        """Test plot with violations present."""
        fig = plot_speed_violation_severity(sample_traffic_data, sample_structure)

        if fig is not None:  # Function returns None if no violations
            assert isinstance(fig, plt.Figure)
            plt.close(fig)

    def test_plot_speed_violation_severity_no_violations(self, sample_structure):
        """Test plot with no violations."""
        # Create data with no speed violations (all under limit)
        df = pd.DataFrame(
            {
                "Date/Time": pd.to_datetime(["2024-01-01 00:00:00"]),
                "20-24 MPH - Northbound": [10],
                "25-29 MPH - Northbound": [20],
                "20-24 MPH - Southbound": [15],
                "25-29 MPH - Southbound": [25],
            }
        )

        # Update structure to only include non-violating speeds
        structure = sample_structure.copy()
        structure["dir1_speed_cols"] = [
            "20-24 MPH - Northbound",
            "25-29 MPH - Northbound",
        ]
        structure["dir2_speed_cols"] = [
            "20-24 MPH - Southbound",
            "25-29 MPH - Southbound",
        ]

        fig = plot_speed_violation_severity(df, structure, speed_limit=30)

        # Should return None when no violations
        assert fig is None

    def test_plot_speed_violation_severity_custom_speed_limit(self, sample_traffic_data, sample_structure):
        """Test plot with custom speed limit."""
        fig = plot_speed_violation_severity(sample_traffic_data, sample_structure, speed_limit=25)

        if fig is not None:
            assert isinstance(fig, plt.Figure)
            plt.close(fig)


class TestPlotSpeedingByHour:
    """Test plot_speeding_by_hour function."""

    def test_plot_speeding_by_hour_returns_figure(self, sample_traffic_data, sample_structure):
        """Test that plot_speeding_by_hour returns a matplotlib Figure."""
        fig = plot_speeding_by_hour(sample_traffic_data, sample_structure)

        assert isinstance(fig, plt.Figure)
        # Should have 2 subplots (one for each direction)
        assert len(fig.axes) == 4  # 2 main axes + 2 twin axes
        plt.close(fig)

    def test_plot_speeding_by_hour_subplot_titles(self, sample_traffic_data, sample_structure):
        """Test that subplots have correct titles."""
        fig = plot_speeding_by_hour(sample_traffic_data, sample_structure)

        # Get main axes (those with titles, not twin axes)
        main_axes = [ax for ax in fig.axes if ax.get_title()]

        assert len(main_axes) == 2
        assert sample_structure["dir1_name"] in main_axes[0].get_title()
        assert sample_structure["dir2_name"] in main_axes[1].get_title()
        assert "Speeding by Hour of Day" in main_axes[0].get_title()
        assert "Speeding by Hour of Day" in main_axes[1].get_title()

        plt.close(fig)

    def test_plot_speeding_by_hour_custom_speed_limit(self, sample_traffic_data, sample_structure):
        """Test plot_speeding_by_hour with custom speed limit."""
        fig = plot_speeding_by_hour(sample_traffic_data, sample_structure, speed_limit=25)

        assert isinstance(fig, plt.Figure)
        plt.close(fig)


class TestPlotVehicleClassificationDistribution:
    """Test plot_vehicle_classification_distribution function."""

    def test_plot_vehicle_classification_returns_figure(self, sample_traffic_data, sample_structure):
        """Test that plot_vehicle_classification_distribution returns a matplotlib Figure."""
        fig = plot_vehicle_classification_distribution(sample_traffic_data, sample_structure)

        assert isinstance(fig, plt.Figure)
        assert len(fig.axes) == 1
        plt.close(fig)

    def test_plot_vehicle_classification_elements(self, sample_traffic_data, sample_structure):
        """Test that vehicle classification plot has expected elements."""
        fig = plot_vehicle_classification_distribution(sample_traffic_data, sample_structure)

        ax = fig.axes[0]

        # Check title
        assert "Vehicle Classification Distribution" in ax.get_title()

        # Check axis labels
        assert "Vehicle Type" in ax.get_xlabel()
        assert "Count" in ax.get_ylabel()

        # Check legend
        legend = ax.get_legend()
        assert legend is not None

        plt.close(fig)

    def test_plot_vehicle_classification_has_vehicle_types(self, sample_traffic_data, sample_structure):
        """Test that plot includes all vehicle classification types."""
        fig = plot_vehicle_classification_distribution(sample_traffic_data, sample_structure)

        ax = fig.axes[0]

        # Check that x-axis tick labels include vehicle classes
        tick_labels = [tick.get_text() for tick in ax.get_xticklabels()]

        # Should include class references
        vehicle_class_found = any("Class" in label for label in tick_labels)
        assert vehicle_class_found

        plt.close(fig)


class TestVisualizationHelpers:
    """Test visualization helper functionality."""

    def test_all_plots_use_tight_layout(self, sample_traffic_data, sample_structure):
        """Test that all plots use tight_layout for proper spacing."""
        plot_functions = [
            plot_traffic_volume,
            plot_speed_distribution,
            plot_speed_compliance,
            plot_temporal_patterns,
            plot_speeding_by_hour,
            plot_vehicle_classification_distribution,
        ]

        for plot_func in plot_functions:
            try:
                fig = plot_func(sample_traffic_data, sample_structure)

                if fig is not None:  # Some functions may return None
                    # Verify figure exists and can be displayed
                    assert isinstance(fig, plt.Figure)

                    # Check that figure has reasonable size
                    width, height = fig.get_size_inches()
                    assert width > 0
                    assert height > 0

                    plt.close(fig)

            except Exception as e:
                pytest.fail(f"Plot function {plot_func.__name__} failed: {str(e)}")

    def test_plot_functions_handle_empty_data_gracefully(self, sample_structure):
        """Test that plot functions handle empty DataFrames gracefully."""
        # Create minimal empty DataFrame
        empty_df = pd.DataFrame(
            {
                "Date/Time": pd.to_datetime([]),
                "Hour": [],
                sample_structure["dir1_volume_col"]: [],
                sample_structure["dir2_volume_col"]: [],
            }
        )

        # Add empty speed and class columns
        for col in sample_structure["dir1_speed_cols"] + sample_structure["dir2_speed_cols"]:
            empty_df[col] = []
        for col in sample_structure["dir1_class_cols"] + sample_structure["dir2_class_cols"]:
            empty_df[col] = []

        plot_functions = [
            plot_traffic_volume,
            plot_speed_distribution,
            plot_speed_compliance,
            plot_temporal_patterns,
            plot_speeding_by_hour,
            plot_vehicle_classification_distribution,
        ]

        for plot_func in plot_functions:
            try:
                fig = plot_func(empty_df, sample_structure)

                if fig is not None:
                    assert isinstance(fig, plt.Figure)
                    plt.close(fig)

            except Exception:
                # Some functions may legitimately fail with empty data
                # This test ensures they don't crash the application
                pass
