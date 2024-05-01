from pydantic.dataclasses import dataclass
from yaml import safe_load


@dataclass
class Config:
    qq: dict[str, int]
    proxy: dict[str, str]
    plugin: dict[str, bool | dict]
    admin: list[int]
    auth_token: str
    name: str


config: Config | None = None


def load_config():
    global config
    with open('config.yaml') as fp:
        config = Config(**safe_load(fp))
    return config
