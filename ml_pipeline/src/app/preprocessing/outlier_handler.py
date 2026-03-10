# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from typing import Dict, Any, List
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor


class OutlierHandler:
    """
    Executor de tratamento de outliers.

    Responsabilidades:
    - Executar política definida no feature_schema
    - Suportar métodos univariados e multivariados
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
        self.model = None

    # --------------------------------------------------
    # API pública
    # --------------------------------------------------
    def fit(self, df: pd.DataFrame) -> None:
        """
        Ajusta detector multivariado SOMENTE no treino.
        """
        method = self.policy.get("method")

        if method == "isolation_forest":
            self.model = IsolationForest(
                contamination=self.policy.get("contamination", 0.05),
                random_state=self.policy.get("random_state", 42),
            )
            self.model.fit(df[self.features])

        elif method == "lof":
            self.model = LocalOutlierFactor(
                n_neighbors=self.policy.get("n_neighbors", 20),
                contamination=self.policy.get("contamination", 0.05),
                novelty=True,
            )
            self.model.fit(df[self.features])

        elif method in {"iqr", "zscore", "winsor"}:
            return

        else:
            raise ValueError(f"Política de outlier não suportada: {method}")

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aplica tratamento de outliers e retorna novo DataFrame.
        """
        new_df = df.copy(deep=True)
        method = self.policy.get("method")

        if method == "iqr":
            for f in self.features:
                q1 = new_df[f].quantile(0.25)
                q3 = new_df[f].quantile(0.75)
                iqr = q3 - q1
                lower = q1 - 1.5 * iqr
                upper = q3 + 1.5 * iqr
                new_df[f] = new_df[f].clip(lower, upper)

        elif method == "zscore":
            for f in self.features:
                mean = new_df[f].mean()
                std = new_df[f].std(ddof=0)
                z = (new_df[f] - mean) / std
                threshold = self.policy.get("threshold", 3)
                new_df[f] = new_df[f].where(z.abs() <= threshold, mean)

        elif method == "winsor":
            lower_q = self.policy.get("lower_q", 0.05)
            upper_q = self.policy.get("upper_q", 0.95)
            for f in self.features:
                lower = new_df[f].quantile(lower_q)
                upper = new_df[f].quantile(upper_q)
                new_df[f] = new_df[f].clip(lower, upper)

        elif method in {"isolation_forest", "lof"}:
            if self.model is None:
                raise RuntimeError(
                    "Detector de outliers não ajustado. Chame fit() antes."
                )

            preds = self.model.predict(new_df[self.features])
            mask = preds == 1  # 1 = inlier
            new_df = new_df[mask].reset_index(drop=True)

        else:
            raise ValueError(f"Política de outlier não suportada: {method}")

        return new_df
