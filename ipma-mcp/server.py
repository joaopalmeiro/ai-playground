from datetime import date, datetime
from typing import Literal

import httpx2
from mcp.server import MCPServer
from pydantic import BaseModel, ConfigDict, TypeAdapter
from pydantic.alias_generators import to_camel

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


DailyForecasts = TypeAdapter(list[DailyForecast])


@mcp.tool()
async def get_weather_forecast(city: Literal["Lisboa", "Porto"]) -> DailyForecasts:
    """TODO"""
    async with httpx2.AsyncClient() as client:
        response = await client.get("https://www.example.com/")
        print(response)
