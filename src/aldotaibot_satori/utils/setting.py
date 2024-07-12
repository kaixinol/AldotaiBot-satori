from pathlib import Path

from pydantic.dataclasses import dataclass
from yaml import safe_load


@dataclass
class Config:
    port: int
    proxy: dict[str, str]
    plugin: dict[str, bool | dict]
    admin: list[int]
    auth_token: str
    name: str


config: Config | None = None


def load_config(file: str | Path):
    global config
    with open(file) as fp:
        config = Config(**safe_load(fp))
    return config
