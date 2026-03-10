# -*- coding: utf-8 -*-

import joblib


class ModelBundleLoader:
    """
    Loader do artefato de produção (model_bundle.pkl).
    """

    REQUIRED_KEYS = {
        "model",
        "feature_schema",
        "preprocessing_pipeline",
        "target_name",
        "problem_type",
        "model_metadata",
    }

    def __init__(self, bundle_path: str):
        self.bundle_path = bundle_path
        self.bundle = None

    def load(self) -> dict:
        self.bundle = joblib.load(self.bundle_path)
        self._validate()
        return self.bundle

    def _validate(self):
        missing = self.REQUIRED_KEYS - self.bundle.keys()
        if missing:
            raise RuntimeError(
                f"Bundle inválido, chaves ausentes: {missing}"
            )
