import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.db_models.base import Base

class Scenario(Base):
    __tablename__ = "scenarios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    baseline_scenario_id = Column(UUID(as_uuid=True), nullable=True)
    tags = Column(JSON, nullable=True)           # List[str]
    summary_metrics = Column(JSON, nullable=True)  # JSON of SummaryMetrics
    included_site_ids = Column(JSON, nullable=True)  # List[UUID]
    excluded_site_ids = Column(JSON, nullable=True)
    active_policy_ids = Column(JSON, nullable=True)
    modified_policies = Column(JSON, nullable=True)  # List of {policyId, changes}
    goal_performance = Column(JSON, nullable=True)
    soundness_flags = Column(JSON, nullable=True)
    ai_commentary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_modified = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # All relevant fields for frontend parity are present as JSON or appropriate types.
