from dataclasses import dataclass


@dataclass
class DatasetRunHistory:

    pipeline_version: int
    model_name: str | None
    metric_name: str | None
    metric_value: float | None
    duration_ms: int | None

