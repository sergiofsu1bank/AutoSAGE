# -*- coding: utf-8 -*-

from typing import List, Dict, Any
from src.app.strategies.problem_strategy import ProblemStrategy


class LogisticStrategy(ProblemStrategy):
    """
    Estratégia científica para regressão logística (binária ou multinomial).

    Ênfase em:
    - interpretabilidade
    - estabilidade
    - inferência estatística
    """

    def __init__(self):
        super().__init__(problem_type="logistic")

    # --------------------------------------------------
    # Identidade
    # --------------------------------------------------
    def name(self) -> str:
        return "logistic"

    # --------------------------------------------------
    # Split
    # --------------------------------------------------
    def split_policy(self) -> Dict[str, Any]:
        return {
            "type": "stratified",
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
            "log_loss",
            "roc_auc",
        ]

    # --------------------------------------------------
    # Modelos
    # --------------------------------------------------
    def allowed_models(self) -> List[str]:
        return [
            "logistic_regression",  # baseline obrigatório
        ]

    # --------------------------------------------------
    # Redução de dimensionalidade
    # --------------------------------------------------
    def dimensionality_reduction_policy(self) -> Dict[str, Any]:
        return {
            "pca": {"enabled": False},
            "factor_analysis": {"enabled": False},
            "mca": {"enabled": True},
        }

    # --------------------------------------------------
    # Avaliação
    # --------------------------------------------------
    def evaluation_policy(self) -> Dict[str, Any]:
        return {
            "baseline": "logistic_regression",
            "require_improvement_over_baseline": False,
            "check_coefficient_stability": True,
            "max_coefficient_variation": 0.2,
        }

    # --------------------------------------------------
    # Re-treino
    # --------------------------------------------------
    def retraining_policy(self) -> Dict[str, Any]:
        return {
            "monitor_metric": "log_loss",
            "degradation_threshold": 0.1,
            "coefficient_drift": True,
        }
