# app/routers/policies.py
from fastapi import APIRouter, HTTPException, Query, Depends, status
from typing import List, Optional
from uuid import UUID
# from sqlalchemy.orm import Session # Example for DB dependency

# from app import crud # Placeholder for CRUD operations
# from app.models import policy_models, common_models
# from app.core.dependencies import get_db # Example for DB dependency

from app.models.policy_models import Policy, PolicyCreate, PolicyUpdate, LinkedPolicy, StrategicGoalAlignmentPolicy
from app.models.common_models import PolicyStatusEnum, PolicyTypeEnum, PaginatedResponse
from app.crud.base_crud import CRUDBase # Using the stubbed CRUDBase

router = APIRouter()

# In-memory store for policies (replace with actual CRUD operations)
# crud_policy = crud.policy # If you had a crud_policy.py
crud_policy = CRUDBase[Policy, PolicyCreate, PolicyUpdate](Policy)


@router.post("/policies", response_model=Policy, status_code=status.HTTP_201_CREATED)
async def create_policy(
    *,
    policy_in: PolicyCreate
    # db: Session = Depends(get_db) # Example for DB dependency
):
    """
    Create a new policy.
    - **reference**: Policy reference (e.g., H2, DM12)
    - **title**: Title of the policy
    - **wording**: Full wording of the policy (can be Markdown/HTML)
    - **status**: Current status of the policy
    - **type**: Type of the policy
    - **documentId**: ID of the PlanDocument this policy belongs to
    - Other optional fields as defined in PolicyCreate schema.
    """
    # policy = crud_policy.create(db=db, obj_in=policy_in) # With DB
    policy = crud_policy.create(obj_in=policy_in)
    return policy

@router.get("/policies", response_model=PaginatedResponse[Policy])
async def list_policies(
    search: Optional[str] = Query(None, description="Search term for ref, title, wording keywords"),
    status_filter: Optional[PolicyStatusEnum] = Query(None, alias="status"), # Use alias for query param name
    type_filter: Optional[PolicyTypeEnum] = Query(None, alias="type"),
    document_id: Optional[UUID] = Query(None),
    skip: int = Query(0, ge=0, alias="page_offset"), # Or use page/limit
    limit: int = Query(20, ge=1, le=100, alias="page_limit"),
    sort_by: Optional[str] = Query(None, description="Field to sort by (e.g., 'reference', 'lastModified')"),
    order: Optional[str] = Query("asc", enum=["asc", "desc"], description="Sort order")
    # db: Session = Depends(get_db)
):
    """
    List all policies with optional filtering, sorting, and pagination.
    """
    filters = {}
    if status_filter:
        filters["status"] = status_filter
    if type_filter:
        filters["type"] = type_filter
    if document_id:
        filters["documentId"] = document_id
    if search: # Basic search stub, needs real implementation
        # This is a placeholder. Real search would involve DB text search capabilities.
        all_items = crud_policy.get_multi(skip=0, limit=1000) # Get all to filter in memory
        items = [
            item for item in all_items
            if (search.lower() in item.reference.lower() or
                search.lower() in item.title.lower() or
                search.lower() in item.wording.lower())
        ]
        # Apply other filters
        if filters:
            items = [item for item in items if all(getattr(item, k, None) == v for k,v in filters.items())]

        # Apply sorting (basic in-memory sort)
        if sort_by and hasattr(Policy, sort_by):
            items.sort(key=lambda x: getattr(x, sort_by), reverse=(order == "desc"))
        
        total_items = len(items)
        paginated_items = items[skip : skip + limit]

    else:
        items = crud_policy.get_multi(skip=skip, limit=limit, **filters)
        # For total, you'd normally do a separate count query if using a DB
        # Here, we just get all and count for simplicity of the stub
        total_items = len(crud_policy.get_multi(skip=0, limit=10000, **filters)) 
        paginated_items = items


    return PaginatedResponse[Policy](
        items=paginated_items,
        total=total_items,
        page=(skip // limit) + 1 if limit > 0 else 1,
        limit=limit,
        totalPages=(total_items + limit - 1) // limit if limit > 0 else 1
    )


@router.get("/policies/{policy_id}", response_model=Policy)
async def get_policy_by_id(
    policy_id: UUID
    # db: Session = Depends(get_db)
):
    """
    Get a specific policy by its ID.
    """
    policy = crud_policy.get(item_id=policy_id)
    if not policy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found")
    return policy

@router.put("/policies/{policy_id}", response_model=Policy)
async def update_policy(
    policy_id: UUID,
    policy_in: PolicyUpdate
    # db: Session = Depends(get_db)
):
    """
    Update an existing policy (full update of provided fields).
    """
    existing_policy = crud_policy.get(item_id=policy_id)
    if not existing_policy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found")
    
    # Add lastModified update
    update_data = policy_in.model_dump(exclude_unset=True)
    update_data['lastModified'] = datetime.utcnow()

    updated_policy = crud_policy.update(item_id=policy_id, obj_in=update_data)
    return updated_policy

@router.patch("/policies/{policy_id}", response_model=Policy)
async def partial_update_policy(
    policy_id: UUID,
    policy_in: PolicyUpdate # Pydantic models automatically handle partial updates if fields are Optional
    # db: Session = Depends(get_db)
):
    """
    Partially update an existing policy. Only fields present in the request body will be updated.
    """
    existing_policy = crud_policy.get(item_id=policy_id)
    if not existing_policy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found")
    
    update_data = policy_in.model_dump(exclude_unset=True)
    if not update_data:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")
    update_data['lastModified'] = datetime.utcnow()

    updated_policy = crud_policy.update(item_id=policy_id, obj_in=update_data)
    return updated_policy


@router.delete("/policies/{policy_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_policy(
    policy_id: UUID
    # db: Session = Depends(get_db)
):
    """
    Delete a policy by its ID.
    """
    deleted_policy = crud_policy.remove(item_id=policy_id)
    if not deleted_policy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found")
    return None # FastAPI handles 204 No Content response automatically


# --- Additional Policy-specific endpoints ---

@router.get("/policies/{policy_id}/linked-policies", response_model=List[LinkedPolicy])
async def get_policy_linked_policies(policy_id: UUID):
    """
    Get policies linked to this policy (relationships).
    Stub implementation.
    """
    policy = crud_policy.get(item_id=policy_id)
    if not policy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found")
    return policy.linkedPolicies or []

@router.get("/policies/{policy_id}/site-impacts", response_model=dict) # Define a proper response model
async def get_policy_site_impacts(policy_id: UUID):
    """
    Get summary of sites impacted by this policy.
    Stub implementation.
    """
    # This would involve querying sites based on policy applicability
    return {"message": f"Site impacts for policy {policy_id} (stub). E.g., 20 sites require affordable housing."}

@router.get("/policies/{policy_id}/goal-alignments", response_model=List[StrategicGoalAlignmentPolicy])
async def get_policy_goal_alignments(policy_id: UUID):
    """
    Get strategic goal alignments for this policy.
    Stub implementation.
    """
    policy = crud_policy.get(item_id=policy_id)
    if not policy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found")
    return policy.strategicGoalAlignments or []

