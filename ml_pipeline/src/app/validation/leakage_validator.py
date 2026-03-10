# -*- coding: utf-8 -*-

from typing import List, Dict, Any

from src.app.tools.log_factory import get_dcp_logger


class LeakageValidator:
    """
    Validador de vazamento de target (leakage).

    Responsabilidades:
    - Bloquear leakage explícito identificado no EDA Explore
    - NÃO pontuar risco
    - NÃO tentar corrigir
    - NÃO inferir novos leakages
    """

    BLOCKING_WARNING_TYPES = {
        "LEAKAGE_PROXY",
        "TARGET_LEAKAGE",
    }

    def __init__(self, warnings: List[Dict[str, Any]], trace_id: str):
        self.warnings = warnings or []
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
            "[LeakageValidator] validate() iniciada"
        )
        """
        Bloqueia execução se houver leakage explícito.
        """
        self._validate_warnings_format()
        self._block_explicit_leakage()

    # --------------------------------------------------
    # Validações internas
    # --------------------------------------------------
    def _validate_warnings_format(self) -> None:
        if not isinstance(self.warnings, list):
            raise TypeError("warnings deve ser uma lista")

        for w in self.warnings:
            if not isinstance(w, dict):
                raise ValueError("Cada warning deve ser um dicionário")

            if "type" not in w:
                raise ValueError("Warning inválido: campo 'type' ausente")

    def _block_explicit_leakage(self) -> None:
        blocking = [
            w for w in self.warnings
            if w.get("type") in self.BLOCKING_WARNING_TYPES
        ]

        if blocking:
            columns = [
                w.get("column", "<unknown>")
                for w in blocking
            ]

            raise RuntimeError(
                "Leakage explícito detectado. "
                f"Colunas bloqueadas: {columns}"
            )
