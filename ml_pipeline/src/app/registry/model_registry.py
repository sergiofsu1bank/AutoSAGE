# -*- coding: utf-8 -*-

import os
import json
from typing import Dict, Any


class ModelRegistry:
    """
    Registry científico e de produção de modelos.

    Responsabilidades:
    - Criar estrutura versionada do experimento
    - Persistir artefato de PRODUÇÃO (model_bundle.pkl)
    - Persistir artefatos científicos (JSON)
    """

    def __init__(self, base_path: str):
        self.base_path = base_path

    # --------------------------------------------------
    # API pública
    # --------------------------------------------------
    def register(
        self,
        *,
        experiment_id: str,
        model_name: str,
        bundle_builder,
        artifacts: Dict[str, Any],
    ) -> str:
        """
        Registra modelo aprovado e seus artefatos.
        """
        experiment_path = os.path.join(
            self.base_path,
            experiment_id,
            model_name,
        )

        os.makedirs(experiment_path, exist_ok=True)

        # --------------------------------------------------
        # 1. Salvar artefato de PRODUÇÃO
        # --------------------------------------------------
        bundle_path = bundle_builder.save(experiment_path)

        # --------------------------------------------------
        # 2. Salvar artefatos científicos
        # --------------------------------------------------
        for name, content in artifacts.items():
            self._save_json(
                base_path=experiment_path,
                name=name,
                content=content,
            )

        return experiment_path

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------
    def _save_json(
        self,
        *,
        base_path: str,
        name: str,
        content: Dict[str, Any],
    ) -> None:
        path = os.path.join(base_path, f"{name}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(content, f, indent=2, ensure_ascii=False)
