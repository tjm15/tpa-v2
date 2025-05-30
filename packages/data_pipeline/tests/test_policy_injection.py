import os
import tempfile
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from libs.shared_db_models.base import Base
from libs.shared_db_models.policies import Policy
from libs.shared_db_models.plan_documents import PlanDocument
from libs.shared_db_models.source_files import SourceFile
from libs.shared_db_models.text_chunks import ExtractedTextChunk
from libs.shared_db_models.policy_cross_links import PolicyCrossLink
from libs.shared_db_models.constraints import Constraint
from libs.shared_db_models.vectors import PolicyVector
from libs.shared_db_models.logging import AIEnrichment, WriteLog

# You may need to adjust the import below to point to your orchestrator
from ingest_pipeline.orchestrator import ingest_document

def setup_in_memory_db():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    return engine

@pytest.fixture
def session():
    engine = setup_in_memory_db()
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

# Example test: adjust as needed for your schema and logic
def test_policy_injection_places_data_correctly(session, tmp_path):
    # Prepare dummy PDF and enrichment JSON
    pdf_path = tmp_path / "dummy.pdf"
    enrichment_json_path = tmp_path / "enrich.json"
    pdf_path.write_bytes(b"%PDF-1.4 dummy content")
    enrichment_json_path.write_text('[{"policy_id": "P1", "policy_title": "Test Policy", "summary": "Summary", "page_number": 1}]')

    # Call the injection logic
    ingest_document(
        pdf_path=str(pdf_path),
        enrichment_json_path=str(enrichment_json_path),
        lpa_code="TESTLPA",
        document_name="TestDoc"
    )

    # Now check the database for correct placement
    policies = session.query(Policy).all()
    assert len(policies) == 1
    assert policies[0].policy_id == "P1"
    assert policies[0].policy_title == "Test Policy"
    # Add more assertions for other tables as needed

    # Check that no data is written to wrong tables/fields
    # ...
