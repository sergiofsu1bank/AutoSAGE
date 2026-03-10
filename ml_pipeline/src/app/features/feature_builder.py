# -*- coding: utf-8 -*-

import pandas as pd
from typing import Tuple
from src.app.tools.log_factory import get_dcp_logger


class FeatureBuilder:
    """
    Responsável por separar features (X) e target (y)
    a partir do dataset preparado.

    Responsabilidades:
    - Garantir ausência de leakage do target em X
    - Retornar X e y prontos para split/treino
    - NÃO criar features
    - NÃO transformar dados
    """

    def __init__(self, *, target_name: str,trace_id: str):
        self.target_name = target_name
        self.trace_id = trace_id

        self.logger = get_dcp_logger(
            trace_id=self.trace_id,
            classe=self.__class__.__name__,
        )

    # --------------------------------------------------
    # API pública
    # --------------------------------------------------
    def build(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:

        self.logger.info(
            "[FeatureBuilder] build() iniciado | "
            f"df={pd.DataFrame}"
        )

        if not isinstance(df, pd.DataFrame):
            raise TypeError("Entrada deve ser pandas.DataFrame")

        if self.target_name not in df.columns:
            raise RuntimeError(
                f"Target '{self.target_name}' não encontrado no DataFrame"
            )

        y = df[self.target_name]
        X = df.drop(columns=[self.target_name])

        if X.empty:
            raise RuntimeError("FeatureBuilder gerou X vazio")

        if y.empty:
            raise RuntimeError("FeatureBuilder gerou y vazio")

        return X, y
