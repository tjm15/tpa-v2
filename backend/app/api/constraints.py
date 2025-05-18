from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models.constraints import Constraint

router = APIRouter(prefix="/constraints", tags=["Constraints"])


@router.get("/", response_model=List[Constraint])
async def list_constraints(db: AsyncSession = Depends(get_db)):
    """
    List all constraints.
    """
    return []  # Replace with: await ConstraintCRUD(db).list_all()


@router.get("/{constraint_id}", response_model=Constraint)
async def get_constraint(constraint_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Get a single constraint by ID.
    """
    raise HTTPException(status_code=404, detail="Constraint not found")
