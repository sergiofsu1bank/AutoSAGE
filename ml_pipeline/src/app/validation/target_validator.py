# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

from src.app.tools.log_factory import get_dcp_logger


class TargetValidator:
    """
    Validador do target do dataset.

    Responsabilidades:
    - Garantir existência do target
    - Validar compatibilidade target × problem_type
    - NÃO inferir problem_type
    - NÃO corrigir dados
    """

    def __init__(self, df: pd.DataFrame, target_name: str, problem_type: str, trace_id: str):
        self.df = df
        self.target_name = target_name
        self.problem_type = problem_type
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
            "[TargetValidator] validate() iniciada"
        )

        self._validate_target_exists()
        self._validate_target_type()

    # --------------------------------------------------
    # Validações internas
    # --------------------------------------------------
    def _validate_target_exists(self) -> None:
        if self.target_name not in self.df.columns:
            raise ValueError(
                f"Target '{self.target_name}' não encontrado no dataset"
            )

    def _validate_target_type(self) -> None:
        series = self.df[self.target_name]

        if self.problem_type == "classification":
            if not (
                series.dtype == "object"
                or pd.api.types.is_integer_dtype(series)
                or pd.api.types.is_bool_dtype(series)
            ):
                raise ValueError(
                    "Target incompatível com classification"
                )

        elif self.problem_type == "logistic":
            unique_vals = set(series.dropna().unique())
            if not unique_vals.issubset({0, 1, True, False}):
                raise ValueError(
                    "Target logístico deve ser binário (0/1 ou bool)"
                )

        elif self.problem_type == "regression":
            if not pd.api.types.is_numeric_dtype(series):
                raise ValueError(
                    "Target incompatível com regression"
                )

        elif self.problem_type == "count_model":
            if not pd.api.types.is_integer_dtype(series):
                raise ValueError(
                    "Target de modelo de contagem deve ser inteiro"
                )
            if (series < 0).any():
                raise ValueError(
                    "Target de modelo de contagem não pode conter valores negativos"
                )

        elif self.problem_type == "time_series":
            if not pd.api.types.is_numeric_dtype(series):
                raise ValueError(
                    "Target de série temporal deve ser numérico"
                )

        else:
            raise ValueError(
                f"problem_type não suportado: {self.problem_type}"
            )
