# -*- coding: utf-8 -*-

import os
import pandas as pd
from pathlib import Path

from src.app.tools.log_factory import get_dcp_logger
from src.app.tools.config_loader import load_config


class DCPDatasetLoader:
    """
    Loader do dataset físico produzido pelo DCP.

    Responsabilidades:
    - Carregar o parquet do DCP
    - Garantir existência do arquivo
    - Retornar DataFrame bruto, sem qualquer validação
    """

    def __init__(self, artifact_path: str, trace_id: str):
        if not trace_id:
            raise ValueError("trace_id é obrigatório para DCPDatasetLoader")

        if not isinstance(artifact_path, str):
            raise TypeError("artifact_path deve ser string")

        self.artifact_path = artifact_path
        self.trace_id = trace_id

        self.logger = get_dcp_logger(
            trace_id=self.trace_id,
            classe=self.__class__.__name__,
        )

        config = load_config()
        autosage_registry_base = config["data"].get("autosage_registry_base")
        if not autosage_registry_base:
            raise ValueError("autosage_registry_base é obrigatório para DCPDatasetLoader")

        self.path = str(Path(autosage_registry_base) / self.artifact_path)

    # --------------------------------------------------
    # API pública
    # --------------------------------------------------
    async def load(self) -> pd.DataFrame:
        """
        Carrega o dataset do caminho informado.

        Retorna:
            pd.DataFrame
        """
        self.logger.info("[DCPDatasetLoader] load() iniciado")

        self._validate_path()

        try:

            df = pd.read_parquet(self.path)
            self.logger.info(
                f"[ML][LOAD] parquet lido com sucesso | "
                f"rows={df.shape[0]} | cols={df.shape[1]}"
            )
            return df

        except Exception as exc:
            raise RuntimeError(
                f"Erro ao carregar parquet do DCP: {self.path}"
            ) from exc

    # --------------------------------------------------
    # Validação mínima
    # --------------------------------------------------
    def _validate_path(self) -> None:
        if not os.path.isfile(self.path):
            raise FileNotFoundError(
                f"Arquivo de dataset não encontrado: {self.path}"
            )
