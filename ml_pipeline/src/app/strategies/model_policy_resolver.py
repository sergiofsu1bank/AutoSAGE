# -*- coding: utf-8 -*-

from typing import List, Type

from src.app.training.baseline_trainer import BaselineTrainer
from src.app.training.advanced_sklearn_trainer import AdvancedSklearnTrainer
from src.app.training.xgboost_trainer import XGBoostTrainer
from src.app.training.statsmodels_trainer import StatsModelsTrainer
from src.app.training.time_series_trainer import TimeSeriesTrainer


class ModelPolicyResolver:
    """
    Resolve modelos científicos para trainers técnicos.
    NÃO decide ciência.
    """

    _POLICY = {
        # Classification / Regression
        "logistic_regression": BaselineTrainer,
        "random_forest": AdvancedSklearnTrainer,
        "gradient_boosting": AdvancedSklearnTrainer,
        "xgboost": XGBoostTrainer,

        # Estatístico
        "statsmodels": StatsModelsTrainer,

        # Time Series
        "time_series": TimeSeriesTrainer,
    }

    def resolve(self, model_names: List[str]) -> List[Type]:
        trainer_classes = []

        for name in model_names:
            if name not in self._POLICY:
                raise RuntimeError(
                    f"Modelo não reconhecido pelo resolver técnico: {name}"
                )
            trainer_classes.append(self._POLICY[name])

        return trainer_classes
