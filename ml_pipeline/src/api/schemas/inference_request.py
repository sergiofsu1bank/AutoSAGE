# -*- coding: utf-8 -*-

from typing import List, Dict, Any
from pydantic import BaseModel, Field


class InferenceRequest(BaseModel):
    model_path: str = Field(
        ..., description="Caminho absoluto do model_bundle.pkl"
    )
    data: List[Dict[str, Any]] = Field(
        ..., description="Lista de registros para inferência"
    )
