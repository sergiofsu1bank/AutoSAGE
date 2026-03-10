# -*- coding: utf-8 -*-

from typing import Dict, Any
from pydantic import BaseModel


class MLTrainResponse(BaseModel):
    experiment_id: str
    status: str

    model: Dict[str, Any] | None = None
    registry: Dict[str, str] | None = None
    diagnostics: Dict[str, Any] | None = None
