# app/routers/plan_documents.py
from fastapi import APIRouter, HTTPException, Query, Depends, status
from typing import List, Optional
from uuid import UUID
from app.models.document_models import PlanDocument, PlanDocumentCreate, PlanDocumentUpdate, DocumentNode, DocumentNodeCreate, DocumentNodeUpdate
from app.models.common_models import PaginatedResponse
from app.crud.base_crud import CRUDBase

router = APIRouter()
crud_plan_document = CRUDBase[PlanDocument, PlanDocumentCreate, PlanDocumentUpdate](PlanDocument)
crud_document_node = CRUDBase[DocumentNode, DocumentNodeCreate, DocumentNodeUpdate](DocumentNode) # Simplified stub

@router.post("/plan-documents", response_model=PlanDocument, status_code=status.HTTP_201_CREATED)
async def create_plan_document(doc_in: PlanDocumentCreate):
    # In a real app, creating rootNode might be more complex or handled separately
    return crud_plan_document.create(obj_in=doc_in)

@router.get("/plan-documents", response_model=PaginatedResponse[PlanDocument])
async def list_plan_documents(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    items = crud_plan_document.get_multi(skip=skip, limit=limit)
    total_items = len(crud_plan_document.get_multi(skip=0, limit=10000))
    return PaginatedResponse[PlanDocument](
        items=items,
        total=total_items,
        page=(skip // limit) + 1 if limit > 0 else 1,
        limit=limit,
        totalPages=(total_items + limit - 1) // limit if limit > 0 else 1
    )

@router.get("/plan-documents/{document_id}", response_model=PlanDocument)
async def get_plan_document_by_id(document_id: UUID):
    doc = crud_plan_document.get(item_id=document_id)
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan Document not found")
    # In a real app, you'd ensure rootNode and its children are properly fetched and structured
    return doc

# --- Document Node Endpoints (Simplified Stubs) ---
@router.post("/plan-documents/{document_id}/nodes", response_model=DocumentNode, status_code=status.HTTP_201_CREATED)
async def create_document_node(document_id: UUID, node_in: DocumentNodeCreate):
    # This is a stub. Real implementation needs to link to the document and handle hierarchy.
    # Check if document_id exists
    if not crud_plan_document.get(item_id=document_id):
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parent Plan Document not found")
    return crud_document_node.create(obj_in=node_in)

@router.get("/plan-documents/{document_id}/nodes/{node_id}", response_model=DocumentNode)
async def get_document_node(document_id: UUID, node_id: UUID):
    # Stub
    node = crud_document_node.get(item_id=node_id)
    if not node: # Add logic to check if node belongs to document_id
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document Node not found")
    return node

# Add PUT, PATCH, DELETE for PlanDocument and DocumentNode as needed
