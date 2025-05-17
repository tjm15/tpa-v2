# app/routers/goals.py
from fastapi import APIRouter, HTTPException, Query, Depends, status
from typing import List, Optional
from uuid import UUID
from app.models.goal_models import Goal, GoalCreate, GoalUpdate
from app.models.common_models import PaginatedResponse
from app.crud.base_crud import CRUDBase

router = APIRouter()
crud_goal = CRUDBase[Goal, GoalCreate, GoalUpdate](Goal)

@router.post("/goals", response_model=Goal, status_code=status.HTTP_201_CREATED)
async def create_goal(goal_in: GoalCreate):
    return crud_goal.create(obj_in=goal_in)

@router.get("/goals", response_model=PaginatedResponse[Goal])
async def list_goals(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    items = crud_goal.get_multi(skip=skip, limit=limit)
    total_items = len(crud_goal.get_multi(skip=0, limit=10000))
    return PaginatedResponse[Goal](
        items=items,
        total=total_items,
        page=(skip // limit) + 1 if limit > 0 else 1,
        limit=limit,
        totalPages=(total_items + limit - 1) // limit if limit > 0 else 1
    )

@router.get("/goals/{goal_id}", response_model=Goal)
async def get_goal_by_id(goal_id: UUID):
    goal = crud_goal.get(item_id=goal_id)
    if not goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    return goal

@router.put("/goals/{goal_id}", response_model=Goal)
async def update_goal(goal_id: UUID, goal_in: GoalUpdate):
    updated_goal = crud_goal.update(item_id=goal_id, obj_in=goal_in)
    if not updated_goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    return updated_goal

@router.patch("/goals/{goal_id}", response_model=Goal)
async def partial_update_goal(goal_id: UUID, goal_in: GoalUpdate):
    updated_goal = crud_goal.update(item_id=goal_id, obj_in=goal_in.model_dump(exclude_unset=True))
    if not updated_goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    return updated_goal

@router.delete("/goals/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_goal(goal_id: UUID):
    deleted = crud_goal.remove(item_id=goal_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    return None

@router.get("/goals/{goal_id}/performance-summary", response_model=dict) # Define proper response model
async def get_goal_performance_summary(goal_id: UUID):
    # Stub implementation
    goal = crud_goal.get(item_id=goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return {
        "goal_id": goal_id,
        "name": goal.name,
        "status": goal.status,
        "current_value": goal.currentValue,
        "target_value": goal.targetValue,
        "summary": f"Performance summary for {goal.name} (stub)."
    }
