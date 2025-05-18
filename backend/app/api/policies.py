from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models.policies import Policy

router = APIRouter(prefix="/policies", tags=["Policies"])


@router.get("/", response_model=List[Policy])
async def list_policies(db: AsyncSession = Depends(get_db)):
    """
    List all policies.
    """
    return []  # Replace with: await PolicyCRUD(db).list_all()


@router.get("/{policy_id}", response_model=Policy)
async def get_policy(policy_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Get a single policy by ID.
    """
    # Replace with real lookup:
    # policy = await PolicyCRUD(db).get(policy_id)
    # if not policy: raise ...
    raise HTTPException(status_code=404, detail="Policy not found")
