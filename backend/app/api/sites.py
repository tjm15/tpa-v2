from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models.sites import Site

router = APIRouter(prefix="/sites", tags=["Sites"])


@router.get("/", response_model=List[Site])
async def list_sites(db: AsyncSession = Depends(get_db)):
    """
    List all sites.
    """
    return []  # Replace with: await SiteCRUD(db).list_all()


@router.get("/{site_id}", response_model=Site)
async def get_site(site_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Get a single site by ID.
    """
    raise HTTPException(status_code=404, detail="Site not found")
