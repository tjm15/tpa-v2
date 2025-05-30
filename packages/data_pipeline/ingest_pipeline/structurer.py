from uuid import uuid4
from pypdf import PdfReader


def extract_nodes(pdf_path: str):
    """
    Treat each PDF page as a document node.
    Returns list of { id, parent_id, title, reference, content, order_no }.
    """
    reader = PdfReader(pdf_path)
    nodes = []
    for idx, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        nodes.append({
            'id': str(uuid4()),
            'parent_id': None,
            'title': f'Page {idx+1}',
            'reference': None,
            'content': text,
            'order_no': idx + 1
        })
    return nodes


def chunk_text(pdf_path: str, nodes: list):
    """
    Break node text into ~2000‑char chunks by paragraphs.
    Returns list of { id, page_number, chunk_order, chunk_text }.
    """
    chunks = []
    for node in nodes:
        paras = [p.strip() for p in node['content'].split('\n\n') if p.strip()]
        current = ''
        order = 1
        for para in paras:
            if len(current) + len(para) + 2 <= 2000:
                current = f"{current}\n\n{para}" if current else para
            else:
                chunks.append({
                    'id': str(uuid4()),
                    'page_number': node['order_no'],
                    'chunk_order': order,
                    'chunk_text': current
                })
                order += 1
                current = para
        if current:
            chunks.append({
                'id': str(uuid4()),
                'page_number': node['order_no'],
                'chunk_order': order,
                'chunk_text': current
            })
    return chunks
