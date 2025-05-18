from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models.plan_documents import PlanDocument, DocumentNode

router = APIRouter(prefix="/plan-documents", tags=["PlanDocuments"])


@router.get("/", response_model=List[PlanDocument])
async def list_plan_documents(db: AsyncSession = Depends(get_db)):
    """
    List all plan documents.
    """
    return []  # Replace with: await PlanDocumentCRUD(db).list_all()


@router.get("/{document_id}", response_model=PlanDocument)
async def get_plan_document(document_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Get a single plan document by ID.
    """
    raise HTTPException(status_code=404, detail="PlanDocument not found")


@router.get("/{document_id}/nodes", response_model=List[DocumentNode])
async def list_document_nodes(document_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    List top-level nodes of a plan document.
    """
    return []  # Replace with: await DocumentNodeCRUD(db).list_for_document(document_id)


@router.get("/{document_id}/nodes/{node_id}", response_model=DocumentNode)
async def get_document_node(
    document_id: UUID, node_id: UUID, db: AsyncSession = Depends(get_db)
):
    """
    Get a single document node by ID.
    """
    raise HTTPException(status_code=404, detail="DocumentNode not found")
