from datetime import datetime
from typing import Optional


class Execution:

    def __init__(
        self,
        trace_id: str,
        pipeline_name: str,
        status: str,
        started_at: datetime,
        finished_at: Optional[datetime] = None
    ):
        self.trace_id = trace_id
        self.pipeline_name = pipeline_name
        self.status = status
        self.started_at = started_at
        self.finished_at = finished_at
