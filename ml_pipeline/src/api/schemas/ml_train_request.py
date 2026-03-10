# -*- coding: utf-8 -*-

from pydantic import BaseModel, Field


class MLTrainRequest(BaseModel):
    pipeline: str = Field(
        ...,
        example={"pipeline": "ml"}
    )

    pipeline_version: int = Field(
        ...,
        example={"pipeline_version": 1}
    )

    vendor: str = Field(
        ...,
        example={"vendor": "postgres"}
    )

    dataset_name: str = Field(
        ...,
        example={"dataset_name": "customer_churn"}
    )

    parquet_artifact_path: str = Field(
        ...,
        example={
            "parquet_artifact_path": "\\dcp\\customer_churn\\customer_churn_v0062.parquet"
        }
    )

    eda_prepare_registry_path: str = Field(
        ...,
        example={
            "eda_prepare_registry_path": "\\edapre\\processed\\customer_churn\\customer_churn_v0062"
        }
    )

    target_name: str = Field(
        ...,
        example={"target_name": "churn"}
    )
