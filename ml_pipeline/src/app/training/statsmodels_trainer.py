# -*- coding: utf-8 -*-

import pandas as pd
import statsmodels.api as sm

from src.app.training.training_report import TrainingReport


class StatsModelsTrainer:
    """
    Trainer estatístico simples (statsmodels).

    Neste estágio:
    - Sem validação
    - Sem metric_fn externo
    - Um modelo padrão por problem_type
    - Inferência completa
    """

    def train(
        self,
        *,
        problem_type: str,
        X_train: pd.DataFrame,
        y_train: pd.Series,
    ):
        if problem_type == "regression":
            return self._ols(X_train, y_train)

        if problem_type in {"classification", "logistic"}:
            return self._logit(X_train, y_train)

        if problem_type == "count_model":
            return self._poisson(X_train, y_train)

        raise ValueError(
            f"StatsModelsTrainer não suporta problem_type={problem_type}"
        )

    # --------------------------------------------------
    # Modelos
    # --------------------------------------------------
    def _ols(self, X, y):
        X_c = sm.add_constant(X)
        model = sm.OLS(y, X_c).fit()

        score = float(model.rsquared)

        report = TrainingReport(
            model_name="ols",
            score=score,
            params={},
            inference=self._extract_inference(model),
        )

        return report, model

    def _logit(self, X, y):
        X_c = sm.add_constant(X)
        model = sm.Logit(y, X_c).fit(disp=False)

        score = float(model.llf)  # log-likelihood como score interno

        report = TrainingReport(
            model_name="logit",
            score=score,
            params={},
            inference=self._extract_inference(model),
        )

        return report, model

    def _poisson(self, X, y):
        X_c = sm.add_constant(X)
        model = sm.Poisson(y, X_c).fit(disp=False)

        score = float(model.llf)

        report = TrainingReport(
            model_name="poisson",
            score=score,
            params={},
            inference=self._extract_inference(model),
        )

        return report, model

    # --------------------------------------------------
    # Inferência
    # --------------------------------------------------
    def _extract_inference(self, model):
        return {
            "coefficients": model.params.to_dict(),
            "p_values": model.pvalues.to_dict(),
            "conf_int": model.conf_int().to_dict(),
            "summary": str(model.summary()),
        }
