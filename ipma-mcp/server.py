from datetime import date, datetime
from typing import Literal

import httpx2
from mcp.server import MCPServer
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from constants import LOCAL_TO_ID, LocalNames

mcp = MCPServer("IPMA Weather Forecast")


class DailyForecastResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    precipita_prob: float
    t_min: float
    t_max: float
    pred_wind_dir: Literal["NW", "N"]
    id_weather_type: int
    class_wind_speed: int
    longitude: float
    forecast_date: date
    latitude: float


class ForecastResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    owner: Literal["IPMA"]
    country: Literal["PT"]
    global_id_local: int
    data_update: datetime
    data: list[DailyForecastResponse]


class DailyForecast(BaseModel):
    min_temperature: float
    max_temperature: float
    date: date


@mcp.tool()
async def get_weather_forecast(local: LocalNames) -> list[DailyForecast]:
    """Get the daily weather forecast for up to 5 days for a specific location (such as a city or town) in Portugal."""

    local_id = LOCAL_TO_ID[local]

    async with httpx2.AsyncClient() as client:
        url = f"https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/{local_id}.json"

        response = await client.get(url)
        response.raise_for_status()
        raw_data = ForecastResponse.model_validate_json(response.content)

    return [
        DailyForecast(
            min_temperature=daily_forecast.t_min,
            max_temperature=daily_forecast.t_max,
            date=daily_forecast.forecast_date,
        )
        for daily_forecast in raw_data.data
    ]
