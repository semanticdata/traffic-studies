import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set the style before creating any plots
plt.style.use('seaborn-v0_8-darkgrid')

# Read the data
df = pd.read_csv('data/speed-data-totals.csv', skiprows=6)

# Convert Date/Time to datetime
df['Date/Time'] = pd.to_datetime(df['Date/Time'].str.split(' - ').str[0])
df['Hour'] = df['Date/Time'].dt.hour

# Calculate speed compliance
speed_columns = [col for col in df.columns if col not in ['Date/Time', 'Hour', 'Total']]

# Print column names for debugging
print("Available columns:", df.columns.tolist())

# Calculate compliant speeds (0-30 mph)
df['Compliant'] = df[['0-20'] + [str(i) for i in range(21, 31) if str(i) in df.columns]].sum(axis=1)

# Calculate non-compliant speeds (31+ mph)
non_compliant_cols = [col for col in speed_columns 
                     if col not in ['0-20'] and 
                     (col != '45-99') and 
                     (col.isdigit() and int(col) > 30 if col.isdigit() else False)]
if '45-99' in df.columns:
    non_compliant_cols.append('45-99')
df['Non_Compliant'] = df[non_compliant_cols].sum(axis=1)

# Create a figure with three subplots
fig = plt.figure(figsize=(15, 12))

# 1. Traffic Volume by Hour
ax1 = plt.subplot(3, 1, 1)
sns.barplot(data=df, x='Hour', y='Total', color='skyblue', ax=ax1)
ax1.set_title('Traffic Volume by Hour', fontsize=12, pad=15)
ax1.set_xlabel('Hour of Day', fontsize=10)
ax1.set_ylabel('Total Vehicles', fontsize=10)
ax1.grid(True, alpha=0.3)

# 2. Speed Distribution
ax2 = plt.subplot(3, 1, 2)
speed_dist = df[speed_columns].mean()
if '0-20' in speed_dist.index:
    speed_dist = speed_dist.drop('0-20')  # Drop the 0-20 category for better visualization
sns.barplot(x=speed_dist.index, y=speed_dist.values, color='lightgreen', ax=ax2)
ax2.set_title('Average Speed Distribution', fontsize=12, pad=15)
ax2.set_xlabel('Speed (mph)', fontsize=10)
ax2.set_ylabel('Average Vehicle Count', fontsize=10)
plt.xticks(rotation=45)
ax2.grid(True, alpha=0.3)

# 3. Speed Compliance by Hour
ax3 = plt.subplot(3, 1, 3)
compliance_data = pd.DataFrame({
    'Hour': df['Hour'],
    'Compliant': df['Compliant'],
    'Non-Compliant': df['Non_Compliant']
})
compliance_data_melted = pd.melt(compliance_data, id_vars=['Hour'], var_name='Compliance', value_name='Count')
sns.barplot(data=compliance_data_melted, x='Hour', y='Count', hue='Compliance', 
            palette=['lightgreen', 'salmon'], ax=ax3)
ax3.set_title('Speed Compliance by Hour', fontsize=12, pad=15)
ax3.set_xlabel('Hour of Day', fontsize=10)
ax3.set_ylabel('Vehicle Count', fontsize=10)
ax3.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('traffic_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# Print some summary statistics
print("\nTraffic Analysis Summary:")
print(f"Total vehicles recorded: {df['Total'].sum():,}")
print(f"Average vehicles per hour: {df['Total'].mean():.1f}")
print(f"Peak hour: {df.loc[df['Total'].idxmax(), 'Hour']:02d}:00 with {df['Total'].max()} vehicles")
print(f"Speed compliance rate: {(df['Compliant'].sum() / df['Total'].sum() * 100):.1f}%") 