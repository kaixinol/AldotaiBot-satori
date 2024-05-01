from utils.setting import load_config
from arclet.entari import ContextSession, Entari, WebsocketsInfo,EntariCommands
from arclet.entari.plugin import load_plugin

app = Entari()
tmp = load_config().plugin
plugins = [i for i in tmp if tmp[i]]
commands = EntariCommands().current()

for i in plugins:
    load_plugin(f'plugins.{i}')
app.apply(WebsocketsInfo(port=5501,
                         token='38be6838db388ba3f921457064850590bf2d65fadd5aeaa4288f41711e5b60ca'))

app.run()
