from datetime import date, datetime
from typing import Annotated, Literal

import httpx2
from mcp.server import MCPServer
from pydantic import BaseModel, ConfigDict, Field, TypeAdapter
from pydantic.alias_generators import to_camel

from constants import LOCAL_TO_ID, LocalNames

mcp = MCPServer("IPMA Weather Forecast")


class HourlyForecast(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    t_med: float
    temp_agua_mar: float | None = None
    probabilidade_precipita: float
    id_tipo_tempo: int
    periodo_pico: float | None = None
    ondulacao: float | None = None
    h_r: float
    data_update: datetime
    utci: float
    dir_ondulacao: str | None = None
    ff_vento: float
    global_id_local: int
    mar_total: float | None = None
    periodo_ondulacao: float | None = None
    id_periodo: Literal[1]
    data_prev: datetime
    dd_vento: str


class ThreeHourForecast(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    t_med: float
    id_tipo_tempo: int
    h_r: float
    data_update: datetime
    utci: float
    ff_vento: float
    global_id_local: int
    probabilidade_precipita: float
    id_periodo: Literal[3]
    data_prev: datetime
    dd_vento: str


class DailyForecast(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    t_min: float
    id_ffx_vento: int
    data_update: datetime
    t_max: float
    i_uv: float | None = None
    intervalo_hora: str | None = None
    id_tipo_tempo: int
    global_id_local: int
    probabilidade_precipita: float
    id_periodo: Literal[24]
    data_prev: datetime
    dd_vento: str


Forecast = Annotated[
    HourlyForecast | ThreeHourForecast | DailyForecast,
    Field(discriminator="id_periodo"),
]

Forecasts = TypeAdapter(list[Forecast])


class ModelForecast(BaseModel):
    min_temperature: float
    max_temperature: float
    date: date


@mcp.tool()
async def get_weather_forecast(local: LocalNames) -> list[ModelForecast]:
    """Get the daily 10-day weather forecast from today for a specific location (such as a city or town) in Portugal."""

    local_id = LOCAL_TO_ID[local]

    async with httpx2.AsyncClient() as client:
        url = f"https://api.ipma.pt/public-data/forecast/aggregate/{local_id}.json"

        response = await client.get(url)
        response.raise_for_status()
        raw_data = Forecasts.validate_json(response.content)

    return [
        ModelForecast(
            min_temperature=forecast.t_min,
            max_temperature=forecast.t_max,
            date=forecast.data_prev.date(),
        )
        for forecast in raw_data
        if isinstance(forecast, DailyForecast)
    ]
