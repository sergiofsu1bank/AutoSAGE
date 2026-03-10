# -*- coding: utf-8 -*-

from typing import List, Dict, Any
from src.app.strategies.problem_strategy import ProblemStrategy


class ClassificationStrategy(ProblemStrategy):
    """
    Estratégia científica para problemas de classificação.
    """

    def __init__(self):
        super().__init__(problem_type="classification")

    # --------------------------------------------------
    # Identidade
    # --------------------------------------------------
    def name(self) -> str:
        return "classification"

    # --------------------------------------------------
    # Split
    # --------------------------------------------------
    def split_policy(self) -> Dict[str, Any]:
        return {
            "allowed": [
                "random",
                "stratified",
            ]
        }

    # --------------------------------------------------
    # Cross-Validation
    # --------------------------------------------------
    def cv_policy(self) -> Dict[str, Any]:
        return {
            "enabled": True,
            "type": "stratified_kfold",
            "n_splits": 5,
            "shuffle": True,
            "random_state": 42,
        }

    # --------------------------------------------------
    # Métricas
    # --------------------------------------------------
    def allowed_metrics(self) -> List[str]:
        return [
            "roc_auc",
            "pr_auc",
        ]

    # --------------------------------------------------
    # Modelos
    # --------------------------------------------------
    def allowed_models(self) -> List[str]:
        return [
            "logistic_regression",  # baseline obrigatório
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
            "mca": {"enabled": True},
        }

    # --------------------------------------------------
    # Avaliação
    # --------------------------------------------------
    def evaluation_policy(self) -> Dict[str, Any]:
        return {
            "baseline": "logistic_regression",
            "require_improvement_over_baseline": True,
            "min_delta": 0.01,
        }

    # --------------------------------------------------
    # Re-treino
    # --------------------------------------------------
    def retraining_policy(self) -> Dict[str, Any]:
        return {
            "monitor_metric": "roc_auc",
            "degradation_threshold": 0.05,
            "drift_detection": True,
        }
