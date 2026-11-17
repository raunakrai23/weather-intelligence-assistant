
from unittest.mock import patch, MagicMock

from app.rag.retrieval import retrieve_relevant_chunks


def test_retrieve_relevant_chunks():
    mock_db = MagicMock()

    mock_chunks = [
        MagicMock(chunk_text="Avoid travelling through flooded roads."),
        MagicMock(chunk_text="Follow official weather warnings.")
    ]

    mock_db.query.return_value.order_by.return_value.limit.return_value.all.return_value = mock_chunks

    with patch(
        "app.rag.retrieval.generate_embedding",
        return_value=[0.1] * 384
    ):
        result = retrieve_relevant_chunks(
            db=mock_db,
            query="What precautions should I take during heavy rainfall?",
            top_k=2
        )

    assert len(result) == 2
    assert result[0].chunk_text == "Avoid travelling through flooded roads."
    assert result[1].chunk_text == "Follow official weather warnings."


def test_retrieve_no_chunks():
    mock_db = MagicMock()

    mock_db.query.return_value.order_by.return_value.limit.return_value.all.return_value = []

    with patch(
        "app.rag.retrieval.generate_embedding",
        return_value=[0.1] * 384
    ):
        result = retrieve_relevant_chunks(
            db=mock_db,
            query="What is a heatwave?",
            top_k=3
        )

    assert result == []


def test_retrieval_respects_top_k():
    mock_db = MagicMock()

    mock_db.query.return_value.order_by.return_value.limit.return_value.all.return_value = [
        MagicMock(chunk_text="Chunk 1"),
        MagicMock(chunk_text="Chunk 2")
    ]

    with patch(
        "app.rag.retrieval.generate_embedding",
        return_value=[0.1] * 384
    ):
        result = retrieve_relevant_chunks(
            db=mock_db,
            query="Weather safety",
            top_k=2
        )

    assert len(result) <= 2
    mock_db.query.return_value.order_by.return_value.limit.assert_called_once_with(2)
