from pathlib import Path

from .utils.setting import load_config
from arclet.entari import Entari, WebsocketsInfo
from arclet.entari.plugin import load_plugin

config = load_config(Path(__file__).parent / Path('_config.yaml'))
app = Entari()
tmp = config.plugin
plugins = [i for i in tmp if tmp[i]]

for i in plugins:
    load_plugin(f'aldotaibot_satori.plugins.{i}')
app.apply(WebsocketsInfo(port=5501,
                         token=config.auth_token))

app.run()
