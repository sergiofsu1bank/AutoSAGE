# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from src.app.tools.log_factory import get_dcp_logger


class DatasetValidator:
    """
    Validador científico inicial do dataset.

    Responsabilidades:
    - Garantir que o dataset é utilizável
    - Bloquear dados estruturalmente inválidos
    - NÃO corrigir dados
    - NÃO gerar relatórios
    """

    def __init__(self, df: pd.DataFrame, trace_id: str):
        self.df = df
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
            "[DatasetValidator] validate() iniciada"
        )
        """
        Executa todas as validações mínimas do dataset.
        """
        self._validate_dataframe()
        self._validate_not_empty()
        self._validate_columns_unique()
        self._validate_finite_values()
        self._validate_minimum_shape()

    # --------------------------------------------------
    # Validações internas
    # --------------------------------------------------
    def _validate_dataframe(self) -> None:
        if not isinstance(self.df, pd.DataFrame):
            raise TypeError("Dataset deve ser um pandas.DataFrame")

    def _validate_not_empty(self) -> None:
        if self.df.empty:
            raise ValueError("Dataset vazio")

    def _validate_columns_unique(self) -> None:
        if self.df.columns.duplicated().any():
            raise ValueError("Dataset possui colunas duplicadas")

    def _validate_finite_values(self) -> None:
        if not np.isfinite(self.df.select_dtypes(include=[np.number])).all().all():
            raise ValueError(
                "Dataset contém valores infinitos (inf ou -inf)"
            )

    def _validate_minimum_shape(self) -> None:
        if self.df.shape[1] < 2:
            raise ValueError(
                "Dataset deve possuir ao menos uma feature e um target"
            )
