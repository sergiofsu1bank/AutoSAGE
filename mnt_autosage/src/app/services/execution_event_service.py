from typing import List

from src.app.domain.execution_event import ExecutionEvent
from src.app.repository.execution_event_repository import ExecutionEventRepository


class ExecutionEventService:

    def __init__(self, trace_id: str):
        self.repository = ExecutionEventRepository()
        self.trace_id = trace_id

    def list_events(self) -> List[ExecutionEvent]:

        events = self.repository.list_events(self.trace_id)
        return events
