from dataclasses import dataclass


@dataclass
class DatasetSummary:

    dataset_name: str
    last_pipeline_version: int
    last_run_timestamp: str
    last_metric_value: float | None
    last_model: str | None
