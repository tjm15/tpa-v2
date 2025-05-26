import json

def load_enrichments(path: str):
    """
    Load the enrichment JSON array for policies.
    Returns a list of dicts.
    """
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data
