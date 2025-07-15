"""
Data loading utilities for Traffic Studies dashboard.

This module provides functions to load and process traffic data from CSV files
exported from TrafficViewer Pro software. It handles file structure detection,
metadata extraction, data preprocessing, validation, and optimization for the Streamlit dashboard.

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
from typing import Dict, Optional, Tuple

import pandas as pd


class TrafficDataError(Exception):
    """Base exception for traffic data processing."""

    pass


class DataValidationError(TrafficDataError):
    """Raised when data validation fails."""

    def __init__(self, message, validation_details=None):
        super().__init__(message)
        self.validation_details = validation_details or {}


class FileStructureError(TrafficDataError):
    """Raised when CSV structure doesn't match expected format."""

    pass


def validate_traffic_data(df: pd.DataFrame, structure: Dict[str, any]) -> Dict[str, any]:
    """Comprehensive data validation with detailed reporting."""
    validation_results = {"is_valid": True, "warnings": [], "errors": [], "stats": {}}

    # Volume validation
    vol_cols = [structure["dir1_volume_col"], structure["dir2_volume_col"]]

    for col in vol_cols:
        if col in df.columns:
            # Check for negative values
            negative_count = (df[col] < 0).sum()
            if negative_count > 0:
                validation_results["errors"].append(f"Found {negative_count} negative values in {col}")
                validation_results["is_valid"] = False

            # Check for unrealistic maximum values (>1000 vehicles/hour)
            max_val = df[col].max()
            if max_val > 1000:
                validation_results["warnings"].append(
                    f"Unusually high traffic volume in {col}: {max_val} vehicles/hour"
                )

            # Store statistics
            validation_results["stats"][f"{col}_max"] = max_val
            validation_results["stats"][f"{col}_mean"] = df[col].mean()

    # Cross-check total vs sum of directional volumes
    if "Total" in df.columns and all(col in df.columns for col in vol_cols):
        total_diff = abs(df["Total"] - (df[vol_cols[0]] + df[vol_cols[1]])).sum()
        if total_diff > 0:
            validation_results["errors"].append(
                f"Total column doesn't match sum of directional volumes (difference: {total_diff})"
            )
            validation_results["is_valid"] = False

    # Speed validation
    speed_cols = structure["dir1_speed_cols"] + structure["dir2_speed_cols"]
    for col in speed_cols:
        if col in df.columns:
            # Check for negative values
            negative_count = (df[col] < 0).sum()
            if negative_count > 0:
                validation_results["errors"].append(f"Found {negative_count} negative values in speed column {col}")
                validation_results["is_valid"] = False

    # Temporal validation
    if "Date/Time" in df.columns:
        # Check for missing time periods (assuming hourly data)
        time_diffs = df["Date/Time"].diff().dropna()
        expected_diff = pd.Timedelta(hours=1)
        irregular_intervals = (time_diffs != expected_diff).sum()
        if irregular_intervals > 0:
            validation_results["warnings"].append(f"Found {irregular_intervals} irregular time intervals")

        # Store temporal statistics
        validation_results["stats"]["date_range"] = {
            "start": df["Date/Time"].min(),
            "end": df["Date/Time"].max(),
            "total_hours": len(df),
        }

    # Classification validation
    class_cols = structure["dir1_class_cols"] + structure["dir2_class_cols"]
    for col in class_cols:
        if col in df.columns:
            # Check for negative values
            negative_count = (df[col] < 0).sum()
            if negative_count > 0:
                validation_results["errors"].append(
                    f"Found {negative_count} negative values in classification column {col}"
                )
                validation_results["is_valid"] = False

    return validation_results


def get_data_directory() -> Path:
    """Get the path to the data directory relative to the project root."""
    # Get the current file's directory (utils)
    current_dir = Path(__file__).parent
    # Go up one level to project root and then into data directory
    data_dir = current_dir.parent / "data"
    return data_dir


def get_location_from_file(file_path: str) -> str:
    """Extract location name from the CSV file metadata."""
    try:
        with open(file_path, "r") as f:
            header_lines = []
            for _ in range(6):
                try:
                    header_lines.append(next(f))
                except StopIteration:
                    break

        for line in header_lines:
            # Handle both "Location," and "Location:" formats
            if line.startswith("Location,") or "Location:" in line:
                if "Location," in line:
                    location = line.split("Location,")[1].strip().strip('"').strip("'").strip(",").strip()
                else:
                    location = line.split("Location:")[1].strip().strip('"').strip("'").strip(",").strip()

                if location:
                    return location

        # Fallback: try to extract from filename
        stem = Path(file_path).stem
        if "-" in stem:
            return stem.split("-")[1].replace("_", " ").strip().strip('"').strip("'").title()
        else:
            return "Unknown Location"
    except Exception:
        return "Unknown Location"


def detect_file_structure(file_path: str) -> Optional[Dict[str, any]]:
    """Detect the structure of the CSV file and return appropriate parsing parameters."""
    try:
        with open(file_path, "r") as f:
            header_lines = []
            for _ in range(15):
                try:
                    header_lines.append(next(f))
                except StopIteration:
                    break

        # Extract metadata information
        location = None
        comments = None
        title = None

        for line in header_lines:
            # Handle CSV format (comma-separated) and other formats
            if line.startswith("Location,") or "Location:" in line:
                if "Location," in line:
                    location = line.split("Location,")[1].strip().strip('"').strip("'").strip(",").strip()
                else:
                    parts = line.strip().split('","')
                    if len(parts) > 1:
                        location = parts[1].replace('"', "").strip()
                    else:
                        location = line.split("Location:")[1].strip().strip('"').strip("'").strip(",").strip()
            elif line.startswith("Comments,") or "Comments:" in line:
                if "Comments," in line:
                    comments = line.split("Comments,")[1].strip().strip('"').strip(",")
                else:
                    comments = line.split("Comments:")[1].strip().strip('"').strip(",")
            elif line.startswith("Title,") or "Title:" in line:
                if "Title," in line:
                    title = line.split("Title,")[1].strip().strip('"').strip(",")
                else:
                    title = line.split("Title:")[1].strip().strip('"').strip(",")

        # Find data columns
        column_line = None
        for i, line in enumerate(header_lines):
            if "Date/Time" in line:
                column_line = line
                metadata_rows = i
                break

        if column_line:
            columns = [col.strip().strip('"') for col in column_line.split(",")]

            # Debug print
            # print("\nAll columns found:", columns)

            # Detect direction names
            if "Northbound" in "".join(columns):
                dir1_name = "Northbound"
                dir2_name = "Southbound"
            else:
                dir1_name = "Eastbound"
                dir2_name = "Westbound"

            # Debug print
            # print(f"\nDirections detected: {dir1_name}, {dir2_name}")

            # Detect speed columns - handle both single and double space formats
            dir1_speed_cols = [col for col in columns if f"MPH - {dir1_name}" in col or f"MPH  - {dir1_name}" in col]
            dir2_speed_cols = [col for col in columns if f"MPH - {dir2_name}" in col or f"MPH  - {dir2_name}" in col]

            # print(f"\nSpeed columns found for {dir1_name}:", dir1_speed_cols)
            # print(f"Speed columns found for {dir2_name}:", dir2_speed_cols)

            # Detect classification columns - try multiple patterns
            dir1_class_cols = []
            dir2_class_cols = []
            for class_num in range(1, 7):  # Classes 1 through 6
                # Try different possible patterns
                patterns1 = [
                    f"Class #{class_num} - {dir1_name}",
                    f"Class {class_num} - {dir1_name}",
                    f"Class{class_num} - {dir1_name}",
                    f"Class #{class_num}-{dir1_name}",
                    f"Class {class_num}-{dir1_name}",
                ]
                patterns2 = [
                    f"Class #{class_num} - {dir2_name}",
                    f"Class {class_num} - {dir2_name}",
                    f"Class{class_num} - {dir2_name}",
                    f"Class #{class_num}-{dir2_name}",
                    f"Class {class_num}-{dir2_name}",
                ]

                # Try to find matching column for direction 1
                class1_col = None
                for pattern in patterns1:
                    # print(f"Trying pattern for dir1: '{pattern}'")
                    matching_cols = [col for col in columns if pattern in col]
                    if matching_cols:
                        class1_col = matching_cols[0]
                        break

                # Try to find matching column for direction 2
                class2_col = None
                for pattern in patterns2:
                    # print(f"Trying pattern for dir2: '{pattern}'")
                    matching_cols = [col for col in columns if pattern in col]
                    if matching_cols:
                        class2_col = matching_cols[0]
                        break

                if class1_col:
                    # print(f"Found {dir1_name} Class {class_num}: {class1_col}")
                    dir1_class_cols.append(class1_col)
                else:
                    print(f"No column found for {dir1_name} Class {class_num}")

                if class2_col:
                    # print(f"Found {dir2_name} Class {class_num}: {class2_col}")
                    dir2_class_cols.append(class2_col)
                else:
                    print(f"No column found for {dir2_name} Class {class_num}")

            # Debug print final results
            # print(f"\nFinal classification columns found:")
            # print(f"{dir1_name}:", dir1_class_cols)
            # print(f"{dir2_name}:", dir2_class_cols)

            # Detect volume columns - try multiple patterns
            dir1_volume_col = None
            dir2_volume_col = None

            volume_patterns1 = [f"Volume - {dir1_name}", dir1_name, f"{dir1_name} Volume"]
            volume_patterns2 = [f"Volume - {dir2_name}", dir2_name, f"{dir2_name} Volume"]

            for pattern in volume_patterns1:
                if pattern in columns:
                    dir1_volume_col = pattern
                    break

            for pattern in volume_patterns2:
                if pattern in columns:
                    dir2_volume_col = pattern
                    break

            # print(f"\nVolume columns found:")
            # print(f"  {dir1_name}: {dir1_volume_col}")
            # print(f"  {dir2_name}: {dir2_volume_col}")

            return {
                "metadata_rows": metadata_rows,
                "columns": columns,
                "location": location,
                "comments": comments,
                "title": title,
                "dir1_name": dir1_name,
                "dir2_name": dir2_name,
                "dir1_speed_cols": dir1_speed_cols,
                "dir2_speed_cols": dir2_speed_cols,
                "dir1_volume_col": dir1_volume_col,
                "dir2_volume_col": dir2_volume_col,
                "dir1_class_cols": dir1_class_cols,
                "dir2_class_cols": dir2_class_cols,
            }
    except Exception as e:
        import traceback

        print(f"Error detecting file structure: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return None


def load_data(file_path: str, speed_limit: int = 30) -> Tuple[pd.DataFrame, str, Dict[str, any]]:
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

        # Process datetime with validation
        df["Date/Time"] = pd.to_datetime(df["Date/Time"], errors="coerce")
        invalid_dates = df["Date/Time"].isna().sum()
        if invalid_dates > 0:
            raise DataValidationError(f"Found {invalid_dates} invalid date/time values in '{file_path}'")

        df["Hour"] = df["Date/Time"].dt.hour

        # Store original row count for filtering statistics
        original_row_count = len(df)

        # Speed compliance calculations using proper speed range logic
        dir1_speed_cols = structure["dir1_speed_cols"]
        dir2_speed_cols = structure["dir2_speed_cols"]

        # Calculate compliance for direction 1
        df["Dir1_Compliant"] = 0
        df["Dir1_Non_Compliant"] = 0
        
        for col in dir1_speed_cols:
            if col in df.columns:
                try:
                    # Extract speed from column name
                    speed_part = col.split("MPH")[0].strip()
                    if "+" in speed_part:
                        # Handle "45+" format - use the number as-is
                        speed = float(speed_part.replace("+", "").strip())
                    else:
                        # Handle "25-29" format - use lower bound
                        speed = float(speed_part.split("-")[0].strip())
                    
                    # Add vehicle counts to appropriate compliance category
                    if speed <= speed_limit:
                        df["Dir1_Compliant"] += df[col]
                    else:
                        df["Dir1_Non_Compliant"] += df[col]
                except (ValueError, IndexError):
                    # Skip columns that don't have valid speed format
                    continue

        # Calculate compliance for direction 2
        df["Dir2_Compliant"] = 0
        df["Dir2_Non_Compliant"] = 0
        
        for col in dir2_speed_cols:
            if col in df.columns:
                try:
                    # Extract speed from column name
                    speed_part = col.split("MPH")[0].strip()
                    if "+" in speed_part:
                        # Handle "45+" format - use the number as-is
                        speed = float(speed_part.replace("+", "").strip())
                    else:
                        # Handle "25-29" format - use lower bound
                        speed = float(speed_part.split("-")[0].strip())
                    
                    # Add vehicle counts to appropriate compliance category
                    if speed <= speed_limit:
                        df["Dir2_Compliant"] += df[col]
                    else:
                        df["Dir2_Non_Compliant"] += df[col]
                except (ValueError, IndexError):
                    # Skip columns that don't have valid speed format
                    continue

        # Vectorized total calculation
        df["Total"] = df[structure["dir1_volume_col"]] + df[structure["dir2_volume_col"]]

        # Filter out rows where both volume columns are 0 (no traffic activity)
        df = df[(df[structure["dir1_volume_col"]] > 0) | (df[structure["dir2_volume_col"]] > 0)]

        # Calculate filtering statistics
        filtered_row_count = len(df)
        filtering_stats = {
            "original_rows": original_row_count,
            "filtered_rows": filtered_row_count,
            "removed_rows": original_row_count - filtered_row_count,
            "removal_percentage": (
                ((original_row_count - filtered_row_count) / original_row_count) * 100 if original_row_count > 0 else 0
            ),
            "date_range": {"start": df["Date/Time"].min(), "end": df["Date/Time"].max()} if len(df) > 0 else None,
            "active_hours": filtered_row_count,
            "inactive_hours": original_row_count - filtered_row_count,
        }

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
        enhanced_structure = {**structure, "filtering_stats": filtering_stats, "data_quality": validation_results}

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
) -> Tuple[pd.DataFrame, str, Dict[str, any]]:
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

            # Process datetime
            chunk["Date/Time"] = pd.to_datetime(chunk["Date/Time"], errors="coerce")
            chunk["Hour"] = chunk["Date/Time"].dt.hour

            # Speed compliance calculations using proper speed range logic
            dir1_speed_cols = structure["dir1_speed_cols"]
            dir2_speed_cols = structure["dir2_speed_cols"]

            # Calculate compliance for direction 1
            chunk["Dir1_Compliant"] = 0
            chunk["Dir1_Non_Compliant"] = 0
            
            for col in dir1_speed_cols:
                if col in chunk.columns:
                    try:
                        # Extract speed from column name
                        speed_part = col.split("MPH")[0].strip()
                        if "+" in speed_part:
                            # Handle "45+" format - use the number as-is
                            speed = float(speed_part.replace("+", "").strip())
                        else:
                            # Handle "25-29" format - use lower bound
                            speed = float(speed_part.split("-")[0].strip())
                        
                        # Add vehicle counts to appropriate compliance category
                        if speed <= speed_limit:
                            chunk["Dir1_Compliant"] += chunk[col]
                        else:
                            chunk["Dir1_Non_Compliant"] += chunk[col]
                    except (ValueError, IndexError):
                        # Skip columns that don't have valid speed format
                        continue

            # Calculate compliance for direction 2
            chunk["Dir2_Compliant"] = 0
            chunk["Dir2_Non_Compliant"] = 0
            
            for col in dir2_speed_cols:
                if col in chunk.columns:
                    try:
                        # Extract speed from column name
                        speed_part = col.split("MPH")[0].strip()
                        if "+" in speed_part:
                            # Handle "45+" format - use the number as-is
                            speed = float(speed_part.replace("+", "").strip())
                        else:
                            # Handle "25-29" format - use lower bound
                            speed = float(speed_part.split("-")[0].strip())
                        
                        # Add vehicle counts to appropriate compliance category
                        if speed <= speed_limit:
                            chunk["Dir2_Compliant"] += chunk[col]
                        else:
                            chunk["Dir2_Non_Compliant"] += chunk[col]
                    except (ValueError, IndexError):
                        # Skip columns that don't have valid speed format
                        continue

            # Calculate total
            chunk["Total"] = chunk[structure["dir1_volume_col"]] + chunk[structure["dir2_volume_col"]]

            # Filter zero rows
            filtered_chunk = chunk[
                (chunk[structure["dir1_volume_col"]] > 0) | (chunk[structure["dir2_volume_col"]] > 0)
            ]

            if len(filtered_chunk) > 0:
                processed_chunks.append(filtered_chunk)

        # Combine all processed chunks
        if processed_chunks:
            df = pd.concat(processed_chunks, ignore_index=True)
        else:
            # Return empty dataframe with proper structure
            df = pd.DataFrame()

        # Calculate filtering statistics
        filtered_row_count = len(df)
        filtering_stats = {
            "original_rows": original_row_count,
            "filtered_rows": filtered_row_count,
            "removed_rows": original_row_count - filtered_row_count,
            "removal_percentage": (
                ((original_row_count - filtered_row_count) / original_row_count) * 100 if original_row_count > 0 else 0
            ),
            "date_range": {"start": df["Date/Time"].min(), "end": df["Date/Time"].max()} if len(df) > 0 else None,
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
    for file in data_dir.glob("*.csv"):
        location_name = get_location_from_file(str(file))
        locations[location_name] = str(file)

    return locations
