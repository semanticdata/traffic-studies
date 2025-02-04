import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re  # Import regex for parsing
import csv  # Add this with other imports
import numpy as np
import traceback

# Set the directory containing the CSV files
data_directory = 'data'
error_log_file = 'error_log.txt'  # File to log errors
output_directory = 'output'  # Directory to save output figures

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

def detect_file_structure(file_path):
    """Detect the structure of the CSV file and return appropriate parsing parameters."""
    try:
        with open(file_path, 'r') as f:
            header_lines = [next(f) for _ in range(15)]
        
        # Extract metadata information
        location = None
        comments = None
        title = None
        
        for line in header_lines:
            if 'Location:' in line:
                location = line.split('Location:')[1].strip().strip('"').strip(',')
            elif 'Comments:' in line:
                comments = line.split('Comments:')[1].strip().strip('"').strip(',')
            elif 'Title:' in line:
                title = line.split('Title:')[1].strip().strip('"').strip(',')
        
        # Find data columns
        column_line = None
        for i, line in enumerate(header_lines):
            if 'Date/Time' in line:
                column_line = line
                metadata_rows = i
                break
        
        if column_line:
            columns = [col.strip().strip('"') for col in column_line.split(',')]
            
            # Detect direction pairs based on column names
            dir1_speed_cols = [col for col in columns if 'MPH  - Northbound' in col]
            dir2_speed_cols = [col for col in columns if 'MPH  - Southbound' in col]
            
            # If no N/S columns found, try E/W
            if not (dir1_speed_cols and dir2_speed_cols):
                dir1_speed_cols = [col for col in columns if 'MPH  - Eastbound' in col]
                dir2_speed_cols = [col for col in columns if 'MPH  - Westbound' in col]
            
            # Determine the direction pairs
            if 'Northbound' in ''.join(columns):
                dir1_name = 'Northbound'
                dir2_name = 'Southbound'
            else:
                dir1_name = 'Eastbound'
                dir2_name = 'Westbound'
            
            return {
                'metadata_rows': metadata_rows,
                'columns': columns,
                'location': location,
                'comments': comments,
                'title': title,
                'dir1_name': dir1_name,
                'dir2_name': dir2_name,
                'dir1_speed_cols': dir1_speed_cols,
                'dir2_speed_cols': dir2_speed_cols,
                'dir1_volume_col': f'Volume - {dir1_name}',
                'dir2_volume_col': f'Volume - {dir2_name}'
            }
    except Exception as e:
        print(f"Error detecting file structure: {e}")
        return None

def create_speed_compliance_plot(df, structure, output_path):
    """Create speed compliance visualization."""
    plt.figure(figsize=(12, 6))
    
    # Calculate compliance for both directions
    speed_limit = 30  # mph
    directions = [structure['dir1_name'], structure['dir2_name']]
    compliant_data = []
    non_compliant_data = []
    
    for direction in directions:
        speed_cols = structure['dir1_speed_cols'] if direction == structure['dir1_name'] else structure['dir2_speed_cols']
        compliant_cols = [col for col in speed_cols if int(col.split('-')[0].strip()) <= speed_limit]
        non_compliant_cols = [col for col in speed_cols if int(col.split('-')[0].strip()) > speed_limit]
        
        compliant = df[compliant_cols].sum().sum()
        non_compliant = df[non_compliant_cols].sum().sum()
        
        compliant_data.append(compliant)
        non_compliant_data.append(non_compliant)
    
    # Create stacked bar chart
    x = np.arange(len(directions))
    width = 0.35
    
    plt.bar(x, compliant_data, width, label='Compliant (≤30 mph)', color='lightgreen')
    plt.bar(x, non_compliant_data, width, bottom=compliant_data, label='Non-Compliant (>30 mph)', color='salmon')
    
    plt.title(f'Speed Compliance by Direction\n{structure["location"]}')
    plt.xlabel('Direction')
    plt.ylabel('Number of Vehicles')
    plt.xticks(x, directions)
    plt.legend()
    
    # Add percentage labels
    for i in range(len(directions)):
        total = compliant_data[i] + non_compliant_data[i]
        if total > 0:
            pct_compliant = (compliant_data[i] / total) * 100
            plt.text(i, total/2, f'{pct_compliant:.1f}%\nCompliant', 
                    ha='center', va='center')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, f'speed_compliance.png'))
    plt.close()

def create_hourly_pattern_heatmap(df, structure, output_path):
    """Create hourly pattern heatmap by day of week."""
    plt.figure(figsize=(12, 6))
    
    # Add day of week and prepare data
    df['DayOfWeek'] = df['Date/Time'].dt.day_name()
    df['Hour'] = df['Date/Time'].dt.hour
    
    # Calculate average total volume by day and hour
    volume_cols = [structure['dir1_volume_col'], structure['dir2_volume_col']]
    df['Total'] = df[volume_cols].sum(axis=1)
    
    pivot_data = df.pivot_table(
        values='Total',
        index='DayOfWeek',
        columns='Hour',
        aggfunc='mean'
    )
    
    # Reorder days to start with Monday
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot_data = pivot_data.reindex(days_order)
    
    # Create heatmap
    sns.heatmap(pivot_data, cmap='YlOrRd', annot=True, fmt='.0f', cbar_kws={'label': 'Average Vehicles'})
    
    plt.title(f'Average Hourly Traffic Pattern by Day\n{structure["location"]}')
    plt.xlabel('Hour of Day')
    plt.ylabel('Day of Week')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, f'hourly_pattern_heatmap.png'))
    plt.close()

def main():
    """Main function to run traffic analysis."""
    try:
        # Process each CSV file in the data directory
        for filename in os.listdir(data_directory):
            if filename.endswith('.csv'):
                file_path = os.path.join(data_directory, filename)
                
                # Detect file structure
                structure = detect_file_structure(file_path)
                if not structure:
                    continue
                
                # Read and process data
                df = pd.read_csv(file_path, skiprows=structure['metadata_rows'])
                df['Date/Time'] = pd.to_datetime(df['Date/Time'])
                
                # Create visualizations
                create_speed_compliance_plot(df, structure, output_directory)
                create_hourly_pattern_heatmap(df, structure, output_directory)
                plot_traffic_analysis(df, structure['location'])
                
    except Exception as e:
        print(f"Error in main: {str(e)}")
        print(traceback.format_exc())

# Loop through all CSV files in the data directory
for filename in os.listdir(data_directory):
    if filename.endswith('.csv'):
        # Read the CSV file
        file_path = os.path.join(data_directory, filename)
        try:
            # Read the first 14 lines to extract metadata
            with open(file_path, 'r') as file:
                header_lines = [next(file) for _ in range(14)]
            
            # Parse the required information
            location = re.search(r'Location:\s*(.*)', header_lines[3]).group(1).strip()
            comments = re.search(r'Comments:\s*(.*)', header_lines[4]).group(1).strip()
            title = re.search(r'Title:\s*(.*)', header_lines[13]).group(1).strip()
            
            # Read the actual data starting from line 15
            data = pd.read_csv(file_path, skiprows=14, on_bad_lines='skip')  # Skip bad lines
            
            # Parse the 'Date/Time' column for date and hour
            data['DateTime'] = pd.to_datetime(data['Date/Time'])
            data['Date'] = data['DateTime'].dt.date
            data['Hour'] = data['DateTime'].dt.hour
            data['DayOfWeek'] = data['DateTime'].dt.day_name()

            # Calculate total volumes by direction
            direction_columns = [col for col in data.columns if 'Volume' in col]
            data['Total Volume'] = data[direction_columns].sum(axis=1)

            # Create hourly traffic pattern visualization
            plt.figure(figsize=(12, 6))
            
            # Plot each direction separately
            for col in direction_columns:
                direction = col.split(' - ')[1]  # Extract direction name
                hourly_avg = data.groupby('Hour')[col].mean()
                plt.plot(hourly_avg.index, hourly_avg.values, label=direction, marker='o')

            plt.title(f'Average Hourly Traffic Pattern\n{location}\n{title}')
            plt.xlabel('Hour of Day')
            plt.ylabel('Average Vehicle Count')
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.legend()
            plt.xticks(range(0, 24))
            
            # Adjust layout and save
            plt.tight_layout()
            output_file = os.path.join(output_directory, f'{filename}_hourly_pattern.png')
            plt.savefig(output_file)
            plt.close()

            # Create daily traffic pattern by day of week
            plt.figure(figsize=(12, 6))
            
            # Calculate daily totals and handle missing days
            daily_totals = data.groupby(['DayOfWeek', 'Date'])['Total Volume'].sum().reset_index()
            daily_averages = daily_totals.groupby('DayOfWeek')['Total Volume'].mean()
            
            # Reorder days to start with Monday
            days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            daily_averages = daily_averages.reindex(days_order)
            
            # Create bar plot
            bars = plt.bar(daily_averages.index, daily_averages.values)
            
            # Add value labels on top of each bar
            for bar in bars:
                height = bar.get_height()
                if pd.notna(height):  # Only add label if height is not NaN
                    plt.text(bar.get_x() + bar.get_width()/2., height,
                            f'{int(round(height))}',  # Round to nearest integer
                            ha='center', va='bottom')

            plt.title(f'Average Daily Traffic Volume by Day\n{location}\n{title}')
            plt.xlabel('Day of Week')
            plt.ylabel('Average Daily Vehicle Count')
            plt.grid(True, linestyle='--', alpha=0.7, axis='y')
            plt.xticks(rotation=45)
            
            # Adjust layout and save
            plt.tight_layout()
            output_file = os.path.join(output_directory, f'{filename}_daily_pattern.png')
            plt.savefig(output_file)
            plt.close()

        except Exception as e:
            with open(error_log_file, 'a') as log_file:
                log_file.write(f"Error processing {filename}: {str(e)}\n")
            continue
