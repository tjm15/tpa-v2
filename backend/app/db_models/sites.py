import uuid
from datetime import datetime

from sqlalchemy import Column, String, Float, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from app.db_models.base import Base

class Site(Base):
    __tablename__ = "sites"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=True)
    address = Column(String, nullable=True)
    uprn = Column(String, nullable=True)
    lpa_code = Column(String, nullable=True)
    coordinates = Column(JSON, nullable=True)      # store {lat, lon} or GeoJSON
    area_ha = Column(Float, nullable=True)
    parish = Column(String, nullable=True)
    plan_making_status = Column(String, nullable=True)
    submission_date = Column(DateTime, nullable=True)
    source = Column(String, nullable=True)
    proposed_use_plan_making = Column(String, nullable=True)
    planning_history_summary = Column(ARRAY(String), nullable=True)
    constraints = Column(JSON, nullable=True)
    applicable_policies = Column(JSON, nullable=True)
    policy_requirements_summary = Column(JSON, nullable=True)
    allocation_justification = Column(String, nullable=True)
    ai_draft_justification = Column(String, nullable=True)
    strategic_goal_contributions = Column(JSON, nullable=True)
    deliverability_assessment = Column(JSON, nullable=True)
    soundness_checks_plan_making = Column(JSON, nullable=True)
