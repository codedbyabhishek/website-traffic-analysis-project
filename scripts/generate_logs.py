import os
import numpy as np
import pandas as pd

RNG = np.random.default_rng(7)


def main(rows: int = 90000) -> None:
    os.makedirs("data/raw", exist_ok=True)

    ts = pd.date_range("2025-01-01", "2025-12-31 23:00", freq="h")
    channels = ["organic", "paid", "email", "social", "referral"]
    devices = ["mobile", "desktop", "tablet"]

    df = pd.DataFrame(
        {
            "session_id": np.arange(1, rows + 1),
            "timestamp": RNG.choice(ts, rows),
            "channel": RNG.choice(channels, rows, p=[0.35, 0.25, 0.15, 0.15, 0.10]),
            "device": RNG.choice(devices, rows, p=[0.58, 0.35, 0.07]),
            "pageviews": RNG.poisson(3.8, rows) + 1,
            "duration_sec": RNG.gamma(2.2, 80, rows).astype(int),
            "converted": RNG.choice([0, 1], rows, p=[0.91, 0.09]),
        }
    )

    # Add dirty records for cleaning logic coverage.
    bad_idx = RNG.choice(df.index, 350, replace=False)
    df.loc[bad_idx, "duration_sec"] = -1
    miss_idx = RNG.choice(df.index, 500, replace=False)
    df.loc[miss_idx, "channel"] = None

    df.to_csv("data/raw/web_logs.csv", index=False)
    print(f"Generated {rows} website log rows")


if __name__ == "__main__":
    main()
