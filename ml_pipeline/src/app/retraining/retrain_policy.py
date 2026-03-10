# -*- coding: utf-8 -*-

class RetrainPolicy:
    """
    Define regras de recomendação de retreino.
    """

    DRIFT_ALERT_THRESHOLD = 1
    METRIC_DROP_THRESHOLD = 0.10

    @classmethod
    def should_retrain(cls, *, alerts: list, metric_drop: float | None):
        reasons = []

        if alerts and len(alerts) >= cls.DRIFT_ALERT_THRESHOLD:
            reasons.append("drift_detected")

        if metric_drop is not None and metric_drop >= cls.METRIC_DROP_THRESHOLD:
            reasons.append("metric_degradation")

        return reasons
