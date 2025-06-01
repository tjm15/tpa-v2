import datetime
from libs.shared_db_models.spatial_designations import SpatialDesignation, DerivedGeographicSpatialDesignation

def map_spatial_designations(
    session,
    enrichments: list,
    plan_doc
):
    now = datetime.datetime.utcnow()
    for item in enrichments:
        for place in item.get('geographic_mentions', []):
            sd = SpatialDesignation(
                name=place,
                type='geographic',
                source_policy_id=None,
                source_document=str(plan_doc.id),
                created_at=now
            )
            session.add(sd)
            session.flush()
            d = DerivedGeographicSpatialDesignation(
                place_name=place,
                spatial_designation_id=sd.id,
                confidence=0.9
            )
            session.add(d)
    session.flush()
