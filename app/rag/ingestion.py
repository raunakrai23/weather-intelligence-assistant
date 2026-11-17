
from pathlib import Path
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.rag.embeddings import generate_embeddings


def split_text(text: str, chunk_size: int = 500, overlap: int = 50):
    words = text.split()
    chunks = []

    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def ingest_document(file_path: str):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Document not found: {file_path}")

    text = path.read_text(encoding="utf-8")
    chunks = split_text(text)

    embeddings = generate_embeddings(chunks)

    db: Session = SessionLocal()

    try:
        document = Document(
            title=path.name,
            file_path=str(path),
            document_type="text"
        )

        db.add(document)
        db.flush()

        for index, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            db_chunk = DocumentChunk(
                document_id=document.id,
                chunk_text=chunk,
                chunk_index=index,
                embedding=embedding
            )

            db.add(db_chunk)

        db.commit()

        return len(chunks)

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    file_path = "data/documents/weather_safety.txt"

    total_chunks = ingest_document(file_path)

    print("Document ingested successfully!")
    print("Total chunks stored:", total_chunks)
