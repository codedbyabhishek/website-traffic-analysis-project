# Website Traffic Analysis Project (High-End)

Advanced traffic intelligence project (Jul 2025 - Dec 2025).

## What Makes This High-End
- High-fidelity synthetic event logs with **220K sessions**.
- Rich dimensions: channel, device, geo, landing page, funnel stage, bot flag, revenue.
- Robust cleaning and quality filters (invalid duration, missing channels, bot exclusion).
- Advanced analytics: funnel metrics, monthly performance, channel/country efficiency, anomaly detection.
- Dashboard-ready exports for Tableau and cross-functional reporting.

## Run
```bash
python scripts/generate_logs.py
python src/analysis.py
python src/visualize.py
```

## Key Outputs
- `/Users/abhishekkumar/Documents/Projects/website-traffic-analysis-project/data/processed/clean_traffic.csv`
- `/Users/abhishekkumar/Documents/Projects/website-traffic-analysis-project/kpi/kpi_metrics.csv`
- `/Users/abhishekkumar/Documents/Projects/website-traffic-analysis-project/kpi/funnel_metrics.csv`
- `/Users/abhishekkumar/Documents/Projects/website-traffic-analysis-project/kpi/hourly_anomaly_scan.csv`
- `/Users/abhishekkumar/Documents/Projects/website-traffic-analysis-project/visuals/monthly_revenue.png`
