# -*- coding: utf-8 -*-

from fastapi import APIRouter, HTTPException, Header

from src.api.schemas.ml_train_request import MLTrainRequest
from src.api.schemas.ml_train_response import MLTrainResponse
from src.app.tools.log_factory import get_dcp_logger
from src.app.pipeline.ml_train_pipeline import MLTrainPipeline

router = APIRouter(prefix="/ml", tags=["ML"])

@router.post("/train", response_model=MLTrainResponse)
async def train_ml(
    request: MLTrainRequest,
    trace_id: str = Header(..., alias="trace-id", include_in_schema=True),
):
    logger = get_dcp_logger(
        trace_id=trace_id,
        classe="ml_router"
    )

    logger.info(f"[Request] {request.dict()}")

    try:
        logger.info("[ML][API] Iniciando treino")

        pipeline = MLTrainPipeline(
            request=request,
            trace_id=trace_id
        )

        result = await pipeline.run()
        return MLTrainResponse(**result)

        # 🗣️ Tradução para API
    except Exception as exc:
        logger.error(f"[ML][API][ERROR] {exc}")
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )
