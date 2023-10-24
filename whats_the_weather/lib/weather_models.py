"""Types connected with weather"""

from enum import Enum
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .coordinates import Coordinates
from .types import (
    Celsius,
    Degrees,
    Hectopascal,
    Meters,
    MeterSec,
    Millimeters,
    Percent,
    PositiveInt,
    Timestamp,
    TimezoneOffset,
)


class GlobalConfigModel(BaseModel):
    """Base model with global settings"""

    model_config = ConfigDict(frozen=True)


class Weather(GlobalConfigModel):
    """Base class which returns from `get_weather` function"""


class OpenWeatherForecastNames(Enum):
    """OpenWeather weather names"""

    THUNDERSTORM = "Thunderstorm"
    DRIZZLE = "Drizzle"
    RAIN = "Rain"
    SNOW = "Snow"
    CLEAR = "Clear"
    ATMOSPHERE = "Atmosphere"
    CLOUDS = "Clouds"


class OpenWeatherForecastType(GlobalConfigModel):
    """OpenWeather weather type"""

    condition_id: PositiveInt = Field(validation_alias="id")
    name: OpenWeatherForecastNames = Field(validation_alias="main")
    description: str
    icon: str


class OpenWeatherForecastTemperature(GlobalConfigModel):
    """OpenWeather weather temperature model"""

    temp: Celsius
    feels_like: Celsius
    temp_min: Celsius
    temp_max: Celsius
    pressure: Hectopascal
    humidity: Percent
    sea_level: Hectopascal
    grnd_level: Hectopascal

    @field_validator("temp", "feels_like", "temp_min", "temp_max", mode="before")
    @classmethod
    def temp_to_int(cls, temp: float) -> Celsius:
        """Transforms temperature floats to int"""
        return int(round(temp, 0))


class OpenWeatherForecastWind(GlobalConfigModel):
    """OpenWeather weather wind model"""

    speed: MeterSec
    direction: Degrees = Field(validation_alias="deg")
    gust: MeterSec


class OpenWeatherForecastRain(GlobalConfigModel):
    """OpenWeather weather rain model"""

    rainfall_volume_1h: Millimeters
    rainfall_volume_3h: Millimeters


class OpenWeatherForecastSnow(GlobalConfigModel):
    """OpenWeather weather snow model"""

    snow_volume_1h: Millimeters
    snow_volume_3h: Millimeters


class OpenWeatherSysInternal(GlobalConfigModel):
    """OpenWeather weather sys internal model"""

    type: int
    id: PositiveInt
    message: Optional[str] = Field(default=None)
    country: str
    sunrise: Timestamp
    sunset: Timestamp


class OpenWeatherForecast(Weather):
    """OpenWeather's forecast class"""

    coordinates: Coordinates = Field(validation_alias="coord")
    weather: list[OpenWeatherForecastType]
    base: str
    temperature: OpenWeatherForecastTemperature = Field(validation_alias="main")
    wind: OpenWeatherForecastWind
    rain: Optional[OpenWeatherForecastRain] = Field(default=None)
    snow: Optional[OpenWeatherForecastSnow] = Field(default=None)
    cloudiness: dict[Literal["all"], Percent] = Field(validation_alias="clouds")
    visibility: Meters
    dt: Timestamp
    sys: OpenWeatherSysInternal
    timezone: TimezoneOffset
    city_id: PositiveInt = Field(validation_alias="id")
    city_name: str = Field(validation_alias="name")
    cod: int
