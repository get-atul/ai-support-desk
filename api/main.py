from dotenv import load_dotenv
from fastapi import FastAPI

from database.connection import init_db
from api.projects import router as projects_router
from api.sources import router as sources_router
from api.chat import router as chat_router


load_dotenv()


app = FastAPI(
    title="AI Support Desk",
    version="1.0.0",
)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "AI Support Desk",
    }


app.include_router(projects_router)
app.include_router(sources_router)
app.include_router(chat_router)