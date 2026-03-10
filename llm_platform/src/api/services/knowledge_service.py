from src.app.rag.service import RAGService
from src.app.tools.log_factory import get_dcp_logger


class KnowledgeService:

    def __init__(self, rag_service: RAGService):
        self._rag_service = rag_service

    def create_knowledge(
        self,
        *,
        trace_id: str,
        agent_id: str,
        documents,
    ):
        logger = get_dcp_logger(
            trace_id=trace_id,
            classe=self.__class__.__name__,
        )

        if not agent_id:
            raise ValueError("agent_id é obrigatório")

        if not documents:
            raise ValueError("documents não pode ser vazio")

        logger.info(
            f"agent_id={agent_id} "
            f"documents_count={len(documents)}"
        )

        try:
            for doc in documents:
                self._rag_service.ingest(
                    agent_id=agent_id,
                    content=doc,
                    source="api_upload",
                )

            logger.info("knowledge indexada com sucesso")

            return "indexed"

        except Exception as e:
            logger.error(
                f"erro_interno={str(e)} "
                f"agent_id={agent_id}"
            )
            raise
