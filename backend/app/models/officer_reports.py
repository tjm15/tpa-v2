from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class OfficerReportSection(BaseModel):
    applicationId: str
    sectionId: str
    parentSectionId: Optional[str] = None
    title: str
    content: str
    orderNo: int
    agentStage: Optional[str] = None  # tag for generation pass
    createdAt: datetime

class OfficerReport(BaseModel):
    applicationId: str
    aiContextId: Optional[str] = None
    version: str
    status: Optional[List[str]] = None  # dynamic tags
    recommendation: Optional[str] = None
    provenance: Optional[Dict[str, Any]] = None  # e.g. { retrieval_log_id, write_log_id }
    createdBy: Optional[str] = None
    lastEditedBy: Optional[str] = None
    lastModified: datetime
