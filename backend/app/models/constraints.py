from typing import Optional
from pydantic import BaseModel

class Constraint(BaseModel):
    id: str
    name: str
    type: str
    severity: Optional[str] = None
    sourceDocument: Optional[str] = None
    geometry: Optional[dict] = None
    description: Optional[str] = None
