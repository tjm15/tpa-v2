from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models.officer_reports import OfficerReport, OfficerReportSection

router = APIRouter(prefix="/planning-applications/{application_id}/officer-report", tags=["OfficerReports"])


@router.get("/", response_model=OfficerReport)
async def get_officer_report(application_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Get the officer report for a given application ID.
    """
    raise HTTPException(status_code=404, detail="OfficerReport not found")


@router.get("/sections", response_model=List[OfficerReportSection])
async def list_officer_report_sections(application_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    List all sections of an officer report for a given application ID.
    """
    # TODO: Implement actual DB fetch logic
    # Example placeholder:
    # report = await get_officer_report_from_db(application_id, db)
    # if not report:
    #     raise HTTPException(status_code=404, detail="OfficerReport not found")
    # return report.sections
    return []
