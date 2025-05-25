import uuid
from datetime import datetime

from sqlalchemy import Column, String, Float, DateTime, TIMESTAMP, Date, REAL
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from geoalchemy2 import Geometry
from app.db_models.base import Base

class Site(Base):
    __tablename__ = "sites"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=True)
    address = Column(String, nullable=True)
    uprn = Column(String, nullable=True)
    lpa_code = Column(String, nullable=True)
    geom = Column(Geometry, nullable=True)  # GEOMETRY type for spatial data
    area_ha = Column(REAL, nullable=True)
    plan_making_status = Column(ARRAY(String), nullable=True)  # Changed to ARRAY
    submission_date = Column(Date, nullable=True)  # Changed to Date
    source = Column(String, nullable=True)
    deliverability_assessment = Column(JSONB, nullable=True)
    soundness_checks = Column(JSONB, nullable=True)  # Renamed from soundness_checks_plan_making
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
