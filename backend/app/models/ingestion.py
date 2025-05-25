from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class SourceFile(BaseModel):
    id: str
    filename: str
    mimeType: str
    extension: Optional[str] = None
    uploadedAt: datetime
    storagePath: str
    sourceUrl: Optional[str] = None
    sha256Hash: Optional[str] = None
    lpaCode: Optional[str] = None
    notes: Optional[str] = None

class ExtractedTextChunk(BaseModel):
    id: str
    fileId: str
    pageNumber: Optional[int] = None
    chunkOrder: int
    chunkText: str
    createdAt: datetime
