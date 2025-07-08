import os
import pandas as pd


def preprocess() -> pd.DataFrame:
    df = pd.read_csv("data/raw/web_logs.csv", parse_dates=["timestamp"])

    df["channel"] = df["channel"].fillna("unknown")
    df = df[df["duration_sec"] >= 0].copy()
    df["hour"] = df["timestamp"].dt.hour
    df["weekday"] = df["timestamp"].dt.day_name()
    df["engaged"] = (df["duration_sec"] >= 120).astype(int)

    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/clean_traffic.csv", index=False)
    return df


def build_kpis(df: pd.DataFrame) -> pd.DataFrame:
    conversion_rate = float(df["converted"].mean())
    avg_duration = float(df["duration_sec"].mean())
    avg_pageviews = float(df["pageviews"].mean())
    engagement_rate = float(df["engaged"].mean())

    hourly_peak = (
        df.groupby("hour", as_index=False)["session_id"]
        .count()
        .rename(columns={"session_id": "sessions"})
        .sort_values("sessions", ascending=False)
        .head(3)
    )

    kpis = pd.DataFrame(
        {
            "metric": ["conversion_rate", "avg_duration_sec", "avg_pageviews", "engagement_rate"],
            "value": [conversion_rate, avg_duration, avg_pageviews, engagement_rate],
        }
    )

    os.makedirs("kpi", exist_ok=True)
    kpis.to_csv("kpi/kpi_metrics.csv", index=False)
    hourly_peak.to_csv("kpi/peak_hours.csv", index=False)
    (
        df.groupby("channel", as_index=False)
        .agg(sessions=("session_id", "count"), conversion_rate=("converted", "mean"))
        .sort_values("sessions", ascending=False)
        .to_csv("kpi/channel_performance.csv", index=False)
    )

    return kpis


if __name__ == "__main__":
    df_clean = preprocess()
    build_kpis(df_clean)
    print("Analysis complete. KPI files generated.")
