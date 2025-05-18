from typing import List, Optional
from pydantic import BaseModel

class OfficerReportSection(BaseModel):
    id: str
    title: str
    content: str
    order: int

class EvidenceLink(BaseModel):
    name: str
    url_or_id: str

class ComplianceFlag(BaseModel):
    flag: str
    met: bool

class OfficerReport(BaseModel):
    applicationId: str
    version: str
    sections: List[OfficerReportSection]
    recommendation: Optional[str] = None
    supportingEvidenceLinks: Optional[List[EvidenceLink]] = None
    conflictSummary: Optional[str] = None
    complianceFlags: Optional[List[ComplianceFlag]] = None
    lastModified: str
    status: str  # 'Draft' | 'Review' | 'Final'
