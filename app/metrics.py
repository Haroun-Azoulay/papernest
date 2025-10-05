from prometheus_client import Counter, Histogram

job_duration_seconds = Histogram(
    "job_duration_seconds",
    "Job end-to-end duration in seconds",
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10],
)

job_requests_total = Counter(
    "job_requests_total", "Number of job submissions", labelnames=("result",)
)

job_items_processed_total = Counter(
    "job_items_processed_total", "Total number of items processed across jobs"
)
