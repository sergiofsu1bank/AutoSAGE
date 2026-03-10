from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import uuid4

from src.db.models import Agent


class AgentRepository:

    def __init__(self, db: Session,
                 trace_id: str):
        self.db = db
        self.trace_id = trace_id

    def create(
        self,
        name: str,
        role: str,
        model: str,
        temperature: float | None = None,
        max_tokens: int | None = None,
        use_rag: bool = False,
    ) -> Agent:

        agent = Agent(
            id=str(uuid4()),
            name=name,
            role=role,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            use_rag=use_rag,
        )

        self.db.add(agent)
        self.db.commit()
        self.db.refresh(agent)

        return agent

    def get_by_name(self, name: str) -> Agent | None:
        stmt = select(Agent).where(Agent.name == name)
        return self.db.execute(stmt).scalar_one_or_none()

    def list_all(self) -> list[Agent]:
        stmt = select(Agent)
        return self.db.execute(stmt).scalars().all()
