# -*- coding: utf-8 -*-

from typing import List, Dict, Any
from src.app.strategies.problem_strategy import ProblemStrategy


class RegressionStrategy(ProblemStrategy):
    """
    Estratégia científica para problemas de regressão.
    """

    def __init__(self):
        super().__init__(problem_type="regression")

    # --------------------------------------------------
    # Identidade
    # --------------------------------------------------
    def name(self) -> str:
        return "regression"

    # --------------------------------------------------
    # Split
    # --------------------------------------------------
    def split_policy(self) -> Dict[str, Any]:
        return {
            "type": "random",
            "test_size": 0.2,
            "shuffle": True,
            "random_state": 42,
        }

    # --------------------------------------------------
    # Cross-Validation
    # --------------------------------------------------
    def cv_policy(self) -> Dict[str, Any]:
        return {
            "enabled": True,
            "type": "kfold",
            "n_splits": 5,
            "shuffle": True,
            "random_state": 42,
        }

    # --------------------------------------------------
    # Métricas
    # --------------------------------------------------
    def allowed_metrics(self) -> List[str]:
        return [
            "rmse",
            "mae",
            "r2",
        ]

    # --------------------------------------------------
    # Modelos
    # --------------------------------------------------
    def allowed_models(self) -> List[str]:
        return [
            "linear_regression",   # baseline obrigatório
            "ridge",
            "lasso",
            "elastic_net",
            "random_forest",
            "gradient_boosting",
            "xgboost",
        ]

    # --------------------------------------------------
    # Redução de dimensionalidade
    # --------------------------------------------------
    def dimensionality_reduction_policy(self) -> Dict[str, Any]:
        return {
            "pca": {"enabled": True},
            "factor_analysis": {"enabled": True},
            "mca": {"enabled": False},
        }

    # --------------------------------------------------
    # Avaliação
    # --------------------------------------------------
    def evaluation_policy(self) -> Dict[str, Any]:
        return {
            "baseline": "linear_regression",
            "require_improvement_over_baseline": True,
            "min_delta": 0.01,
        }

    # --------------------------------------------------
    # Re-treino
    # --------------------------------------------------
    def retraining_policy(self) -> Dict[str, Any]:
        return {
            "monitor_metric": "rmse",
            "degradation_threshold": 0.05,
            "drift_detection": True,
        }
