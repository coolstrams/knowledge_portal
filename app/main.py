from fastapi import FastAPI
from sqlmodel import SQLModel
from app.api import router
from app.core.database import engine

app = FastAPI(title="RAG HTTP SSE Service")


@app.on_event("startup")
def on_startup():
    # 自动建表
    SQLModel.metadata.create_all(engine)


app.include_router(router)
