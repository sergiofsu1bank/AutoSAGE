from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI

from src.api.routers.agents_router import router as agents_router
from src.api.routers.knowledge_router import router as knowledge_router
from src.api.routers.execute_router import router as execute_router
from src.api.routers.pipeline_router import router as pipeline_router


app = FastAPI(title="AutoSAGE API LLM", version="v1")

app.include_router(agents_router)
app.include_router(knowledge_router)
app.include_router(execute_router)
app.include_router(pipeline_router)
