from typing import Optional

from src.app.domain.dataset_run import DatasetRun
from src.app.connectors.connector_postgres import ConnectorPostgres
from src.app.domain.dataset_summary import DatasetSummary
from src.app.domain.pipeline_execution import PipelineExecution
from src.app.domain.pipeline_stage import PipelineStage
from src.app.tools.log_factory import get_dcp_logger
from src.app.domain.dataset_run_history import DatasetRunHistory
from src.app.domain.pipeline_timeline import PipelineTimeline, PipelineTimelineStage
from src.app.domain.platform_health import PlatformHealth, PlatformServiceHealth
import requests
from src.app.config.platform_services import PLATFORM_SERVICES


class DatasetRunRepository:

    def __init__(self, trace_id: str):

        self.trace_id = trace_id
        self.connector = ConnectorPostgres(trace_id)

        self.logger = get_dcp_logger(
            trace_id=trace_id,
            classe="eda_prepare_pipeline"
        )


    def get_latest_run(self, dataset_name: str) -> Optional[DatasetRun]:

        self.logger.info(
            f"[MNT][{self.trace_id}] stage=get action=get_latest_run"
         )

        conn = self.connector.get_conn()
        cursor = conn.cursor()

        query = """
        SELECT
            pm.dataset_name,
            pm.pipeline_version,
            pm.duration_ms,
            dcp.rows_count,
            dcp.columns_count,
            ml.model_name,
            ml.metric_name,
            ml.metric_value
        FROM pipeline_metrics pm

        LEFT JOIN dcp_monitor_event dcp
            ON pm.trace_id = dcp.trace_id

        LEFT JOIN ml_experiment_result ml
            ON pm.trace_id = ml.trace_id

        WHERE pm.dataset_name = %s
        ORDER BY pm.created_at DESC
        LIMIT 1
        """

        cursor.execute(query, (dataset_name,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row is None:
            return None

        return DatasetRun(
            dataset_name=row[0],
            pipeline_version=row[1],
            rows_count=row[3],
            columns_count=row[4],
            model_name=row[5],
            metric_name=row[6],
            metric_value=row[7],
            duration_ms=row[2]
        )


    def list_datasets(self) -> list[DatasetSummary]:

        self.logger.info(
            f"[MNT][{self.trace_id}] stage=get action=list_datasets"
        )

        conn = self.connector.get_conn()
        cursor = conn.cursor()

        query = """
        SELECT
            pm.dataset_name,
            MAX(pm.pipeline_version) as last_pipeline_version,
            MAX(pm.created_at) as last_run_timestamp,
            MAX(ml.metric_value) as last_metric_value,
            MAX(ml.model_name) as last_model
        FROM pipeline_metrics pm
        LEFT JOIN ml_experiment_result ml
            ON pm.dataset_name = ml.dataset_name
            AND pm.pipeline_version = ml.pipeline_version
        GROUP BY pm.dataset_name
        ORDER BY last_run_timestamp DESC
        """

        cursor.execute(query)

        rows = cursor.fetchall()

        result = []

        for row in rows:

            result.append(
                DatasetSummary(
                    dataset_name=row[0],
                    last_pipeline_version=row[1],
                    last_run_timestamp=str(row[2]),
                    last_metric_value=row[3],
                    last_model=row[4],
                )
            )

        cursor.close()
        conn.close()

        return result


    def get_pipeline_execution(self, dataset_name: str) -> PipelineExecution:

        self.logger.info(
            f"[MNT][{self.trace_id}] stage=get action=get_pipeline_execution"
        )

        conn = self.connector.get_conn()
        cursor = conn.cursor()

        query = """
        SELECT MAX(pipeline_version)
        FROM pipeline_metrics
        WHERE dataset_name = %s
        """

        cursor.execute(query, (dataset_name,))
        pipeline_version = cursor.fetchone()[0]

        stages = []

        # DCP
        cursor.execute(
            """
            SELECT created_at
            FROM dcp_monitor_event
            WHERE dataset_name = %s
            AND pipeline_version = %s
            """,
            (dataset_name, pipeline_version),
        )
        row = cursor.fetchone()

        if row:
            stages.append(
                PipelineStage(
                    stage_name="DCP",
                    status="completed",
                    created_at=str(row[0]),
                    duration_ms=None,
                )
            )
        # EDA Explore
        cursor.execute(
            """
            SELECT created_at
            FROM eda_explore_snapshot
            WHERE dataset_name = %s
            AND pipeline_version = %s
            """,
            (dataset_name, pipeline_version),
        )

        row = cursor.fetchone()

        if row:
            stages.append(
                PipelineStage(
                    stage_name="EDA Explore",
                    status="completed",
                    created_at=str(row[0]),
                    duration_ms=None,
                )
            )

        # EDA Prepare
        cursor.execute(
            """
            SELECT created_at
            FROM eda_prepare_snapshots
            WHERE dataset_name = %s
            AND pipeline_version = %s
            """,
            (dataset_name, pipeline_version),
        )

        row = cursor.fetchone()

        if row:
            stages.append(
                PipelineStage(
                    stage_name="EDA Prepare",
                    status="completed",
                    created_at=str(row[0]),
                    duration_ms=None,
                )
            )

        # ML
        cursor.execute(
            """
            SELECT created_at
            FROM ml_experiment_result
            WHERE dataset_name = %s
            AND pipeline_version = %s
            """,
            (dataset_name, pipeline_version),
        )

        row = cursor.fetchone()

        if row:
            stages.append(
                PipelineStage(
                    stage_name="ML",
                    status="completed",
                    created_at=str(row[0]),
                    duration_ms=None,
                )
            )

        cursor.close()
        conn.close()

        return PipelineExecution(
            dataset_name=dataset_name,
            pipeline_version=pipeline_version,
            stages=stages,
        )

    def get_runs(self, dataset_name: str):

        conn = self.connector.get_conn()
        cursor = conn.cursor()

        query = """
        SELECT
            pm.pipeline_version,
            ml.model_name,
            ml.metric_name,
            ml.metric_value,
            pm.duration_ms
        FROM pipeline_metrics pm

        LEFT JOIN ml_experiment_result ml
            ON pm.trace_id = ml.trace_id

        WHERE pm.dataset_name = %s
        ORDER BY pm.pipeline_version DESC
        LIMIT 20
        """

        cursor.execute(query, (dataset_name,))
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        results = []

        for row in rows:
            results.append(
                DatasetRunHistory(
                    pipeline_version=row[0],
                    model_name=row[1],
                    metric_name=row[2],
                    metric_value=row[3],
                    duration_ms=row[4]
                )
            )

        return results


    def get_pipeline_timeline(self, dataset_name: str):

        conn = self.connector.get_conn()
        cursor = conn.cursor()

        query = """
        SELECT pipeline_version, duration_ms
        FROM pipeline_metrics
        WHERE dataset_name = %s
        ORDER BY pipeline_version DESC
        LIMIT 1
        """

        cursor.execute(query, (dataset_name,))
        row = cursor.fetchone()

        if not row:
            return None

        pipeline_version = row[0]
        total_duration = row[1]

        stages = []

        # DCP
        cursor.execute(
            """
            SELECT 1
            FROM dcp_monitor_event
            WHERE dataset_name = %s
            AND pipeline_version = %s
            LIMIT 1
            """,
            (dataset_name, pipeline_version),
        )

        if cursor.fetchone():
            stages.append(
                PipelineTimelineStage(
                    stage_name="DCP",
                    duration_ms=None
                )
            )

        # EDA Explore
        cursor.execute(
            """
            SELECT 1
            FROM eda_explore_snapshot
            WHERE dataset_name = %s
            AND pipeline_version = %s
            LIMIT 1
            """,
            (dataset_name, pipeline_version),
        )

        if cursor.fetchone():
            stages.append(
                PipelineTimelineStage(
                    stage_name="EDA Explore",
                    duration_ms=None
                )
            )

        # EDA Prepare
        cursor.execute(
            """
            SELECT 1
            FROM eda_prepare_snapshots
            WHERE dataset_name = %s
            AND pipeline_version = %s
            LIMIT 1
            """,
            (dataset_name, pipeline_version),
        )

        if cursor.fetchone():
            stages.append(
                PipelineTimelineStage(
                    stage_name="EDA Prepare",
                    duration_ms=None
                )
            )

        # ML
        cursor.execute(
            """
            SELECT 1
            FROM ml_experiment_result
            WHERE dataset_name = %s
            AND pipeline_version = %s
            LIMIT 1
            """,
            (dataset_name, pipeline_version),
        )

        if cursor.fetchone():
            stages.append(
                PipelineTimelineStage(
                    stage_name="ML",
                    duration_ms=None
                )
            )

        cursor.close()
        conn.close()

        return PipelineTimeline(
            dataset_name=dataset_name,
            pipeline_version=pipeline_version,
            total_duration_ms=total_duration,
            stages=stages
        )


    def get_platform_health(self):

        self.logger.info(
            f"[MNT][{self.trace_id}] stage=get action=check_services"
        )

        services = []

        for service, url in PLATFORM_SERVICES.items():

            try:
                self.logger.info(
                    f"[MNT][{url}] stage=get action=get_platform_health"
                )

                response = requests.get(f"{url}/health", timeout=2)
                if response.status_code == 200:
                    status = "healthy"
                else:
                    status = "unhealthy"

            except Exception:
                status = "unhealthy"

            services.append({
                "service_name": service,
                "status": status
            })

        return {
            "services": services
        }
