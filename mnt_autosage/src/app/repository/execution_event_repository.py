from typing import List
from datetime import datetime

from src.app.domain.execution_event import ExecutionEvent


class ExecutionEventRepository:

    def list_events(self, trace_id: str) -> List[ExecutionEvent]:

        events = [
            ExecutionEvent(
                trace_id=trace_id,
                event_type="PIPELINE_STARTED",
                component="rag_pipeline",
                message="pipeline execution started",
                created_at=datetime.utcnow()
            ),
            ExecutionEvent(
                trace_id=trace_id,
                event_type="AGENT_STARTED",
                component="intent_classifier",
                message="intent classifier started",
                created_at=datetime.utcnow()
            ),
            ExecutionEvent(
                trace_id=trace_id,
                event_type="RAG_RETRIEVAL_STARTED",
                component="rag_retriever",
                message="retrieving documents",
                created_at=datetime.utcnow()
            ),
            ExecutionEvent(
                trace_id=trace_id,
                event_type="PIPELINE_FINISHED",
                component="rag_pipeline",
                message="pipeline execution finished",
                created_at=datetime.utcnow()
            )
        ]

        return events
