from typing import Optional

from src.app.domain.dataset_run import DatasetRun
from src.app.repository.dataset_run_repository import DatasetRunRepository
from src.app.tools.log_factory import get_dcp_logger


class DatasetRunService:

    def __init__(self, trace_id: str):
        self.repository = DatasetRunRepository(trace_id)
        self.trace_id = trace_id

        self.logger = get_dcp_logger(
            trace_id=trace_id,
            classe="DatasetRunService"
        )


    def get_latest_run(self, dataset_name: str) -> Optional[DatasetRun]:

        self.logger.info(
            f"[MNT][{self.trace_id}] stage=get action=get_latest_run"
         )

        dataset_run = self.repository.get_latest_run(dataset_name.self.trace_id)
        return dataset_run

    def list_datasets(self):

        self.logger.info(
            f"[MNT][{self.trace_id}] stage=get action=list_datasets"
         )
        return self.repository.list_datasets()

    def get_pipeline_execution(self, dataset_name: str):

        return self.repository.get_pipeline_execution(dataset_name)


    def get_runs(self, dataset_name: str):

        self.logger.info(
            f"[MNT][{self.trace_id}] stage=get action=get_runs"
         )
        return self.repository.get_runs(dataset_name)

    def get_pipeline_timeline(self, dataset_name: str):

        self.logger.info(
            f"[MNT][{self.trace_id}] stage=get action=get_pipeline_timeline"
         )
        return self.repository.get_pipeline_timeline(dataset_name)

    def get_platform_health(self):

        self.logger.info(
            f"[MNT][{self.trace_id}] stage=get action=get_platform_health"
         )
        return self.repository.get_platform_health()
