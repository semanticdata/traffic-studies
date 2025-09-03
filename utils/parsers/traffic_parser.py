"""
Traffic data file format detection and parsing.

This module handles the detection and parsing of TrafficViewer Pro CSV files,
including metadata extraction, column mapping, and structure analysis.
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd


class FileStructureError(Exception):
    """Raised when CSV structure doesn't match expected format."""

    pass


def extract_metadata_from_headers(header_lines: List[str]) -> Dict[str, Optional[str]]:
    """Extract metadata information (location, comments, title) from header lines."""
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

    return {"location": location, "comments": comments, "title": title}


def find_column_header_row(header_lines: List[str]) -> Tuple[Optional[str], int]:
    """Find the line containing 'Date/Time' and return the line itself and its row index."""
    for i, line in enumerate(header_lines):
        if "Date/Time" in line:
            return line, i
    return None, -1


def detect_traffic_directions(columns: List[str]) -> Tuple[str, str]:
    """Determine if the directions are 'Northbound'/'Southbound' or 'Eastbound'/'Westbound'."""
    if "Northbound" in "".join(columns):
        return "Northbound", "Southbound"
    else:
        return "Eastbound", "Westbound"


def map_columns(columns: List[str], dir1: str, dir2: str) -> Dict[str, Any]:
    """Map column names to their respective groups (volume, speed, classification)."""
    # Detect speed columns - handle both single and double space formats
    dir1_speed_cols = [col for col in columns if f"MPH - {dir1}" in col or f"MPH  - {dir1}" in col]
    dir2_speed_cols = [col for col in columns if f"MPH - {dir2}" in col or f"MPH  - {dir2}" in col]

    # Detect classification columns - try multiple patterns
    dir1_class_cols = []
    dir2_class_cols = []
    for class_num in range(1, 7):  # Classes 1 through 6
        # Try different possible patterns
        patterns1 = [
            f"Class #{class_num} - {dir1}",
            f"Class {class_num} - {dir1}",
            f"Class{class_num} - {dir1}",
            f"Class #{class_num}-{dir1}",
            f"Class {class_num}-{dir1}",
        ]
        patterns2 = [
            f"Class #{class_num} - {dir2}",
            f"Class {class_num} - {dir2}",
            f"Class{class_num} - {dir2}",
            f"Class #{class_num}-{dir2}",
            f"Class {class_num}-{dir2}",
        ]

        # Try to find matching column for direction 1
        class1_col = None
        for pattern in patterns1:
            matching_cols = [col for col in columns if pattern in col]
            if matching_cols:
                class1_col = matching_cols[0]
                break

        # Try to find matching column for direction 2
        class2_col = None
        for pattern in patterns2:
            matching_cols = [col for col in columns if pattern in col]
            if matching_cols:
                class2_col = matching_cols[0]
                break

        if class1_col:
            dir1_class_cols.append(class1_col)
        else:
            print(f"No column found for {dir1} Class {class_num}")

        if class2_col:
            dir2_class_cols.append(class2_col)
        else:
            print(f"No column found for {dir2} Class {class_num}")

    # Detect volume columns - try multiple patterns
    dir1_volume_col = None
    dir2_volume_col = None

    volume_patterns1 = [f"Volume - {dir1}", dir1, f"{dir1} Volume"]
    volume_patterns2 = [f"Volume - {dir2}", dir2, f"{dir2} Volume"]

    for pattern in volume_patterns1:
        if pattern in columns:
            dir1_volume_col = pattern
            break

    for pattern in volume_patterns2:
        if pattern in columns:
            dir2_volume_col = pattern
            break

    return {
        "dir1_speed_cols": dir1_speed_cols,
        "dir2_speed_cols": dir2_speed_cols,
        "dir1_volume_col": dir1_volume_col,
        "dir2_volume_col": dir2_volume_col,
        "dir1_class_cols": dir1_class_cols,
        "dir2_class_cols": dir2_class_cols,
    }


def detect_file_structure(file_path: str) -> Optional[Dict[str, Any]]:
    """Detect the structure of the CSV file and return appropriate parsing parameters."""
    try:
        with open(file_path, "r") as f:
            header_lines = []
            for _ in range(15):
                try:
                    header_lines.append(next(f))
                except StopIteration:
                    break

        # Extract metadata information using helper function
        metadata = extract_metadata_from_headers(header_lines)

        # Find data columns using helper function
        column_line, metadata_rows = find_column_header_row(header_lines)

        if column_line:
            columns = [col.strip().strip('"') for col in column_line.split(",")]

            # Detect direction names using helper function
            dir1_name, dir2_name = detect_traffic_directions(columns)

            # Map columns to their respective groups using helper function
            column_mapping = map_columns(columns, dir1_name, dir2_name)

            # Detect reference files in subdirectories
            reference_files = detect_reference_files(file_path)

            return {
                "metadata_rows": metadata_rows,
                "columns": columns,
                "location": metadata["location"],
                "comments": metadata["comments"],
                "title": metadata["title"],
                "dir1_name": dir1_name,
                "dir2_name": dir2_name,
                "reference_files": reference_files,
                **column_mapping,
            }
    except Exception as e:
        import traceback

        print(f"Error detecting file structure: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return None


def detect_reference_files(file_path: str) -> Dict[str, Optional[str]]:
    """
    Detect reference CSV files in the same directory as the main file.

    Returns a dictionary with paths to reference files:
    - total_spd_file: Path to Total-SPD.csv (source of truth for 85th percentile)
    - northbound_spd_file: Path to Northbound-SPD.csv
    - southbound_spd_file: Path to Southbound-SPD.csv
    - eastbound_spd_file: Path to Eastbound-SPD.csv
    - westbound_spd_file: Path to Westbound-SPD.csv
    """
    reference_files = {
        "total_spd_file": None,
        "northbound_spd_file": None,
        "southbound_spd_file": None,
        "eastbound_spd_file": None,
        "westbound_spd_file": None,
    }

    try:
        file_path_obj = Path(file_path)
        data_dir = file_path_obj.parent
        file_stem = file_path_obj.stem
        
        # Extract base name from -ALL.csv file: "2809_Hampshire_Ave_N-ALL" -> "2809_Hampshire_Ave_N"
        if "-ALL" in file_stem:
            base_name = file_stem.replace("-ALL", "")
        else:
            base_name = file_stem

        # Look for reference files with the same base name in the same directory
        for file in data_dir.glob("*.csv"):
            file_name = file.name
            file_upper = file_name.upper()

            # Check if this file belongs to the same location
            if file.stem.startswith(base_name):
                if "TOTAL" in file_upper and "SPD" in file_upper:
                    reference_files["total_spd_file"] = str(file)
                elif "NORTHBOUND" in file_upper and "SPD" in file_upper:
                    reference_files["northbound_spd_file"] = str(file)
                elif "SOUTHBOUND" in file_upper and "SPD" in file_upper:
                    reference_files["southbound_spd_file"] = str(file)
                elif "EASTBOUND" in file_upper and "SPD" in file_upper:
                    reference_files["eastbound_spd_file"] = str(file)
                elif "WESTBOUND" in file_upper and "SPD" in file_upper:
                    reference_files["westbound_spd_file"] = str(file)

    except Exception as e:
        print(f"Warning: Could not detect reference files for {file_path}: {e}")

    return reference_files


def extract_posted_speed(total_spd_file: str) -> Optional[int]:
    """
    Extract the posted speed limit from Total-SPD.csv file.
    
    Returns the posted speed as an integer, or None if not found.
    """
    try:
        if not total_spd_file or not os.path.exists(total_spd_file):
            return None

        with open(total_spd_file, "r") as f:
            lines = f.readlines()

        # Look for the "Posted Speed:" line in the header
        for line in lines:
            if "Posted Speed:" in line:
                # Extract the value after "Posted Speed:"
                # Handle formats like '"Posted Speed:","35"'
                parts = line.split("Posted Speed:")
                if len(parts) > 1:
                    speed_part = parts[1].strip().strip(',').strip('"').strip()
                    try:
                        return int(float(speed_part))
                    except ValueError:
                        continue
        
        return None

    except Exception as e:
        print(f"Warning: Could not extract posted speed from {total_spd_file}: {e}")
        return None


def load_reference_speed_data(total_spd_file: str) -> Optional[pd.DataFrame]:
    """
    Load speed reference data from Total-SPD.csv reference file.

    Returns DataFrame with columns: Date/Time, Mean Speed, 85th Percentile (and other speed data)
    This is the authoritative source of truth from TrafficViewer Pro software.
    """
    try:
        if not total_spd_file or not os.path.exists(total_spd_file):
            return None

        # Read the CSV file and find the header row
        with open(total_spd_file, "r") as f:
            lines = f.readlines()

        # Find the line with column headers
        header_row_idx = None
        for i, line in enumerate(lines):
            if "Date/Time" in line and ("85th Percentile" in line or "Mean Speed" in line):
                header_row_idx = i
                break

        if header_row_idx is None:
            print(f"Warning: Could not find header row in reference file: {total_spd_file}")
            return None

        # Handle malformed CSV by manually fixing the header line before parsing
        fixed_lines = []
        for i, line in enumerate(lines):
            if i == header_row_idx:
                # Fix the malformed header by adding the missing comma
                fixed_line = line.replace('"Total""Mean Speed"', '"Total","Mean Speed"')
                fixed_lines.append(fixed_line)
            elif i > header_row_idx:
                fixed_lines.append(line)

        # Create a temporary string to read the fixed CSV
        from io import StringIO
        fixed_csv_content = ''.join(fixed_lines)
        
        # Load the CSV from the fixed content
        df = pd.read_csv(StringIO(fixed_csv_content))

        # Clean column names
        df.columns = df.columns.str.strip()

        # Parse the Date/Time column - handle the format "07/15/2025 14:00 - 14:59"
        if "Date/Time" in df.columns:
            # Ensure we're working with strings, then extract just the date and start time part
            df["Date/Time"] = df["Date/Time"].astype(str)
            df["Date/Time"] = df["Date/Time"].str.split(" - ").str[0]
            df["Date/Time"] = pd.to_datetime(df["Date/Time"], format="%m/%d/%Y %H:%M", errors="coerce")

        # Check for available speed columns
        has_mean_speed = "Mean Speed" in df.columns
        has_85th_percentile = "85th Percentile" in df.columns

        if not has_mean_speed and not has_85th_percentile:
            print(f"Warning: No speed reference columns found in {total_spd_file}")
            return None

        # Filter out rows with no data (Total = 0)
        if "Total" in df.columns:
            df = df[df["Total"] > 0].copy()

        # Remove rows where available speed data is 0 or NaN
        valid_rows = pd.Series(True, index=df.index)
        
        if has_mean_speed:
            valid_rows &= df["Mean Speed"].notna() & (df["Mean Speed"] > 0)
        
        if has_85th_percentile:
            valid_rows &= df["85th Percentile"].notna() & (df["85th Percentile"] > 0)
        
        df = df[valid_rows].copy()

        columns_loaded = []
        if has_mean_speed:
            columns_loaded.append("Mean Speed")
        if has_85th_percentile:
            columns_loaded.append("85th Percentile")

        print(f"Loaded {len(df)} rows of reference speed data ({', '.join(columns_loaded)}) from {total_spd_file}")
        return df

    except Exception as e:
        print(f"Error loading reference speed data from {total_spd_file}: {e}")
        return None


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
                    # Handle CSV format: "Location:","value"
                    after_split = line.split("Location:")[1].strip()
                    # Remove the leading comma and quotes: '","value"' -> 'value'
                    if after_split.startswith('","'):
                        location = after_split[3:-1]  # Remove '","' from start and '"' from end
                    else:
                        location = after_split.strip().strip('"').strip("'").strip(",").strip()

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
