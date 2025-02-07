import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def plot_traffic_volume(filtered_df, structure):
    """Create traffic volume visualizations."""
    hourly_volumes = (
        filtered_df.groupby("Hour")
        .agg(
            {structure["dir1_volume_col"]: "mean",
                structure["dir2_volume_col"]: "mean"}
        )
        .reset_index()
    )

    fig1, ax1 = plt.subplots(figsize=(15, 8))
    ax1.bar(
        hourly_volumes["Hour"],
        hourly_volumes[structure["dir1_volume_col"]],
        label=structure["dir1_name"],
        alpha=0.7,
        color="skyblue",
    )
    ax1.bar(
        hourly_volumes["Hour"],
        hourly_volumes[structure["dir2_volume_col"]],
        bottom=hourly_volumes[structure["dir1_volume_col"]],
        label=structure["dir2_name"],
        alpha=0.7,
        color="lightgreen",
    )
    ax1.set_title("Hourly Traffic Volume Distribution", pad=20, fontsize=14)
    ax1.set_xlabel("Hour of Day", fontsize=12)
    ax1.set_ylabel("Average Vehicles per Hour", fontsize=12)
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(range(24))
    return fig1


def plot_speed_distribution(filtered_df, structure):
    """Create speed distribution visualizations."""
    dir1_speeds = filtered_df[structure["dir1_speed_cols"]].mean()
    dir2_speeds = filtered_df[structure["dir2_speed_cols"]].mean()

    fig2, (ax2a, ax2b) = plt.subplots(2, 1, figsize=(15, 12))

    # Direction 1 speeds
    sns.barplot(
        x=[col.split("-")[0].strip() for col in structure["dir1_speed_cols"]],
        y=dir1_speeds,
        color="skyblue",
        ax=ax2a,
    )
    ax2a.set_title(f'{structure["dir1_name"]} Speed Distribution')
    ax2a.set_xlabel("Speed Range (MPH)")
    ax2a.set_ylabel("Average Vehicle Count")
    ax2a.tick_params(axis="x", rotation=45)

    # Direction 2 speeds
    sns.barplot(
        x=[col.split("-")[0].strip() for col in structure["dir2_speed_cols"]],
        y=dir2_speeds,
        color="lightgreen",
        ax=ax2b,
    )
    ax2b.set_title(f'{structure["dir2_name"]} Speed Distribution')
    ax2b.set_xlabel("Speed Range (MPH)")
    ax2b.set_ylabel("Average Vehicle Count")
    ax2b.tick_params(axis="x", rotation=45)

    plt.tight_layout()
    return fig2


def plot_speed_compliance(filtered_df, structure, speed_limit=30):
    """Create speed compliance visualizations."""
    # Calculate compliance directly from speed columns
    dir1_compliant = filtered_df[structure["dir1_speed_cols"]].apply(
        lambda row: sum(
            int(col.split('-')[0].strip()) <= speed_limit
            for col, count in row.items()
            if count > 0
        ),
        axis=1
    ).sum()

    dir1_non_compliant = filtered_df[structure["dir1_speed_cols"]].apply(
        lambda row: sum(
            int(col.split('-')[0].strip()) > speed_limit
            for col, count in row.items()
            if count > 0
        ),
        axis=1
    ).sum()

    dir2_compliant = filtered_df[structure["dir2_speed_cols"]].apply(
        lambda row: sum(
            int(col.split('-')[0].strip()) <= speed_limit
            for col, count in row.items()
            if count > 0
        ),
        axis=1
    ).sum()

    dir2_non_compliant = filtered_df[structure["dir2_speed_cols"]].apply(
        lambda row: sum(
            int(col.split('-')[0].strip()) > speed_limit
            for col, count in row.items()
            if count > 0
        ),
        axis=1
    ).sum()

    compliance_data = pd.DataFrame(
        {
            "Direction": [
                structure["dir1_name"],
                structure["dir1_name"],
                structure["dir2_name"],
                structure["dir2_name"],
            ],
            "Compliance": ["Compliant", "Non-Compliant", "Compliant", "Non-Compliant"],
            "Count": [
                dir1_compliant,
                dir1_non_compliant,
                dir2_compliant,
                dir2_non_compliant,
            ],
        }
    )

    fig3, ax3 = plt.subplots(figsize=(15, 8))
    sns.barplot(
        data=compliance_data,
        x="Direction",
        y="Count",
        hue="Compliance",
        palette=["lightgreen", "salmon"],
        ax=ax3,
    )
    ax3.set_title("Speed Compliance Analysis by Direction",
                  pad=20, fontsize=14)
    ax3.set_xlabel("Direction", fontsize=12)
    ax3.set_ylabel("Vehicle Count", fontsize=12)
    ax3.legend(fontsize=10)
    ax3.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig3


def plot_temporal_patterns(filtered_df, structure):
    """Create visualizations for temporal traffic patterns."""
    # Add day of week column using Date/Time instead of Date
    filtered_df['DayOfWeek'] = filtered_df['Date/Time'].dt.day_name()

    # Daily patterns
    daily_volumes = filtered_df.groupby('DayOfWeek').agg({
        structure["dir1_volume_col"]: 'sum',
        structure["dir2_volume_col"]: 'sum'
    }).reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

    fig, ax = plt.subplots(figsize=(15, 8))
    daily_volumes.plot(kind='bar', ax=ax)
    ax.set_title('Daily Traffic Volume Patterns', pad=20, fontsize=14)
    ax.set_xlabel('Day of Week', fontsize=12)
    ax.set_ylabel('Total Vehicle Count', fontsize=12)
    ax.legend(labels=[structure["dir1_name"],
              structure["dir2_name"]], fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


def plot_speed_violation_severity(filtered_df, structure):
    """Create visualization for speed violation severity."""
    # Calculate speed ranges and their frequencies
    speed_ranges = {
        '0-5 mph over': (0, 5),
        '5-10 mph over': (5, 10),
        '10-15 mph over': (10, 15),
        '15+ mph over': (15, float('inf'))
    }

    violation_data = []
    for direction, speed_cols in [
        (structure["dir1_name"], structure["dir1_speed_cols"]),
        (structure["dir2_name"], structure["dir2_speed_cols"])
    ]:
        # Default to 25 if not specified
        speed_limit = structure.get('speed_limit', 25)

        for col in speed_cols:
            speed = int(col.split('-')[0].strip())
            if speed > speed_limit:
                over_limit = speed - speed_limit
                for range_name, (min_over, max_over) in speed_ranges.items():
                    if min_over <= over_limit < max_over:
                        violation_data.append({
                            'Direction': direction,
                            'Violation Range': range_name,
                            'Count': filtered_df[col].mean()
                        })

    violation_df = pd.DataFrame(violation_data)

    fig, ax = plt.subplots(figsize=(15, 8))
    sns.barplot(
        data=violation_df,
        x='Direction',
        y='Count',
        hue='Violation Range',
        palette='YlOrRd',
        ax=ax
    )
    ax.set_title('Speed Violation Severity Analysis', pad=20, fontsize=14)
    ax.set_xlabel('Direction', fontsize=12)
    ax.set_ylabel('Average Vehicle Count', fontsize=12)
    ax.legend(title='Violation Severity', fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig
