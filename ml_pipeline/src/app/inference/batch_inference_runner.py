# -*- coding: utf-8 -*-

import os
import pandas as pd
from datetime import datetime

from src.app.inference.model_bundle_loader import ModelBundleLoader
from src.app.inference.inference_pipeline import InferencePipeline


class BatchInferenceRunner:
    """
    Executor de inferência em batch.
    """

    def __init__(
        self,
        *,
        model_bundle_path: str,
        input_path: str,
        output_path: str,
    ):
        self.model_bundle_path = model_bundle_path
        self.input_path = input_path
        self.output_path = output_path

    def run(self) -> str:
        # --------------------------------------------------
        # 1. Load bundle
        # --------------------------------------------------
        bundle = ModelBundleLoader(
            self.model_bundle_path
        ).load()

        pipeline = InferencePipeline(bundle)

        # --------------------------------------------------
        # 2. Load input dataset
        # --------------------------------------------------
        df = self._load_input()

        if df.empty:
            raise RuntimeError("Dataset de entrada vazio")

        # --------------------------------------------------
        # 3. Predict
        # --------------------------------------------------
        predictions = pipeline.predict(df)

        # --------------------------------------------------
        # 4. Persist output
        # --------------------------------------------------
        result_df = df.copy()
        result_df["prediction"] = predictions

        output_file = self._write_output(result_df)

        return output_file

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------
    def _load_input(self) -> pd.DataFrame:
        if self.input_path.endswith(".parquet"):
            return pd.read_parquet(self.input_path)
        if self.input_path.endswith(".csv"):
            return pd.read_csv(self.input_path)

        raise RuntimeError(
            f"Formato não suportado: {self.input_path}"
        )

    def _write_output(self, df: pd.DataFrame) -> str:
        os.makedirs(self.output_path, exist_ok=True)

        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        out_file = os.path.join(
            self.output_path,
            f"predictions_{ts}.parquet",
        )

        df.to_parquet(out_file, index=False)
        return out_file
