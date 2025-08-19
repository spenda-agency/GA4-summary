import os
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)

def get_ga4_report():
    """Fetches a report from Google Analytics 4 Data API."""
    property_id = os.environ.get("GA4_PROPERTY_ID")
    if not property_id:
        raise ValueError("GA4_PROPERTY_ID environment variable not set")

    client = BetaAnalyticsDataClient()

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="date")],
        metrics=[
            Metric(name="activeUsers"),
            Metric(name="newUsers"),
            Metric(name="sessions"),
        ],
        date_ranges=[DateRange(start_date="yesterday", end_date="yesterday")],
    )
    response = client.run_report(request)

    with open("report.txt", "w") as f:
        f.write("Google Analytics Daily Report:\n\n")
        for row in response.rows:
            f.write(f"Date: {row.dimension_values[0].value}\n")
            f.write(f"Active Users: {row.metric_values[0].value}\n")
            f.write(f"New Users: {row.metric_values[1].value}\n")
            f.write(f"Sessions: {row.metric_values[2].value}\n")

if __name__ == "__main__":
    get_ga4_report()
