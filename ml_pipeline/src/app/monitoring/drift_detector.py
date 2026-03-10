# -*- coding: utf-8 -*-

import pandas as pd
from src.app.monitoring.drift_metrics import DriftMetrics


class DriftDetector:
    """
    Compara estatísticas de treino vs produção.
    """

    def __init__(self, training_stats: dict):
        self.training_stats = training_stats

    def detect_feature_drift(self, df: pd.DataFrame) -> dict:
        report = {}

        for col, stats in self.training_stats["features"].items():
            if col not in df.columns:
                continue

            prod_mean = df[col].mean()

            zshift = DriftMetrics.zscore_shift(
                train_mean=stats["mean"],
                train_std=stats["std"],
                prod_mean=prod_mean,
            )

            report[col] = {
                "train_mean": stats["mean"],
                "prod_mean": float(prod_mean),
                "zscore_shift": zshift,
            }

        return report

    def detect_prediction_drift(self, preds, baseline):
        return {
            "mean_shift": abs(preds.mean() - baseline["mean"]),
            "std_shift": abs(preds.std() - baseline["std"]),
        }
