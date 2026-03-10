from dataclasses import dataclass
from typing import List
from src.api.schemas.pipeline_stage import PipelineStage



@dataclass
class PipelineExecution:

    dataset_name: str
    pipeline_version: int
    stages: List[PipelineStage]
