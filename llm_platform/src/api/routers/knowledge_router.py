from fastapi import APIRouter, HTTPException, Header, status
from sqlalchemy.exc import SQLAlchemyError

from src.api.models.knowledge_create import CreateKnowledgeRequest
from src.api.models.knowledge_response import CreateKnowledgeResponse
from src.app.rag.service import RAGService
from src.api.services.knowledge_service import KnowledgeService
from src.app.tools.log_factory import get_dcp_logger


router = APIRouter(prefix="/knowledge", tags=["knowledge"])

rag_service = RAGService()
knowledge_service = KnowledgeService(rag_service=rag_service)


@router.post("", response_model=CreateKnowledgeResponse)
def create_knowledge(
    payload: CreateKnowledgeRequest,
    trace_id: str = Header(..., alias="trace-id", include_in_schema=True),
):
    logger = get_dcp_logger(
        trace_id=trace_id,
        classe="knowledge_router",
    )

    try:
        documents_count = len(payload.documents) if payload.documents else 0

        logger.info(
            "[Platform][knowledge] inicio processamento | "
            f"agent_id={payload.agent_id} | "
            f"documents_count={documents_count}"
        )

        knowledge_id = knowledge_service.create_knowledge(
            trace_id=trace_id,
            agent_id=payload.agent_id,
            documents=payload.documents,
        )

        logger.info(
            "[Platform][knowledge] indexacao concluida | "
            f"agent_id={payload.agent_id}"
        )

        return CreateKnowledgeResponse(
            knowledge_id=knowledge_id,
            status="indexed",
        )

    except ValueError as e:
        logger.error(
            "[Platform][knowledge] erro_validacao | "
            f"erro={str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    except SQLAlchemyError as e:
        logger.error(
            "[Platform][knowledge] erro_banco | "
            f"erro={str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while indexing knowledge",
        )

    except Exception as e:
        logger.error(
            "[Platform][knowledge] erro_interno | "
            f"erro={str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error while indexing knowledge",
        )
