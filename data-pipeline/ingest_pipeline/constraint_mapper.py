import datetime
from ingest_pipeline.models import Constraint, DerivedGeographicConstraint


def map_constraints(
    session,
    enrichments: list,
    plan_doc
):
    now = datetime.datetime.utcnow()
    for item in enrichments:
        for place in item.get('geographic_mentions', []):
            c = Constraint(
                name=place,
                type='geographic',
                source_policy_id=None,
                source_document=str(plan_doc.id),
                created_at=now
            )
            session.add(c)
            session.flush()
            d = DerivedGeographicConstraint(
                place_name=place,
                constraint_id=c.id,
                confidence=0.9
            )
            session.add(d)
    session.flush()
