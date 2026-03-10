# -*- coding: utf-8 -*-


from src.app.contract.ml_train_contract import MLTrainContract

from src.app.tools.log_factory import get_dcp_logger


class MLContractValidator:
    """
    Validador formal do contrato de ML.

    Responsabilidades:
    - Garantir que o contrato foi validado
    - Verificar coerência científica cruzada
    - Bloquear execução inválida antes do pipeline
    """

    def __init__(self, contract: MLTrainContract,
                 trace_id: str):
        self.contract = contract
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
            "[MLContractValidator] validate() iniciada"
        )
        """
        Executa todas as validações de consistência do contrato.
        Deve ser chamada imediatamente antes do pipeline.
        """
        self._ensure_contract_validated()
        self._validate_problem_vs_policies()
        self._validate_metric_vs_problem()
        self._validate_split_vs_problem()
        self._validate_dimensionality_vs_constraints()

    # --------------------------------------------------
    # Validações internas
    # --------------------------------------------------
    def _ensure_contract_validated(self) -> None:
        if not self.contract.is_valid:
            raise RuntimeError(
                "MLTrainContract não foi validado. "
                "Chame contract.validate() antes."
            )

    def _validate_problem_vs_policies(self) -> None:
        problem = self.contract.problem_type
        policies = self.contract.policies

        # Série temporal não pode usar shuffle
        if problem == "time_series":
            split = policies.get("split", {})
            if split.get("shuffle", False):
                raise ValueError(
                    "time_series não permite split com shuffle=True"
                )

    def _validate_metric_vs_problem(self) -> None:
        problem = self.contract.problem_type
        metric = self.contract.train_config.get("metric")

        invalid_metrics = {
            "time_series": {"roc_auc"},
            "count_model": {"roc_auc", "accuracy"},
        }

        forbidden = invalid_metrics.get(problem, set())
        if metric in forbidden:
            raise ValueError(
                f"Métrica '{metric}' inválida para problem_type '{problem}'"
            )

    def _validate_split_vs_problem(self) -> None:
        problem = self.contract.problem_type
        split = self.contract.policies.get("split", {})

        if problem == "time_series":
            if split.get("type") != "temporal":
                raise ValueError(
                    "time_series exige split do tipo 'temporal'"
                )

    def _validate_dimensionality_vs_constraints(self) -> None:
        dr = self.contract.policies.get("dimensionality_reduction")
        constraints = self.contract.constraints

        if not dr:
            return

        if dr.get("enabled") and constraints.get("require_explainability"):
            raise ValueError(
                "Redução de dimensionalidade proibida "
                "quando require_explainability=True"
            )
