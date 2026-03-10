# -*- coding: utf-8 -*-

from typing import Dict, Any


class TrainingReport:
    """
    Relatório canônico de treino de modelo.

    Responsabilidades:
    - Padronizar métricas de treino
    - Ser comparável entre modelos
    - NÃO executar lógica
    """

    def __init__(
        self,
        *,
        model_name: str,
        metric_name: str,
        metric_value: float,
        metadata: Dict[str, Any] | None = None,
    ):
        self.model_name = model_name
        self.metric_name = metric_name
        self.metric_value = metric_value
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_name": self.model_name,
            "metric_name": self.metric_name,
            "metric_value": self.metric_value,
            "metadata": self.metadata,
        }
