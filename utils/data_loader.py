"""
Data loading orchestrator for Traffic Studies dashboard.

This module provides the main interface for loading and processing traffic data
from CSV files exported from TrafficViewer Pro software. It orchestrates parsing,
validation, and transformation using specialized modules while maintaining
backward compatibility with existing code.

Functions:
    validate_traffic_data(df: pd.DataFrame, structure: Dict) -> Dict: Validate traffic data
    get_data_directory() -> Path: Get the data directory path
    get_location_from_file(file_path: str) -> str: Extract location from CSV metadata
    detect_file_structure(file_path: str) -> Optional[Dict]: Detect CSV structure
    load_data(file_path: str, speed_limit: int = 30) -> Tuple: Load and process data with validation
    get_memory_usage(df: pd.DataFrame) -> Dict: Get memory usage statistics
    load_large_traffic_data(file_path: str, speed_limit: int = 30, chunk_size: int = 50000)
        -> Tuple: Memory-efficient loading
    get_available_locations() -> Dict[str, str]: Get available data files

Exceptions:
    TrafficDataError: Base exception for traffic data processing
    DataValidationError: Raised when data validation fails
    FileStructureError: Raised when CSV structure doesn't match expected format
"""

from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import pandas as pd

from utils.parsers.traffic_parser import (
    FileStructureError as ParserFileStructureError,
)

# Import from specialized modules
from utils.parsers.traffic_parser import (
    detect_file_structure as parser_detect_file_structure,
)
from utils.parsers.traffic_parser import (
    get_location_from_file as parser_get_location_from_file,
)
from utils.parsers.traffic_parser import (
    extract_posted_speed,
    load_reference_speed_data,
)
from utils.transformers.traffic_transformer import (
    add_basic_enrichments,
    calculate_speed_compliance,
    filter_zero_traffic,
)
from utils.validators.data_validator import (
    DataValidationError as ValidatorDataValidationError,
)
from utils.validators.data_validator import (
    validate_traffic_data as validator_validate_traffic_data,
)


class TrafficDataError(Exception):
    """Base exception for traffic data processing."""

    pass


class DataValidationError(TrafficDataError):
    """Raised when data validation fails."""

    def __init__(self, message: str, validation_details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.validation_details = validation_details or {}


class FileStructureError(TrafficDataError):
    """Raised when CSV structure doesn't match expected format."""

    pass


def validate_traffic_data(df: pd.DataFrame, structure: Dict[str, Any]) -> Dict[str, Any]:
    """Comprehensive data validation with detailed reporting."""
    try:
        return validator_validate_traffic_data(df, structure)
    except ValidatorDataValidationError as e:
        # Re-raise as local exception type for backward compatibility
        raise DataValidationError(str(e), e.validation_details)


def get_data_directory() -> Path:
    """Get the path to the data directory relative to the project root."""
    # Get the current file's directory (utils)
    current_dir = Path(__file__).parent
    # Go up one level to project root and then into data directory
    data_dir = current_dir.parent / "data"
    return data_dir


def get_location_from_file(file_path: str) -> str:
    """Extract location name from the CSV file metadata."""
    return parser_get_location_from_file(file_path)


def detect_file_structure(file_path: str) -> Optional[Dict[str, Any]]:
    """Detect the structure of the CSV file and return appropriate parsing parameters."""
    try:
        return parser_detect_file_structure(file_path)
    except ParserFileStructureError as e:
        # Re-raise as local exception type for backward compatibility
        raise FileStructureError(str(e))


def load_data(file_path: str, speed_limit: int = 30) -> Tuple[pd.DataFrame, str, Dict[str, Any]]:
    """Load and process traffic data from CSV file with enhanced validation and optimization."""
    structure = detect_file_structure(file_path)
    if not structure:
        raise FileStructureError(
            f"Could not detect file structure for '{file_path}'. Expected TrafficViewer Pro format."
        )

    location_name = structure["location"]
    if location_name and isinstance(location_name, str):
        location_name = location_name.strip().strip('"').strip("'").strip(",").strip()

    try:
        # Enhanced error handling for CSV reading
        try:
            df = pd.read_csv(file_path, skiprows=structure["metadata_rows"])
        except pd.errors.EmptyDataError:
            raise DataValidationError(f"CSV file '{file_path}' is empty or contains no data rows")
        except pd.errors.ParserError as e:
            raise FileStructureError(
                f"CSV parsing failed for '{file_path}': {str(e)}\n"
                f"Expected TrafficViewer Pro format with metadata headers"
            )

        # Validate required columns exist
        required_columns = ["Date/Time", structure["dir1_volume_col"], structure["dir2_volume_col"]]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise DataValidationError(
                f"Missing required columns in '{file_path}': {missing_columns}\n"
                f"Expected columns: Date/Time, Volume columns, Speed ranges"
            )

        # Validate datetime
        invalid_dates = pd.to_datetime(df["Date/Time"], errors="coerce").isna().sum()
        if invalid_dates > 0:
            raise DataValidationError(f"Found {invalid_dates} invalid date/time values in '{file_path}'")

        # Add basic enrichments (datetime processing, hour extraction, total calculation)
        df = add_basic_enrichments(df, structure)

        # Calculate speed compliance using transformer
        df = calculate_speed_compliance(df, structure, speed_limit)

        # Filter zero traffic and get statistics
        df, filtering_stats = filter_zero_traffic(df, structure)

        # Extract posted speed from reference SPD files if available
        posted_speed = 30  # Default fallback
        if structure.get("reference_files", {}).get("total_spd_file"):
            extracted_speed = extract_posted_speed(structure["reference_files"]["total_spd_file"])
            if extracted_speed:
                posted_speed = extracted_speed

        # Perform data validation
        validation_results = validate_traffic_data(df, structure)

        # Add validation warnings to console if any
        if validation_results["warnings"]:
            print(f"Data validation warnings for '{file_path}':")
            for warning in validation_results["warnings"]:
                print(f"  - {warning}")

        # Raise errors if validation failed
        if not validation_results["is_valid"]:
            error_details = "; ".join(validation_results["errors"])
            raise DataValidationError(f"Data validation failed for '{file_path}': {error_details}", validation_results)

        # Enhanced structure with metadata
        enhanced_structure = {
            **structure,
            "filtering_stats": filtering_stats,
            "data_quality": validation_results,
            "posted_speed": posted_speed,
        }

        return df, location_name, enhanced_structure

    except (TrafficDataError, pd.errors.EmptyDataError, pd.errors.ParserError):
        # Re-raise our custom exceptions
        raise
    except KeyError as e:
        raise DataValidationError(
            f"Missing required column in '{file_path}': {str(e)}\n"
            f"Expected columns: Date/Time, Volume columns, Speed ranges"
        )
    except Exception as e:
        raise TrafficDataError(f"Unexpected error loading data from '{file_path}': {e}")


def get_memory_usage(df: pd.DataFrame) -> Dict[str, str]:
    """Get memory usage statistics for dataframe."""
    memory_usage = df.memory_usage(deep=True).sum()
    return {
        "total_memory": f"{memory_usage / 1024**2:.2f} MB",
        "rows": len(df),
        "columns": len(df.columns),
        "memory_per_row": f"{memory_usage / len(df):.2f} bytes" if len(df) > 0 else "0 bytes",
    }


def load_large_traffic_data(
    file_path: str, speed_limit: int = 30, chunk_size: int = 50000
) -> Tuple[pd.DataFrame, str, Dict[str, Any]]:
    """Memory-efficient loading for large traffic datasets using chunked processing."""
    structure = detect_file_structure(file_path)
    if not structure:
        raise FileStructureError(
            f"Could not detect file structure for '{file_path}'. Expected TrafficViewer Pro format."
        )

    location_name = structure["location"]
    if location_name and isinstance(location_name, str):
        location_name = location_name.strip().strip('"').strip("'").strip(",").strip()

    try:
        # Process data in chunks for memory efficiency
        processed_chunks = []
        original_row_count = 0

        for chunk in pd.read_csv(file_path, skiprows=structure["metadata_rows"], chunksize=chunk_size):
            original_row_count += len(chunk)

            # Add basic enrichments
            chunk = add_basic_enrichments(chunk, structure)

            # Calculate speed compliance using transformer
            chunk = calculate_speed_compliance(chunk, structure, speed_limit)

            # Filter zero rows for this chunk
            filtered_chunk, _ = filter_zero_traffic(chunk, structure)

            if len(filtered_chunk) > 0:
                processed_chunks.append(filtered_chunk)

        # Combine all processed chunks
        if processed_chunks:
            df = pd.concat(processed_chunks, ignore_index=True)
        else:
            # Return empty dataframe with proper structure
            df = pd.DataFrame()

        # Calculate filtering statistics for the combined result
        filtered_row_count = len(df)
        filtering_stats = {
            "original_rows": original_row_count,
            "filtered_rows": filtered_row_count,
            "removed_rows": original_row_count - filtered_row_count,
            "removal_percentage": (
                ((original_row_count - filtered_row_count) / original_row_count) * 100 if original_row_count > 0 else 0
            ),
            "date_range": (
                {"start": df["Date/Time"].min(), "end": df["Date/Time"].max()}
                if len(df) > 0 and "Date/Time" in df.columns
                else None
            ),
            "active_hours": filtered_row_count,
            "inactive_hours": original_row_count - filtered_row_count,
            "memory_usage": get_memory_usage(df),
        }

        # Perform data validation
        validation_results = (
            validate_traffic_data(df, structure)
            if len(df) > 0
            else {"is_valid": True, "warnings": [], "errors": [], "stats": {}}
        )

        # Enhanced structure with metadata
        enhanced_structure = {
            **structure,
            "filtering_stats": filtering_stats,
            "data_quality": validation_results,
            "processing_method": "chunked",
        }

        return df, location_name, enhanced_structure

    except Exception as e:
        raise TrafficDataError(f"Error loading large dataset from '{file_path}': {e}")


def get_available_locations() -> Dict[str, str]:
    """Get list of available data files and their locations."""
    data_dir = get_data_directory()
    if not data_dir.exists():
        return {}

    locations = {}
    
    # Look for -ALL.csv files in the data directory
    for file in data_dir.glob("*-ALL.csv"):
        location_name = get_location_from_file(str(file))
        # If location name extraction fails, derive from filename
        if location_name == "Unknown Location":
            # Extract from filename: "2809_Hampshire_Ave_N-ALL.csv" -> "2809 Hampshire Ave N"
            stem = file.stem.replace("-ALL", "").replace("_", " ")
            location_name = stem.strip()
        locations[location_name] = str(file)

    return locations
