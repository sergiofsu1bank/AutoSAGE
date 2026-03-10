# -*- coding: utf-8 -*-

class ExecutionContext:
    """
    Contexto comum de execução ML.
    """

    def __init__(
        self,
        *,
        pipeline: str,
        pipeline_version: int,
        model_metadata: dict | None = None,
        experiment_id: str | None = None,
    ):
        self.pipeline = pipeline
        self.pipeline_version = pipeline_version
        self.model_metadata = model_metadata
        self.experiment_id = experiment_id

    def export(self) -> dict:
        return {
            "pipeline": self.pipeline,
            "pipeline_version": self.pipeline_version,
            "experiment_id": self.experiment_id,
            "model": self.model_metadata,
        }
