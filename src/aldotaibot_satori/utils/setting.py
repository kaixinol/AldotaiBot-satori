from collections.abc import Callable
from dataclasses import dataclass, replace, field
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


config = Config()


def load_config(after_loaded: Callable[[Config],None] = lambda x: None):
    global config
    with open('config.yaml') as fp:
        config = replace(config, **safe_load(fp))
    after_loaded(config)
