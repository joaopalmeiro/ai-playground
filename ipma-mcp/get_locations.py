from pathlib import Path

import httpx2
from pydantic import BaseModel, ConfigDict, TypeAdapter
from pydantic.alias_generators import to_camel

LOCATIONS_URL = "https://api.ipma.pt/public-data/forecast/locations.json"
OUTPUT_FILE = Path("constants.py")


class Location(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    id_regiao: int
    id_area_aviso: str
    global_id_local: int
    id_concelho: int
    latitude: float
    id_distrito: int
    local: str
    longitude: float


Locations = TypeAdapter(list[Location])


if __name__ == "__main__":
    with httpx2.Client() as client:
        response = client.get(LOCATIONS_URL)
        response.raise_for_status()
        locations = Locations.validate_json(response.content)

    locals = sorted(loc.local for loc in locations)
    local_to_id = {loc.local: loc.global_id_local for loc in locations}

    literal_values = ", ".join(f'"{name}"' for name in locals)
    map_entries = "\n".join(f'"{name}": {local_to_id[name]},' for name in locals)

    content = f"""from typing import Literal, TypeAlias

LocalNames: TypeAlias = Literal[{literal_values}]

LOCAL_TO_ID: dict[str, int] = {{{map_entries}}}
"""

    OUTPUT_FILE.write_text(content, encoding="utf-8")
