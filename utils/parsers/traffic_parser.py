"""
Traffic data file format detection and parsing.

This module handles the detection and parsing of TrafficViewer Pro CSV files,
including metadata extraction, column mapping, and structure analysis.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


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

            return {
                "metadata_rows": metadata_rows,
                "columns": columns,
                "location": metadata["location"],
                "comments": metadata["comments"],
                "title": metadata["title"],
                "dir1_name": dir1_name,
                "dir2_name": dir2_name,
                **column_mapping,
            }
    except Exception as e:
        import traceback

        print(f"Error detecting file structure: {e}")
        print(f"Traceback: {traceback.format_exc()}")
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
