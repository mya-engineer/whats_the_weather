"""This module provides utilities for working with GPS coordinates"""

import abc
import json
import posixpath
from typing import Literal, Optional

import requests
from pydantic import AliasChoices, Field, ValidationError, validate_call
from pydantic.dataclasses import dataclass

from .exc import CantGetCoordinates
from .types import IpAddress


@dataclass(frozen=True, slots=True)
class Coordinates:
    """Coordinates dataclass"""

    latitude: float = Field(validation_alias=AliasChoices("lat", "latitude"))
    longitude: float = Field(validation_alias=AliasChoices("lon", "longitude"))


class CoordinatesGrabber(abc.ABC):
    """Coordinates grabber abstract class"""

    def __init__(self) -> None:
        self._last_coordinates: Optional[Coordinates] = None

    @property
    @abc.abstractmethod
    def last_coordinates(self) -> Optional[Coordinates]:
        """Last coordinates property"""

    @abc.abstractmethod
    def get_coordinates(self) -> Coordinates:
        """Returns coordinates"""


class IpApiCoordinatesGrabber(CoordinatesGrabber):
    """Coordinates grabber which works with http://ip-api.com"""

    IP_API_URL = "http://ip-api.com/json/"

    @property
    def last_coordinates(self):
        """Last coordinates property from ip-api API, use `get_coordinates` to update"""
        return self._last_coordinates

    @validate_call
    def get_coordinates(self, ip_address: IpAddress | Literal[""] = ""):
        """Returns coordinates using ip-api API call"""

        try:
            ip_api_response = requests.get(
                posixpath.join(self.IP_API_URL, ip_address), timeout=10
            )
            ip_api_response.raise_for_status()
            ip_api_response_json = ip_api_response.json()
            coordinates = Coordinates(
                latitude=ip_api_response_json.get("lat"),
                longitude=ip_api_response_json.get("lon"),
            )
        except (
            ValidationError,
            requests.exceptions.RequestException,
            json.decoder.JSONDecodeError,
            requests.exceptions.HTTPError,
        ) as e:
            raise CantGetCoordinates(e) from e

        self._last_coordinates = coordinates

        return coordinates
