# -*- coding: utf-8 -*-

from typing import Dict, Any


class MLDecisionResponseAdapter:
    """
    Traduz decisão científica do pipeline para resposta de API.
    """

    _USER_MESSAGES = {
        "weak_signal_close_to_random": {
            "title": "Modelo rejeitado",
            "message": (
                "Os dados não apresentam sinal estatístico suficiente "
                "para aprender o target informado."
            ),
            "suggestion": (
                "Revise features, target ou granularidade dos dados."
            ),
        }
    }

    @classmethod
    def adapt(cls, pipeline_result: Dict[str, Any]) -> Dict[str, Any]:
        decision = pipeline_result["decision"]
        reason = pipeline_result.get("reason")

        diagnostics = None
        if reason:
            diagnostics = {
                "reason": reason,
                "metric_name": pipeline_result.get("metric_name"),
                "metric_value": pipeline_result.get("metric_value"),
                "user_message": cls._USER_MESSAGES.get(reason),
            }

        return {
            "experiment_id": pipeline_result["experiment_id"],
            "status": decision,
            "model": (
                {"name": pipeline_result["model_name"]}
                if decision == "APPROVED"
                else None
            ),
            "registry": None,
            "diagnostics": diagnostics,
        }
