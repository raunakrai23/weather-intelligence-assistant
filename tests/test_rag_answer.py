
from app.database.connection import SessionLocal
from app.rag.answer import answer_weather_question

db = SessionLocal()

try:
    question = "What precautions should I take during heavy rainfall?"

    answer = answer_weather_question(
        db=db,
        question=question
    )

    print("\nQuestion:", question)
    print("\nAI Generated Answer:\n")
    print(answer)

except Exception as e:
    print("Error:", str(e))

finally:
    db.close()
