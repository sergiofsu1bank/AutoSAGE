# -*- coding: utf-8 -*-

import math
import pandas as pd
import xgboost as xgb


class XGBoostTrainer:
    """
    Trainer XGBoost simples (Stage 1).

    Responsabilidade única:
    - Treinar modelo
    - NÃO produzir métrica científica nesta sprint
    """

    def __init__(self, random_seed: int | None = None):
        self.random_seed = random_seed or 42

    # --------------------------------------------------
    # API pública
    # --------------------------------------------------
    def train(
        self,
        *,
        problem_type: str,
        X_train: pd.DataFrame,
        y_train: pd.Series,
    ):
        if problem_type == "classification":
            return self._classification(X_train, y_train)

        if problem_type == "regression":
            return self._regression(X_train, y_train)

        raise ValueError(
            f"XGBoostTrainer não suporta problem_type={problem_type}"
        )

    # --------------------------------------------------
    # Implementações
    # --------------------------------------------------
    def _classification(self, X: pd.DataFrame, y: pd.Series):
        dtrain = xgb.DMatrix(X, label=y)

        params = {
            "objective": "binary:logistic",
            "seed": self.random_seed,
        }

        booster = xgb.train(
            params=params,
            dtrain=dtrain,
            num_boost_round=50,
            verbose_eval=False,
        )

        return float("nan"), booster

    def _regression(self, X: pd.DataFrame, y: pd.Series):
        dtrain = xgb.DMatrix(X, label=y)

        params = {
            "objective": "reg:squarederror",
            "seed": self.random_seed,
        }

        booster = xgb.train(
            params=params,
            dtrain=dtrain,
            num_boost_round=50,
            verbose_eval=False,
        )

        return float("nan"), booster
