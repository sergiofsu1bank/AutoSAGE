# -*- coding: utf-8 -*-

from typing import Dict, Any
from dataclasses import asdict
from datetime import datetime

from src.app.tools.log_factory import get_dcp_logger
from src.app.loaders.ml_artifact_loader import MLArtifactLoader
from src.app.loaders.dcp_dataset_loader import DCPDatasetLoader
from src.app.experiment.experiment_tracker import ExperimentTracker
from src.app.features.feature_schema_applier import FeatureSchemaApplier
from src.app.features.feature_builder import FeatureBuilder
from src.app.training.model_selector import ModelSelector
from src.app.training.training_runner import TrainingRunner
from src.app.split.ml_dataset_splitter import MLDatasetSplitter

from src.app.strategies.model_policy_resolver import ModelPolicyResolver
from src.app.strategies.classification_strategy import ClassificationStrategy
from src.app.strategies.regression_strategy import RegressionStrategy
from src.app.strategies.time_series_strategy import TimeSeriesStrategy

from src.app.validation.dataset_validator import DatasetValidator
from src.app.validation.schema_validator import SchemaValidator
from src.app.validation.target_validator import TargetValidator
from src.app.validation.leakage_validator import LeakageValidator

from src.app.training.model_evaluator import ModelEvaluator

from src.api.schemas.metrics_context import MetricsContext, MLExperimentMetrics
from src.api.metrics.monitor_client import MetricsClient


class MLPipeline:
    """
    Pipeline canônico de ML do AutoSAGE.

    Responsabilidades:
    - Orquestrar o fluxo completo de ML
    - Respeitar rigorosamente os contratos do EDA Prepare
    - Executar validações científicas no ponto correto
    - NÃO conter lógica científica (somente coordenação)

    Princípios-chave:
    - Dataset físico (DCP) é validado contra o schema físico
    - Dataset transformado (EDA → ML) é validado contra contratos lógicos
    - Cada validator atua exclusivamente no seu nível semântico

        ### Decisão Final do ML

        O AutoSAGE ML possui um critério explícito de término do processo de Machine Learning.

        - **APPROVED**
        O modelo apresenta sinal estatístico acima do limiar mínimo definido e é considerado existente.

        - **TERMINATED**
        O processo de ML é encerrado de forma definitiva quando:
        - a métrica é inválida ou ausente, ou
        - o sinal estatístico é indistinguível do acaso (ex: ROC AUC abaixo do limiar mínimo).

        Nesse caso, **não há re-tentativa automática**, **não há tuning infinito** e **não há overfitting forçado**.
        O encerramento indica que, com os dados atuais e o target informado pelo usuário, **não existe modelo útil**.
        """

    def __init__(
        self,
        *,
        trace_id: str,
        pipeline: str,
        pipeline_version: int,
        vendor: str,
        dataset_name: str,
        parquet_artifact_path: str,
        eda_prepare_registry_path: str,
        target_name: str
    ):
        self.trace_id = trace_id
        self.pipeline = pipeline
        self.pipeline_version = pipeline_version
        self.vendor = vendor
        self.dataset_name = dataset_name
        self.parquet_artifact_path = parquet_artifact_path
        self.eda_prepare_registry_path = eda_prepare_registry_path
        self.target_name = target_name

        self.logger = get_dcp_logger(
            trace_id=self.trace_id,
            classe=self.__class__.__name__,
        )

    async def run(self) -> Dict[str, Any]:
        """
        Executa o pipeline de ML de ponta a ponta.

        Fluxo de alto nível:
        1. Carregar artefatos do EDA Prepare
        2. Resolver governança (strategy, split)
        3. Carregar dataset físico (DCP)
        4. Validar dataset físico contra schema físico
        5. Aplicar contrato EDA → ML (FeatureSchemaApplier)
        6. Validar dataset lógico (features / target / leakage)
        7. Split
        8. Seleção de modelos
        9. Treino
        """
        metrics_client = MetricsClient(self.trace_id)
        started_at = datetime.utcnow()
        try:
            # ----------------------------
            # Métricas START
            # ----------------------------
            timing = metrics_client.build_timing(started_at)
            await metrics_client.pipeline_event(
                    MetricsContext(
                        trace_id=self.trace_id,
                        pipeline=self.pipeline,
                        pipeline_version=self.pipeline_version,
                        vendor=self.vendor,
                        dataset_name=self.dataset_name,
                        stage="pipeline",
                        status="STARTED",
                        started_at=timing["started_at"],
                        finished_at=timing["finished_at"],
                        duration_ms=timing["duration_ms"],
                        metadata=None
                    )
                )

            self.logger.info(
                "[MLPipeline] run() iniciado | "
                f"trace_id={self.trace_id} | "
                f"pipeline={self.pipeline} | "
                f"vendor={self.vendor} | "
                f"dataset_name={self.dataset_name} | "
                f"parquet_artifact_path={self.parquet_artifact_path} | "
                f"eda_prepare_registry_path={self.eda_prepare_registry_path} | "
                f"target_name={self.target_name}"
                )

            # --------------------------------------------------
            # 1. Load artefatos do EDA Prepare
            # --------------------------------------------------
            artifacts = await MLArtifactLoader(
                eda_prepare_registry_path=self.eda_prepare_registry_path,
                trace_id=self.trace_id,
            ).load()

            train_config = artifacts.get("train_config")
            feature_schema = artifacts.get("feature_schema")
            transformations = artifacts.get("transformations")
            physical_schema = artifacts.get("physical_schema")

            if not train_config:
                raise RuntimeError("EDA Prepare inválido: train_config ausente")

            if not feature_schema:
                raise RuntimeError("EDA Prepare inválido: feature_schema ausente")

            if not transformations:
                raise RuntimeError("EDA Prepare inválido: transformations ausente")

            if not physical_schema:
                raise RuntimeError("EDA Prepare inválido: physical_schema ausente")

            self.logger.info(
                "[MLPipeline] EDA Prepare carregado | "
                f"problem_type={train_config.get('problem_type')} | "
                f"metric={train_config.get('metric')}"
            )

            # --------------------------------------------------
            # 2. Extrair split_strategy (DECISÃO DO EDA)
            # --------------------------------------------------
            split_value = None
            for t in transformations:
                if t.get("decision") == "split_strategy":
                    split_value = t.get("value")

            if not split_value:
                raise RuntimeError("split_strategy não encontrado no EDA Prepare")

            # --------------------------------------------------
            # 3. Resolver Strategy (GOVERNANÇA)
            # --------------------------------------------------
            problem_type = train_config.get("problem_type")

            if problem_type == "classification":
                strategy = ClassificationStrategy()
            elif problem_type == "regression":
                strategy = RegressionStrategy()
            elif problem_type == "time_series":
                strategy = TimeSeriesStrategy()
            else:
                raise RuntimeError(f"problem_type não suportado: {problem_type}")

            allowed_splits = strategy.split_policy().get("allowed", [])
            if split_value not in allowed_splits:
                raise RuntimeError(
                    f"split_strategy '{split_value}' não permitido pela strategy {strategy.name()}"
                )

            # --------------------------------------------------
            # 4. Traduzir split_strategy para execução (TÉCNICO)
            # --------------------------------------------------
            if split_value == "random":
                split_strategy = {"type": "holdout", "test_size": 0.2}
            elif split_value == "stratified":
                split_strategy = {"type": "stratified_holdout", "test_size": 0.2}
            elif split_value == "temporal":
                split_strategy = {"type": "temporal"}
            else:
                raise RuntimeError(f"split_strategy não suportado: {split_value}")

            # --------------------------------------------------
            # 5. Load dataset físico (DCP)
            # --------------------------------------------------
            self.logger.info(
                "[MLPipeline] carregando dataset do DCP | "
                f"path={self.parquet_artifact_path}"
            )

            df = await DCPDatasetLoader(
                artifact_path=self.parquet_artifact_path,
                trace_id=self.trace_id,
            ).load()

            if df.empty:
                raise RuntimeError("Dataset do DCP está vazio")

            # --------------------------------------------------
            # 6. Validação do dataset físico (OBRIGATÓRIA)
            # --------------------------------------------------
            # IMPORTANTE:
            # - Aqui validamos o dataset BRUTO
            # - Antes de qualquer transformação
            # - Usando exclusivamente o physical_schema
            DatasetValidator(
                df=df,
                trace_id=self.trace_id,
            ).validate()

            SchemaValidator(
                df=df,
                schema=physical_schema,
                trace_id=self.trace_id,
            ).validate()

            # --------------------------------------------------
            # 7. Aplicar contrato EDA → ML (dataset lógico)
            # --------------------------------------------------
            # df_prepared:
            # - NÃO é dataset físico
            # - Já passou por seleção, encoding, alinhamento de features
            # - Não deve ser validado contra schema físico
            df_prepared = FeatureSchemaApplier(
                feature_schema=feature_schema,
                target_name=self.target_name,
                trace_id=self.trace_id,
            ).apply(df)

            if df_prepared.empty:
                raise RuntimeError("Dataset vazio após FeatureSchemaApplier")

            # --------------------------------------------------
            # 8. Feature building (X, y)
            # --------------------------------------------------
            X, y = FeatureBuilder(
                target_name=self.target_name,
                trace_id=self.trace_id,
            ).build(df_prepared)

            try:
                X = X.astype(float)
            except Exception as exc:
                raise RuntimeError(
                    "X contém colunas não numéricas após FeatureBuilder"
                ) from exc

            # --------------------------------------------------
            # 9. Validações científicas no nível lógico
            # --------------------------------------------------
            # Aqui validamos apenas coerência científica,
            # nunca estrutura física
            TargetValidator(
                df=df_prepared,
                target_name=self.target_name,
                problem_type=problem_type,
                trace_id=self.trace_id,
            ).validate()

            LeakageValidator(
                warnings=artifacts.get("warnings", []),
                trace_id=self.trace_id,
            ).validate()

            # --------------------------------------------------
            # 10. Split do dataset
            # --------------------------------------------------
            splitter = MLDatasetSplitter(
                strategy=split_strategy,
                random_seed=train_config.get("random_seed", 42),
                trace_id=self.trace_id,
            )

            X_train, X_test, y_train, y_test = splitter.split(X=X, y=y)

            # --------------------------------------------------
            # 11. Seleção de modelos (governada por Strategy)
            # --------------------------------------------------
            model_candidates = ModelSelector(
                strategy=strategy,
                resolver=ModelPolicyResolver(),
                random_seed=train_config.get("random_seed"),
                trace_id=self.trace_id,
            ).select()

            # --------------------------------------------------
            # 12. Experiment ID determinístico
            # --------------------------------------------------
            experiment_id = ExperimentTracker(
                dataset_name=self.dataset_name,
                pipeline_version=self.pipeline_version,
                problem_type=problem_type,
                strategy_name=strategy.name(),
                train_config=train_config,
                trace_id=self.trace_id,
            ).experiment_id()

            self.logger.info(
                f"[MLPipeline] experiment_id gerado | id={experiment_id}"
            )

            # --------------------------------------------------
            # 13. Treino (somente treino)
            # --------------------------------------------------
            metric_name = train_config.get("metric")
            if not metric_name:
                raise RuntimeError("metric ausente em train_config")

            best_model, best_report = TrainingRunner(
                problem_type=problem_type,
                random_seed=train_config.get("random_seed"),
                trace_id=self.trace_id,
                metric_name=metric_name,
            ).run(
                X=X_train,
                y=y_train,
                trainers=model_candidates,
            )

            # --------------------------------------------------
            # 14. Decisão de status do experimento
            # --------------------------------------------------
            # Regra objetiva:
            # - SUCCESS  → métrica válida
            # - REJECTED → treino ocorreu, mas métrica não é comparável / ausente
            evaluator = ModelEvaluator(problem_type=problem_type)
            evaluation = evaluator.evaluate(best_report)

            self.logger.info(
                "[MLPipeline] avaliação final | "
                f"decision={evaluation.decision} | "
                f"reason={evaluation.reason} | "
                f"{evaluation.metric_name}={evaluation.metric_value}"
            )

            # ----------------------------
            # ML STATISTICS
            # ----------------------------
            timing = metrics_client.build_timing(started_at)
            await metrics_client.ml_statistics(
                MLExperimentMetrics(
                    trace_id=self.trace_id,
                    pipeline=self.pipeline,
                    pipeline_version=self.pipeline_version,
                    vendor=self.vendor,
                    dataset_name=self.dataset_name,

                    experiment_id=experiment_id,
                    problem_type=problem_type,
                    strategy_name=strategy.name(),

                    metric_name=evaluation.metric_name,
                    metric_value=evaluation.metric_value,
                    decision=evaluation.decision,
                    reason=evaluation.reason,

                    model_name=(
                        best_report.model_name
                        if evaluation.decision == "APPROVED"
                        else None
                    ),
                    training_report=best_report.to_dict(),
                    created_at=timing["started_at"]
                )
            )

            # ----------------------------
            # Métricas SUCCESS
            # ----------------------------
            timing = metrics_client.build_timing(started_at)
            await metrics_client.pipeline_event(
                    MetricsContext(
                        trace_id=self.trace_id,
                        pipeline=self.pipeline,
                        pipeline_version=self.pipeline_version,
                        vendor=self.vendor,
                        dataset_name=self.dataset_name,
                        stage="pipeline",
                        status="SUCCESS",
                        started_at=timing["started_at"],
                        finished_at=timing["finished_at"],
                        duration_ms=timing["duration_ms"],
                        metadata=None
                    )
                )

            # --------------------------------------------------
            # 15. Retorno governado do pipeline
            # --------------------------------------------------
            return {
                "experiment_id": experiment_id,
                "decision": evaluation.decision,
                "reason": evaluation.reason,
                "metric_name": evaluation.metric_name,
                "metric_value": evaluation.metric_value,
                "training_report": best_report,
                "model_name": (
                    best_report.model_name
                    if evaluation.decision == "APPROVED"
                    else None
                ),
            }

        except Exception as exc:
            timing = metrics_client.build_timing(started_at)
            await metrics_client.pipeline_event(
                MetricsContext(
                    trace_id=self.trace_id,
                    pipeline=self.pipeline,
                    pipeline_version=self.pipeline_version,
                    vendor=self.vendor,
                    dataset_name=self.dataset_name,
                    stage="pipeline",
                    status="FAILED",
                    started_at=timing["started_at"],
                    finished_at=timing["finished_at"],
                    duration_ms=timing["duration_ms"],
                    metadata=None
                )
            )
            self.logger.error(
                f"[EDA-PREPARE][FAILED] trace_id={self.trace_id} | error={exc}"
            )
            raise
