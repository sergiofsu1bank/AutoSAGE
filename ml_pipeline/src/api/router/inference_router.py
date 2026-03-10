# -*- coding: utf-8 -*-

import pandas as pd
from fastapi import APIRouter, HTTPException

from src.api.schemas.inference_request import InferenceRequest
from src.api.schemas.inference_response import InferenceResponse
from src.app.inference.model_bundle_loader import ModelBundleLoader
from src.app.inference.inference_pipeline import InferencePipeline

router = APIRouter(prefix="/ml", tags=["Inference"])


@router.post("/predict", response_model=InferenceResponse)
def predict(request: InferenceRequest):

    try:
        # --------------------------------------------------
        # 1. Load model bundle
        # --------------------------------------------------
        bundle = ModelBundleLoader(
            bundle_path=request.model_path
        ).load()

        # --------------------------------------------------
        # 2. Build inference pipeline
        # --------------------------------------------------
        pipeline = InferencePipeline(bundle)

        # --------------------------------------------------
        # 3. Convert input data
        # --------------------------------------------------
        df = pd.DataFrame(request.data)

        # --------------------------------------------------
        # 4. Predict
        # --------------------------------------------------
        predictions = pipeline.predict(df)

        return InferenceResponse(
            model_metadata=bundle["model_metadata"],
            predictions=list(predictions),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )
