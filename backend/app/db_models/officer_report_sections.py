import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db_models.base import Base

class OfficerReportSection(Base):
    __tablename__ = "officer_report_sections"

    application_id = Column(
        UUID(as_uuid=True),
        ForeignKey("officer_reports.application_id", ondelete="CASCADE"),
        nullable=False,
    )
    section_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    parent_section_id = Column(UUID(as_uuid=True), nullable=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    order_no = Column(Integer, nullable=False)
    agent_stage = Column(String, nullable=True)  # tag for generation pass
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
