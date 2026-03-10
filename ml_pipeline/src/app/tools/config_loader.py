# src/config/config_loader.py
"""
ConfigLoader oficial do EDA SEM YAML.
Toda a configuração vem das variáveis de ambiente definidas no docker-compose.

Agora 100% alinhado ao padrão:
EDA_LOG_PATH
EDA_LOG_LEVEL
EDA_REGISTRY_BASE
EDA_OUTPUT_PATH
EDA_ERROR_PATH
EDA_REPORTS_PATH
"""

import os


def load_config() -> dict:
    """
    Carrega configuração exclusivamente do docker-compose (ENV).
    Retorna um dict no formato esperado pelo pipeline.
    """
    # ---------------------------------------------------------
    # REGISTRY ROOT (corrigido)
    # ---------------------------------------------------------
    registry_base = os.getenv("ML_REGISTRY_BASE")
    if not registry_base:
        raise RuntimeError("ML_REGISTRY_BASE é obrigatório e não foi definido no ambiente.")

    autosage_registry_base = os.getenv("AUTOSAGE_REGISTRY_BASE")
    if not autosage_registry_base:
        raise RuntimeError("AUTOSAGE_REGISTRY_BASE é obrigatório e não foi definido no ambiente.")

    # ---------------------------------------------------------
    # PATHS INTERNOS — todos com prefixo EDA_
    # ---------------------------------------------------------
    processed_path = os.getenv("ML_OUTPUT_PATH")
    error_path = os.getenv("ML_ERROR_PATH")
    reports_path = os.getenv("ML_REPORTS_PATH")

    required_paths = {
        "ML_OUTPUT_PATH": processed_path,
        "ML_ERROR_PATH": error_path,
        "ML_REPORTS_PATH": reports_path,
    }

    for name, value in required_paths.items():
        if not value:
            raise RuntimeError(f"{name} é obrigatório e não foi definido no ambiente.")

    # ---------------------------------------------------------
    # ASSEMBLAR CONFIG PARA O PIPELINE
    # ---------------------------------------------------------
    config = {
        "data": {
            "registry_base": registry_base,
            "processed_path": processed_path,
            "error_path": error_path,
            "autosage_registry_base": autosage_registry_base
        },
        "reports": {
            "output_path": reports_path
        }
    }

    return config
