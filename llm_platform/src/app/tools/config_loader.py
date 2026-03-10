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
    registry_base = os.getenv("LLM_PLATFORM_REGISTRY_BASE")
    if not registry_base:
        raise RuntimeError("LLM_PLATFORM_REGISTRY_BASE é obrigatório e não foi definido no ambiente.")

    # ---------------------------------------------------------
    # PATHS INTERNOS — todos com prefixo EDA_
    # ---------------------------------------------------------
    # ---------------------------------------------------------
    # ASSEMBLAR CONFIG PARA O PIPELINE
    # ---------------------------------------------------------
    config = {
        "data": {
            "registry_base": registry_base,
        }
    }

    return config
