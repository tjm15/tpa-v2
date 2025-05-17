# app/models/constraint_models.py
from typing import Optional, Any, Dict
from pydantic import BaseModel, Field, UUID4
import uuid
from .common_models import ConstraintSeverityEnum, GeoJSONGeometry, BaseUUIDModel

# --- Constraint Model ---
class ConstraintBase(BaseModel):
    name: str = Field(..., examples=["Flood Zone 3"])
    type: str = Field(..., examples=["Flood Risk"])
    severity: Optional[ConstraintSeverityEnum] = None
    sourceDocument: Optional[str] = Field(None, examples=["Environment Agency Flood Map for Planning"])
    geometry: Optional[GeoJSONGeometry] = None # Using Any for flexibility, consider a more specific GeoJSON model
    description: Optional[str] = None

class ConstraintCreate(ConstraintBase):
    pass

class ConstraintUpdate(ConstraintBase):
    name: Optional[str] = None
    type: Optional[str] = None
    # All fields are optional for PATCH

class Constraint(ConstraintBase, BaseUUIDModel):
    pass

    class Config:
        from_attributes = True # for ORM mode
