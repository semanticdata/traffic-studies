import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re  # Import regex for parsing

# Set the directory containing the CSV files
data_directory = 'data'
error_log_file = 'error_log.txt'  # File to log errors
output_directory = 'output'  # Directory to save output figures

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

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
