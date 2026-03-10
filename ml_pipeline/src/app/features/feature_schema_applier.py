# -*- coding: utf-8 -*-

import pandas as pd
from typing import Dict, Any, List
from src.app.tools.log_factory import get_dcp_logger


class FeatureSchemaApplier:
    """
    Aplica o contrato de features definido no EDA Prepare.

    Responsabilidades:
    - Aplicar transformações conforme feature_schema
    - Retornar novo DataFrame (imutável)
    - NÃO decidir políticas
    - NÃO inferir comportamento
    """


    def __init__(
        self,
        *,
        feature_schema: List[Dict[str, Any]],
        target_name: str,
        trace_id: str
    ):
        self.feature_schema = feature_schema
        self.target_name = target_name
        self.trace_id = trace_id
        self.logger = get_dcp_logger(
                    trace_id=self.trace_id,
                    classe=self.__class__.__name__,
    )

    # --------------------------------------------------
    # API pública
    # --------------------------------------------------
    def apply(self, df: pd.DataFrame) -> pd.DataFrame:

        try:
            """
            Aplica o schema de features e retorna um novo DataFrame.
            """
            self.logger.info(
                "[FeatureSchemaApplier] apply() iniciado | "
                f"features={len(self.feature_schema)} | target={self.target_name}"
            )

            self._validate_input(df)

            new_df = df.copy(deep=True)

            features: List[Dict[str, Any]] = self.feature_schema
            target = self.target_name

            # Mantém apenas features + target
            selected_columns = [f["name"] for f in features]
            if target:
                selected_columns.append(target)

            new_df = new_df[selected_columns]

            # Aplica transformações feature a feature
            for feature in features:
                name = feature.get("name")

                if "type" not in feature:
                    raise ValueError(
                        f"Feature '{name}' sem campo obrigatório 'type'"
                    )

                ftype = feature["type"]
                if ftype == "numeric":
                    new_df[name] = self._apply_numeric(new_df[name], feature)
                elif ftype == "categorical":
                    new_df = self._apply_categorical(new_df, name, feature)
                else:
                    raise ValueError(
                        f"Tipo de feature não suportado: {ftype}"
                    )

            return new_df

        except Exception as exc:
            self.logger.error(
                f"[FeatureSchemaApplier][FAILED] trace_id={self.trace_id} | error={exc}"
            )
            raise

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------
    def _validate_input(self, df: pd.DataFrame) -> None:
        if not isinstance(df, pd.DataFrame):
            raise TypeError("Entrada deve ser um pandas.DataFrame")

    def _apply_numeric(self, series: pd.Series, feature: Dict[str, Any]) -> pd.Series:
        s = series.copy()

        # Missing values
        missing_policy = feature.get("missing_policy")
        if missing_policy == "mean":
            s = s.fillna(s.mean())
        elif missing_policy == "median":
            s = s.fillna(s.median())
        elif missing_policy == "zero":
            s = s.fillna(0)

        # Scaling
        scaler = feature.get("scaler")
        if scaler == "standard":
            s = (s - s.mean()) / s.std(ddof=0)
        elif scaler == "minmax":
            s = (s - s.min()) / (s.max() - s.min())

        return s

    def _apply_categorical(
        self,
        df: pd.DataFrame,
        name: str,
        feature: Dict[str, Any]
    ) -> pd.DataFrame:
        encoding = feature.get("encoding")

        if encoding == "onehot":
            dummies = pd.get_dummies(df[name], prefix=name)
            df = df.drop(columns=[name])
            df = pd.concat([df, dummies], axis=1)

        else:
            raise ValueError(
                f"Encoding categórico não suportado: {encoding}"
            )

        return df
