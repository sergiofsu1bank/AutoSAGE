# -*- coding: utf-8 -*-

from fastapi import APIRouter, HTTPException
from src.app.registry.model_promotion_manager import ModelPromotionManager

router = APIRouter(prefix="/ml", tags=["ML-Promotion"])


@router.post("/promote")
def promote_model(
    experiment_path: str,
    model_name: str,
    alias: str = "production",
):
    try:
        manager = ModelPromotionManager(
            registry_base="/app/registry/models"
        )

        manager.promote(
            experiment_path=experiment_path,
            model_name=model_name,
            alias=alias,
        )

        return {
            "status": "PROMOTED",
            "alias": alias,
            "path": experiment_path,
        }

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
