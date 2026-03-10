# -*- coding: utf-8 -*-

from typing import List, Dict, Any
from src.app.strategies.problem_strategy import ProblemStrategy


class TimeSeriesStrategy(ProblemStrategy):
    """
    Estratégia científica para problemas de séries temporais.
    """

    def __init__(self):
        super().__init__(problem_type="time_series")

    # --------------------------------------------------
    # Identidade
    # --------------------------------------------------
    def name(self) -> str:
        return "time_series"

    # --------------------------------------------------
    # Split
    # --------------------------------------------------
    def split_policy(self) -> Dict[str, Any]:
        return {
            "type": "temporal",
            "method": "walk_forward",
            "test_size": 0.2,
            "shuffle": False,
        }

    # --------------------------------------------------
    # Cross-Validation
    # --------------------------------------------------
    def cv_policy(self) -> Dict[str, Any]:
        return {
            "enabled": False,
            "reason": "CV clássica causa leakage temporal",
        }

    # --------------------------------------------------
    # Métricas
    # --------------------------------------------------
    def allowed_metrics(self) -> List[str]:
        return [
            "mape",
            "smape",
            "rmse",
        ]

    # --------------------------------------------------
    # Modelos
    # --------------------------------------------------
    def allowed_models(self) -> List[str]:
        return [
            "naive_forecast",   # baseline obrigatório
            "arima",
            "sarima",
            "prophet",
            "lstm",
        ]

    # --------------------------------------------------
    # Redução de dimensionalidade
    # --------------------------------------------------
    def dimensionality_reduction_policy(self) -> Dict[str, Any]:
        return {
            "pca": {"enabled": False},
            "factor_analysis": {"enabled": False},
            "mca": {"enabled": False},
        }

    # --------------------------------------------------
    # Avaliação
    # --------------------------------------------------
    def evaluation_policy(self) -> Dict[str, Any]:
        return {
            "baseline": "naive_forecast",
            "require_improvement_over_baseline": True,
            "min_delta": 0.02,
            "evaluation_window": "future_only",
        }

    # --------------------------------------------------
    # Re-treino
    # --------------------------------------------------
    def retraining_policy(self) -> Dict[str, Any]:
        return {
            "monitor_metric": "mape",
            "degradation_threshold": 0.1,
            "time_based_retraining": True,
        }
