# (c) Danit Consultancy and Development, January-2026, danittech@yahoo.com

""" Main API router """

from fastapi import APIRouter
from app.api.v1 import agent, documents

# ----------------------------------------------------------------------------------------

api_router = APIRouter()
api_router.include_router(agent.router,     prefix="/agent",     tags=["Agent"])
api_router.include_router(documents.router, prefix="/documents", tags=["Documents"])
