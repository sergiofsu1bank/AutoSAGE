# -*- coding: utf-8 -*-

from src.app.retraining.retrain_context import RetrainContext
from src.app.retraining.retrain_policy import RetrainPolicy


class RetrainRecommender:
    """
    Gera recomendações de retreino.
    """

    @staticmethod
    def recommend(
        *,
        model_metadata: dict,
        alerts: list,
        metric_drop: float | None = None,
    ) -> dict | None:

        reasons = RetrainPolicy.should_retrain(
            alerts=alerts,
            metric_drop=metric_drop,
        )

        if not reasons:
            return None

        context = RetrainContext(
            model_metadata=model_metadata,
            reason=" | ".join(reasons),
        )

        return context.export()
