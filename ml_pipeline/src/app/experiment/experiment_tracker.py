# -*- coding: utf-8 -*-

import json
import hashlib
from typing import Dict, Any

from src.app.tools.log_factory import get_dcp_logger


class ExperimentTracker:
    """
    Rastreador determinístico de experimentos.

    Responsabilidades:
    - Gerar experiment_id determinístico
    - Garantir linhagem DCP → EDA → ML
    """

    def __init__(
        self,
        *,
        dataset_name: str,
        pipeline_version: int,
        problem_type: str,
        strategy_name: str,
        train_config: Dict[str, Any],
        trace_id: str
    ):
        self.dataset_name = dataset_name
        self.pipeline_version = pipeline_version
        self.problem_type = problem_type
        self.strategy_name = strategy_name
        self.train_config = train_config
        self.trace_id = trace_id

        self.logger = get_dcp_logger(
            trace_id=self.trace_id,
            classe=self.__class__.__name__,
        )

    # --------------------------------------------------
    #
    # API pública
    # --------------------------------------------------
    def experiment_id(self) -> str:

        self.logger.info(
            "[ExperimentTracker]  experiment_id | "
            f"dataset_name={self.dataset_name} | "
            f"pipeline_version={self.pipeline_version} | "
            f"problem_type={self.problem_type} | "
            f"strategy={self.strategy_name} | "
            f"train_config={self._normalize(self.train_config)} | "
            f"trace_id={self.trace_id}"
        )

        """
        Retorna experiment_id determinístico.
        """
        payload = {
            "dataset_name": self.dataset_name,
            "pipeline_version": self.pipeline_version,
            "problem_type": self.problem_type,
            "strategy": self.strategy_name,
            "train_config": self._normalize(self.train_config),
            "trace_id": self._normalize(self.trace_id),
        }


        raw = json.dumps(payload, sort_keys=True)
        digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()

        return f"exp_{digest[:16]}"

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------
    def _normalize(self, obj: Any) -> Any:
        """
        Normaliza estrutura para hashing determinístico.
        """
        if isinstance(obj, dict):
            return {
                k: self._normalize(obj[k])
                for k in sorted(obj.keys())
            }
        if isinstance(obj, list):
            return [self._normalize(x) for x in obj]
        return obj
