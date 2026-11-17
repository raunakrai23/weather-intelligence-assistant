
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.weather.client import get_city_coordinates, get_weather


@pytest.mark.asyncio
async def test_city_coordinates_found():
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "results": [
            {
                "name": "Delhi",
                "country": "India",
                "latitude": 28.61,
                "longitude": 77.20
            }
        ]
    }

    with patch("app.weather.client.httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            return_value=mock_response
        )

        result = await get_city_coordinates("Delhi")

    assert result["name"] == "Delhi"
    assert result["country"] == "India"
    assert result["latitude"] == 28.61


@pytest.mark.asyncio
async def test_city_not_found():
    mock_response = MagicMock()
    mock_response.json.return_value = {"results": None}

    with patch("app.weather.client.httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            return_value=mock_response
        )

        result = await get_city_coordinates("UnknownCity")

    assert result is None


@pytest.mark.asyncio
async def test_weather_city_not_found():
    with patch(
        "app.weather.client.get_city_coordinates",
        new_callable=AsyncMock
    ) as mock_coordinates:

        mock_coordinates.return_value = None

        result = await get_weather("UnknownCity")

    assert "error" in result
    assert "not found" in result["error"]


@pytest.mark.asyncio
async def test_weather_data_success():
    mock_location = {
        "name": "Jaipur",
        "country": "India",
        "latitude": 26.91,
        "longitude": 75.78
    }

    mock_weather = {
        "current": {"temperature_2m": 28.5},
        "hourly": {"temperature_2m": [28.5, 29.0]},
        "daily": {"temperature_2m_max": [32, 33]},
        "current_units": {"temperature_2m": "°C"},
        "hourly_units": {"temperature_2m": "°C"},
        "daily_units": {"temperature_2m_max": "°C"}
    }

    mock_response = MagicMock()
    mock_response.json.return_value = mock_weather

    with patch(
        "app.weather.client.get_city_coordinates",
        new_callable=AsyncMock
    ) as mock_coordinates:

        mock_coordinates.return_value = mock_location

        with patch("app.weather.client.httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                return_value=mock_response
            )

            result = await get_weather("Jaipur")

    assert result["location"]["name"] == "Jaipur"
    assert result["current_weather"]["temperature_2m"] == 28.5
    assert result["hourly_forecast"]["temperature_2m"] == [28.5, 29.0]
    assert result["daily_forecast"]["temperature_2m_max"] == [32, 33]

