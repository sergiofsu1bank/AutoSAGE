# -*- coding: utf-8 -*-

import math
import pandas as pd

from sklearn.ensemble import (
    RandomForestClassifier,
    RandomForestRegressor,
)


class AdvancedSklearnTrainer:
    """
    Trainer avançado sklearn (simples e auto-contido).

    Escopo explícito:
    - Executa treino do modelo
    - NÃO realiza validação
    - NÃO realiza tuning
    - NÃO produz métrica científica comparável

    Retorna métrica neutra (NaN) apenas para
    obedecer ao contrato da Sprint 6.
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
            return self._train_classifier(X_train, y_train)

        if problem_type == "regression":
            return self._train_regressor(X_train, y_train)

        raise ValueError(
            f"AdvancedSklearnTrainer não suporta problem_type={problem_type}"
        )

    # --------------------------------------------------
    # Implementações internas
    # --------------------------------------------------
    def _train_classifier(self, X: pd.DataFrame, y: pd.Series):
        model = RandomForestClassifier(
            n_estimators=100,
            random_state=self.random_seed,
        )

        model.fit(X, y)

        return float("nan"), model

    def _train_regressor(self, X: pd.DataFrame, y: pd.Series):
        model = RandomForestRegressor(
            n_estimators=100,
            random_state=self.random_seed,
        )

        model.fit(X, y)

        return float("nan"), model
