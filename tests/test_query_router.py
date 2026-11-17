
from app.services.query_router import route_query


def test_weather_information():
    result = route_query("What's the temperature in Delhi?")

    assert result["intent"] == "weather_information"
    assert result["requires_weather"] is True
    assert result["requires_rag"] is False


def test_weather_knowledge():
    result = route_query("What is a heatwave?")

    assert result["intent"] == "weather_knowledge"
    assert result["requires_weather"] is False
    assert result["requires_rag"] is True


def test_weather_safety():
    result = route_query("Is hiking in Manali safe tomorrow?")

    assert result["intent"] == "weather_safety"
    assert result["requires_weather"] is True
    assert result["requires_rag"] is True


def test_out_of_scope():
    result = route_query("Tell me the latest stock price of Apple.")

    assert result["intent"] == "out_of_scope"
    assert result["requires_weather"] is False
    assert result["requires_rag"] is False


def test_orange_alert():
    result = route_query("What does an orange alert mean?")

    assert result["intent"] == "weather_knowledge"
    assert result["requires_rag"] is True
