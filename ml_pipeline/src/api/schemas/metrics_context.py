from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime

@dataclass
class MetricsContext:
    trace_id: str
    pipeline: str
    pipeline_version: int
    vendor: str
    dataset_name: str
    stage: str
    status: str
    started_at: str
    finished_at: str
    duration_ms: int
    metadata: dict | None = None



@dataclass
class MLExperimentMetrics:
    trace_id: str
    pipeline: str
    pipeline_version: int
    vendor: str
    dataset_name: str

    # Identidade do experimento (obrigatórios)
    experiment_id: str
    problem_type: str
    strategy_name: str

    # Resultado científico (obrigatórios)
    metric_name: str
    metric_value: float
    decision: str
    reason: str

    # Opcionais (default None)
    model_name: Optional[str] = None
    training_report: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None

