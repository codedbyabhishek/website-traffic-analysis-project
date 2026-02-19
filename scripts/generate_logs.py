import os
import numpy as np
import pandas as pd

RNG = np.random.default_rng(2026)


def main(rows: int = 220000) -> None:
    os.makedirs("data/raw", exist_ok=True)

    ts = pd.date_range("2025-01-01", "2025-12-31 23:00", freq="min")
    channels = ["organic", "paid_search", "email", "social", "referral", "direct"]
    devices = ["mobile", "desktop", "tablet"]
    countries = ["US", "IN", "UK", "DE", "CA", "AU"]
    landing_pages = ["/home", "/pricing", "/blog", "/product", "/features", "/docs"]

    df = pd.DataFrame(
        {
            "session_id": np.arange(1, rows + 1),
            "timestamp": RNG.choice(ts, rows),
            "channel": RNG.choice(channels, rows, p=[0.30, 0.24, 0.12, 0.12, 0.10, 0.12]),
            "device": RNG.choice(devices, rows, p=[0.6, 0.33, 0.07]),
            "country": RNG.choice(countries, rows),
            "landing_page": RNG.choice(landing_pages, rows),
            "pageviews": RNG.poisson(4.5, rows) + 1,
            "duration_sec": RNG.gamma(2.6, 95, rows).astype(int),
            "is_new_user": RNG.choice([0, 1], rows, p=[0.42, 0.58]),
            "funnel_stage": RNG.choice(["visit", "signup", "trial", "purchase"], rows, p=[0.62, 0.20, 0.12, 0.06]),
            "revenue": np.round(RNG.gamma(1.6, 120, rows), 2),
        }
    )

    df["converted"] = (df["funnel_stage"] == "purchase").astype(int)
    df.loc[df["converted"] == 0, "revenue"] = 0.0

    df["is_bot"] = RNG.choice([0, 1], rows, p=[0.985, 0.015])
    df.loc[df["is_bot"] == 1, "duration_sec"] = RNG.integers(1, 8, int((df["is_bot"] == 1).sum()))
    df.loc[df["is_bot"] == 1, "pageviews"] = RNG.integers(1, 3, int((df["is_bot"] == 1).sum()))

    bad_idx = RNG.choice(df.index, 1600, replace=False)
    df.loc[bad_idx, "duration_sec"] = -1
    miss_idx = RNG.choice(df.index, 2200, replace=False)
    df.loc[miss_idx, "channel"] = None

    df.to_csv("data/raw/web_logs.csv", index=False)
    print(f"Generated high-end website log rows: {rows}")


if __name__ == "__main__":
    main()
