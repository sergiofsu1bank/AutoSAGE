from datetime import datetime
from typing import Any, Dict, List
from uuid import uuid4

from pydantic import BaseModel, Field


class ExecutionContext(BaseModel):
    """
    Runtime execution state of a pipeline run.
    """

    # ==============================
    # Identidade da execução
    # ==============================

    trace_id: str = Field(default_factory=lambda: uuid4().hex)

    # ==============================
    # Estado temporal
    # ==============================

    started_at: datetime = Field(default_factory=datetime.utcnow)
    finished_at: datetime | None = None

    # ==============================
    # Input inicial
    # ==============================

    initial_input: Any

    # ==============================
    # Estado acumulado
    # ==============================

    outputs_by_node: Dict[str, Any] = Field(default_factory=dict)
    errors: List[str] = Field(default_factory=list)

    # ==============================
    # Helpers
    # ==============================

    def mark_finished(self) -> None:
        if self.finished_at is None:
            self.finished_at = datetime.utcnow()

    def add_error(self, error: str) -> None:
        self.errors.append(error)

    @property
    def is_finished(self) -> bool:
        return self.finished_at is not None

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0
