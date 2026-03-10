import os
import httpx
import requests
from datetime import datetime
from typing import Dict, Optional
from dataclasses import asdict
from src.app.tools.log_factory import get_dcp_logger


class MetricsClient:
    def __init__(self, trace_id: str):
        self.base_url = os.environ["METRICS_BASE_URL"].rstrip("/")
        self.timeout = float(os.getenv("METRICS_TIMEOUT", "2"))
        self.trace_id = trace_id

        self.logger = get_dcp_logger(
            trace_id=self.trace_id,
            classe=self.__class__.__name__,
        )

    # --------------------------------------------------
    # Timing utilitário
    # --------------------------------------------------
    @staticmethod
    def build_timing(started_at: datetime) -> Dict[str, Optional[object]]:
        finished_at = datetime.utcnow()
        duration_ms = int((finished_at - started_at).total_seconds() * 1000)

        return {
            "started_at": started_at.isoformat() + "Z",
            "finished_at": finished_at.isoformat() + "Z",
            "duration_ms": duration_ms,
        }

    # --------------------------------------------------
    # Pipeline metric (ASSÍNCRONO)
    # --------------------------------------------------
    async def pipeline_event(self, metrics_context) -> None:
        try:
            self.logger.info(
                f"pipeline={metrics_context.pipeline} "
                f"status={metrics_context.status}"
            )

            payload = asdict(metrics_context)

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(
                    f"{self.base_url}/metrics/pipeline",
                    json=payload,
                    headers={"trace-id": self.trace_id},
                )
                resp.raise_for_status()

        except Exception as e:
            self.logger.error(
                f"message=Falha interna durante a execução | detail={e}"
            )
            raise

    # --------------------------------------------------
    # ML Statistics (ASSÍNCRONO)
    # --------------------------------------------------
    async def ml_statistics(self, ml_context) -> None:
        try:
            self.logger.info(
                f"pipeline={ml_context.experiment_id} "
                f"status={ml_context.decision}"
            )

            payload = asdict(ml_context)

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(
                    f"{self.base_url}/metrics/ml-statistics",
                    json=payload,
                    headers={"trace-id": self.trace_id},
                )

                if resp.status_code != 200:
                    error_body = resp.text

                    self.logger.error(
                        f"[ML → METRICS] HTTP {resp.status_code} | "
                        f"response={error_body}"
                    )

                    raise RuntimeError(
                        f"Metrics service returned {resp.status_code}: {error_body}"
                    )

        except Exception:
            self.logger.error(
                  f"[ML → METRICS] HTTP {resp.status_code} | "
                  f"response={error_body}"
            )
            raise
