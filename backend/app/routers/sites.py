# app/routers/sites.py
from fastapi import APIRouter, HTTPException, Query, Depends, status
from typing import List, Optional
from uuid import UUID
from app.models.site_models import Site, SiteCreate, SiteUpdate
from app.models.common_models import PaginatedResponse
from app.crud.base_crud import CRUDBase

router = APIRouter()
crud_site = CRUDBase[Site, SiteCreate, SiteUpdate](Site)

@router.post("/sites", response_model=Site, status_code=status.HTTP_201_CREATED)
async def create_site(site_in: SiteCreate):
    return crud_site.create(obj_in=site_in)

@router.get("/sites", response_model=PaginatedResponse[Site])
async def list_sites(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    items = crud_site.get_multi(skip=skip, limit=limit)
    total_items = len(crud_site.get_multi(skip=0, limit=10000)) # Simplified total count
    return PaginatedResponse[Site](
        items=items,
        total=total_items,
        page=(skip // limit) + 1 if limit > 0 else 1,
        limit=limit,
        totalPages=(total_items + limit - 1) // limit if limit > 0 else 1
    )

@router.get("/sites/{site_id}", response_model=Site)
async def get_site_by_id(site_id: UUID):
    site = crud_site.get(item_id=site_id)
    if not site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not found")
    return site

@router.put("/sites/{site_id}", response_model=Site)
async def update_site(site_id: UUID, site_in: SiteUpdate):
    updated_site = crud_site.update(item_id=site_id, obj_in=site_in)
    if not updated_site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not found")
    return updated_site

@router.patch("/sites/{site_id}", response_model=Site)
async def partial_update_site(site_id: UUID, site_in: SiteUpdate):
    updated_site = crud_site.update(item_id=site_id, obj_in=site_in.model_dump(exclude_unset=True))
    if not updated_site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not found")
    return updated_site

@router.delete("/sites/{site_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_site(site_id: UUID):
    deleted = crud_site.remove(item_id=site_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not found")
    return None

# Add stubs for specific site-related endpoints like /sites/{site_id}/applicable-policies etc.
@router.get("/sites/{site_id}/applicable-policies", response_model=List[dict]) # Replace dict with Policy model
async def get_site_applicable_policies(site_id: UUID):
    # Stub: In a real app, fetch policies related to this site
    return [{"policy_id": "pol-1", "requirement": "30% affordable"}, {"policy_id": "pol-2", "requirement": "Design code compliance"}]

@router.get("/sites/{site_id}/constraints", response_model=List[dict]) # Replace dict with Constraint model
async def get_site_constraints(site_id: UUID):
    return [{"constraint_id": "con-1", "name": "Flood Zone 3"}]

@router.get("/sites/{site_id}/goal-contributions", response_model=List[dict])
async def get_site_goal_contributions(site_id: UUID):
    return [{"goal_id": "goal-1", "contribution": "Supports Housing Target"}]

@router.get("/sites/{site_id}/deliverability-soundness", response_model=dict)
async def get_site_deliverability_soundness(site_id: UUID):
    return {"deliverability_score": 8, "soundness_status": "Sound"}

