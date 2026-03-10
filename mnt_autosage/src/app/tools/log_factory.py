# -*- coding: utf-8 -*-

import os
from src.app.tools.logger import Logger


def get_dcp_logger(
    trace_id: str,
    classe: str,
    level: str = "INFO"
) -> Logger:
    """
    Factory para Logger do DCP.
    A classe chamadora injeta contexto:
    - module
    - stage
    - classe
    """

    registry_base = os.getenv("MNT_REGISTRY_BASE")
    if not registry_base:
        raise RuntimeError("MNT_REGISTRY_BASE não definido no ambiente")

    log_path = os.path.join(registry_base, "logs", "autosage-mnt.log")

    return Logger(
        log_path=log_path,
        trace_id=trace_id,
        level=level,
        classe=classe,
    )
