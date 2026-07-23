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

    id_periodo: Literal[1]
    id_tipo_tempo: int
    probabilidade_precipita: float
    dd_vento: str
    ff_vento: float
    data_prev: datetime
    data_update: datetime
    global_id_local: int
    t_med: float
    h_r: float
    utci: float
    temp_agua_mar: float
    ondulacao: float
    mar_total: float
    periodo_ondulacao: float
    periodo_pico: float
    dir_ondulacao: str


class ThreeHourForecast(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    id_periodo: Literal[3]
    id_tipo_tempo: int
    probabilidade_precipita: float
    dd_vento: str
    ff_vento: float
    data_prev: datetime
    data_update: datetime
    global_id_local: int
    t_med: float
    h_r: float
    utci: float


class DailyForecast(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    id_periodo: Literal[24]
    id_tipo_tempo: int
    probabilidade_precipita: float
    dd_vento: str
    data_prev: datetime
    data_update: datetime
    global_id_local: int
    t_min: float
    t_max: float
    i_uv: float | None = None
    intervalo_hora: str | None = None
    id_ffx_vento: int


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
async def get_weather_forecast(local: LocalNames) -> list[DailyForecast]:
    """Get the daily 10-day weather forecast from today for a specific location (such as a city or town) in Portugal."""

    local_id = LOCAL_TO_ID[local]

    async with httpx2.AsyncClient() as client:
        url = f"https://api.ipma.pt/public-data/forecast/aggregate/{local_id}.json"

        response = await client.get(url)
        response.raise_for_status()
        raw_data = Forecasts.validate_json(response.content)

    return [
        DailyForecast(
            min_temperature=daily_forecast.t_min,
            max_temperature=daily_forecast.t_max,
            date=daily_forecast.forecast_date,
        )
        for daily_forecast in raw_data
    ]
