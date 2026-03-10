from typing import Optional


class DatasetRun:

    def __init__(
        self,
        dataset_name: str,
        pipeline_version: int,
        rows_count: Optional[int],
        columns_count: Optional[int],
        model_name: Optional[str],
        metric_name: Optional[str],
        metric_value: Optional[float],
        duration_ms: Optional[int]
    ):
        self.dataset_name = dataset_name
        self.pipeline_version = pipeline_version
        self.rows_count = rows_count
        self.columns_count = columns_count
        self.model_name = model_name
        self.metric_name = metric_name
        self.metric_value = metric_value
        self.duration_ms = duration_ms
