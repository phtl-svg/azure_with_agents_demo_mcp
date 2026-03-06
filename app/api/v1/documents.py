# (c) Danit Consultancy and Development, January-2026, danittech@yahoo.com

""" Documents API endpoints — seed and manage the agent's knowledge base """

import structlog
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.db.models import Document

logger = structlog.get_logger(__name__)
router = APIRouter()

# ----------------------------------------------------------------------------------------

class DocumentCreate(BaseModel):
    """
    Input model for creating a document.
    Pydantic validates the request body and rejects missing/wrong-typed fields
    before any DB code runs — same pattern as AgentRequest in agent.py.
    """
    title: str
    content: str

class DocumentResponse(BaseModel):
    """
    Output model — only exposes id and title, not the full content,
    to keep the response payload small.
    """
    id: int
    title: str

# ----------------------------------------------------------------------------------------

@router.post("/", response_model=DocumentResponse, status_code=201)
async def create_document(
    doc: DocumentCreate,
    db: AsyncSession = Depends(get_db),
) -> DocumentResponse:
    """
    Add a document to the knowledge base.

    The `db` parameter is injected by FastAPI's Depends(get_db) — it calls the
    get_db() generator in session.py and passes in a live AsyncSession.
    This is the standard FastAPI pattern for DB access in HTTP endpoints.

    Example:
        POST /api/v1/documents
        {"title": "Azure App Service", "content": "Azure App Service is a ..."}
    """
    document = Document(title=doc.title, content=doc.content)
    db.add(document)
    await db.commit()
    await db.refresh(document)  # re-reads the row to get the server-assigned id and created_at
    logger.info("document_created", id=document.id, title=document.title)
    return DocumentResponse(id=document.id, title=document.title)
