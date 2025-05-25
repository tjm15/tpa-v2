from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class Constraint(BaseModel):
    id: str
    name: str
    type: str  # free-text or from tags[]
    description: Optional[str] = None
    sourcePolicyId: Optional[str] = None
    sourceDocument: Optional[str] = None
    geom: Optional[Dict[str, Any]] = None  # GEOMETRY(POLYGON, 4326) as dict
    createdAt: datetime
