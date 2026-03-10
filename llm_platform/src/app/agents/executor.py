from typing import Any, Optional

from src.app.agents.contracts import AgentDefinition
from src.app.llm.openai_adapter import (
    OpenAIAdapter,
    LLMRequest,
    LLMResponse,
)
from src.app.rag.service import RAGService, RAGQuery


class AgentExecutor:
    """
    Executes an AgentDefinition using:
    - LLM Adapter
    - Optional RAG Service (controlled by agent.use_rag)

    Responsibilities:
    - Assemble LLMRequest
    - Retrieve context from RAG when enabled
    - Execute LLM call
    - Return normalized LLMResponse

    Explicitly does NOT:
    - Decide pipeline flow
    - Know DAG structure
    - Mutate execution context
    """

    def __init__(
        self,
        llm_adapter: OpenAIAdapter,
        rag_service: Optional[RAGService] = None,
    ) -> None:
        self._llm_adapter = llm_adapter
        self._rag_service = rag_service

    # ------------------------------------------------------
    # Public API
    # ------------------------------------------------------

    def execute(
        self,
        agent: AgentDefinition,
        input_payload: Any,
    ) -> LLMResponse:
        """
        Execute a single agent.
        """

        rag_context: Optional[str] = None

        if agent.use_rag:
            if not self._rag_service:
                raise RuntimeError(
                    f"Agent '{agent.name}' requires RAG, but no RAGService was provided."
                )

            rag_context = self._retrieve_rag_context(input_payload)

        request = LLMRequest(
            system_prompt=agent.role,
            user_prompt=self._normalize_input(input_payload),
            context=rag_context,
            model=agent.model,
            temperature=agent.temperature,
            max_tokens=agent.max_tokens,
        )

        return self._llm_adapter.generate(request)

    # ------------------------------------------------------
    # RAG integration
    # ------------------------------------------------------

    def _retrieve_rag_context(self, input_payload: Any) -> str:
        """
        Retrieve and assemble RAG context as plain text.
        """
        query = RAGQuery(
            query=self._normalize_input(input_payload),
            top_k=5,
        )

        documents = self._rag_service.retrieve(query)

        if not documents:
            return ""

        return "\n\n".join(
            f"[Source: {doc.source}]\n{doc.content}"
            for doc in documents
        )

    # ------------------------------------------------------
    # Helpers
    # ------------------------------------------------------

    @staticmethod
    def _normalize_input(input_payload: Any) -> str:
        if isinstance(input_payload, str):
            return input_payload
        return str(input_payload)
