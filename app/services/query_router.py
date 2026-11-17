
def route_query(question: str) -> dict:
    text = question.lower()

    weather_keywords = [
       "temperature", "weather", "forecast",
    "rain", "rainfall", "humidity",
    "wind", "wind speed", "uv index",
    "climate today", "weather tomorrow",
    "current conditions",
    "today", "tomorrow", "tonight",
    "this evening", "this week",
    "hiking", "outdoor activities"
    ]

    rag_keywords = [
        "precaution", "safety", "safe",
        "heatwave", "cold wave", "thunderstorm",
        "cyclone", "flood", "lightning",
        "orange alert", "weather warning",
        "what is", "explain", "protect",
        "elderly", "heavy rainfall"
    ]

    out_of_scope_keywords = [
        "stock price", "share price",
        "cryptocurrency", "football score",
        "movie recommendation"
    ]

    if any(keyword in text for keyword in out_of_scope_keywords):
        return {
            "intent": "out_of_scope",
            "requires_weather": False,
            "requires_rag": False
        }

    requires_weather = any(
        keyword in text for keyword in weather_keywords
    )

    requires_rag = any(
        keyword in text for keyword in rag_keywords
    )

    if requires_weather and requires_rag:
        intent = "weather_safety"
    elif requires_weather:
        intent = "weather_information"
    elif requires_rag:
        intent = "weather_knowledge"
    else:
        intent = "general"

    return {
        "intent": intent,
        "requires_weather": requires_weather,
        "requires_rag": requires_rag
    }
