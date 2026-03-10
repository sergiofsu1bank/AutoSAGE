# -*- coding: utf-8 -*-

import os
import json
from typing import Dict, Any
from pathlib import Path

from src.app.tools.config_loader import load_config
from src.app.tools.log_factory import get_dcp_logger


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
        "physical_schema": "physical_schema.json",
        "manifest": "manifest.json",
        "train_config": "train_config.json",
        "transformations": "transformations.json",
    }

    def __init__(self,
                 eda_prepare_registry_path: str,
                 trace_id: str):
        """
        Args:
            eda_prepare_registry_path: caminho relativo ao registry (dentro do container)
            trace_id: identificador de rastreio da pipeline
        """
        self.trace_id = trace_id
        self.eda_prepare_registry_path = eda_prepare_registry_path

        self.logger = get_dcp_logger(
            trace_id=self.trace_id,
            classe=self.__class__.__name__,
        )

        self.logger.info(
            "[MLArtifactLoader] _init_() iniciado | "
            f"trace_id={self.trace_id} | "
            f"eda_prepare_registry_path={self.eda_prepare_registry_path}"
        )

        if not self.trace_id:
            raise ValueError("trace_id é obrigatório para MLArtifactLoader")

        if not isinstance(self.eda_prepare_registry_path, str):
            raise TypeError("eda_prepare_registry_path deve ser string")

        config = load_config()
        self.autosage_registry_base = config["data"].get("autosage_registry_base")
        if not self.autosage_registry_base:
            raise ValueError(
                "autosage_registry_base é obrigatório e deve apontar para o volume do registry"
            )

        # ---- path final dentro do container ----
        self.path = Path(self.autosage_registry_base).joinpath(
            self.eda_prepare_registry_path
        ).resolve()

        self.logger.info(
            "[MLArtifactLoader] inicializado | "
            f"container_registry_path={self.path}"
        )

        # ---- validação real no filesystem do container ----
        if not self.path.exists():
            raise FileNotFoundError(
                f"Diretório não encontrado no registry do container: {self.path}"
            )

        if not self.path.is_dir():
            raise NotADirectoryError(
                f"Path não é diretório no registry do container: {self.path}"
            )
    # --------------------------------------------------
    # API pública
    # --------------------------------------------------
    async def load(self) -> Dict[str, Any]:
        """
        Carrega todos os artefatos obrigatórios (JSON).

        Retorna:
            dict com os conteúdos dos JSONs
        """
        self.logger.info(
            "[MLArtifactLoader] load() iniciado | "
            f"trace_id={self.trace_id} | "
            f"base_path={self.path}"
        )

        self._validate_base_path()

        artifacts: Dict[str, Any] = {}

        for key, fname in self.REQUIRED_FILES.items():
            pathJson = os.path.join(self.path, fname)
            artifacts[key] = self._load_json(pathJson)

        return artifacts

    # --------------------------------------------------
    # Helpers privados
    # --------------------------------------------------
    def _validate_base_path(self) -> None:
        if not os.path.isdir(self.path):
            raise FileNotFoundError(
                f"Diretório de artefatos não encontrado: {self.path}"
            )

    def _load_json(self, path: str) -> Dict[str, Any]:
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Artefato JSON não encontrado: {path}")

        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as exc:
            raise RuntimeError(
                f"Erro ao carregar JSON: {path}"
            ) from exc
