# -*- coding: utf-8 -*-
import os
import sys
import traceback

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from src.api.router.dataset_router import router
from src.app.tools.log_factory import get_dcp_logger


app = FastAPI(title="AutoSAGE")


# -------------------------------------------------
# CORS
# -------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # em desenvolvimento
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------------
# STARTUP
# -------------------------------------------------
@app.on_event("startup")
def startup_event():

    logger = get_dcp_logger(
        trace_id="startup",
        classe="MNT-Main",
    )

    logger.info("🚀 AutoSAGE MNT iniciado com sucesso")


# -------------------------------------------------
# ROUTERS
# -------------------------------------------------
app.include_router(router)
