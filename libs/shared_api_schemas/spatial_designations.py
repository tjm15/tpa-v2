from typing import Optional, Dict, Any
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel

class SpatialDesignation(BaseModel):
    id: str
    name: str
    type: str  # free-text or from tags[]
    description: Optional[str] = None
    sourcePolicyId: Optional[str] = None
    sourceDocument: Optional[str] = None
    geom: Optional[Dict[str, Any]] = None  # GEOMETRY(POLYGON, 4326) as dict
    createdAt: datetime

class DerivedGeographicSpatialDesignation(BaseModel):
    id: str
    placeName: str
    spatialDesignationId: str
    confidence: Optional[Decimal] = None
    createdAt: datetime
