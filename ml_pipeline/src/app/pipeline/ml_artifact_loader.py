# -*- coding: utf-8 -*-

import os
import json
from typing import Dict, Any
from src.app.tools.config_loader import load_config
from src.app.tools.log_factory import get_dcp_logger

from pathlib import Path

class MLArtifactLoader:
    """
    Loader dos artefatos produzidos pelo EDA Prepare.

    Responsabilidades:
    - Localizar artefatos no registry
    - Carregar arquivos JSON
    - Retornar conteúdo bruto, sem validação científica
    """

    REQUIRED_FILES = {
        "feature_schema": "feature_schema.json",
        "physical_schema": "physical_schema.json",  # ← NOVO
        "manifest": "manifest.json",
        "train_config": "train_config.json",
        "transformations": "transformations.json",
    }

    def __init__(self, base_path: str, trace_id: str):
        """
        Args:
            base_path: caminho relativo ao registry do EDA Prepare
            trace_id: identificador de rastreio da pipeline
        """

        if not trace_id:
            raise ValueError("trace_id é obrigatório para MLArtifactLoader")

        if not isinstance(base_path, str):
            raise TypeError("base_path deve ser string")

        # ENV obrigatória
        config = load_config()
        self.registry_base = config["data"]["processed_path"]


        registry_base = os.getenv("ML_EDAPRE_REGISTRY_BASE")
        if not registry_base:
            raise RuntimeError(
                "ML_EDAPRE_REGISTRY_BASE é obrigatório e não foi definido no ambiente."
            )

        base_path_obj = Path(base_path)

        # Proteção contra path absoluto (quebra isolamento do registry)
        if base_path_obj.is_absolute():
            raise ValueError(
                f"base_path deve ser relativo ao registry, não absoluto: {base_path}"
            )

        self.base_path = str(Path(registry_base) / base_path_obj)
        self.trace_id = trace_id

        self.logger = get_dcp_logger(
            trace_id=self.trace_id,
            classe=self.__class__.__name__,
        )

    # --------------------------------------------------
    # API pública
    # --------------------------------------------------
    def load(self) -> Dict[str, Any]:
        """
        Carrega todos os artefatos obrigatórios.

        Retorna:
            dict com os conteúdos dos JSONs

        Levanta:
            FileNotFoundError se algum arquivo não existir
            RuntimeError se algum JSON for inválido
        """
        self.logger.info(
            "[MLArtifactLoader] load() iniciado | "
            f"trace_id={self.trace_id} | "
            f"base_path={self.base_path}"
        )

        self._validate_base_path()

        artifacts: Dict[str, Any] = {}

        for key, fname in self.REQUIRED_FILES.items():
            path = os.path.join(self.base_path, fname)
            artifacts[key] = self._load_json(path)

        return artifacts

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------
    def _validate_base_path(self) -> None:
        if not isinstance(self.base_path, str):
            raise TypeError("base_path deve ser string")

        if not os.path.isdir(self.base_path):
            raise FileNotFoundError(
                f"Diretório de artefatos não encontrado: {self.base_path}"
            )

    def _load_json(self, path: str) -> Dict[str, Any]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Artefato não encontrado: {path}")

        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as exc:
            raise RuntimeError(
                f"Erro ao carregar JSON: {path}"
            ) from exc
