# Power BI Template Guide

## Recommended Pages
1. Traffic Overview
2. Funnel Conversion
3. Channel and Country Performance
4. Engagement and Bounce
5. Anomaly Monitoring

## Data Sources
- `kpi/kpi_metrics.csv`
- `kpi/funnel_metrics.csv`
- `kpi/channel_performance.csv`
- `kpi/country_performance.csv`
- `kpi/monthly_performance.csv`
- `kpi/hourly_anomaly_scan.csv`

## Suggested DAX Measures
- `Conversion Rate = AVERAGE([conversion_rate])`
- `Revenue per Session = DIVIDE(SUM([revenue]), SUM([sessions]))`
- `Bounce Rate = AVERAGE([bounce_rate])`
