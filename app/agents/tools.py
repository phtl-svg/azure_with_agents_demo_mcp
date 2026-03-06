# (c) Danit Consultancy and Development, September-2023, danittech@yahoo.com

""" Custom tools for the agent """

import structlog
from typing import List
from langchain_core.tools import tool

# ----------------------------------------------------------------------------------------

logger = structlog.get_logger(__name__)

# ----------------------------------------------------------------------------------------

@tool
def calculator(expression: str) -> str:
    """ Evaluate a mathematical expression """
    try:
        result = eval(expression, {"__builtins__": {}})
        logger.info("calculator_used", expression=expression, result=result)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

# ----------------------------------------------------------------------------------------

@tool
def get_current_time() -> str:
    """ Get the current time in ISO format """
    from datetime import datetime
    return datetime.now().isoformat()

# ----------------------------------------------------------------------------------------

@tool
async def search_documents(query: str) -> str:
    """
    Search the document knowledge base for information matching the query.
    Use this tool when asked about any topic that might be covered in stored documents.
    """
    from sqlalchemy import select, or_
    from app.db.session import AsyncSessionLocal
    from app.db.models import Document

    # Tools are not inside an HTTP request, so FastAPI's Depends(get_db) is not
    # available here. We open our own session directly from AsyncSessionLocal —
    # the same factory used by get_db(), just called manually.
    try:
        async with AsyncSessionLocal() as session:
            stmt = (
                select(Document)
                .where(
                    or_(
                        Document.title.ilike(f"%{query}%"),
                        Document.content.ilike(f"%{query}%"),
                    )
                )
                .limit(3)  # return at most 3 results to keep the LLM context small
            )
            result = await session.execute(stmt)
            documents = result.scalars().all()
    except Exception as e:
        logger.warning("search_documents_db_unavailable", error=str(e))
        return "Document search is currently unavailable."

    if not documents:
        return f"No documents found matching '{query}'."

    parts = []
    for doc in documents:
        # Truncate long documents to 300 chars so the LLM context stays manageable
        excerpt = doc.content[:300] + "..." if len(doc.content) > 300 else doc.content
        parts.append(f"Title: {doc.title}\nContent: {excerpt}")

    logger.info("search_documents_used", query=query, results=len(documents))
    return "\n\n---\n\n".join(parts)

# ----------------------------------------------------------------------------------------

def get_tools() -> List:
    return [calculator, get_current_time, search_documents]
