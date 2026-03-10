# -*- coding: utf-8 -*-

import pandas as pd
from typing import Dict, Any

from src.app.tools.log_factory import get_dcp_logger

class SchemaValidator:
    """
    Validador de schema físico do dataset.

    Responsabilidades:
    - Garantir que o DataFrame respeita o schema físico do EDA Explore
    - Bloquear incompatibilidades estruturais
    - NÃO corrigir tipos
    - NÃO inferir schema
    """

    def __init__(self, df: pd.DataFrame, schema: Dict[str, Any], trace_id: str):
        self.df = df
        self.schema = schema
        self.trace_id = trace_id

        self.logger = get_dcp_logger(
            trace_id=self.trace_id,
            classe=self.__class__.__name__,
        )

    # --------------------------------------------------
    # API pública
    # --------------------------------------------------
    def validate(self) -> None:

        self.logger.info(
            "[SchemaValidator] validate() iniciada"
        )
        self._validate_schema_format()
        self._validate_columns_presence()
        self._validate_physical_types()

    # --------------------------------------------------
    # Validações internas
    # --------------------------------------------------
    def _validate_schema_format(self) -> None:
        if not isinstance(self.schema, dict):
            raise TypeError("Schema físico deve ser um dicionário")

        for col, meta in self.schema.items():
            if not isinstance(meta, dict):
                raise ValueError(
                    f"Schema inválido para coluna '{col}': esperado dict"
                )

            if "physical_dtype" not in meta:
                raise ValueError(
                    f"Schema da coluna '{col}' não possui 'physical_dtype'"
                )

    def _validate_columns_presence(self) -> None:
        schema_cols = set(self.schema.keys())
        df_cols = set(self.df.columns)

        missing = schema_cols - df_cols
        if missing:
            raise ValueError(
                f"Dataset não contém colunas esperadas pelo schema: {missing}"
            )

    def _validate_physical_types(self) -> None:
        for col, meta in self.schema.items():
            expected_dtype = meta["physical_dtype"]
            actual_dtype = str(self.df[col].dtype)

            if actual_dtype != expected_dtype:
                raise ValueError(
                    f"Tipo físico incompatível na coluna '{col}': "
                    f"esperado={expected_dtype}, encontrado={actual_dtype}"
                )
