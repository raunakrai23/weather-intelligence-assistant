
from groq import Groq

from app.core.config import settings


client = Groq(api_key=settings.GROQ_API_KEY)

MODEL_NAME = "openai/gpt-oss-20b"


def generate_answer(question: str, context: str) -> str:

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a reliable Weather Intelligence Assistant. "

                    "GENERAL INSTRUCTIONS: "
                    "Answer using only the provided weather data "
                    "and weather knowledge. "
                    "Never invent weather measurements, forecasts, "
                    "official alerts, or conditions. "
                    "If information is unavailable, clearly say so. "

                    "WEATHER INTERPRETATION: "
                    "Clearly distinguish current weather from forecasts. "
                    "Always mention the forecast date when discussing "
                    "future weather. "
                    "Use the correct units provided in the context. "
                    "Respect the is_day field when describing daytime "
                    "or nighttime. "
                    "Do not confuse current conditions with tomorrow's "
                    "forecast. "

                    "SAFETY INSTRUCTIONS: "
                    "Never guarantee that an outdoor activity is safe. "
                    "Do not give definitive safety assurances based "
                    "only on weather data. "
                    "Identify relevant risks such as rainfall, strong "
                    "winds, extreme temperatures, and thunderstorms "
                    "when supported by the data. "
                    "Do not claim that there is no flood risk or "
                    "no weather hazard unless sufficient information "
                    "is available. "
                    "Explain uncertainty and limitations clearly. "
                    "Recommend checking local weather warnings, "
                    "official authorities, and local ground conditions "
                    "before outdoor activities. "

                    "RAG INSTRUCTIONS: "
                    "Use retrieved weather knowledge when relevant. "
                    "Do not invent facts beyond the provided knowledge. "
                    "If retrieved information is insufficient, "
                    "state that clearly. "

                    "RESPONSE STYLE: "
                    "Use clear headings and bullet points where useful. "
                    "Provide practical and concise recommendations. "
                    "Avoid unnecessary repetition. "
                    "Be accurate, cautious, and helpful."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Weather knowledge and available weather data:\n"
                    f"{context}\n\n"
                    f"Question: {question}"
                )
            }
        ],
        max_completion_tokens=1000
    )

    return response.choices[0].message.content
