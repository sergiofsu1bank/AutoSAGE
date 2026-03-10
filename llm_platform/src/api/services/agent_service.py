from src.db.session import SessionLocal
from src.db.agent_repository import AgentRepository
from src.db.models import Agent


class AgentService:
    """
    Service da camada API.
    Responsável por persistir e recuperar agentes via banco.
    """

    def create_agent(self, payload, trace_id: str):

        db = SessionLocal()
        repo = AgentRepository(db, trace_id)

        existing = repo.get_by_name(payload.name)
        if existing:
            db.close()
            return existing.id

        agent = repo.create(
            name=payload.name,
            role=payload.role,
            model=payload.model,
            temperature=payload.temperature,
            max_tokens=payload.max_tokens,
            use_rag=payload.use_rag,
        )

        db.close()

        return agent.id

    def get_agent(self, agent_id: str) -> Agent:
        db = SessionLocal()
        repo = AgentRepository(db)

        agent = repo.get_by_id(agent_id)

        db.close()

        return agent
