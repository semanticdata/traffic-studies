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
            data['Date'] = pd.to_datetime(data['Date/Time']).dt.date
            data['Hour'] = pd.to_datetime(data['Date/Time']).dt.hour
            
            # Create a simple visualization
            plt.figure(figsize=(10, 6))
            sns.lineplot(data=data)
            plt.title(f'Visualization of {filename}')
            plt.xlabel('Index')
            plt.ylabel('Values')
            plt.legend(data.columns)

            # Save the figure instead of showing it
            output_file = os.path.join(output_directory, f'{filename}.png')  # Save to output directory
            plt.savefig(output_file)
            plt.close()  # Close the figure to free memory
        except pd.errors.ParserError as e:
            with open(error_log_file, 'a') as log_file:
                log_file.write(f"Error reading {filename}: {e}\n")
            continue  # Skip to the next file if there's an error
