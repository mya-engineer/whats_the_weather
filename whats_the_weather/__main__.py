"""Entry point"""

from dotenv import load_dotenv

from .lib.coordinates import IpApiCoordinatesGrabber
from .lib.weather_api_service import get_weather


def main():
    """
    Main
    """
    load_dotenv()
    coordinates = IpApiCoordinatesGrabber().get_coordinates("46.242.12.211")
    weather = get_weather(coordinates)
    print(weather)


if __name__ == "__main__":
    main()
