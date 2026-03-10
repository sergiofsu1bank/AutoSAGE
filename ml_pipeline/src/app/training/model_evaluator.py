# -*- coding: utf-8 -*-

import math
from dataclasses import dataclass
from typing import Literal

from src.app.training.training_report import TrainingReport


Decision = Literal["APPROVED", "TERMINATED"]


@dataclass(frozen=True)
class EvaluationResult:
    decision: Decision
    reason: str
    metric_name: str
    metric_value: float
    model_name: str


class ModelEvaluator:
    """
    Avaliador científico final do modelo.

    Responsabilidade única:
    - Decidir se o processo de ML CONTINUA ou TERMINA.
    """

    def __init__(self, *, problem_type: str):
        self.problem_type = problem_type

    # --------------------------------------------------
    # API pública
    # --------------------------------------------------
    def evaluate(self, report: TrainingReport) -> EvaluationResult:
        if self.problem_type == "classification":
            return self._evaluate_classification(report)

        raise ValueError(
            f"ModelEvaluator não suporta problem_type={self.problem_type}"
        )

    # --------------------------------------------------
    # Regras explícitas de término (Sprint Final)
    # --------------------------------------------------
    def _evaluate_classification(
        self, report: TrainingReport
    ) -> EvaluationResult:

        metric_value = report.metric_value

        # 1. Métrica inválida ou ausente → encerramento
        if (
            metric_value is None
            or not isinstance(metric_value, (int, float))
            or math.isnan(metric_value)
        ):
            return EvaluationResult(
                decision="TERMINATED",
                reason="invalid_or_missing_metric",
                metric_name=report.metric_name,
                metric_value=metric_value,
                model_name=report.model_name,
            )

        metric_value = float(metric_value)

        # 2. Sinal fraco / indistinguível do acaso → encerramento
        MIN_SIGNAL = 0.55

        if metric_value < MIN_SIGNAL:
            return EvaluationResult(
                decision="TERMINATED",
                reason="signal_below_minimum_threshold",
                metric_name=report.metric_name,
                metric_value=metric_value,
                model_name=report.model_name,
            )

        # 3. Modelo existe e é válido
        return EvaluationResult(
            decision="APPROVED",
            reason="signal_above_minimum_threshold",
            metric_name=report.metric_name,
            metric_value=metric_value,
            model_name=report.model_name,
        )
