# -*- coding: utf-8 -*-

from typing import List, Dict, Any
from pydantic import BaseModel


class InferenceResponse(BaseModel):
    model_metadata: Dict[str, Any]
    predictions: List[float]
