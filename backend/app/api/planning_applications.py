from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models.planning_applications import PlanningApplication

router = APIRouter(prefix="/planning-applications", tags=["PlanningApplications"])


@router.get("/", response_model=List[PlanningApplication])
async def list_planning_applications(db: AsyncSession = Depends(get_db)):
    """
    List all planning applications.
    """
    return []  # Replace with: await ApplicationCRUD(db).list_all()


@router.get("/{application_id}", response_model=PlanningApplication)
async def get_planning_application(
    application_id: UUID, db: AsyncSession = Depends(get_db)
):
    """
    Get a single planning application by ID.
    """
    raise HTTPException(status_code=404, detail="PlanningApplication not found")
