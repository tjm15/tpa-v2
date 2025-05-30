import datetime
from libs.shared_db_models.source_files import SourceFile
from libs.shared_db_models.plan_documents import PlanDocument
from ingest_pipeline.utils import hash_file


def check_duplicate(session, sha256_hash: str) -> bool:
    return (
        session.query(SourceFile)
        .filter(SourceFile.sha256_hash == sha256_hash)
        .first() is not None
    )


def register_source(
    session,
    filepath: str,
    sha256_hash: str,
    lpa_code: str
):
    now = datetime.datetime.utcnow()
    sf = SourceFile(
        filename=filepath.split('/')[-1],
        mime_type='application/pdf',
        extension='pdf',
        storage_path=filepath,
        sha256_hash=sha256_hash,
        lpa_code=lpa_code,
        uploaded_at=now
    )
    session.add(sf)
    session.flush()
    return sf


def register_plan_document(
    session,
    source: SourceFile,
    name: str,
    lpa_code: str
):
    now = datetime.datetime.utcnow()
    pd = PlanDocument(
        filename=source.filename,
        name=name,
        version='v1',
        document_status='active',
        lpa_code=lpa_code,
        created_at=now
    )
    session.add(pd)
    session.flush()
    return pd
