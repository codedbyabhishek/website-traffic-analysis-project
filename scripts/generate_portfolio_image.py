import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main() -> None:
    kpi = pd.read_csv("kpi/kpi_metrics.csv")
    monthly = pd.read_csv("kpi/monthly_performance.csv")
    funnel = pd.read_csv("kpi/funnel_metrics.csv")

    fig, axes = plt.subplots(2, 2, figsize=(14, 8))
    fig.suptitle("Website Traffic Analysis Dashboard Preview", fontsize=16, fontweight="bold")

    axes[0, 0].plot(monthly["month"], monthly["sessions"], marker="o")
    axes[0, 0].set_title("Monthly Sessions")
    axes[0, 0].tick_params(axis="x", rotation=45)

    axes[0, 1].bar(funnel["funnel_stage"], funnel["sessions"])
    axes[0, 1].set_title("Funnel Distribution")

    kpi_disp = kpi.copy()
    kpi_disp["value"] = kpi_disp["value"].round(4)
    axes[1, 0].axis("off")
    table = axes[1, 0].table(cellText=kpi_disp.values, colLabels=kpi_disp.columns, cellLoc="center", loc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    axes[1, 0].set_title("KPI Snapshot")

    axes[1, 1].text(
        0.02,
        0.9,
        "Highlights:\n- 220K sessions\n- Funnel + anomaly analytics\n- Channel/country efficiency\n- BI-ready KPI marts",
        fontsize=11,
        va="top",
    )
    axes[1, 1].axis("off")

    plt.tight_layout()
    plt.savefig("assets/website_traffic_dashboard_preview.png", dpi=170)


if __name__ == "__main__":
    main()
