import pandas as pd
from src.analysis import build_kpis


def test_build_kpis_returns_expected_metrics():
    df = pd.DataFrame(
        {
            "session_id": [1, 2, 3],
            "duration_sec": [100, 200, 300],
            "pageviews": [2, 3, 4],
            "converted": [0, 1, 0],
            "hour": [10, 11, 10],
            "channel": ["organic", "paid", "organic"],
            "engaged": [0, 1, 1],
        }
    )
    out = build_kpis(df)
    assert set(out["metric"]) == {"conversion_rate", "avg_duration_sec", "avg_pageviews", "engagement_rate"}
