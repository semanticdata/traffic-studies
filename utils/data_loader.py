import pandas as pd
from pathlib import Path


def get_data_directory():
    """Get the path to the data directory relative to the project root."""
    # Get the current file's directory (utils)
    current_dir = Path(__file__).parent
    # Go up one level to project root and then into data directory
    data_dir = current_dir.parent / "data"
    return data_dir


def get_location_from_file(file_path):
    """Extract location name from the CSV file metadata."""
    try:
        with open(file_path, "r") as f:
            header_lines = [next(f) for _ in range(6)]

        for line in header_lines:
            if "Location:" in line:
                location = (
                    line.split("Location:")[1]
                    .strip()
                    .strip('"')
                    .strip("'")
                    .strip(",")
                    .strip()
                )
                return location

        return (
            Path(file_path)
            .stem.split("-")[1]
            .replace("_", " ")
            .strip()
            .strip('"')
            .strip("'")
            .title()
        )
    except Exception:
        return (
            Path(file_path)
            .stem.split("-")[1]
            .replace("_", " ")
            .strip()
            .strip('"')
            .strip("'")
            .title()
        )


def detect_file_structure(file_path):
    """Detect the structure of the CSV file and return appropriate parsing parameters."""
    try:
        with open(file_path, "r") as f:
            header_lines = [next(f) for _ in range(15)]

        # Extract metadata information
        location = None
        comments = None
        title = None

        for line in header_lines:
            if "Location:" in line:
                parts = line.strip().split('","')
                if len(parts) > 1:
                    location = parts[1].replace('"', "").strip()
                else:
                    location = (
                        line.split("Location:")[1]
                        .strip()
                        .strip('"')
                        .strip("'")
                        .strip(",")
                        .strip()
                    )
            elif "Comments:" in line:
                comments = line.split("Comments:")[
                    1].strip().strip('"').strip(",")
            elif "Title:" in line:
                title = line.split("Title:")[1].strip().strip('"').strip(",")

        # Find data columns
        column_line = None
        for i, line in enumerate(header_lines):
            if "Date/Time" in line:
                column_line = line
                metadata_rows = i
                break

        if column_line:
            columns = [col.strip().strip('"')
                       for col in column_line.split(",")]

            # Detect direction pairs based on column names
            dir1_speed_cols = [
                col for col in columns if "MPH  - Northbound" in col]
            dir2_speed_cols = [
                col for col in columns if "MPH  - Southbound" in col]

            if not (dir1_speed_cols and dir2_speed_cols):
                dir1_speed_cols = [
                    col for col in columns if "MPH  - Eastbound" in col]
                dir2_speed_cols = [
                    col for col in columns if "MPH  - Westbound" in col]

            if "Northbound" in "".join(columns):
                dir1_name = "Northbound"
                dir2_name = "Southbound"
            else:
                dir1_name = "Eastbound"
                dir2_name = "Westbound"

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
                "dir1_volume_col": f"Volume - {dir1_name}",
                "dir2_volume_col": f"Volume - {dir2_name}",
            }
    except Exception as e:
        print(f"Error detecting file structure: {e}")
        return None


def load_data(file_path, speed_limit=30):
    """Load and process traffic data from CSV file."""
    structure = detect_file_structure(file_path)
    if not structure:
        raise ValueError("Could not detect file structure")

    location_name = structure["location"]
    if location_name and isinstance(location_name, str):
        location_name = location_name.strip().strip('"').strip("'").strip(",").strip()

    try:
        df = pd.read_csv(file_path, skiprows=structure["metadata_rows"])
        df["Date/Time"] = pd.to_datetime(df["Date/Time"], errors="coerce")
        df["Hour"] = df["Date/Time"].dt.hour

        dir1_speed_cols = structure["dir1_speed_cols"]
        dir2_speed_cols = structure["dir2_speed_cols"]

        df["Dir1_Compliant"] = df[dir1_speed_cols].apply(
            lambda x: (x <= speed_limit).sum(), axis=1
        )
        df["Dir1_Non_Compliant"] = df[dir1_speed_cols].apply(
            lambda x: (x > speed_limit).sum(), axis=1
        )

        df["Dir2_Compliant"] = df[dir2_speed_cols].apply(
            lambda x: (x <= speed_limit).sum(), axis=1
        )
        df["Dir2_Non_Compliant"] = df[dir2_speed_cols].apply(
            lambda x: (x > speed_limit).sum(), axis=1
        )

        df["Total"] = (
            df[structure["dir1_volume_col"]] + df[structure["dir2_volume_col"]]
        )

        return df, location_name, structure

    except Exception as e:
        raise Exception(f"Error loading data: {e}")


def get_available_locations():
    """Get list of available data files and their locations."""
    data_dir = get_data_directory()
    if not data_dir.exists():
        return {}

    locations = {}
    for file in data_dir.glob("*.csv"):
        location_name = get_location_from_file(str(file))
        locations[location_name] = str(file)

    return locations
