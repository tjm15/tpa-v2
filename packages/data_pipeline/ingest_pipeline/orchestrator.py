from ingest_pipeline.utils import get_session, hash_file
from ingest_pipeline.loaders import load_enrichments
from ingest_pipeline.registrar import (
    check_duplicate, register_source, register_plan_document
)
from ingest_pipeline.structurer import extract_nodes, chunk_text
from ingest_pipeline.enrich_ingester import ingest_enrichments, promote_policies
from ingest_pipeline.constraint_mapper import map_constraints
from ingest_pipeline.embedder import generate_embeddings, ingest_vectors
from ingest_pipeline.logger import write_logs
from ingest_pipeline.models import DocumentNode, ExtractedTextChunk


def ingest_document(
    pdf_path: str,
    enrichment_json_path: str,
    lpa_code: str,
    document_name: str
):
    with get_session() as session:
        sha = hash_file(pdf_path)
        if check_duplicate(session, sha):
            print("⚠️ Document already ingested—skipping.")
            return

        source = register_source(session, pdf_path, sha, lpa_code)
        plan = register_plan_document(session, source, document_name, lpa_code)

        nodes = extract_nodes(pdf_path)
        for n in nodes:
            node = DocumentNode(
                id=n['id'],
                document_id=plan.id,
                parent_id=n['parent_id'],
                title=n['title'],
                reference=n['reference'],
                content=n['content'],
                order_no=n['order_no']
            )
            session.add(node)
        session.flush()

        chunks = chunk_text(pdf_path, nodes)
        db_chunks = []
        for c in chunks:
            chunk = ExtractedTextChunk(
                id=c['id'],
                file_id=source.id,
                page_number=c['page_number'],
                chunk_order=c['chunk_order'],
                chunk_text=c['chunk_text']
            )
            session.add(chunk)
            db_chunks.append(chunk)
        session.flush()

        enrichments = load_enrichments(enrichment_json_path)
        ingest_enrichments(session, enrichments, db_chunks, plan, lpa_code)
        promote_policies(session, enrichments, plan, lpa_code)

        map_constraints(session, enrichments, plan)

        embeddings = generate_embeddings(db_chunks)
        ingest_vectors(session, embeddings)

        write_logs(session, plan.id, enrichments, embeddings)

        session.commit()
        print(f"✅ Ingestion complete for '{document_name}'")
