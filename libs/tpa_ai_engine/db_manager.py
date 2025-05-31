# db_manager.py
# Refactored to use SQLAlchemy and shared models. Removed ingestion and embedding logic.
from sqlalchemy.orm import Session
from libs.shared_db_models.source_files import SourceFile
from libs.shared_db_models.text_chunks import ExtractedTextChunk
from libs.shared_db_models.vectors import PolicyVector, ApplicationVector
from libs.shared_db_models.logging import RetrievalLog
from libs.shared_db_models.plan_documents import PlanDocument

class DatabaseManager:
    def __init__(self, session: Session):
        self.session = session

    def get_source_file_by_id(self, file_id):
        return self.session.query(SourceFile).filter(SourceFile.id == file_id).first()

    def get_plan_document_by_id(self, doc_id):
        return self.session.query(PlanDocument).filter(PlanDocument.id == doc_id).first()

    def get_chunks_by_file_id(self, file_id):
        return self.session.query(ExtractedTextChunk).filter(ExtractedTextChunk.file_id == file_id).order_by(ExtractedTextChunk.page_number, ExtractedTextChunk.chunk_order).all()

    def get_full_document_text_by_file_id(self, file_id):
        chunks = self.get_chunks_by_file_id(file_id)
        return "\n\n".join([str(chunk.chunk_text) for chunk in chunks]) if chunks else None

    def get_full_document_text_by_id(self, file_id):
        # For backward compatibility with retriever
        return self.get_full_document_text_by_file_id(file_id)

    def get_policy_vector_by_chunk_id(self, chunk_id):
        return self.session.query(PolicyVector).filter(PolicyVector.source_chunk_id == chunk_id).first()

    def get_application_vector_by_chunk_id(self, chunk_id):
        return self.session.query(ApplicationVector).filter(ApplicationVector.source_chunk_id == chunk_id).first()

    def log_retrieval(self, query_text, filters, matched_chunk_ids, agent_context):
        log = RetrievalLog(
            query=query_text,
            filters=filters,
            matched_chunk_ids=matched_chunk_ids,
            agent_context=agent_context
        )
        self.session.add(log)
        self.session.commit()
        return log.id

    def execute_query(self, *args, **kwargs):
        # For backward compatibility with retriever
        raise NotImplementedError("Direct SQL execution is not supported. Use SQLAlchemy ORM methods.")
