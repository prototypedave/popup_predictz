import pytest
from unittest.mock import patch
from API.weather import get_weather

@patch("API.weather.requests.get")
def test_get_weather_valid_response(mock_get):
    mock_response = {
        "forecast": {
            "forecastday": [
                {
                    "date": "2025-04-24",
                    "hour": [
                        {"time": "2025-04-24 14:00", "condition": {"text": "Sunny"}},
                        {"time": "2025-04-24 15:00", "condition": {"text": "Cloudy"}},
                    ]
                }
            ]
        }
    }
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    api_key = "fake_api_key"
    location = "London"
    date_str = "2025-04-24"
    target_hour = 14
    result = get_weather(api_key, location, date_str, target_hour)

    assert result == "Sunny"


@patch("API.weather.requests.get")
def test_get_weather_invalid_date(mock_get):
    mock_response = {
        "forecast": {
            "forecastday": [
                {
                    "date": "2025-04-23",
                    "hour": [
                        {"time": "2025-04-23 14:00", "condition": {"text": "Rainy"}},
                    ]
                }
            ]
        }
    }
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    api_key = "fake_api_key"
    location = "London"
    date_str = "2025-04-24"
    target_hour = 14
    with pytest.raises(ValueError, match="No forecast data available for 2025-04-24"):
        get_weather(api_key, location, date_str, target_hour)


@patch("API.weather.requests.get")
def test_get_weather_missing_hour(mock_get):
    mock_response = {
        "forecast": {
            "forecastday": [
                {
                    "date": "2025-04-24",
                    "hour": [
                        {"time": "2025-04-24 13:00", "condition": {"text": "Cloudy"}},
                    ]
                }
            ]
        }
    }
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    api_key = "fake_api_key"
    location = "London"
    date_str = "2025-04-24"
    target_hour = 14
    with pytest.raises(ValueError, match="No weather data found for hour 14 on 2025-04-24"):
        get_weather(api_key, location, date_str, target_hour)


@patch("API.weather.requests.get")
def test_get_weather_api_error(mock_get):
    mock_get.side_effect = Exception("API request failed")

    api_key = "fake_api_key"
    location = "London"
    date_str = "2025-04-24"
    target_hour = 14
    with pytest.raises(Exception, match="API request failed"):
        get_weather(api_key, location, date_str, target_hour)


def test_get_weather_invalid_inputs():
    with pytest.raises(Exception):
        get_weather("", "London", "2025-04-24", 14)
    with pytest.raises(Exception):
        get_weather("fake_api_key", "", "2025-04-24", 14)
    with pytest.raises(Exception):
        get_weather("fake_api_key", "London", "invalid-date", 14)