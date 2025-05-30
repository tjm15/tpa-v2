import datetime
from libs.shared_db_models.logging import WriteLog


def write_logs(
    session,
    source_id,
    enrichments: list,
    vector_records: list
):
    now = datetime.datetime.utcnow()
    steps = [
        'register_source', 'register_document', 'structuring',
        'chunking', 'enrichment', 'policy_promotion',
        'constraint_mapping', 'vector_indexing'
    ]
    for step in steps:
        log = WriteLog(
            timestamp=now,
            output_type=step,
            source_entity='plan_document',
            source_id=source_id,
            input_snapshot={},
            model_version=None,
            output_text=f"Step {step} completed",
            author='pipeline',
            confidence=None
        )
        session.add(log)
    session.flush()
