import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main() -> None:
    df = pd.read_csv("data/processed/clean_traffic.csv")
    channel = pd.read_csv("kpi/channel_performance.csv")
    monthly = pd.read_csv("kpi/monthly_performance.csv")
    funnel = pd.read_csv("kpi/funnel_metrics.csv")
    os.makedirs("visuals", exist_ok=True)

    hourly = df.groupby("hour", as_index=False)["session_id"].count().rename(columns={"session_id": "sessions"})

    plt.figure(figsize=(10, 4))
    plt.plot(hourly["hour"], hourly["sessions"], marker="o")
    plt.title("Hourly Website Sessions")
    plt.xlabel("Hour of Day")
    plt.ylabel("Sessions")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("visuals/hourly_traffic.png", dpi=150)

    plt.figure(figsize=(8, 4))
    plt.bar(channel["channel"], channel["conversion_rate"])
    plt.title("Channel Conversion Rate")
    plt.xlabel("Channel")
    plt.ylabel("Conversion Rate")
    plt.tight_layout()
    plt.savefig("visuals/channel_conversion.png", dpi=150)

    plt.figure(figsize=(10, 4))
    plt.plot(monthly["month"], monthly["revenue"], marker="o")
    plt.title("Monthly Revenue Trend")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("visuals/monthly_revenue.png", dpi=150)

    plt.figure(figsize=(8, 4))
    plt.bar(funnel["funnel_stage"], funnel["sessions"])
    plt.title("Funnel Stage Distribution")
    plt.tight_layout()
    plt.savefig("visuals/funnel_distribution.png", dpi=150)

    print("Visualizations generated in visuals/.")


if __name__ == "__main__":
    main()
