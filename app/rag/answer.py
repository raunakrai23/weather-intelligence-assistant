
from sqlalchemy.orm import Session

from app.rag.retrieval import retrieve_relevant_chunks
from app.services.llm import generate_answer


def answer_weather_question(
    db: Session,
    question: str,
    weather_context: str | None = None,
    include_rag: bool = True
) -> str:

    context = ""

    if include_rag:
        chunks = retrieve_relevant_chunks(
            db=db,
            query=question,
            top_k=3
        )

        context = "\n\n".join(
            chunk.chunk_text for chunk in chunks
        )

        if not context:
            context = "No relevant weather-safety knowledge was found."

    if weather_context:
        context += "\n\nLIVE WEATHER INFORMATION:\n" + weather_context

    answer = generate_answer(
        question=question,
        context=context
    )

    return answer
