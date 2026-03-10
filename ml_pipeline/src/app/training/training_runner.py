# -*- coding: utf-8 -*-

from typing import List, Tuple, Any

import pandas as pd

from src.app.tools.log_factory import get_dcp_logger
from src.app.training.training_report import TrainingReport


class TrainingRunner:
    """
    Executor do loop de treino + seleção do melhor modelo.
    """

    def __init__(
        self,
        *,
        problem_type: str,
        random_seed: int,
        trace_id: str,
        metric_name: str,
    ):
        self.problem_type = problem_type
        self.random_seed = random_seed
        self.trace_id = trace_id
        self.metric_name = metric_name

        self.logger = get_dcp_logger(
            trace_id=self.trace_id,
            classe=self.__class__.__name__,
        )

    # --------------------------------------------------
    # API pública
    # --------------------------------------------------
    def run(
        self,
        *,
        X: pd.DataFrame,
        y: pd.Series,
        trainers: List[Any],
    ) -> Tuple[Any, TrainingReport]:

        if X.empty or y.empty:
            raise RuntimeError("X ou y vazios no TrainingRunner")

        if not trainers:
            raise RuntimeError("Nenhum trainer fornecido ao TrainingRunner")

        best_model = None
        best_report: TrainingReport | None = None

        for trainer in trainers:
            trainer_name = trainer.__class__.__name__

            self.logger.info(
                f"[TrainingRunner] iniciando treino | trainer={trainer_name}"
            )

            try:
                metric_value, model = trainer.train(
                    problem_type=self.problem_type,
                    X_train=X,
                    y_train=y,
                )
            except Exception as exc:
                self.logger.error(
                    f"[TrainingRunner] falha no treino | "
                    f"trainer={trainer_name} | error={exc}"
                )
                continue

            if metric_value is None or model is None:
                raise RuntimeError(
                    f"Retorno inválido do trainer {trainer_name}: "
                    f"metric_value ou model é None"
                )

            if not isinstance(metric_value, (int, float)):
                raise TypeError(
                    f"Métrica inválida retornada pelo trainer "
                    f"{trainer_name}: {type(metric_value)}"
                )

            metric_value = float(metric_value)

            report = TrainingReport(
                model_name=model.__class__.__name__,
                metric_name=self.metric_name,
                metric_value=metric_value,
                metadata={
                    "problem_type": self.problem_type,
                    "trainer": trainer_name,
                },
            )

            if (
                best_report is None
                or report.metric_value > best_report.metric_value
            ):
                self.logger.info(
                    f"[TrainingRunner] novo melhor modelo | "
                    f"trainer={trainer_name} | "
                    f"{self.metric_name}={report.metric_value}"
                )

                best_report = report
                best_model = model

        if best_model is None or best_report is None:
            raise RuntimeError(
                "Nenhum modelo válido foi treinado com sucesso"
            )

        self.logger.info(
            f"[TrainingRunner] melhor modelo selecionado | "
            f"model={best_report.model_name} | "
            f"{best_report.metric_name}={best_report.metric_value}"
        )

        return best_model, best_report
