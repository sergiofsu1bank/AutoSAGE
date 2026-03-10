# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from typing import Dict, Any, List
from sklearn.model_selection import KFold


class CategoricalEncoder:
    """
    Executor de encoding categórico.

    Responsabilidades:
    - Executar encoding definido no feature_schema
    - Suportar Target Encoding com CV interno
    - NÃO decidir política
    - NÃO causar leakage
    """

    def __init__(
        self,
        *,
        feature: str,
        policy: Dict[str, Any],
        target: str | None = None,
    ):
        self.feature = feature
        self.policy = policy
        self.target = target
        self.mapping = {}

    # --------------------------------------------------
    # API pública
    # --------------------------------------------------
    def fit(self, df: pd.DataFrame) -> None:
        """
        Ajusta encoder SOMENTE no conjunto de treino.
        """
        method = self.policy.get("method")

        if method == "ordinal":
            categories = self.policy.get("categories")
            if categories is None:
                raise ValueError(
                    "Ordinal encoding exige categorias explícitas"
                )
            self.mapping = {
                cat: idx for idx, cat in enumerate(categories)
            }

        elif method == "target":
            if self.target is None:
                raise RuntimeError(
                    "Target Encoding exige nome do target"
                )
            self.mapping = self._fit_target_encoding(df)

        elif method == "one_hot":
            return

        else:
            raise ValueError(f"Encoding categórico não suportado: {method}")

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aplica encoding e retorna novo DataFrame.
        """
        new_df = df.copy(deep=True)
        method = self.policy.get("method")

        if method == "one_hot":
            dummies = pd.get_dummies(new_df[self.feature], prefix=self.feature)
            new_df = new_df.drop(columns=[self.feature])
            new_df = pd.concat([new_df, dummies], axis=1)

        elif method == "ordinal":
            new_df[self.feature] = new_df[self.feature].map(self.mapping)

        elif method == "target":
            global_mean = np.mean(list(self.mapping.values()))
            new_df[self.feature] = (
                new_df[self.feature]
                .map(self.mapping)
                .fillna(global_mean)
            )

        else:
            raise ValueError(f"Encoding categórico não suportado: {method}")

        return new_df

    # --------------------------------------------------
    # Target Encoding com CV interno
    # --------------------------------------------------
    def _fit_target_encoding(self, df: pd.DataFrame) -> Dict[Any, float]:
        """
        Ajusta Target Encoding com CV interno (anti-leakage).
        """
        n_splits = self.policy.get("n_splits", 5)
        kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)

        encoding = {}

        for train_idx, _ in kf.split(df):
            fold = df.iloc[train_idx]
            means = (
                fold.groupby(self.feature)[self.target]
                .mean()
                .to_dict()
            )
            encoding.update(means)

        return encoding
