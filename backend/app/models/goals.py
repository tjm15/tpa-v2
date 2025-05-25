from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class Goal(BaseModel):
    id: str
    name: str
    category: Optional[List[str]] = None  # Changed to array
    description: Optional[str] = None
    targetMetric: Optional[str] = None
    targetValue: Optional[float] = None
    currentValue: Optional[float] = None
    unit: Optional[str] = None
    source: Optional[str] = None
    status: Optional[List[str]] = None  # Changed to array
    type: Optional[List[str]] = None  # Changed to array
    createdAt: datetime
