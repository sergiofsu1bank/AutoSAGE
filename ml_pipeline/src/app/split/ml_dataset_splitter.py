# -*- coding: utf-8 -*-

from typing import Dict, Tuple

import pandas as pd
from sklearn.model_selection import train_test_split

from src.app.tools.log_factory import get_dcp_logger


class MLDatasetSplitter:
    """
    Executa o split do dataset para avaliação honesta.

    Responsabilidade única:
    - Aplicar uma estratégia de split EXPLÍCITA
    - Retornar partições estáveis e reprodutíveis

    NÃO:
    - infere estratégia
    - avalia modelo
    - altera dados
    """

    def __init__(
        self,
        *,
        strategy: Dict,
        random_seed: int,
        trace_id: str,
    ):
        self.strategy = strategy
        self.random_seed = random_seed
        self.trace_id = trace_id

        self.logger = get_dcp_logger(
            trace_id=self.trace_id,
            classe=self.__class__.__name__,
        )

        self._validate_strategy()

    # --------------------------------------------------
    # API pública
    # --------------------------------------------------
    def split(
        self,
        *,
        X: pd.DataFrame,
        y: pd.Series,
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:

        if X.empty or y.empty:
            raise RuntimeError("X ou y vazios no MLDatasetSplitter")

        split_type = self.strategy.get("type")

        self.logger.info(
            f"[MLDatasetSplitter] executando split | type={split_type}"
        )

        if split_type == "stratified_holdout":
            return self._stratified_holdout(X, y)

        if split_type == "holdout":
            return self._simple_holdout(X, y)

        raise ValueError(
            f"Estratégia de split não suportada: {split_type}"
        )

    # --------------------------------------------------
    # Implementações
    # --------------------------------------------------
    def _stratified_holdout(
        self,
        X: pd.DataFrame,
        y: pd.Series,
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:

        test_size = self.strategy.get("test_size", 0.2)

        self.logger.info(
            f"[MLDatasetSplitter] stratified_holdout | test_size={test_size}"
        )

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=test_size,
            random_state=self.random_seed,
            stratify=y,
        )

        return X_train, X_test, y_train, y_test

    def _simple_holdout(
        self,
        X: pd.DataFrame,
        y: pd.Series,
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:

        test_size = self.strategy.get("test_size", 0.2)

        self.logger.info(
            f"[MLDatasetSplitter] holdout | test_size={test_size}"
        )

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=test_size,
            random_state=self.random_seed,
            shuffle=True,
        )

        return X_train, X_test, y_train, y_test

    # --------------------------------------------------
    # Validação
    # --------------------------------------------------
    def _validate_strategy(self) -> None:
        if not isinstance(self.strategy, dict):
            raise TypeError("strategy deve ser um dict")

        if "type" not in self.strategy:
            raise ValueError("strategy.type é obrigatório")

        split_type = self.strategy.get("type")

        if split_type not in {"stratified_holdout", "holdout"}:
            raise ValueError(
                f"strategy.type inválido: {split_type}"
            )

        test_size = self.strategy.get("test_size", 0.2)

        if not isinstance(test_size, float) or not (0.0 < test_size < 1.0):
            raise ValueError(
                "strategy.test_size deve ser float entre 0 e 1"
            )
