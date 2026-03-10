from dataclasses import dataclass


@dataclass
class PipelineTimelineStage:

    stage_name: str
    duration_ms: int | None


@dataclass
class PipelineTimeline:

    dataset_name: str
    pipeline_version: int
    total_duration_ms: int | None
    stages: list[PipelineTimelineStage]
