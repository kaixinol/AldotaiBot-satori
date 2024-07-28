import re

from arclet.entari import PluginMetadata, Session, Quote, MessageChain
from arclet.entari.event import MessageCreatedEvent
from aldotaibot_satori.plugins import AUTHOR

from ..utils.setting import config
from satori import select, Author
# from loguru import logger
__plugin_metadata__ = PluginMetadata(author=AUTHOR, name=__name__)


@MessageCreatedEvent.dispatch().on()
async def _(event: MessageCreatedEvent, session: Session, msg: MessageChain):
    if event.quote and (authors := select(event.quote, Author)):
        if authors[0].id != event.account.self_id:
            return
    if event.user.id == event.account.self_id or event.user is None:
        return
    for regex, reply in config.plugin['KeywordReply']['regex']:
        if re.match(regex, event.message.content) and all([kw != msg.extract_plain_text() for kw, _ in
                                                           config.plugin['KeywordReply']['keywords']]):
            await session.send([Quote(event.message.id), re.sub(regex, reply, msg.extract_plain_text())])
            return
    for keyword, reply in config.plugin['KeywordReply']['keywords']:
        if keyword in event.message.content:
            await session.send([Quote(event.message.id), reply])
            return
