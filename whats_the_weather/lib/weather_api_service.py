"""
This module provides utilities for working with OpenWeather API coordinates
"""

import json
import os

import requests
from pydantic import ValidationError

from .coordinates import Coordinates
from .exc import CantGetWeatherFromAPI
from .weather_models import OpenWeatherForecast, Weather


def get_weather(coordinates: Coordinates) -> Weather:
    """Requests weather from API and returns `Weather` object"""

    openweather_url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"lat={coordinates.latitude}&lon={coordinates.longitude}&"
        f"appid={os.getenv('OPENWEATHER_API_KEY')}&units=metric"
    )

    try:
        weather_api_response = requests.get(openweather_url, timeout=10)
        weather_api_response.raise_for_status()
        weather_api_response_json = weather_api_response.json()
        weather = OpenWeatherForecast(**weather_api_response_json)
    except (
        requests.exceptions.RequestException,
        json.decoder.JSONDecodeError,
        requests.exceptions.HTTPError,
        ValidationError,
    ) as e:
        raise CantGetWeatherFromAPI(e) from e

    return weather
