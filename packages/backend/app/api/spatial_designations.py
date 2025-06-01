# API logic for spatial designations (formerly constraints)

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from libs.shared_api_schemas.spatial_designations import SpatialDesignation

router = APIRouter(prefix="/spatial_designations", tags=["SpatialDesignations"])


@router.get("/", response_model=List[SpatialDesignation])
async def list_spatial_designations(db: AsyncSession = Depends(get_db)):
    """
    List all spatial designations.
    """
    return []  # Replace with: await SpatialDesignationCRUD(db).list_all()


@router.get("/{spatial_designation_id}", response_model=SpatialDesignation)
async def get_spatial_designation(spatial_designation_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Get a single spatial designation by ID.
    """
    raise HTTPException(status_code=404, detail="SpatialDesignation not found")
