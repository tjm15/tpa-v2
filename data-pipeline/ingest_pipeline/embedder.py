# File: ingest_pipeline/embedder.py

import os
import datetime
from huggingface_hub import InferenceClient

# Model to use
MODEL = "BAAI/bge-large-en-v1.5"
# Batch size to stay within rate limits
BATCH_SIZE = 50

# Instantiate once
HF_TOKEN = os.getenv("HF_TOKEN")
client = InferenceClient(token=HF_TOKEN)

def generate_embeddings(chunks: list) -> list[dict]:
    """
    Call the HF Inference API to embed each chunk using BGE-large-en-v1.5.
    Returns a list of records ready for ingestion.
    """
    texts = [c["chunk_text"] for c in chunks]
    now = datetime.datetime.utcnow()
    records = []

    # Process each text individually (safer with current API)
    for c in chunks:
        text = c["chunk_text"]
        emb = client.feature_extraction(model=MODEL, text=text)
        
        records.append({
            "source_chunk_id": c["id"],
            # Store as list of floats for pgvector
            "embedding": emb,
            "policy_ref": None,
            "key_themes": [],
            "cross_references": [],
            "geographic_mentions": [],
            "tokens": len(text.split()),
            "model_version": MODEL,
            "created_at": now
        })

    return records

def ingest_vectors(session, vectors: list):
    """
    Insert the embedding records into the policy_vectors table.
    """
    from ingest_pipeline.models import PolicyVector

    for v in vectors:
        pv = PolicyVector(
            source_chunk_id=v["source_chunk_id"],
            embedding=v["embedding"],
            policy_ref=v["policy_ref"],
            key_themes=v["key_themes"],
            cross_references=v["cross_references"],
            geographic_mentions=v["geographic_mentions"],
            tokens=v["tokens"],
            model_version=v["model_version"],
            created_at=v["created_at"]
        )
        session.add(pv)

    session.flush()
