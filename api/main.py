from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.connection import init_db

from api.projects import router as projects_router
from api.sources import router as sources_router
from api.chat import router as chat_router


load_dotenv()


app = FastAPI(
    title="AI Support Desk",
    version="1.0.0",
)


# ---------------------------------
# CORS
# ---------------------------------

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ],

    allow_credentials=True,

    allow_methods=[
        "*"
    ],

    allow_headers=[
        "*"
    ],
)


# ---------------------------------
# Startup
# ---------------------------------

@app.on_event("startup")
def startup():

    init_db()


# ---------------------------------
# Health
# ---------------------------------

@app.get("/health")
def health():

    return {
        "status": "ok",
        "service": "AI Support Desk",
    }


# ---------------------------------
# Routers
# ---------------------------------

app.include_router(
    projects_router
)

app.include_router(
    sources_router
)

app.include_router(
    chat_router
)