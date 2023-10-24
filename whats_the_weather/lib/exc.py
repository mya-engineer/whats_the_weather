"""
Module with WhatsTheWeather app's exceptions
"""


class WhatsTheWeatherException(Exception):
    """Base WhatsTheWeather exception"""


class CantGetCoordinates(WhatsTheWeatherException):
    """Raises when get_coordinates fails"""


class CantGetWeatherFromAPI(WhatsTheWeatherException):
    """Raises when get_weather fails"""
