from enum import Enum
from typing import Dict

from src.db.agent_repository import AgentRepository
from src.db.session import SessionLocal
from src.app.agents.contracts import AgentDefinition


# ==================================================
# Exceptions
# ==================================================

class AgentRegistryError(Exception):
    """Base exception for AgentRegistry."""
    pass


class AgentAlreadyExistsError(AgentRegistryError):
    """Raised when trying to register an agent that already exists."""
    pass


class AgentNotFoundError(AgentRegistryError):
    """Raised when an agent is not found in the registry."""
    pass


class AgentNotActiveError(AgentRegistryError):
    """Raised when an agent exists but is not active."""
    pass


# ==================================================
# Agent Status
# ==================================================

class AgentStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    DEPRECATED = "deprecated"


# ==================================================
# Internal Representation
# ==================================================

class _RegisteredAgent:
    """
    Internal representation of a registered agent.
    Holds definition + lifecycle status.
    """

    def __init__(self, definition: AgentDefinition, status: AgentStatus) -> None:
        self.definition = definition
        self.status = status


# ==================================================
# Agent Registry
# ==================================================

class AgentRegistry:
    """
    Central and deterministic registry for agent definitions.

    Responsibilities:
    - Register agents
    - Enforce unique agent IDs
    - Control lifecycle (draft / active / deprecated)
    - Resolve only ACTIVE agents

    Explicitly does NOT:
    - Execute agents
    - Know pipelines
    - Know OpenAI / LLM
    - Maintain execution state
    """

    def __init__(self, trace_id: str) -> None:
        self._agents: Dict[str, _RegisteredAgent] = {}
        self.trace_id = trace_id
    # --------------------------------------------------
    # Registration
    # --------------------------------------------------

    def register(
        self,
        agent: AgentDefinition,
        status: AgentStatus = AgentStatus.DRAFT,
    ) -> None:
        if agent.id in self._agents:
            raise AgentAlreadyExistsError(
                f"Agent id '{agent.id}' already exists."
            )

        self._agents[agent.id] = _RegisteredAgent(
            definition=agent,
            status=status,
        )

    # --------------------------------------------------
    # Lifecycle
    # --------------------------------------------------

    def activate(self, agent_id: str) -> None:
        agent = self._get_internal(agent_id)
        agent.status = AgentStatus.ACTIVE

    def deprecate(self, agent_id: str) -> None:
        agent = self._get_internal(agent_id)
        agent.status = AgentStatus.DEPRECATED

    # --------------------------------------------------
    # Resolution
    # --------------------------------------------------

    def get(self, agent_id: str) -> AgentDefinition:
        agent = self._get_internal(agent_id)

        if agent.status != AgentStatus.ACTIVE:
            raise AgentNotActiveError(
                f"Agent '{agent_id}' is not active (status={agent.status})."
            )

        return agent.definition

    def exists(self, agent_id: str) -> bool:
        return agent_id in self._agents

    def status(self, agent_id: str) -> AgentStatus:
        return self._get_internal(agent_id).status

    # --------------------------------------------------
    # Internal
    # --------------------------------------------------

    def _get_internal(self, agent_id: str) -> _RegisteredAgent:
        if agent_id not in self._agents:
            raise AgentNotFoundError(
                f"Agent '{agent_id}' not found."
            )
        return self._agents[agent_id]

    # --------------------------------------------------
    # Persistence Integration
    # --------------------------------------------------

    def load_from_database(self) -> None:
        """
        Carrega todos os agentes do banco
        e popula o registry interno como ACTIVE.
        """

        db = SessionLocal()
        repo = AgentRepository(db, self.trace_id)

        agents = repo.list_all()

        for db_agent in agents:
            definition = AgentDefinition(
                id=db_agent.id,
                name=db_agent.name,
                role=db_agent.role,
                model=db_agent.model,
                use_rag=db_agent.use_rag,
                temperature=db_agent.temperature,
                max_tokens=db_agent.max_tokens,
            )

            self._agents[db_agent.id] = _RegisteredAgent(
                definition=definition,
                status=AgentStatus.ACTIVE,
            )

        db.close()
