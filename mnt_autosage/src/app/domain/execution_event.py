from datetime import datetime


class ExecutionEvent:

    def __init__(
        self,
        trace_id: str,
        event_type: str,
        component: str,
        message: str,
        created_at: datetime
    ):
        self.trace_id = trace_id
        self.event_type = event_type
        self.component = component
        self.message = message
        self.created_at = created_at
