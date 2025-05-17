# app/routers/planning_applications.py
from fastapi import APIRouter, HTTPException, Query, Depends, status
from typing import List, Optional
from uuid import UUID
from app.models.planning_application_models import PlanningApplication, PlanningApplicationCreate, PlanningApplicationUpdate, ReasoningStep
from app.models.officer_report_models import OfficerReport, OfficerReportCreate, OfficerReportUpdate, OfficerReportSection, OfficerReportSectionCreate
from app.models.common_models import PaginatedResponse
from app.crud.base_crud import CRUDBase

router = APIRouter()
crud_planning_application = CRUDBase[PlanningApplication, PlanningApplicationCreate, PlanningApplicationUpdate](PlanningApplication)
# For officer reports, assuming they are tightly coupled and managed via application ID
crud_officer_report = CRUDBase[OfficerReport, OfficerReportCreate, OfficerReportUpdate](OfficerReport) # Simplified stub

@router.post("/planning-applications", response_model=PlanningApplication, status_code=status.HTTP_201_CREATED)
async def create_planning_application(application_in: PlanningApplicationCreate):
    return crud_planning_application.create(obj_in=application_in)

@router.get("/planning-applications", response_model=PaginatedResponse[PlanningApplication])
async def list_planning_applications(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    items = crud_planning_application.get_multi(skip=skip, limit=limit)
    total_items = len(crud_planning_application.get_multi(skip=0, limit=10000))
    return PaginatedResponse[PlanningApplication](
        items=items,
        total=total_items,
        page=(skip // limit) + 1 if limit > 0 else 1,
        limit=limit,
        totalPages=(total_items + limit - 1) // limit if limit > 0 else 1
    )

@router.get("/planning-applications/{application_id}", response_model=PlanningApplication)
async def get_planning_application_by_id(application_id: UUID):
    application = crud_planning_application.get(item_id=application_id)
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Planning Application not found")
    return application

@router.put("/planning-applications/{application_id}", response_model=PlanningApplication)
async def update_planning_application(application_id: UUID, application_in: PlanningApplicationUpdate):
    updated_application = crud_planning_application.update(item_id=application_id, obj_in=application_in)
    if not updated_application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Planning Application not found")
    return updated_application
    
@router.patch("/planning-applications/{application_id}", response_model=PlanningApplication)
async def partial_update_planning_application(application_id: UUID, application_in: PlanningApplicationUpdate):
    updated_application = crud_planning_application.update(item_id=application_id, obj_in=application_in.model_dump(exclude_unset=True))
    if not updated_application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Planning Application not found")
    return updated_application

@router.delete("/planning-applications/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_planning_application(application_id: UUID):
    deleted = crud_planning_application.remove(item_id=application_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Planning Application not found")
    # Also delete associated officer report if any (cascade logic)
    # For stub, this is manual. In real app, DB relations or service layer handles this.
    # Example: crud_officer_report.remove_by_application_id(application_id)
    return None

# --- Officer Report Sub-resource ---
@router.post("/planning-applications/{application_id}/officer-report", response_model=OfficerReport, status_code=status.HTTP_201_CREATED)
async def create_officer_report_for_application(application_id: UUID, report_in: OfficerReportCreate):
    # Check if application exists
    if not crud_planning_application.get(item_id=application_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Planning Application not found")
    # In a real app, ensure only one report per application or handle versioning
    # For stub, we directly create. The OfficerReport model itself doesn't have application_id for create.
    # We'd associate it here.
    report_data_with_app_id = report_in.model_dump()
    report_data_with_app_id["applicationId"] = application_id
    
    # Use a temporary model that includes applicationId for creation if OfficerReportCreate doesn't
    class TempOfficerReportCreate(OfficerReportCreate):
        applicationId: UUID
        
    created_report = crud_officer_report.create(obj_in=TempOfficerReportCreate(**report_data_with_app_id))
    return created_report


@router.get("/planning-applications/{application_id}/officer-report", response_model=Optional[OfficerReport])
async def get_officer_report_for_application(application_id: UUID):
    # This assumes officer_report is stored with application_id as a key or relation
    # For stub, we filter the in-memory store
    reports = [r for r_id, r in crud_officer_report._db.items() if hasattr(r, 'applicationId') and r.applicationId == application_id]
    if not reports:
        # It's okay for an application to not have a report yet
        return None
    return reports[0] # Assuming one report per application for simplicity

# Add PUT, PATCH, DELETE for officer reports and sections

@router.post("/planning-applications/{application_id}/officer-report/sections", response_model=OfficerReportSection)
async def add_officer_report_section(application_id: UUID, section_in: OfficerReportSectionCreate):
    # Stub: Get report, add section, save report
    reports = [r for r_id, r in crud_officer_report._db.items() if hasattr(r, 'applicationId') and r.applicationId == application_id]
    if not reports:
        raise HTTPException(status_code=404, detail="Officer report not found for this application")
    report = reports[0]
    
    new_section_id = uuid.uuid4()
    new_section = OfficerReportSection(id=new_section_id, **section_in.model_dump())
    report.sections.append(new_section)
    crud_officer_report.update(item_id=report.applicationId, obj_in=report) # Assuming report ID is app ID for stub
    return new_section


# Stubs for other DM specific endpoints
@router.get("/planning-applications/{application_id}/site-assessment", response_model=dict)
async def get_application_site_assessment(application_id: UUID):
    return {"message": f"Site assessment data for application {application_id} (stub)"}

@router.get("/planning-applications/{application_id}/reasoning", response_model=dict)
async def get_application_reasoning_data(application_id: UUID):
    app = crud_planning_application.get(item_id=application_id)
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    return {
        "relevantPolicies": app.relevantPolicies,
        "reasoningSteps": app.reasoningSteps,
        "tradeOffAnalysis": app.tradeOffAnalysis
    }

@router.post("/planning-applications/{application_id}/reasoning/steps", response_model=ReasoningStep)
async def add_reasoning_step(application_id: UUID, step_in: ReasoningStep):
    # Stub: Add step to application's reasoningSteps
    app = crud_planning_application.get(item_id=application_id)
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    if app.reasoningSteps is None:
        app.reasoningSteps = []
    app.reasoningSteps.append(step_in)
    crud_planning_application.update(item_id=application_id, obj_in=app)
    return step_in

@router.post("/planning-applications/{application_id}/linked-precedents", response_model=dict)
async def link_precedent_to_application(application_id: UUID, precedent_link: dict = {"precedentCaseId": "uuid"}):
    # Stub: Link precedent_link["precedentCaseId"] to application
    return {"message": f"Precedent {precedent_link.get('precedentCaseId')} linked to application {application_id} (stub)"}

