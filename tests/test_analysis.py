import pandas as pd
from src.analysis import build_kpis, detect_anomalies


def test_build_kpis_returns_expected_metrics():
    df = pd.DataFrame(
        {
            "session_id": [1, 2, 3, 4],
            "timestamp": pd.to_datetime(["2025-01-01 10:00", "2025-01-01 11:00", "2025-01-01 12:00", "2025-01-01 13:00"]),
            "duration_sec": [100, 200, 300, 240],
            "pageviews": [2, 3, 4, 5],
            "converted": [0, 1, 0, 1],
            "hour": [10, 11, 12, 13],
            "channel": ["organic", "paid_search", "organic", "email"],
            "engaged": [0, 1, 1, 1],
            "bounce": [0, 0, 0, 0],
            "funnel_stage": ["visit", "signup", "trial", "purchase"],
            "country": ["US", "IN", "US", "UK"],
            "month": ["2025-01", "2025-01", "2025-01", "2025-01"],
            "revenue": [0.0, 20.0, 0.0, 45.0],
        }
    )
    out = build_kpis(df)
    assert set(out["metric"]) == {
        "conversion_rate",
        "avg_duration_sec",
        "avg_pageviews",
        "engagement_rate",
        "bounce_rate",
        "revenue_per_session",
    }


def test_detect_anomalies_has_flag_column():
    df = pd.DataFrame(
        {
            "session_id": [1, 2, 3],
            "timestamp": pd.to_datetime(["2025-01-01 00:00", "2025-01-01 00:00", "2025-01-01 01:00"]),
            "converted": [0, 1, 0],
            "revenue": [0.0, 10.0, 0.0],
        }
    )
    out = detect_anomalies(df)
    assert "is_anomaly" in out.columns
