# -*- coding: utf-8 -*-
import os
import sys
import traceback
from fastapi import FastAPI, Request

from src.api.router.ml_router import router

from src.app.tools.log_factory import get_dcp_logger

app = FastAPI(title="AutoSAGE")

# -------------------------------------------------
# STARTUP
# -------------------------------------------------
@app.on_event("startup")
def startup_event():
    logger = get_dcp_logger(
        trace_id="startup",
        classe="ML-Main",
    )

    logger.info("🚀 AutoSAGE ML iniciado com sucesso")

# -------------------------------------------------
# Middleware de erro GLOBAL
# -------------------------------------------------
app.include_router(router)
