# -*- coding: utf-8 -*-

from typing import List
from src.app.tools.log_factory import get_dcp_logger
from src.app.strategies.problem_strategy import ProblemStrategy
from src.app.strategies.model_policy_resolver import ModelPolicyResolver


class ModelSelector:
    """
    Materializa trainers permitidos por uma ProblemStrategy.

    Responsabilidades:
    - Executar política de modelos
    - NÃO decidir ciência
    - NÃO inferir problem_type
    """

    def __init__(
        self,
        *,
        strategy: ProblemStrategy,
        resolver: ModelPolicyResolver,
        random_seed: int | None,
        trace_id: str
    ):
        self.strategy = strategy
        self.resolver = resolver
        self.random_seed = random_seed
        self.trace_id = trace_id

        self.logger = get_dcp_logger(
            trace_id=self.trace_id,
            classe=self.__class__.__name__,
        )

    def select(self) -> List[object]:
        self.logger.info(
            "[ModelSelector] select() iniciado | "
            f"strategy={self.strategy.name()}"
        )

        model_names = self.strategy.allowed_models()
        if not model_names:
            raise RuntimeError(
                "ProblemStrategy inválida: allowed_models vazio"
            )

        trainer_classes = self.resolver.resolve(model_names)

        trainers = []
        for trainer_cls in trainer_classes:
            try:
                trainers.append(
                    trainer_cls(random_seed=self.random_seed)
                )
            except TypeError:
                trainers.append(trainer_cls())

        return trainers
