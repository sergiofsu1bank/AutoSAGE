from typing import Dict, Optional

from src.db.session import SessionLocal
from src.db.models import Agent as AgentModel


class AgentDefinition:
    """
    Representação em memória do agente.
    """

    def __init__(
        self,
        *,
        id: str,
        name: str,
        role: str,
        model: str,
        temperature: float | None,
        max_tokens: int | None,
        use_rag: bool,
    ) -> None:
        self.id = id
        self.name = name
        self.role = role
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.use_rag = use_rag


class AgentRegistry:
    """
    Registry responsável por:
    - Carregar agentes do banco
    - Indexar por ID (principal)
    - Indexar por nome (auxiliar)
    """

    def __init__(self) -> None:
        self._agents_by_id: Dict[str, AgentDefinition] = {}
        self._agents_by_name: Dict[str, AgentDefinition] = {}

    # ==================================================
    # Load do banco
    # ==================================================

    def load_from_database(self) -> None:
        db = SessionLocal()

        agents = db.query(AgentModel).all()

        for agent in agents:
            definition = AgentDefinition(
                id=agent.id,
                name=agent.name,
                role=agent.role,
                model=agent.model,
                temperature=agent.temperature,
                max_tokens=agent.max_tokens,
                use_rag=agent.use_rag,
            )

            # Indexação principal
            self._agents_by_id[agent.id] = definition

            # Indexação auxiliar
            self._agents_by_name[agent.name] = definition

        db.close()

    # ==================================================
    # Getters
    # ==================================================

    def get_by_id(self, agent_id: str) -> AgentDefinition:
        agent = self._agents_by_id.get(agent_id)
        if not agent:
            raise ValueError(f"Agent id '{agent_id}' não encontrado.")
        return agent

    def get_by_name(self, name: str) -> AgentDefinition:
        agent = self._agents_by_name.get(name)
        if not agent:
            raise ValueError(f"Agent name '{name}' não encontrado.")
        return agent

    # Compatibilidade antiga (se ainda existir código usando .get())
    def get(self, key: str) -> AgentDefinition:
        if key in self._agents_by_id:
            return self._agents_by_id[key]
        if key in self._agents_by_name:
            return self._agents_by_name[key]

        raise ValueError(f"Agent '{key}' não encontrado.")
