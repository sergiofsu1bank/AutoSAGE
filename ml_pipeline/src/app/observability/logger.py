# -*- coding: utf-8 -*-

import json
import logging


class MLLogger:
    """
    Logger estruturado para ML.
    """

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

    def info(self, message: str, context: dict | None = None):
        payload = {"message": message}
        if context:
            payload["context"] = context
        self.logger.info(json.dumps(payload))

    def error(self, message: str, context: dict | None = None):
        payload = {"message": message}
        if context:
            payload["context"] = context
        self.logger.error(json.dumps(payload))
