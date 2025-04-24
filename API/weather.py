import requests

# =============================================================
# Weather API
# =============================================================

# WeatherAPI: str, str, str  -> String
# using weather api return weather condition in the given api key, stadium location, given date and time

def get_weather(api_key: str, location: str, date_str: str, target_hour: int) -> str:
    """
        Get weather condition for a specific location, date, and hour using the WeatherAPI.

        Args:
            api_key (str): The API key for the WeatherAPI.
            location (str): The location for which to get the weather information (e.g., 'London').
            date_str (str): The date in YYYY-MM-DD format (e.g., '2025-04-24').
            target_hour (int): The hour of the day (0-23) to get the weather condition for.

        Returns:
            str: The weather condition text (e.g., 'Sunny', 'Patchy rain nearby').

    """
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days=1&aqi=no&alerts=no"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        forecast_day = data['forecast']['forecastday'][0]
        if forecast_day['date'] != date_str:
            raise ValueError(f"No forecast data available for {date_str}")

        for hour_data in forecast_day['hour']:
            hour = int(hour_data['time'].split(" ")[1].split(":")[0])
            if hour == target_hour:
                return hour_data['condition']['text']

        raise ValueError(f"No weather data found for hour {target_hour} on {date_str}")

    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {str(e)}")
    except (KeyError, IndexError) as e:
        raise Exception(f"Error parsing API response: {str(e)}")