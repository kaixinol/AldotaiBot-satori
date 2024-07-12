from pathlib import Path
from importlib.metadata import version
from .utils.setting import load_config
from arclet.entari import Entari, WebsocketsInfo
from arclet.entari.plugin import load_plugin
from loguru import logger
config = load_config(Path(__file__).parent / Path('_config.yaml'))
app = Entari()
tmp = config.plugin
plugins = [i for i in tmp if tmp[i]]
logger.debug("version: " + version("arclet-entari"))
for i in plugins:
    load_plugin(f'aldotaibot_satori.plugins.{i}')
app.apply(WebsocketsInfo(port=config.port,
                         token=config.auth_token))

app.run()
