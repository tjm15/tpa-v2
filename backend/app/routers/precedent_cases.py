# app/routers/precedent_cases.py
from fastapi import APIRouter, HTTPException, Query, Depends, status
from typing import List, Optional
from uuid import UUID
from app.models.precedent_models import PrecedentCase, PrecedentCaseCreate, PrecedentCaseUpdate
from app.models.common_models import PaginatedResponse
from app.crud.base_crud import CRUDBase

router = APIRouter()
crud_precedent_case = CRUDBase[PrecedentCase, PrecedentCaseCreate, PrecedentCaseUpdate](PrecedentCase)

@router.post("/precedent-cases", response_model=PrecedentCase, status_code=status.HTTP_201_CREATED)
async def create_precedent_case(precedent_in: PrecedentCaseCreate):
    return crud_precedent_case.create(obj_in=precedent_in)

@router.get("/precedent-cases", response_model=PaginatedResponse[PrecedentCase])
async def list_precedent_cases(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    items = crud_precedent_case.get_multi(skip=skip, limit=limit)
    total_items = len(crud_precedent_case.get_multi(skip=0, limit=10000))
    return PaginatedResponse[PrecedentCase](
        items=items,
        total=total_items,
        page=(skip // limit) + 1 if limit > 0 else 1,
        limit=limit,
        totalPages=(total_items + limit - 1) // limit if limit > 0 else 1
    )

@router.get("/precedent-cases/{precedent_id}", response_model=PrecedentCase)
async def get_precedent_case_by_id(precedent_id: UUID):
    precedent = crud_precedent_case.get(item_id=precedent_id)
    if not precedent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Precedent Case not found")
    return precedent

@router.put("/precedent-cases/{precedent_id}", response_model=PrecedentCase)
async def update_precedent_case(precedent_id: UUID, precedent_in: PrecedentCaseUpdate):
    updated_precedent = crud_precedent_case.update(item_id=precedent_id, obj_in=precedent_in)
    if not updated_precedent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Precedent Case not found")
    return updated_precedent

@router.patch("/precedent-cases/{precedent_id}", response_model=PrecedentCase)
async def partial_update_precedent_case(precedent_id: UUID, precedent_in: PrecedentCaseUpdate):
    updated_precedent = crud_precedent_case.update(item_id=precedent_id, obj_in=precedent_in.model_dump(exclude_unset=True))
    if not updated_precedent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Precedent Case not found")
    return updated_precedent

@router.delete("/precedent-cases/{precedent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_precedent_case(precedent_id: UUID):
    deleted = crud_precedent_case.remove(item_id=precedent_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Precedent Case not found")
    return None
