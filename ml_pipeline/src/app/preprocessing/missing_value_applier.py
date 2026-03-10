# -*- coding: utf-8 -*-

import pandas as pd
from typing import Dict, Any, List
from sklearn.impute import KNNImputer
from sklearn.experimental import enable_iterative_imputer  # noqa
from sklearn.impute import IterativeImputer


class MissingValueApplier:
    """
    Executor de imputação de valores faltantes.

    Responsabilidades:
    - Executar política definida no feature_schema
    - Suportar imputação simples e multivariada
    - NÃO decidir política
    - NÃO usar target
    """

    def __init__(
        self,
        *,
        features: List[str],
        policy: Dict[str, Any],
    ):
        self.features = features
        self.policy = policy
        self.imputer = None

    # --------------------------------------------------
    # API pública
    # --------------------------------------------------
    def fit(self, df: pd.DataFrame) -> None:
        """
        Ajusta o imputador SOMENTE no conjunto de treino.
        """
        data = df[self.features]

        method = self.policy.get("method")

        if method in {"mean", "median", "most_frequent", "zero"}:
            # imputação simples não precisa de fit global
            return

        if method == "knn":
            self.imputer = KNNImputer(
                n_neighbors=self.policy.get("n_neighbors", 5)
            )
            self.imputer.fit(data)

        elif method == "iterative":
            self.imputer = IterativeImputer(
                random_state=self.policy.get("random_state", 42),
                max_iter=self.policy.get("max_iter", 10),
            )
            self.imputer.fit(data)

        else:
            raise ValueError(f"Política de missing não suportada: {method}")

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aplica imputação e retorna novo DataFrame.
        """
        new_df = df.copy(deep=True)

        method = self.policy.get("method")

        if method == "mean":
            for f in self.features:
                new_df[f] = new_df[f].fillna(new_df[f].mean())

        elif method == "median":
            for f in self.features:
                new_df[f] = new_df[f].fillna(new_df[f].median())

        elif method == "most_frequent":
            for f in self.features:
                new_df[f] = new_df[f].fillna(new_df[f].mode().iloc[0])

        elif method == "zero":
            for f in self.features:
                new_df[f] = new_df[f].fillna(0)

        elif method in {"knn", "iterative"}:
            if self.imputer is None:
                raise RuntimeError(
                    "Imputer não ajustado. Chame fit() antes de transform()."
                )

            imputed = self.imputer.transform(new_df[self.features])
            new_df[self.features] = imputed

        else:
            raise ValueError(f"Política de missing não suportada: {method}")

        return new_df
