# -*- coding: utf-8 -*-

from fastapi import APIRouter, HTTPException, Header
from sqlalchemy.exc import SQLAlchemyError

from src.api.models.run_pipeline_request import RunPipelineRequest
from src.api.models.run_pipeline_response import RunPipelineResponse
from src.api.models.add_node_request import AddNodeRequest
from src.api.models.add_edge_request import AddEdgeRequest
from src.api.models.create_pipeline_request import CreatePipelineRequest

from src.app.agents.registry import AgentRegistry
from src.app.orchestration.engine import ExecutionEngine
from src.app.orchestration.pipeline_loader import PipelineLoader
from src.app.llm.openai_adapter import OpenAIAdapter
from src.app.rag.service import RAGService

from src.db.session import SessionLocal
from src.db.pipeline_repository import PipelineRepository

from src.app.tools.log_factory import get_dcp_logger


router = APIRouter(prefix="/pipeline", tags=["pipeline"])


# ==========================================================
# RUN PIPELINE
# ==========================================================

@router.post("/run", response_model=RunPipelineResponse)
def run_pipeline(
    payload: RunPipelineRequest,
    trace_id: str = Header(..., alias="trace-id", include_in_schema=True),
):
    logger = get_dcp_logger(trace_id=trace_id, classe="pipeline_router")

    try:
        logger.info(
            "[Platform][pipeline] inicio processamento | "
            f"pipeline_name={payload.pipeline_name}"
        )

        registry = AgentRegistry(trace_id)
        registry.load_from_database()

        loader = PipelineLoader(trace_id)
        pipeline = loader.load(payload.pipeline_name)

        if not pipeline:
            raise HTTPException(
                status_code=404,
                detail="Pipeline não encontrado.",
            )

        engine = ExecutionEngine(
            registry=registry,
            llm_adapter=OpenAIAdapter(),
            rag_service=RAGService(),
            trace_id=trace_id,
        )

        context = engine.run(
            pipeline=pipeline,
            initial_input=payload.input,
        )

        logger.info(
            "[Platform][pipeline] execucao concluida | "
            f"pipeline_name={payload.pipeline_name}"
        )

        return RunPipelineResponse(
            outputs=context.outputs_by_node
        )

    except ValueError as e:
        logger.error(
            "[Platform][pipeline] erro_validacao | "
            f"erro={str(e)}"
        )
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(
            "[Platform][pipeline] erro_interno | "
            f"erro={str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail="Unexpected error during pipeline execution",
        )


# ==========================================================
# ADD NODE
# ==========================================================

@router.post("/node")
def add_node(
    payload: AddNodeRequest,
    trace_id: str = Header(..., alias="trace-id", include_in_schema=True),
):
    logger = get_dcp_logger(trace_id=trace_id, classe="pipeline_router")
    db = SessionLocal()

    try:
        logger.info(
            "[Platform][node] inicio processamento | "
            f"pipeline_name={payload.pipeline_name}"
        )

        repo = PipelineRepository(db, trace_id)

        pipeline = repo.get_pipeline_by_name(payload.pipeline_name)
        if not pipeline:
            raise HTTPException(status_code=404, detail="Pipeline não encontrado.")

        version = repo.get_active_version(pipeline.id)
        if not version:
            raise HTTPException(
                status_code=400,
                detail="Pipeline não possui versão ativa.",
            )

        repo.add_node(
            pipeline_version_id=version.id,
            node_id=payload.node_id,
            agent_id=payload.agent_id,
        )

        return {"status": "node_added"}

    except HTTPException:
        raise

    except SQLAlchemyError as e:
        logger.error(
            "[Platform][node] erro_banco | "
            f"erro={str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail="Database error while adding node",
        )

    except Exception as e:
        logger.error(
            "[Platform][node] erro_interno | "
            f"erro={str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail="Unexpected error while adding node",
        )

    finally:
        db.close()


# ==========================================================
# ADD EDGE
# ==========================================================

@router.post("/edge")
def add_edge(
    payload: AddEdgeRequest,
    trace_id: str = Header(..., alias="trace-id", include_in_schema=True),
):
    logger = get_dcp_logger(trace_id=trace_id, classe="pipeline_router")
    db = SessionLocal()

    try:
        logger.info(
            "[Platform][edge] inicio processamento | "
            f"pipeline_name={payload.pipeline_name}"
        )

        repo = PipelineRepository(db, trace_id)

        pipeline = repo.get_pipeline_by_name(payload.pipeline_name)
        if not pipeline:
            raise HTTPException(status_code=404, detail="Pipeline não encontrado.")

        version = repo.get_active_version(pipeline.id)
        if not version:
            raise HTTPException(
                status_code=400,
                detail="Pipeline não possui versão ativa.",
            )

        repo.add_edge(
            version_id=version.id,
            source_node_id=payload.source_node_id,
            target_node_id=payload.target_node_id,
            condition_json=payload.condition,
        )

        return {"status": "edge_added"}

    except HTTPException:
        raise

    except SQLAlchemyError as e:
        logger.error(
            "[Platform][edge] erro_banco | "
            f"erro={str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail="Database error while adding edge",
        )

    except Exception as e:
        logger.error(
            "[Platform][edge] erro_interno | "
            f"erro={str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail="Unexpected error while adding edge",
        )

    finally:
        db.close()


# ==========================================================
# CREATE PIPELINE
# ==========================================================

@router.post("")
def create_pipeline(
    payload: CreatePipelineRequest,
    trace_id: str = Header(..., alias="trace-id", include_in_schema=True),
):
    logger = get_dcp_logger(trace_id=trace_id, classe="pipeline_router")
    db = SessionLocal()

    try:
        logger.info(
            "[Platform][create_pipeline] inicio processamento | "
            f"name={payload.name}"
        )

        repo = PipelineRepository(db, trace_id)

        existing = repo.get_pipeline_by_name(payload.name)
        if existing:
            return {
                "status": "already_exists",
                "pipeline_id": existing.id,
            }

        pipeline = repo.create_pipeline(payload.name)

        repo.create_new_version(
            pipeline_id=pipeline.id,
            activate=True,
        )

        return {
            "status": "created",
            "pipeline_id": pipeline.id,
        }

    except HTTPException:
        raise

    except SQLAlchemyError as e:
        logger.error(
            "[Platform][create_pipeline] erro_banco | "
            f"erro={str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail="Database error while creating pipeline",
        )

    except Exception as e:
        logger.error(
            "[Platform][create_pipeline] erro_interno | "
            f"erro={str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail="Unexpected error while creating pipeline",
        )

    finally:
        db.close()
