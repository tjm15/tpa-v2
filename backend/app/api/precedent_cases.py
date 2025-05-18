from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models.precedent_cases import PrecedentCase

router = APIRouter(prefix="/precedent-cases", tags=["PrecedentCases"])


@router.get("/", response_model=List[PrecedentCase])
async def list_precedent_cases(db: AsyncSession = Depends(get_db)):
    """
    List all precedent cases.
    """
    return []  # Replace with: await PrecedentCaseCRUD(db).list_all()


@router.get("/{precedent_id}", response_model=PrecedentCase)
async def get_precedent_case(precedent_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Get a single precedent case by ID.
    """
    raise HTTPException(status_code=404, detail="PrecedentCase not found")
