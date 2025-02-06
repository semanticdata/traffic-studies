import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def plot_traffic_volume(filtered_df, structure):
    """Create traffic volume visualizations."""
    hourly_volumes = (
        filtered_df.groupby("Hour")
        .agg(
            {structure["dir1_volume_col"]: "mean", structure["dir2_volume_col"]: "mean"}
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
    ax1.set_xlabel("Hour of Day")
    ax1.set_ylabel("Average Vehicles per Hour")
    ax1.legend()
    ax1.grid(True, alpha=0.3)
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


def plot_speed_compliance(filtered_df, structure):
    """Create speed compliance visualizations."""
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
                filtered_df["Dir1_Compliant"].sum(),
                filtered_df["Dir1_Non_Compliant"].sum(),
                filtered_df["Dir2_Compliant"].sum(),
                filtered_df["Dir2_Non_Compliant"].sum(),
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
    ax3.set_ylabel("Vehicle Count")
    ax3.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig3
