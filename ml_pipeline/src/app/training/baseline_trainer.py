# -*- coding: utf-8 -*-

import pandas as pd

from sklearn.linear_model import LogisticRegression, LinearRegression


class BaselineTrainer:
    """
    Baseline simples e robusto (Stage 1).

    Responsabilidades:
    - Garantir baseline funcional
    - Gerar métrica comparável
    - NÃO conhecer naming, métrica global ou reporting
    """

    def __init__(self, random_seed: int | None = None):
        self.random_seed = random_seed

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
            f"BaselineTrainer não suporta problem_type={problem_type}"
        )

    # --------------------------------------------------
    # Implementações
    # --------------------------------------------------
    def _classification(self, X, y):
        model = LogisticRegression(
            max_iter=500,
            random_state=self.random_seed,
        )

        model.fit(X, y)

        metric_value = float(model.score(X, y))

        return metric_value, model

    def _regression(self, X, y):
        model = LinearRegression()

        model.fit(X, y)

        metric_value = float(model.score(X, y))

        return metric_value, model
