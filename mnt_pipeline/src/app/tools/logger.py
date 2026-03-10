# -*- coding: utf-8 -*-

import logging
import os


class Logger:
    _loggers = {}

    def __init__(
        self,
        log_path: str,
        trace_id: str,
        classe: str,
        level: str = "INFO",
    ):
        self.module = "MNT-AUTOSAGE"

        if not trace_id:
            raise ValueError("trace_id é obrigatório para inicializar o Logger")
        self.trace_id = trace_id

        if not classe:
            raise ValueError("classe é obrigatório para inicializar o Logger")
        self.classe = classe

        # Garante diretório do log
        log_dir = os.path.dirname(log_path)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)

        key = f"{trace_id}:{self.module}:{classe}"

        if key not in Logger._loggers:
            logger = logging.getLogger(key)
            logger.setLevel(level.upper())
            logger.propagate = False

            formatter = logging.Formatter(
                "[%(asctime)s] [%(levelname)s] "
                "[trace_id=%(trace_id)s] "
                "[component=%(module)s] "
                "[classe=%(classe)s] "
                "%(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            # File handler
            fh = logging.FileHandler(log_path)
            fh.setFormatter(formatter)

            # Console handler
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)

            logger.addHandler(fh)
            logger.addHandler(ch)

            Logger._loggers[key] = logger

        self._logger = Logger._loggers[key]

    # ------------------------------
    # Métodos públicos
    # ------------------------------
    def _log(self, level: str, message: str):
        getattr(self._logger, level)(
            message,
            extra={
                "trace_id": self.trace_id,
                "component": self.module,
                "classe": self.classe,
            },
        )

    def info(self, message: str):
        self._log("info", message)

    def warning(self, message: str):
        self._log("warning", message)

    def error(self, message: str):
        self._log("error", message)

    def debug(self, message: str):
        self._log("debug", message)

    def critical(self, message: str):
        self._log("critical", message)
