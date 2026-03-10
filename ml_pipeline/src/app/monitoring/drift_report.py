# -*- coding: utf-8 -*-

from datetime import datetime


class DriftReport:

    @staticmethod
    def build(
        *,
        model_metadata: dict,
        feature_drift: dict,
        prediction_drift: dict,
        alerts: list,
    ):
        return {
            "model": model_metadata,
            "checked_at": datetime.utcnow().isoformat(),
            "feature_drift": feature_drift,
            "prediction_drift": prediction_drift,
            "alerts": alerts,
        }
