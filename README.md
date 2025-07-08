# Website Traffic Analysis Project

Website analytics project (Jul 2025 - Dec 2025) focused on traffic behavior, engagement, and conversion insights.

## Highlights
- Preprocessed and cleaned website logs with Pandas and NumPy.
- Performed statistical analysis for peak traffic windows and user behavior patterns.
- Produced visual summaries for cross-team presentations.
- Defined KPI framework for engagement and conversion monitoring.

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/generate_logs.py
python src/analysis.py
python src/visualize.py
```

## Outputs
- `data/processed/clean_traffic.csv`
- `kpi/kpi_metrics.csv`
- `visuals/hourly_traffic.png`
- `visuals/channel_conversion.png`

## Tableau
`tableau/README.md` explains importing KPI/output CSV files into Tableau dashboards.
