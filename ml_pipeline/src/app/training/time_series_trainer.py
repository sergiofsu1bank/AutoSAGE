# -*- coding: utf-8 -*-

from typing import Dict, Any, List
import numpy as np
import pandas as pd
import statsmodels.api as sm

from src.app.training.training_report import TrainingReport


class TimeSeriesTrainer:
    """
    Executor de treino para séries temporais.

    Responsabilidades:
    - Treinar modelos estatísticos
    - Executar walk-forward evaluation
    - Avaliar métricas temporais
    """

    # --------------------------------------------------
    # API pública
    # --------------------------------------------------
    def train(
        self,
        *,
        model_type: str,
        series: pd.Series,
        order: tuple | None = None,
        seasonal_order: tuple | None = None,
        metric_fn,
        horizon: int = 1,
    ):
        if model_type == "naive":
            return self._naive_forecast(series, metric_fn, horizon)

        if model_type == "arima":
            return self._arima(series, order, metric_fn, horizon)

        if model_type == "sarima":
            return self._sarima(
                series,
                order,
                seasonal_order,
                metric_fn,
                horizon,
            )

        raise ValueError(f"Modelo temporal não suportado: {model_type}")

    # --------------------------------------------------
    # Naive Forecast (baseline)
    # --------------------------------------------------
    def _naive_forecast(
        self,
        series: pd.Series,
        metric_fn,
        horizon: int,
    ):
        preds = series.shift(1).dropna()
        actuals = series.iloc[1:]

        score = metric_fn(actuals, preds)

        report = TrainingReport(
            model_name="naive_forecast",
            score=score,
            params={},
        )

        return report, None

    # --------------------------------------------------
    # ARIMA
    # --------------------------------------------------
    def _arima(
        self,
        series: pd.Series,
        order: tuple,
        metric_fn,
        horizon: int,
    ):
        preds, actuals = self._walk_forward(
            series,
            lambda train: sm.tsa.ARIMA(train, order=order).fit(),
            horizon,
        )

        score = metric_fn(actuals, preds)

        report = TrainingReport(
            model_name="arima",
            score=score,
            params={"order": order},
        )

        return report, None

    # --------------------------------------------------
    # SARIMA
    # --------------------------------------------------
    def _sarima(
        self,
        series: pd.Series,
        order: tuple,
        seasonal_order: tuple,
        metric_fn,
        horizon: int,
    ):
        preds, actuals = self._walk_forward(
            series,
            lambda train: sm.tsa.SARIMAX(
                train,
                order=order,
                seasonal_order=seasonal_order,
            ).fit(disp=False),
            horizon,
        )

        score = metric_fn(actuals, preds)

        report = TrainingReport(
            model_name="sarima",
            score=score,
            params={
                "order": order,
                "seasonal_order": seasonal_order,
            },
        )

        return report, None

    # --------------------------------------------------
    # Walk-forward
    # --------------------------------------------------
    def _walk_forward(
        self,
        series: pd.Series,
        fit_fn,
        horizon: int,
    ):
        preds = []
        actuals = []

        for i in range(len(series) - horizon):
            train = series.iloc[: i + 1]
            test = series.iloc[i + horizon]

            model = fit_fn(train)
            forecast = model.forecast(horizon)[-1]

            preds.append(forecast)
            actuals.append(test)

        return np.array(preds), np.array(actuals)
