# Concatenated DB models for debugging purposes

# --- base.py ---
from sqlalchemy.orm import declarative_base
Base = declarative_base()

# --- vectors.py ---
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, ForeignKey, TIMESTAMP, NUMERIC
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

class PolicyVector(Base):
    __tablename__ = "policy_vectors"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_chunk_id = Column(UUID(as_uuid=True), ForeignKey("extracted_text_chunks.id", ondelete="CASCADE"), nullable=False)
    embedding = Column(Vector(1024), nullable=True)  # BGE-large-en-v1.5 produces 1024-dimensional vectors
    policy_ref = Column(String, nullable=True)
    key_themes = Column(ARRAY(String), nullable=True)
    cross_references = Column(ARRAY(String), nullable=True)
    geographic_mentions = Column(ARRAY(String), nullable=True)
    tokens = Column(Integer, nullable=True)
    model_version = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    source_chunk = relationship("ExtractedTextChunk", back_populates="policy_vectors")

class ApplicationVector(Base):
    __tablename__ = "application_vectors"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_chunk_id = Column(UUID(as_uuid=True), ForeignKey("extracted_text_chunks.id", ondelete="CASCADE"), nullable=False)
    application_id = Column(UUID(as_uuid=True), ForeignKey("planning_applications.id", ondelete="SET NULL"), nullable=True)
    embedding = Column(Vector(1024), nullable=True)
    document_type = Column(String, nullable=True)
    section_title = Column(String, nullable=True)
    tokens = Column(Integer, nullable=True)
    model_version = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    source_chunk = relationship("ExtractedTextChunk", back_populates="application_vectors")

class PrecedentVector(Base):
    __tablename__ = "precedent_vectors"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_case_id = Column(UUID(as_uuid=True), ForeignKey("precedent_cases.id", ondelete="CASCADE"), nullable=True)
    embedding = Column(Vector(1024), nullable=True)
    summary = Column(Text, nullable=True)
    key_policies = Column(ARRAY(String), nullable=True)
    site_context = Column(String, nullable=True)
    model_version = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

# --- scenarios.py ---
from sqlalchemy import DateTime, JSON
class Scenario(Base):
    __tablename__ = "scenarios"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    baseline_scenario_id = Column(UUID(as_uuid=True), nullable=True)
    tags = Column(JSON, nullable=True)
    summary_metrics = Column(JSON, nullable=True)
    included_site_ids = Column(JSON, nullable=True)
    excluded_site_ids = Column(JSON, nullable=True)
    active_policy_ids = Column(JSON, nullable=True)
    modified_policies = Column(JSON, nullable=True)
    goal_performance = Column(JSON, nullable=True)
    soundness_flags = Column(JSON, nullable=True)
    ai_commentary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_modified = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# --- logging.py ---
from sqlalchemy import Float
from sqlalchemy.dialects.postgresql import JSONB
class RetrievalLog(Base):
    __tablename__ = "retrieval_logs"
    log_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(TIMESTAMP, default=datetime.utcnow)
    query = Column(Text, nullable=True)
    filters = Column(JSONB, nullable=True)
    matched_chunk_ids = Column(ARRAY(String), nullable=True)
    retrieval_target = Column(String, nullable=True)
    agent_context = Column(JSONB, nullable=True)

class WriteLog(Base):
    __tablename__ = "write_logs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(TIMESTAMP, default=datetime.utcnow)
    output_type = Column(String, nullable=False)
    source_entity = Column(String, nullable=True)
    source_id = Column(UUID(as_uuid=True), nullable=True)
    input_snapshot = Column(JSONB, nullable=True)
    model_version = Column(String, nullable=True)
    output_text = Column(Text, nullable=True)
    author = Column(String, nullable=True, default='LLM')
    confidence = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)

class AIEnrichment(Base):
    __tablename__ = "ai_enrichment"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    target_table = Column(String, nullable=False)
    target_id = Column(UUID(as_uuid=True), nullable=False)
    enrichment_type = Column(String, nullable=False)
    enriched_fields = Column(JSONB, nullable=False)
    model_version = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

# --- planning_applications.py ---
from sqlalchemy import Date
from sqlalchemy.dialects.postgresql import JSONB
class PlanningApplication(Base):
    __tablename__ = "planning_applications"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reference_number = Column(String, nullable=False)
    site_id = Column(UUID(as_uuid=True), ForeignKey("sites.id", ondelete="SET NULL"), nullable=True)
    status = Column(ARRAY(String), nullable=True)
    proposal_details = Column(Text, nullable=False)
    received_date = Column(Date, nullable=False)
    decision_date = Column(Date, nullable=True)
    applicant_name = Column(String, nullable=True)
    agent_name = Column(String, nullable=True)
    case_officer = Column(String, nullable=True)
    planner_weightings = Column(JSONB, nullable=True)
    lpa_code = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    officer_report = relationship("OfficerReport", back_populates="application")
    precedents = relationship("PrecedentCase", back_populates="application")

# --- precedent_cases.py ---
class PrecedentCase(Base):
    __tablename__ = "precedent_cases"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_id = Column(UUID(as_uuid=True), ForeignKey("planning_applications.id", ondelete="SET NULL"), nullable=True)
    case_reference = Column(String, nullable=False)
    address = Column(String, nullable=True)
    decision_date = Column(Date, nullable=True)
    outcome = Column(ARRAY(String), nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    application = relationship("PlanningApplication", back_populates="precedents")

# --- ai_context.py ---
class ApplicationAIContext(Base):
    __tablename__ = "application_ai_context"
    application_id = Column(UUID(as_uuid=True), ForeignKey("planning_applications.id", ondelete="CASCADE"), primary_key=True)
    retrieval_log_id = Column(UUID(as_uuid=True), ForeignKey("retrieval_logs.log_id"), nullable=True)
    reasoning_steps = Column(JSONB, nullable=True)
    competing_goals = Column(JSONB, nullable=True)
    narrative = Column(Text, nullable=True)
    model_version = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class ApplicationMaterialRef(Base):
    __tablename__ = "application_material_refs"
    application_id = Column(UUID(as_uuid=True), ForeignKey("planning_applications.id", ondelete="CASCADE"), primary_key=True)
    material_type = Column(String, primary_key=True)
    material_code = Column(String, primary_key=True)
    material_id = Column(UUID(as_uuid=True), nullable=True)

# --- sites.py ---
from geoalchemy2 import Geometry
from sqlalchemy import REAL
class Site(Base):
    __tablename__ = "sites"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=True)
    address = Column(String, nullable=True)
    uprn = Column(String, nullable=True)
    lpa_code = Column(String, nullable=True)
    geom = Column(Geometry, nullable=True)
    area_ha = Column(REAL, nullable=True)
    plan_making_status = Column(ARRAY(String), nullable=True)
    submission_date = Column(Date, nullable=True)
    source = Column(String, nullable=True)
    deliverability_assessment = Column(JSONB, nullable=True)
    soundness_checks = Column(JSONB, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

# --- plan_documents.py ---
class PlanDocument(Base):
    __tablename__ = "plan_documents"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String, nullable=False)
    name = Column(String, nullable=False)
    version = Column(String, nullable=True)
    document_status = Column(String, nullable=True)
    lpa_code = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    root_nodes = relationship("DocumentNode", back_populates="document")

class DocumentNode(Base):
    __tablename__ = "document_nodes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("plan_documents.id", ondelete="CASCADE"), nullable=False)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("document_nodes.id"), nullable=True)
    title = Column(String, nullable=False)
    reference = Column(String, nullable=True)
    content = Column(Text, nullable=True)
    order_no = Column(Integer, nullable=True)
    last_modified = Column(TIMESTAMP, nullable=True)
    author = Column(String, nullable=True)
    document = relationship("PlanDocument", back_populates="root_nodes")
    children = relationship("DocumentNode", backref="parent", remote_side=[id])

# --- officer_reports.py ---
class OfficerReport(Base):
    __tablename__ = "officer_reports"
    application_id = Column(UUID(as_uuid=True), ForeignKey("planning_applications.id", ondelete="CASCADE"), primary_key=True)
    ai_context_id = Column(UUID(as_uuid=True), ForeignKey("application_ai_context.application_id"), nullable=True)
    version = Column(String, nullable=False)
    status = Column(ARRAY(String), nullable=True)
    recommendation = Column(Text, nullable=True)
    provenance = Column(JSONB, nullable=True)
    created_by = Column(String, nullable=True)
    last_edited_by = Column(String, nullable=True)
    last_modified = Column(TIMESTAMP, default=datetime.utcnow)
    application = relationship("PlanningApplication", back_populates="officer_report")

# --- source_files.py ---
class SourceFile(Base):
    __tablename__ = "source_files"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String, nullable=False)
    mime_type = Column(String, nullable=False)
    extension = Column(String, nullable=True)
    uploaded_at = Column(TIMESTAMP, default=datetime.utcnow)
    storage_path = Column(String, nullable=False)
    source_url = Column(String, nullable=True)
    sha256_hash = Column(String, nullable=True)
    lpa_code = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    text_chunks = relationship("ExtractedTextChunk", back_populates="source_file")

# --- officer_report_sections.py ---
class OfficerReportSection(Base):
    __tablename__ = "officer_report_sections"
    application_id = Column(UUID(as_uuid=True), ForeignKey("officer_reports.application_id", ondelete="CASCADE"), nullable=False)
    section_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    parent_section_id = Column(UUID(as_uuid=True), nullable=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    order_no = Column(Integer, nullable=False)
    agent_stage = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

# --- policies.py ---
class Policy(Base):
    __tablename__ = "policies"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    policy_id = Column(String, nullable=True)
    policy_title = Column(String, nullable=False)
    tags = Column(ARRAY(String), nullable=True)
    summary = Column(Text, nullable=False)
    cross_references = Column(ARRAY(String), nullable=True)
    geographic_mentions = Column(ARRAY(String), nullable=True)
    document_id = Column(UUID(as_uuid=True), ForeignKey("plan_documents.id", ondelete="SET NULL"), nullable=True)
    lpa_code = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

# --- precedent_key_policies.py ---
class PrecedentKeyPolicy(Base):
    __tablename__ = "precedent_key_policies"
    precedent_id = Column(UUID(as_uuid=True), ForeignKey("precedent_cases.id", ondelete="CASCADE"), primary_key=True)
    policy_code = Column(String, primary_key=True)
    policy_id = Column(UUID(as_uuid=True), nullable=True)

# --- text_chunks.py ---
class ExtractedTextChunk(Base):
    __tablename__ = "extracted_text_chunks"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_id = Column(UUID(as_uuid=True), ForeignKey("source_files.id", ondelete="CASCADE"), nullable=False)
    page_number = Column(Integer, nullable=True)
    chunk_order = Column(Integer, nullable=False)
    chunk_text = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    source_file = relationship("SourceFile", back_populates="text_chunks")
    policy_vectors = relationship("PolicyVector", back_populates="source_chunk")
    application_vectors = relationship("ApplicationVector", back_populates="source_chunk")

# --- constraints.py ---
from geoalchemy2 import Geometry
class Constraint(Base):
    __tablename__ = "constraints"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    source_policy_id = Column(UUID(as_uuid=True), ForeignKey("policies.id", ondelete="SET NULL"), nullable=True)
    source_document = Column(String, nullable=True)
    geom = Column(Geometry('POLYGON', 4326), nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class DerivedGeographicConstraint(Base):
    __tablename__ = "derived_geographic_constraints"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    place_name = Column(String, nullable=False)
    constraint_id = Column(UUID(as_uuid=True), ForeignKey("constraints.id", ondelete="CASCADE"), nullable=False)
    confidence = Column(NUMERIC, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

# --- goals.py ---
from sqlalchemy import NUMERIC
class Goal(Base):
    __tablename__ = "goals"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    category = Column(ARRAY(String), nullable=True)
    description = Column(Text, nullable=True)
    target_metric = Column(String, nullable=True)
    target_value = Column(NUMERIC, nullable=True)
    current_value = Column(NUMERIC, nullable=True)
    unit = Column(String, nullable=True)
    source = Column(String, nullable=True)
    status = Column(ARRAY(String), nullable=True)
    type = Column(ARRAY(String), nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

# --- policy_cross_links.py ---
class PolicyCrossLink(Base):
    __tablename__ = "policy_cross_links"
    source_policy_code = Column(String, primary_key=True)
    target_policy_code = Column(String, primary_key=True)
    source_policy_id = Column(UUID(as_uuid=True), ForeignKey("policies.id", ondelete="SET NULL"), nullable=True)
    target_policy_id = Column(UUID(as_uuid=True), ForeignKey("policies.id", ondelete="SET NULL"), nullable=True)

