
import httpx

from app.core.config import settings


async def get_city_coordinates(city: str):
    """Find latitude and longitude for a city."""

    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get(
            settings.GEOCODING_API_URL,
            params=params
        )
        response.raise_for_status()
        data = response.json()

    if not data.get("results"):
        return None

    location = data["results"][0]

    return {
        "name": location["name"],
        "country": location.get("country"),
        "latitude": location["latitude"],
        "longitude": location["longitude"]
    }


async def get_weather(city: str):
    """Fetch current weather and 7-day forecast for a city."""

    location = await get_city_coordinates(city)

    if location is None:
        return {"error": f"City '{city}' not found"}

    params = {
        "latitude": location["latitude"],
        "longitude": location["longitude"],

        # Current weather conditions
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "is_day",
            "precipitation",
            "weather_code",
            "wind_speed_10m"
        ],

        # Hourly weather forecast
        "hourly": [
            "temperature_2m",
            "precipitation_probability",
            "precipitation",
            "wind_speed_10m",
            "relative_humidity_2m"
        ],

        # Daily weather forecast
        "daily": [
            "weather_code",
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_probability_max",
            "precipitation_sum",
            "wind_speed_10m_max"
        ],

        "forecast_days": 7,
        "timezone": "auto"
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get(
            settings.WEATHER_API_URL,
            params=params
        )
        response.raise_for_status()
        weather_data = response.json()

    return {
        "location": location,

        "current_weather": weather_data.get("current"),
        "hourly_forecast": weather_data.get("hourly"),
        "daily_forecast": weather_data.get("daily"),

        "units": {
            "current": weather_data.get("current_units"),
            "hourly": weather_data.get("hourly_units"),
            "daily": weather_data.get("daily_units")
        }
    }
