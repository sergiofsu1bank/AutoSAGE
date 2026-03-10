# -*- coding: utf-8 -*-

from typing import Dict, Any

from src.api.schemas.ml_train_request import MLTrainRequest
from src.app.pipeline.ml_pipeline import MLPipeline
from src.api.adapters.ml_decision_response_adapter import (
    MLDecisionResponseAdapter
)


class MLTrainPipeline:
    """
    Orquestrador de treino para a API.
    Camada de borda entre API e pipeline científico.
    """

    def __init__(self, *, request: MLTrainRequest, trace_id: str):
        self.request = request
        self.trace_id = trace_id

    async def run(self) -> Dict[str, Any]:

        pipeline = MLPipeline(
            trace_id=self.trace_id,
            pipeline=self.request.pipeline,
            pipeline_version=self.request.pipeline_version,
            vendor=self.request.vendor,
            dataset_name=self.request.dataset_name,
            parquet_artifact_path=self.request.parquet_artifact_path,
            eda_prepare_registry_path=self.request.eda_prepare_registry_path,
            target_name=self.request.target_name
        )

        result = await pipeline.run()

        # ADAPTER FICA AQUI (e só aqui)
        return MLDecisionResponseAdapter.adapt(result)
