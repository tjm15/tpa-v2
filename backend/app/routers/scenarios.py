# app/routers/scenarios.py
from fastapi import APIRouter, HTTPException, Query, Depends, status
from typing import List, Optional
from uuid import UUID
from app.models.scenario_models import Scenario, ScenarioCreate, ScenarioUpdate
from app.models.common_models import PaginatedResponse
from app.crud.base_crud import CRUDBase

router = APIRouter()
crud_scenario = CRUDBase[Scenario, ScenarioCreate, ScenarioUpdate](Scenario)

@router.post("/scenarios", response_model=Scenario, status_code=status.HTTP_201_CREATED)
async def create_scenario(scenario_in: ScenarioCreate):
    return crud_scenario.create(obj_in=scenario_in)

@router.get("/scenarios", response_model=PaginatedResponse[Scenario])
async def list_scenarios(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    items = crud_scenario.get_multi(skip=skip, limit=limit)
    total_items = len(crud_scenario.get_multi(skip=0, limit=10000))
    return PaginatedResponse[Scenario](
        items=items,
        total=total_items,
        page=(skip // limit) + 1 if limit > 0 else 1,
        limit=limit,
        totalPages=(total_items + limit - 1) // limit if limit > 0 else 1
    )

@router.get("/scenarios/{scenario_id}", response_model=Scenario)
async def get_scenario_by_id(scenario_id: UUID):
    scenario = crud_scenario.get(item_id=scenario_id)
    if not scenario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scenario not found")
    return scenario

@router.put("/scenarios/{scenario_id}", response_model=Scenario)
async def update_scenario(scenario_id: UUID, scenario_in: ScenarioUpdate):
    updated_scenario = crud_scenario.update(item_id=scenario_id, obj_in=scenario_in)
    if not updated_scenario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scenario not found")
    return updated_scenario

@router.patch("/scenarios/{scenario_id}", response_model=Scenario)
async def partial_update_scenario(scenario_id: UUID, scenario_in: ScenarioUpdate):
    updated_scenario = crud_scenario.update(item_id=scenario_id, obj_in=scenario_in.model_dump(exclude_unset=True))
    if not updated_scenario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scenario not found")
    return updated_scenario

@router.delete("/scenarios/{scenario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scenario(scenario_id: UUID):
    deleted = crud_scenario.remove(item_id=scenario_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scenario not found")
    return None

@router.post("/scenarios/{scenario_id}/duplicate", response_model=Scenario)
async def duplicate_scenario(scenario_id: UUID):
    # Stub implementation
    original_scenario = crud_scenario.get(item_id=scenario_id)
    if not original_scenario:
        raise HTTPException(status_code=404, detail="Original scenario not found")
    
    # Create a new scenario based on the original, modify name, new ID will be generated
    new_scenario_data = original_scenario.model_copy(update={"name": f"{original_scenario.name} (Copy)"}).model_dump()
    del new_scenario_data['id'] # Remove old ID so a new one is generated
    if 'createdAt' in new_scenario_data: del new_scenario_data['createdAt']
    if 'lastModified' in new_scenario_data: del new_scenario_data['lastModified']

    # Use ScenarioCreate model if it has specific fields for creation
    # For simplicity, directly using the dict from the original model
    duplicated_scenario_create = ScenarioCreate(**new_scenario_data)
    
    new_scenario = crud_scenario.create(obj_in=duplicated_scenario_create)
    return new_scenario

@router.get("/scenarios/{scenario_id}/comparison", response_model=dict) # Define proper response model
async def compare_scenario(scenario_id: UUID, baseline_scenario_id: UUID = Query(...)):
    # Stub implementation
    return {"message": f"Comparison details for scenario {scenario_id} against baseline {baseline_scenario_id} (stub)."}

