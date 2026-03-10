# -*- coding: utf-8 -*-

class RetrainContext:
    """
    Contexto que embasa uma decisão de retreino.
    """

    def __init__(
        self,
        *,
        model_metadata: dict,
        drift_report: dict | None = None,
        production_metrics: dict | None = None,
        reason: str,
    ):
        self.model_metadata = model_metadata
        self.drift_report = drift_report
        self.production_metrics = production_metrics
        self.reason = reason

    def export(self) -> dict:
        return {
            "model": self.model_metadata,
            "reason": self.reason,
            "drift": self.drift_report,
            "metrics": self.production_metrics,
        }
