# app/models/officer_report_models.py
from typing import Optional, List
from pydantic import BaseModel, Field, UUID4, HttpUrl
import uuid
from datetime import datetime
from .common_models import OfficerReportStatusEnum, BaseUUIDModel

class OfficerReportSectionBase(BaseModel):
    title: str = Field(..., examples=["Introduction", "Site Context"])
    content: str # Markdown or rich text
    order: int

class OfficerReportSectionCreate(OfficerReportSectionBase):
    pass

class OfficerReportSectionUpdate(OfficerReportSectionBase):
    title: Optional[str] = None
    content: Optional[str] = None
    order: Optional[int] = None
    # All fields are optional for PATCH

class OfficerReportSection(OfficerReportSectionBase, BaseUUIDModel):
    pass

    class Config:
        from_attributes = True


class SupportingEvidenceLink(BaseModel):
    name: str
    url_or_id: str # Could be a URL or an internal ID to another resource

class ComplianceFlag(BaseModel):
    flag: str
    met: bool

# --- OfficerReport Model ---
class OfficerReportBase(BaseModel):
    # applicationId: UUID4 # This will be a path parameter, not in body for create/update typically
    version: str
    sections: List[OfficerReportSection] = Field(default_factory=list)
    recommendation: Optional[str] = None
    supportingEvidenceLinks: Optional[List[SupportingEvidenceLink]] = Field(default_factory=list)
    conflictSummary: Optional[str] = None
    complianceFlags: Optional[List[ComplianceFlag]] = Field(default_factory=list)
    status: OfficerReportStatusEnum

class OfficerReportCreate(OfficerReportBase):
    pass

class OfficerReportUpdate(OfficerReportBase):
    version: Optional[str] = None
    status: Optional[OfficerReportStatusEnum] = None
    # All fields are optional for PATCH

class OfficerReport(OfficerReportBase): # No BaseUUIDModel as it's tied to application
    applicationId: UUID4 # Added for response model clarity
    lastModified: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True
