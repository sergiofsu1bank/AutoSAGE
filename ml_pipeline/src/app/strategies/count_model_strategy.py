# -*- coding: utf-8 -*-

from typing import List, Dict, Any
from src.app.strategies.problem_strategy import ProblemStrategy


class CountModelStrategy(ProblemStrategy):
    """
    Estratégia científica para modelos de contagem.

    Ênfase em:
    - distribuição correta
    - overdispersion
    - inferência estatística
    """

    def __init__(self):
        super().__init__(problem_type="count_model")

    # --------------------------------------------------
    # Identidade
    # --------------------------------------------------
    def name(self) -> str:
        return "count_model"

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
            "note": "Usar CV com cautela em dados de contagem",
        }

    # --------------------------------------------------
    # Métricas
    # --------------------------------------------------
    def allowed_metrics(self) -> List[str]:
        return [
            "deviance",
            "log_likelihood",
            "rmse",
        ]

    # --------------------------------------------------
    # Modelos
    # --------------------------------------------------
    def allowed_models(self) -> List[str]:
        return [
            "poisson_regression",          # baseline obrigatório
            "negative_binomial_regression",
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
            "baseline": "poisson_regression",
            "require_improvement_over_baseline": True,
            "overdispersion_check": True,
            "min_deviance_improvement": 0.05,
        }

    # --------------------------------------------------
    # Re-treino
    # --------------------------------------------------
    def retraining_policy(self) -> Dict[str, Any]:
        return {
            "monitor_metric": "deviance",
            "degradation_threshold": 0.1,
            "dispersion_shift": True,
        }
