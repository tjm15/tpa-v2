from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models.goals import Goal

router = APIRouter(prefix="/goals", tags=["Goals"])


@router.get("/", response_model=List[Goal])
async def list_goals(db: AsyncSession = Depends(get_db)):
    """
    List all goals.
    """
    return []  # Replace with: await GoalCRUD(db).list_all()


@router.get("/{goal_id}", response_model=Goal)
async def get_goal(goal_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Get a single goal by ID.
    """
    raise HTTPException(status_code=404, detail="Goal not found")
