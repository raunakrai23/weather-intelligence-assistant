
from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk
from app.rag.embeddings import generate_embedding


def retrieve_relevant_chunks(
    db: Session,
    query: str,
    top_k: int = 3
) -> list[DocumentChunk]:

    query_embedding = generate_embedding(query)

    results = (
        db.query(DocumentChunk)
        .order_by(
            DocumentChunk.embedding.cosine_distance(query_embedding)
        )
        .limit(top_k)
        .all()
    )

    return results
