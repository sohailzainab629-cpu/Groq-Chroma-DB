from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from app.rag_service import RAGService


app = FastAPI(
    title="Groq + ChromaDB RAG API",
    version="1.0.0",
)


# Static files
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)


# HTML templates
templates = Jinja2Templates(directory="templates")


rag_service: Optional[RAGService] = None


class QuestionRequest(BaseModel):
    question: str = Field(
        min_length=1
    )

    top_k: Optional[int] = Field(
        default=None,
        ge=1,
        le=50,
    )

    source: Optional[str] = None


@app.on_event("startup")
def startup() -> None:
    global rag_service
    rag_service = RAGService()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={},
    )

@app.get("/health")
def health():
    if rag_service is None:
        return {
            "status": "starting"
        }

    return {
        "status": "ok",
        "indexed_chunks": rag_service.store.count(),
    }


@app.post("/rag/query")
def query_rag(
    payload: QuestionRequest
):
    if rag_service is None:
        raise HTTPException(
            status_code=503,
            detail="RAG service is not ready.",
        )

    try:
        return rag_service.ask(
            question=payload.question,
            top_k=payload.top_k,
            source=payload.source,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc