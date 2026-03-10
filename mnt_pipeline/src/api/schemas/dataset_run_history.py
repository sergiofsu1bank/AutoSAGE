from dataclasses import dataclass


@dataclass
class DatasetRunHistory:

    pipeline_version: int
    pipeline: str | None
    stage: str | None
    status: str | None
    model_name: str | None
    metric_name: str | None
    metric_value: float | None
    duration_ms: int | None

