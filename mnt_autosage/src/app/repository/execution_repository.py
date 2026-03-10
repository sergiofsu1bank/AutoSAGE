from typing import List
from datetime import datetime

from src.app.domain.execution import Execution


class ExecutionRepository:

    def list_executions(self) -> List[Execution]:

        executions = [
            Execution(
                trace_id="trace_001",
                pipeline_name="rag_pipeline",
                status="RUNNING",
                started_at=datetime.utcnow(),
                finished_at=None
            ),
            Execution(
                trace_id="trace_002",
                pipeline_name="agent_sales",
                status="SUCCESS",
                started_at=datetime.utcnow(),
                finished_at=datetime.utcnow()
            )
        ]

        return executions
