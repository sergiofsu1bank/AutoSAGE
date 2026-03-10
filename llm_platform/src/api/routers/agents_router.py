from fastapi import APIRouter, HTTPException, Header, status
from sqlalchemy.exc import SQLAlchemyError

from src.api.models.agent_create import CreateAgentRequest
from src.api.models.agent_response import CreateAgentResponse
from src.api.services.agent_service import AgentService
from src.app.tools.log_factory import get_dcp_logger


router = APIRouter(prefix="/agents", tags=["agents"])

_agent_service = AgentService()


@router.post("", response_model=CreateAgentResponse)
def create_agent(
    payload: CreateAgentRequest,
    trace_id: str = Header(..., alias="trace-id", include_in_schema=True),
):
    logger = get_dcp_logger(
        trace_id=trace_id,
        classe="agents_router",
    )

    logger.info(
        "[Platform][agents] inicio processamento | "
        f"name={payload.name}"
    )

    try:
        agent_id = _agent_service.create_agent(payload, trace_id)

        logger.info(
            "[Platform][agents] agente criado com sucesso | "
            f"agent_id={agent_id}"
        )

        return CreateAgentResponse(
            agent_id=agent_id,
            status="created",
        )

    except ValueError as e:
        logger.error(
            "[Platform][agents] erro_validacao | "
            f"erro={str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    except SQLAlchemyError as e:
        logger.error(
            "[Platform][agents] erro_banco | "
            f"erro={str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while creating agent",
        )

    except Exception as e:
        logger.error(
            "[Platform][agents] erro_interno | "
            f"erro={str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error while creating agent",
        )
