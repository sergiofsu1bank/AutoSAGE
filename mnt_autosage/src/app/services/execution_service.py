from typing import List

from src.app.domain.execution import Execution
from src.app.repository.execution_repository import ExecutionRepository


class ExecutionService:

    def __init__(self):
        self.repository = ExecutionRepository()

    def list_executions(self) -> List[Execution]:

        executions = self.repository.list_executions()

        return executions
