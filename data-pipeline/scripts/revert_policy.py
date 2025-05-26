# File: scripts/revert_policy.py

import argparse
import sys
import os
from sqlalchemy import or_

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ingest_pipeline.utils import get_session
from ingest_pipeline.models import (
    SourceFile,
    PlanDocument,
    DocumentNode,
    ExtractedTextChunk,
    AIEnrichment,
    Policy,
    PolicyCrossLink,
    Constraint,
    DerivedGeographicConstraint,
    PolicyVector,
    WriteLog
)

def list_documents():
    """List all available documents that can be reverted"""
    with get_session() as session:
        docs = session.query(PlanDocument).all()
        files = session.query(SourceFile).all()
        
        print("📋 Available documents to revert:")
        print("=" * 50)
        
        if not docs:
            print("   No PlanDocuments found in database")
        else:
            print("   PlanDocuments:")
            for doc in docs:
                print(f"     LPA: {doc.lpa_code} | Name: {doc.name} | File: {doc.filename}")
        
        print()
        if not files:
            print("   No SourceFiles found in database")
        else:
            print("   SourceFiles:")
            for file in files:
                print(f"     LPA: {file.lpa_code} | File: {file.filename}")
        print()

def revert(lpa_code: str, name: str, filename: str):
    try:
        with get_session() as session:
            print(f"🔍 Looking for document '{name}' and file '{filename}' for LPA '{lpa_code}'...")
            
            # 1. Find the plan_document and source_file
            pd = (
                session.query(PlanDocument)
                .filter_by(lpa_code=lpa_code, name=name)
                .first()
            )
            if not pd:
                print(f"[ERROR] No PlanDocument '{name}' for LPA '{lpa_code}'", file=sys.stderr)
                print("\nℹ️  Available documents:")
                list_documents()
                return

            sf = (
                session.query(SourceFile)
                .filter_by(lpa_code=lpa_code, filename=filename)
                .first()
            )
            if not sf:
                print(f"[ERROR] No SourceFile '{filename}' for LPA '{lpa_code}'", file=sys.stderr)
                print("\nℹ️  Available documents:")
                list_documents()
                return

            print(f"✅ Found PlanDocument ID: {pd.id}")
            print(f"✅ Found SourceFile ID: {sf.id}")

            # 2. Delete write_logs for this document
            print("🗑️  Deleting write logs...")
            write_log_count = session.query(WriteLog) \
                .filter(WriteLog.source_entity=='plan_document', WriteLog.source_id==pd.id) \
                .count()
            session.query(WriteLog) \
                .filter(WriteLog.source_entity=='plan_document', WriteLog.source_id==pd.id) \
                .delete(synchronize_session=False)
            print(f"   Deleted {write_log_count} write log entries")

            # 3. Delete vectors & enrichments tied to this source_file
            print("🗑️  Deleting vectors and enrichments...")
            chunk_ids = [
                c.id for c in session.query(ExtractedTextChunk.id)
                            .filter(ExtractedTextChunk.file_id==sf.id)
            ]
            print(f"   Found {len(chunk_ids)} text chunks")
            
            if chunk_ids:
                # Delete policy vectors
                vector_count = session.query(PolicyVector) \
                    .filter(PolicyVector.source_chunk_id.in_(chunk_ids)) \
                    .count()
                session.query(PolicyVector) \
                    .filter(PolicyVector.source_chunk_id.in_(chunk_ids)) \
                    .delete(synchronize_session=False)
                print(f"   Deleted {vector_count} policy vectors")

                # Delete AI enrichments for chunks
                chunk_enrichment_count = session.query(AIEnrichment) \
                    .filter(
                        AIEnrichment.target_table=='extracted_text_chunks',
                        AIEnrichment.target_id.in_(chunk_ids)
                    ) \
                    .count()
                session.query(AIEnrichment) \
                    .filter(
                        AIEnrichment.target_table=='extracted_text_chunks',
                        AIEnrichment.target_id.in_(chunk_ids)
                    ) \
                    .delete(synchronize_session=False)
                print(f"   Deleted {chunk_enrichment_count} chunk enrichments")

            # 4. Delete policies + cross-links for this plan_document
            print("🗑️  Deleting policies and cross-links...")
            policy_ids = [
                p.id for p in session.query(Policy.id)
                            .filter(Policy.document_id == pd.id)
            ]
            print(f"   Found {len(policy_ids)} policies")
            
            if policy_ids:
                # Delete AI enrichments for policies
                policy_enrichment_count = session.query(AIEnrichment) \
                    .filter(
                        AIEnrichment.target_table=='policies',
                        AIEnrichment.target_id.in_(policy_ids)
                    ) \
                    .count()
                session.query(AIEnrichment) \
                    .filter(
                        AIEnrichment.target_table=='policies',
                        AIEnrichment.target_id.in_(policy_ids)
                    ) \
                    .delete(synchronize_session=False)
                print(f"   Deleted {policy_enrichment_count} policy enrichments")

                # Delete any cross‐links where either side references our policies
                crosslink_count = session.query(PolicyCrossLink) \
                    .filter(
                        or_(
                            PolicyCrossLink.source_policy_id.in_(policy_ids),
                            PolicyCrossLink.target_policy_id.in_(policy_ids)
                        )
                    ) \
                    .count()
                session.query(PolicyCrossLink) \
                    .filter(
                        or_(
                            PolicyCrossLink.source_policy_id.in_(policy_ids),
                            PolicyCrossLink.target_policy_id.in_(policy_ids)
                        )
                    ) \
                    .delete(synchronize_session=False)
                print(f"   Deleted {crosslink_count} policy cross-links")

                # Then delete the policies themselves
                session.query(Policy) \
                    .filter(Policy.id.in_(policy_ids)) \
                    .delete(synchronize_session=False)
                print(f"   Deleted {len(policy_ids)} policies")

            # 5. Delete constraints & derived constraints
            print("🗑️  Deleting constraints...")
            const_ids = [
                c.id for c in session.query(Constraint.id)
                            .filter(Constraint.source_document==str(pd.id))
            ]
            print(f"   Found {len(const_ids)} constraints")
            
            if const_ids:
                derived_count = session.query(DerivedGeographicConstraint) \
                    .filter(DerivedGeographicConstraint.constraint_id.in_(const_ids)) \
                    .count()
                session.query(DerivedGeographicConstraint) \
                    .filter(DerivedGeographicConstraint.constraint_id.in_(const_ids)) \
                    .delete(synchronize_session=False)
                print(f"   Deleted {derived_count} derived geographic constraints")

                session.query(Constraint) \
                    .filter(Constraint.id.in_(const_ids)) \
                    .delete(synchronize_session=False)
                print(f"   Deleted {len(const_ids)} constraints")

            # 6. Delete document nodes & text chunks
            print("🗑️  Deleting document nodes and text chunks...")
            node_count = session.query(DocumentNode) \
                .filter(DocumentNode.document_id==pd.id) \
                .count()
            session.query(DocumentNode) \
                .filter(DocumentNode.document_id==pd.id) \
                .delete(synchronize_session=False)
            print(f"   Deleted {node_count} document nodes")

            chunk_count = session.query(ExtractedTextChunk) \
                .filter(ExtractedTextChunk.file_id==sf.id) \
                .count()
            session.query(ExtractedTextChunk) \
                .filter(ExtractedTextChunk.file_id==sf.id) \
                .delete(synchronize_session=False)
            print(f"   Deleted {chunk_count} text chunks")

            # 7. Delete the plan_document and source_file themselves
            print("🗑️  Deleting plan document and source file...")
            session.delete(pd)
            session.delete(sf)

            session.commit()
            print(f"✅ Successfully reverted ingestion for document '{name}' (LPA {lpa_code})")
            
    except Exception as e:
        print(f"❌ Error during revert: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Revert a previously injected policy document")
    parser.add_argument("--list", action="store_true", help="List all available documents that can be reverted")
    parser.add_argument("--lpa", required=False, help="LPA code used during inject")
    parser.add_argument("--name", required=False, help="Document name used during inject")
    parser.add_argument("--file", required=False, help="PDF filename used during inject")
    args = parser.parse_args()
    
    if args.list:
        list_documents()
    elif args.lpa and args.name and args.file:
        revert(args.lpa, args.name, args.file)
    else:
        print("Error: Either use --list to see available documents, or provide --lpa, --name, and --file arguments")
        parser.print_help()
