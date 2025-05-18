from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models.scenarios import Scenario

router = APIRouter(prefix="/scenarios", tags=["Scenarios"])


@router.get("/", response_model=List[Scenario])
async def list_scenarios(db: AsyncSession = Depends(get_db)):
    """
    List all scenarios.
    """
    return []  # Replace with: await ScenarioCRUD(db).list_all()


@router.get("/{scenario_id}", response_model=Scenario)
async def get_scenario(scenario_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Get a single scenario by ID.
    """
    raise HTTPException(status_code=404, detail="Scenario not found")
