import uuid
from sqlalchemy import Column, String, Float, Text, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from app.db_models.base import Base
from app.models.shared import GoalStatus, GoalType

class Goal(Base):
    __tablename__ = "goals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    target_metric = Column(String, nullable=False)
    target_value = Column(Float, nullable=True)
    current_value = Column(Float, nullable=True)
    unit = Column(String, nullable=True)
    source = Column(String, nullable=True)
    status = Column(Enum(GoalStatus), nullable=False)
    type = Column(Enum(GoalType), nullable=False)
    risks = Column(JSONB, nullable=True)
    notes = Column(Text, nullable=True)
    contributing_policy_ids = Column(ARRAY(String), nullable=True)
    contributing_site_ids = Column(ARRAY(String), nullable=True)
    related_goal_ids = Column(ARRAY(String), nullable=True)
