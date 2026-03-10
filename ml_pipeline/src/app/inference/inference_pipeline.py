# -*- coding: utf-8 -*-

import pandas as pd


class InferencePipeline:
    """
    Pipeline de inferência em produção.
    """

    def __init__(self, bundle: dict):
        self.model = bundle["model"]
        self.feature_schema = bundle["feature_schema"]
        self.preprocessing_pipeline = bundle["preprocessing_pipeline"]
        self.target_name = bundle["target_name"]
        self.problem_type = bundle["problem_type"]

    def predict(self, df: pd.DataFrame):
        # --------------------------------------------------
        # 1. Aplicar pré-processamento
        # --------------------------------------------------
        if self.preprocessing_pipeline is not None:
            df = self.preprocessing_pipeline.transform(df)

        # --------------------------------------------------
        # 2. Garantir mesmas features
        # --------------------------------------------------
        X = df[self.feature_schema["features"]]

        # --------------------------------------------------
        # 3. Inferência
        # --------------------------------------------------
        if self.problem_type == "classification":
            preds = self.model.predict_proba(X)[:, 1]
        else:
            preds = self.model.predict(X)

        return preds
