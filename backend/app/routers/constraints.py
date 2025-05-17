# app/routers/constraints.py
from fastapi import APIRouter, HTTPException, Query, Depends, status
from typing import List, Optional
from uuid import UUID
from app.models.constraint_models import Constraint, ConstraintCreate, ConstraintUpdate
from app.models.common_models import PaginatedResponse
from app.crud.base_crud import CRUDBase

router = APIRouter()
crud_constraint = CRUDBase[Constraint, ConstraintCreate, ConstraintUpdate](Constraint)

@router.post("/constraints", response_model=Constraint, status_code=status.HTTP_201_CREATED)
async def create_constraint(constraint_in: ConstraintCreate):
    return crud_constraint.create(obj_in=constraint_in)

@router.get("/constraints", response_model=PaginatedResponse[Constraint])
async def list_constraints(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    items = crud_constraint.get_multi(skip=skip, limit=limit)
    total_items = len(crud_constraint.get_multi(skip=0, limit=10000))
    return PaginatedResponse[Constraint](
        items=items,
        total=total_items,
        page=(skip // limit) + 1 if limit > 0 else 1,
        limit=limit,
        totalPages=(total_items + limit - 1) // limit if limit > 0 else 1
    )

@router.get("/constraints/{constraint_id}", response_model=Constraint)
async def get_constraint_by_id(constraint_id: UUID):
    constraint = crud_constraint.get(item_id=constraint_id)
    if not constraint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Constraint not found")
    return constraint

@router.put("/constraints/{constraint_id}", response_model=Constraint)
async def update_constraint(constraint_id: UUID, constraint_in: ConstraintUpdate):
    updated_constraint = crud_constraint.update(item_id=constraint_id, obj_in=constraint_in)
    if not updated_constraint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Constraint not found")
    return updated_constraint

@router.patch("/constraints/{constraint_id}", response_model=Constraint)
async def partial_update_constraint(constraint_id: UUID, constraint_in: ConstraintUpdate):
    updated_constraint = crud_constraint.update(item_id=constraint_id, obj_in=constraint_in.model_dump(exclude_unset=True))
    if not updated_constraint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Constraint not found")
    return updated_constraint

@router.delete("/constraints/{constraint_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_constraint(constraint_id: UUID):
    deleted = crud_constraint.remove(item_id=constraint_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Constraint not found")
    return None
