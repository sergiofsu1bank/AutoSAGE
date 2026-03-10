# -*- coding: utf-8 -*-

import time


class MLMetrics:
    """
    Coletor simples de métricas.
    """

    def __init__(self):
        self._start = None

    def start_timer(self):
        self._start = time.time()

    def stop_timer(self) -> float:
        return (time.time() - self._start) * 1000

    def record(self, name: str, value: float, labels: dict | None = None):
        # Placeholder para Prometheus / OpenTelemetry
        pass
