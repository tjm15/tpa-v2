from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class AIGuidance(BaseModel):
    """AI-generated guidance or suggestion"""
    id: Optional[str] = None
    type: str  # e.g., "policy_suggestion", "wording_improvement", "compliance_check"
    title: str
    content: str
    confidence: Optional[float] = None
    reasoning: Optional[str] = None
    source_references: Optional[List[str]] = None
    created_at: Optional[datetime] = None

class AIResponse(BaseModel):
    """Generic AI response wrapper"""
    success: bool
    content: str
    metadata: Optional[Dict[str, Any]] = None
    confidence: Optional[float] = None
    processing_time: Optional[float] = None