"""Module for types"""

import ipaddress
from typing import Annotated

from annotated_types import Ge
from pydantic import AfterValidator


def validate_percent(value: int) -> int:
    """Custom percents validator"""

    if not 0 <= value <= 100:
        raise ValueError(
            "It's percentage value so it should be "
            "greater or equal to 0 and less or equal 100"
        )

    return value


def validate_degrees(value: int) -> int:
    """Custom degrees validator"""

    if not 0 <= value <= 360:
        raise ValueError(
            "It's degrees value so it should be greater "
            "or equal to 0 and less or equal 360"
        )
    return value


def validate_ip_address(
    ip_address: str,
) -> str:
    """Custom ipv4 and ipv6 addresses validator"""

    ipaddress.ip_address(ip_address)
    return ip_address


Celsius = Annotated[int, AfterValidator(lambda temp: round(temp, 1))]
Hectopascal = int
PositiveInt = Annotated[int, Ge(0)]
PositiveFloat = Annotated[float, Ge(0)]
Timestamp = PositiveInt
TimezoneOffset = PositiveInt
Percent = Annotated[int, AfterValidator(validate_percent)]
Degrees = Annotated[int, AfterValidator(validate_degrees)]
Meters = PositiveFloat
MeterSec = PositiveFloat
Millimeters = PositiveFloat
IpAddress = Annotated[str, AfterValidator(validate_ip_address)]
