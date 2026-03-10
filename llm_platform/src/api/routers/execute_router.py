from fastapi import APIRouter, HTTPException, Header, status
from sqlalchemy.exc import SQLAlchemyError

from src.api.models.execute_request import ExecuteAgentRequest
from src.api.models.execute_response import ExecuteAgentResponse
from src.api.services.execution_service import ExecutionService
from src.api.services.agent_service import AgentService
from src.api.services.knowledge_service import KnowledgeService
from src.app.llm.openai_adapter import OpenAIAdapter
from src.app.rag.service import RAGService
from src.app.tools.log_factory import get_dcp_logger


router = APIRouter(prefix="/execute", tags=["execution"])

# Instancia serviços localmente (sem registry)
agent_service = AgentService()
rag_service = RAGService()
knowledge_service = KnowledgeService(rag_service=rag_service)
llm_adapter = OpenAIAdapter()

_execution_service = ExecutionService(
    agent_service=agent_service,
    knowledge_service=knowledge_service,
    llm_adapter=llm_adapter,
)


@router.post("", response_model=ExecuteAgentResponse)
def execute(
    payload: ExecuteAgentRequest,
    trace_id: str = Header(..., alias="trace-id", include_in_schema=True),
):
    logger = get_dcp_logger(
        trace_id=trace_id,
        classe="execute_router",
    )

    try:
        logger.info(
            "[Platform][execute] inicio processamento | "
            f"agent_id={payload.agent_id}"
        )

        response = _execution_service.execute(
            agent_id=payload.agent_id,
            user_input=payload.input,
            trace_id=trace_id,
        )

        logger.info(
            "[Platform][execute] execucao concluida | "
            f"agent_id={payload.agent_id}"
        )

        return ExecuteAgentResponse(
            output=response.text,
            usage=response.usage.__dict__,
        )

    except ValueError as e:
        logger.error(
            "[Platform][execute] erro_validacao | "
            f"erro={str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    except SQLAlchemyError as e:
        logger.error(
            "[Platform][execute] erro_banco | "
            f"erro={str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error during execution",
        )

    except Exception as e:
        logger.error(
            "[Platform][execute] erro_interno | "
            f"erro={str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error during execution",
        )
