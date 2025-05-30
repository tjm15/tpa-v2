import uuid

from sqlalchemy import Column, String, Text, ForeignKey, TIMESTAMP, NUMERIC
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry
from datetime import datetime
from libs.shared_db_models.base import Base

class Constraint(Base):
    __tablename__ = "constraints"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # free-text or from tags[]
    description = Column(Text, nullable=True)
    source_policy_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("policies.id", ondelete="SET NULL"), 
        nullable=True
    )
    source_document = Column(String, nullable=True)
    geom = Column(Geometry('POLYGON', 4326), nullable=True)  # GEOMETRY(POLYGON, 4326)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class DerivedGeographicConstraint(Base):
    __tablename__ = "derived_geographic_constraints"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    place_name = Column(String, nullable=False)
    constraint_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("constraints.id", ondelete="CASCADE"), 
        nullable=False
    )
    confidence = Column(NUMERIC, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
