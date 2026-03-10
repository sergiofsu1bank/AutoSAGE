# -*- coding: utf-8 -*-

import pandas as pd
from typing import Dict, Any, List
from sklearn.preprocessing import (
    StandardScaler,
    MinMaxScaler,
    RobustScaler,
    PowerTransformer,
)


class NumericalScaler:
    """
    Executor de scaling numérico.

    Responsabilidades:
    - Executar política definida no feature_schema
    - Suportar normalização e transformação de potência
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
        self.scaler = None

    # --------------------------------------------------
    # API pública
    # --------------------------------------------------
    def fit(self, df: pd.DataFrame) -> None:
        """
        Ajusta o scaler SOMENTE no conjunto de treino.
        """
        method = self.policy.get("method")

        if method == "standard":
            self.scaler = StandardScaler()

        elif method == "minmax":
            self.scaler = MinMaxScaler()

        elif method == "robust":
            self.scaler = RobustScaler()

        elif method == "power":
            self.scaler = PowerTransformer(
                method="yeo-johnson",
                standardize=self.policy.get("standardize", True),
            )

        else:
            raise ValueError(f"Método de scaling não suportado: {method}")

        self.scaler.fit(df[self.features])

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aplica scaling e retorna novo DataFrame.
        """
        if self.scaler is None:
            raise RuntimeError(
                "Scaler não ajustado. Chame fit() antes de transform()."
            )

        new_df = df.copy(deep=True)
        scaled = self.scaler.transform(new_df[self.features])
        new_df[self.features] = scaled

        return new_df
