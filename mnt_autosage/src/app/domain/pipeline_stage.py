from dataclasses import dataclass


@dataclass
class PipelineStage:

    stage_name: str
    status: str
    created_at: str | None
    duration_ms: int | None
