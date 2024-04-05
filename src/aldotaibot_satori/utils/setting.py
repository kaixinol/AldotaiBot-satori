from dataclasses import field

from pydantic.dataclasses import dataclass
from typing import TypeVar
from yaml import safe_load

T = TypeVar('T')


@dataclass
class Config:
    proxy: dict[str, str] | None = None
    plugin: dict[str, T | dict] | None = None
    token: str = ''
    admin: list[int] = field(default_factory=list)
    name: str = 'Aldotai'


config: Config | None = None


def load_config():
    global config
    with open('config.yaml') as fp:
        config = Config(**safe_load(fp))
    return config
