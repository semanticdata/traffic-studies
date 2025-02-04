import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import traceback

def extract_location(metadata_lines):
    """Extract location from metadata."""
    for line in metadata_lines:
        if line.startswith('"Location:","'):
            return line.split('","')[1]
    return "Unknown Location"

def read_traffic_data(file_path):
    """Read and process traffic data from CSV file."""
    try:
        # Read metadata first (first 14 lines)
        with open(file_path, 'r') as f:
            metadata_lines = [next(f) for _ in range(14)]
        
        location = extract_location(metadata_lines)
        
        # Read the actual data, skipping metadata
        df = pd.read_csv(file_path, skiprows=14)
        
        # Convert Date/Time column
        try:
            df['Date/Time'] = pd.to_datetime(df['Date/Time'], format='%m/%d/%Y %H:%M')
        except Exception as e:
            print(f"Error parsing dates: {e}")
            # Try alternative date parsing if the first attempt fails
            df['Date/Time'] = pd.to_datetime(df['Date/Time'])
            
        df['Hour'] = df['Date/Time'].dt.hour
        
        return df, location
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        print(traceback.format_exc())
        return None, None

def calculate_compliance(df):
    """Calculate speed compliance statistics for both directions."""
    speed_limit = 30  # mph
    
    try:
        # Northbound compliance
        nb_speeds = df[[col for col in df.columns if 'MPH  - Northbound' in col]]
        nb_total = nb_speeds.sum().sum()
        nb_compliant = df[[col for col in df.columns if 'MPH  - Northbound' in col and int(col.split('-')[0].strip()) <= speed_limit]].sum().sum()
        nb_compliance = (nb_compliant / nb_total * 100) if nb_total > 0 else 0
        
        # Southbound compliance
        sb_speeds = df[[col for col in df.columns if 'MPH  - Southbound' in col]]
        sb_total = sb_speeds.sum().sum()
        sb_compliant = df[[col for col in df.columns if 'MPH  - Southbound' in col and int(col.split('-')[0].strip()) <= speed_limit]].sum().sum()
        sb_compliance = (sb_compliant / sb_total * 100) if sb_total > 0 else 0
        
        return nb_compliance, sb_compliance
    except Exception as e:
        print(f"Error calculating compliance: {str(e)}")
        return 0, 0

def plot_traffic_analysis(df, location):
    """Create visualizations for traffic analysis."""
    plt.style.use('seaborn')
    fig = plt.figure(figsize=(20, 15))
    
    # 1. Total Volume by Direction
    total_nb = df['Volume - Northbound'].sum()
    total_sb = df['Volume - Southbound'].sum()
    total_vehicles = total_nb + total_sb
    
    # Calculate dominant direction
    dominant_dir = "Northbound" if total_nb > total_sb else "Southbound"
    dominant_pct = (max(total_nb, total_sb) / total_vehicles * 100)
    
    # 2. Hourly Volume by Direction
    plt.subplot(2, 2, 1)
    hourly_data = df.groupby('Hour')[['Volume - Northbound', 'Volume - Southbound']].mean()
    hourly_data.plot(kind='bar', stacked=True)
    plt.title('Average Hourly Traffic Volume by Direction')
    plt.xlabel('Hour of Day')
    plt.ylabel('Average Vehicles per Hour')
    
    # 3. Speed Distribution - Northbound
    plt.subplot(2, 2, 2)
    speed_cols_nb = [col for col in df.columns if 'MPH  - Northbound' in col]
    speed_data_nb = df[speed_cols_nb].sum()
    speed_data_nb.index = [int(col.split('-')[0]) for col in speed_cols_nb]
    speed_data_nb.plot(kind='bar')
    plt.title('Speed Distribution - Northbound')
    plt.xlabel('Speed (MPH)')
    plt.ylabel('Number of Vehicles')
    
    # 4. Speed Distribution - Southbound
    plt.subplot(2, 2, 3)
    speed_cols_sb = [col for col in df.columns if 'MPH  - Southbound' in col]
    speed_data_sb = df[speed_cols_sb].sum()
    speed_data_sb.index = [int(col.split('-')[0]) for col in speed_cols_sb]
    speed_data_sb.plot(kind='bar')
    plt.title('Speed Distribution - Southbound')
    plt.xlabel('Speed (MPH)')
    plt.ylabel('Number of Vehicles')
    
    # 5. Time Series Plot
    plt.subplot(2, 2, 4)
    df.set_index('Date/Time')[['Volume - Northbound', 'Volume - Southbound']].plot()
    plt.title('Traffic Volume Over Time')
    plt.xlabel('Date/Time')
    plt.ylabel('Number of Vehicles')
    
    # Calculate compliance
    nb_compliance, sb_compliance = calculate_compliance(df)
    
    # Add title with summary statistics
    plt.suptitle(f'Traffic Analysis for {location}\n' +
                f'Total Vehicles: {total_vehicles:,.0f} ' +
                f'(Dominant Direction: {dominant_dir} {dominant_pct:.1f}%)\n' +
                f'Speed Compliance: Northbound {nb_compliance:.1f}%, Southbound {sb_compliance:.1f}%',
                fontsize=14)
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.85)
    return fig

def main():
    """Main function to run traffic analysis."""
    try:
        # Process each CSV file in the data directory
        file_path = 'data/2809-Hampshire_AIO.csv'
        df, location = read_traffic_data(file_path)
        
        if df is not None:
            fig = plot_traffic_analysis(df, location)
            plt.show()
            
    except Exception as e:
        print(f"Error in main: {str(e)}")
        print(traceback.format_exc())

if __name__ == "__main__":
    main() 