
from sentence_transformers import SentenceTransformer

# Load the embedding model on CPU
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2",
    device="cpu"
)


def generate_embedding(text: str) -> list[float]:
    """
    Convert text into a 384-dimensional embedding.
    """
    embedding = model.encode(
        text,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embedding.tolist()


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Generate embeddings for multiple text chunks.
    """
    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        batch_size=8
    )

    return embeddings.tolist()
