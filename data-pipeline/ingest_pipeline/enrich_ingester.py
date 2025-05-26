import datetime
from difflib import SequenceMatcher
from ingest_pipeline.models import AIEnrichment, Policy, PolicyCrossLink


def ingest_enrichments(
    session,
    enrichments: list,
    chunks: list,
    plan_doc,
    lpa_code: str
):
    now = datetime.datetime.utcnow()
    for item in enrichments:
        # find best chunk match by page and text similarity
        best = None
        best_score = 0.0
        for c in chunks:
            if c.page_number != item.get('page_number'):
                continue
            snippet = c.chunk_text[: len(item.get('summary', ''))]
            score = SequenceMatcher(None, item.get('summary', ''), snippet).ratio()
            if score > best_score:
                best_score, best = score, c
        
        if best is None:
            print(f"Warning: No matching chunk found for enrichment policy_id {item.get('policy_id', 'unknown')} on page {item.get('page_number', 'unknown')}")
            continue  # Skip this enrichment instead of creating with null target_id
            
        target_id = best.id
        enrich = AIEnrichment(
            target_table='extracted_text_chunks',
            target_id=target_id,
            enrichment_type='policy_metadata',
            enriched_fields=item,
            model_version=item.get('model_version', 'unknown'),
            created_at=now
        )
        session.add(enrich)
    session.flush()


def promote_policies(
    session,
    enrichments: list,
    plan_doc,
    lpa_code: str
):
    now = datetime.datetime.utcnow()
    for item in enrichments:
        pol = (
            session.query(Policy)
            .filter(
                Policy.policy_id == item['policy_id'],
                Policy.document_id == plan_doc.id
            )
            .first()
        )
        if not pol:
            pol = Policy(
                policy_id=item['policy_id'],
                policy_title=item['policy_title'],
                summary=item['summary'],
                tags=item.get('targets', []),
                cross_references=item.get('cross_references', []),
                geographic_mentions=item.get('geographic_mentions', []),
                document_id=plan_doc.id,
                lpa_code=lpa_code,
                created_at=now
            )
        else:
            pol.summary = item['summary']
            pol.cross_references = item.get('cross_references', [])
            pol.geographic_mentions = item.get('geographic_mentions', [])
        session.add(pol)

        # cross-links
        for code in item.get('cross_references', []):
            link = PolicyCrossLink(
                source_policy_code=item['policy_id'],
                target_policy_code=code,
                source_policy_id=pol.id
            )
            session.add(link)
    session.flush()
