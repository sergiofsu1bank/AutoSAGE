from fastapi import FastAPI


from src.api.router.dataset_router import router


app = FastAPI(
    title="AutoSAGE Monitor",
    version="1.0.0"
)

app.include_router(router)

