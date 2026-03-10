# -*- coding: utf-8 -*-

import pandas as pd


class SchemaValidator:
    """
    Valida o schema de entrada em runtime
    com base no feature_schema do treino.
    """

    def __init__(self, feature_schema: dict):
        self.feature_schema = feature_schema
        self.expected_features = feature_schema["features"]
        self.expected_types = feature_schema.get("types", {})

    def validate(self, df: pd.DataFrame) -> pd.DataFrame:
        # --------------------------------------------------
        # 1. Colunas obrigatórias
        # --------------------------------------------------
        missing = set(self.expected_features) - set(df.columns)
        if missing:
            raise RuntimeError(
                f"Colunas ausentes para inferência: {missing}"
            )

        # --------------------------------------------------
        # 2. Colunas inesperadas (warning forte)
        # --------------------------------------------------
        extra = set(df.columns) - set(self.expected_features)
        if extra:
            # opção conservadora: falhar
            raise RuntimeError(
                f"Colunas inesperadas no input: {extra}"
            )

        # --------------------------------------------------
        # 3. Tipos esperados (quando disponível)
        # --------------------------------------------------
        for col, expected_type in self.expected_types.items():
            if col not in df.columns:
                continue

            if expected_type == "numeric":
                if not pd.api.types.is_numeric_dtype(df[col]):
                    raise RuntimeError(
                        f"Coluna '{col}' esperada numérica"
                    )

            if expected_type == "categorical":
                if not pd.api.types.is_object_dtype(df[col]):
                    raise RuntimeError(
                        f"Coluna '{col}' esperada categórica"
                    )

        # --------------------------------------------------
        # 4. Reordenar colunas
        # --------------------------------------------------
        return df[self.expected_features]
