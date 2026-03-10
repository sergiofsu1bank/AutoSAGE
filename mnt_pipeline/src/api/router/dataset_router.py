from fastapi import APIRouter, HTTPException, Header


from src.app.services.dataset_run_service import DatasetRunService
from src.app.tools.log_factory import get_dcp_logger


router = APIRouter()


@router.get("/datasets/{dataset_name}/latest")
def get_latest_run(
    dataset_name: str,
    trace_id: str = Header(..., alias="trace-id", include_in_schema=True),
):

    if not trace_id:
        raise HTTPException(400, "trace-id obrigatório no header")

    logger = get_dcp_logger(
        trace_id=trace_id,
        classe="root",
    )

    logger.info(
        f"[MNT][{trace_id}] stage=get action=get_latest_run"
    )

    service = DatasetRunService(trace_id)
    return service.get_latest_run(dataset_name)

@router.get("/datasets/{dataset_name}/runs")
def get_runs(
    dataset_name: str,
    trace_id: str = Header(..., alias="trace-id", include_in_schema=True),
):

    if not trace_id:
        raise HTTPException(400, "trace-id obrigatório no header")

    logger = get_dcp_logger(
        trace_id=trace_id,
        classe="root",
    )

    logger.info(
        f"[MNT][{trace_id}] stage=get action=get_runs"
    )

    service = DatasetRunService(trace_id)
    return service.get_runs(dataset_name)

@router.get("/datasets")
def list_datasets(
    trace_id: str = Header(..., alias="trace-id", include_in_schema=True),
):

    if not trace_id:
        raise HTTPException(400, "trace-id obrigatório no header")

    logger = get_dcp_logger(
        trace_id=trace_id,
        classe="root",
    )

    logger.info(
        f"[MNT][{trace_id}] stage=get action=list_datasets"
    )

    service = DatasetRunService(trace_id)
    return service.list_datasets()

@router.get("/datasets/{dataset_name}/pipeline")
def get_pipeline_execution(
    dataset_name: str,
    trace_id: str = Header(..., alias="trace-id", include_in_schema=True),
):

    if not trace_id:
        raise HTTPException(400, "trace-id obrigatório no header")

    logger = get_dcp_logger(
        trace_id=trace_id,
        classe="root",
    )

    logger.info(
        f"[MNT][{trace_id}] stage=get action=get_pipeline_execution"
    )
    service = DatasetRunService(trace_id)
    return service.get_pipeline_execution(dataset_name)

@router.get("/datasets/{dataset_name}/runs")
def get_runs(
    dataset_name: str,
    trace_id: str = Header(..., alias="trace-id", include_in_schema=True),
):
    if not trace_id:
        raise HTTPException(400, "trace-id obrigatório no header")

    logger = get_dcp_logger(
        trace_id=trace_id,
        classe="root",
    )

    logger.info(
        f"[MNT][{trace_id}] stage=get action=/datasets/dataset_name/runs"
    )

    service = DatasetRunService(trace_id)
    return service.get_runs(dataset_name)

@router.get("/datasets/{dataset_name}/timeline")
def get_pipeline_timeline(dataset_name: str,
    trace_id: str = Header(..., alias="trace-id", include_in_schema=True),
):
    if not trace_id:
        raise HTTPException(400, "trace-id obrigatório no header")

    logger = get_dcp_logger(
        trace_id=trace_id,
        classe="root",
    )

    logger.info(
        f"[MNT][{trace_id}] stage=get action=/datasets/dataset_name/timeline"
    )

    service = DatasetRunService(trace_id)
    return service.get_pipeline_timeline(dataset_name)


@router.get("/platform/health")
def get_platform_health(
    trace_id: str = Header(..., alias="trace-id", include_in_schema=True),
):

    logger = get_dcp_logger(
        trace_id=trace_id,
        classe="root",
    )

    logger.info(
        f"[MNT][{trace_id}] stage=get action=/platform/health"
    )

    service = DatasetRunService(trace_id)
    return service.get_platform_health()
