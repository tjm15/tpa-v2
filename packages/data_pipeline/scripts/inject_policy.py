import argparse
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ingest_pipeline.orchestrator import ingest_document


def main():
    parser = argparse.ArgumentParser(
        description="Inject a policy document into the system."
    )
    parser.add_argument(
        "--pdf", required=True,
        help="Path to the policy PDF file"
    )
    parser.add_argument(
        "--json", required=True,
        help="Path to the enrichment JSON file"
    )
    parser.add_argument(
        "--lpa", required=True,
        help="LPA code for this document"
    )
    parser.add_argument(
        "--name", required=True,
        help="Descriptive name/version of the document"
    )
    args = parser.parse_args()

    ingest_document(
        pdf_path=args.pdf,
        enrichment_json_path=args.json,
        lpa_code=args.lpa,
        document_name=args.name
    )


if __name__ == "__main__":
    main()
