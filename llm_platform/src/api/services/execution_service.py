from src.api.services.agent_service import AgentService
from src.api.services.knowledge_service import KnowledgeService
from src.app.llm.openai_adapter import OpenAIAdapter
from src.app.llm.openai_adapter import LLMRequest


class ExecutionService:
    def __init__(
        self,
        agent_service: AgentService,
        knowledge_service: KnowledgeService,
        llm_adapter: OpenAIAdapter,
    ):
        self._agent_service = agent_service
        self._knowledge_service = knowledge_service
        self._llm = llm_adapter

    def execute(self, agent_id: str, user_input: str, trace_id: str):
        agent = self._agent_service.get_agent(agent_id)

        context = None
        if agent.use_rag:
            documents = self._knowledge_service._store.get(agent_id)
            if documents:
                context = "\n".join(documents)

        request = LLMRequest(
            system_prompt=agent.role,
            user_prompt=user_input,
            context=context,
            model=agent.model,
            temperature=agent.temperature,
            max_tokens=agent.max_tokens,
        )

        response = self._llm.generate(request)
        return response
