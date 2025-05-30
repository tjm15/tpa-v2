import hashlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# TODO: update with your real database URL
database_url = "postgresql://tpa:tpa@localhost:5432/tpa"

_engine = create_engine(database_url)
SessionLocal = sessionmaker(bind=_engine)

@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def hash_file(path: str) -> str:
    """
    Compute the SHA256 hash of a file for idempotency.
    """
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()
