import os
import numpy as np
import pandas as pd


def preprocess() -> pd.DataFrame:
    df = pd.read_csv("data/raw/web_logs.csv", parse_dates=["timestamp"])

    df["channel"] = df["channel"].fillna("unknown")
    df = df[df["duration_sec"] >= 0].copy()
    df = df[df["is_bot"] == 0].copy()

    df["hour"] = df["timestamp"].dt.hour
    df["month"] = df["timestamp"].dt.to_period("M").astype(str)
    df["weekday"] = df["timestamp"].dt.day_name()
    df["engaged"] = ((df["duration_sec"] >= 120) & (df["pageviews"] >= 3)).astype(int)
    df["bounce"] = ((df["pageviews"] <= 1) & (df["duration_sec"] < 30)).astype(int)

    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/clean_traffic.csv", index=False)
    return df


def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    tmp = df.copy()
    tmp["hour_ts"] = tmp["timestamp"].dt.floor("h")
    hourly = tmp.groupby("hour_ts", as_index=False).agg(
        sessions=("session_id", "count"),
        conversions=("converted", "sum"),
        revenue=("revenue", "sum"),
    )
    mean_sessions = hourly["sessions"].mean()
    std_sessions = max(hourly["sessions"].std(ddof=0), 1)
    hourly["z_sessions"] = (hourly["sessions"] - mean_sessions) / std_sessions
    hourly["is_anomaly"] = (hourly["z_sessions"].abs() >= 3.0).astype(int)
    return hourly


def build_kpis(df: pd.DataFrame) -> pd.DataFrame:
    conversion_rate = float(df["converted"].mean())
    avg_duration = float(df["duration_sec"].mean())
    avg_pageviews = float(df["pageviews"].mean())
    engagement_rate = float(df["engaged"].mean())
    bounce_rate = float(df["bounce"].mean())
    revenue_per_session = float(df["revenue"].sum() / max(len(df), 1))

    kpis = pd.DataFrame(
        {
            "metric": [
                "conversion_rate",
                "avg_duration_sec",
                "avg_pageviews",
                "engagement_rate",
                "bounce_rate",
                "revenue_per_session",
            ],
            "value": [conversion_rate, avg_duration, avg_pageviews, engagement_rate, bounce_rate, revenue_per_session],
        }
    )

    funnel = (
        df.groupby("funnel_stage", as_index=False)
        .agg(sessions=("session_id", "count"))
        .sort_values("sessions", ascending=False)
    )
    total_sessions = len(df)
    funnel["share"] = funnel["sessions"] / max(total_sessions, 1)

    channel_perf = (
        df.groupby("channel", as_index=False)
        .agg(
            sessions=("session_id", "count"),
            conversion_rate=("converted", "mean"),
            avg_revenue=("revenue", "mean"),
            engagement_rate=("engaged", "mean"),
        )
        .sort_values("sessions", ascending=False)
    )

    country_perf = (
        df.groupby("country", as_index=False)
        .agg(sessions=("session_id", "count"), conversion_rate=("converted", "mean"), revenue=("revenue", "sum"))
        .sort_values("sessions", ascending=False)
    )

    monthly = (
        df.groupby("month", as_index=False)
        .agg(sessions=("session_id", "count"), conversion_rate=("converted", "mean"), revenue=("revenue", "sum"))
        .sort_values("month")
    )

    anomaly = detect_anomalies(df)

    os.makedirs("kpi", exist_ok=True)
    kpis.to_csv("kpi/kpi_metrics.csv", index=False)
    funnel.to_csv("kpi/funnel_metrics.csv", index=False)
    channel_perf.to_csv("kpi/channel_performance.csv", index=False)
    country_perf.to_csv("kpi/country_performance.csv", index=False)
    monthly.to_csv("kpi/monthly_performance.csv", index=False)
    anomaly.to_csv("kpi/hourly_anomaly_scan.csv", index=False)

    return kpis


if __name__ == "__main__":
    df_clean = preprocess()
    build_kpis(df_clean)
    print("Advanced traffic analysis complete. KPI files generated.")
