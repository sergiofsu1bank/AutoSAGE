# -*- coding: utf-8 -*-

import pandas as pd
from typing import Dict, Any, List
from sklearn.decomposition import PCA, FactorAnalysis


class DimensionalityReducer:
    """
    Executor de redução dimensional.

    Responsabilidades:
    - Executar PCA, Factor Analysis ou MCA conforme contrato
    - Usar variância explicada mínima
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
        self.reducer = None
        self.feature_names_: List[str] = []

    # --------------------------------------------------
    # API pública
    # --------------------------------------------------
    def fit(self, df: pd.DataFrame) -> None:
        """
        Ajusta redutor SOMENTE no conjunto de treino.
        """
        method = self.policy.get("method")
        X = df[self.features]

        if method == "pca":
            var_threshold = self.policy.get("min_variance", 0.95)
            self.reducer = PCA(n_components=var_threshold)
            self.reducer.fit(X)

            self.feature_names_ = [
                f"pca_{i}" for i in range(self.reducer.n_components_)
            ]

        elif method == "factor_analysis":
            n_components = self.policy.get("n_components")
            if n_components is None:
                raise ValueError(
                    "Factor Analysis exige n_components explícito"
                )

            self.reducer = FactorAnalysis(n_components=n_components)
            self.reducer.fit(X)

            self.feature_names_ = [
                f"fa_{i}" for i in range(n_components)
            ]

        elif method == "mca":
            # MCA pressupõe categóricos já codificados (one-hot)
            # Implementação explícita futura (v1.1)
            raise NotImplementedError(
                "MCA será implementado em v1.1"
            )

        else:
            raise ValueError(f"Redução dimensional não suportada: {method}")

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aplica redução dimensional e retorna novo DataFrame.
        """
        if self.reducer is None:
            raise RuntimeError(
                "Reducer não ajustado. Chame fit() antes de transform()."
            )

        new_df = df.copy(deep=True)
        reduced = self.reducer.transform(new_df[self.features])

        reduced_df = pd.DataFrame(
            reduced,
            columns=self.feature_names_,
            index=new_df.index,
        )

        new_df = new_df.drop(columns=self.features)
        new_df = pd.concat([new_df, reduced_df], axis=1)

        return new_df
