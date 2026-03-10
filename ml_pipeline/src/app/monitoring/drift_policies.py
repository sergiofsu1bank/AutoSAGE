# -*- coding: utf-8 -*-

class DriftPolicies:

    FEATURE_ZSCORE_THRESHOLD = 3.0
    PREDICTION_MEAN_THRESHOLD = 0.15

    @classmethod
    def evaluate(cls, feature_report, prediction_report):
        alerts = []

        for col, metrics in feature_report.items():
            if metrics["zscore_shift"] > cls.FEATURE_ZSCORE_THRESHOLD:
                alerts.append(
                    f"Feature drift detected on '{col}'"
                )

        if prediction_report["mean_shift"] > cls.PREDICTION_MEAN_THRESHOLD:
            alerts.append("Prediction drift detected")

        return alerts
