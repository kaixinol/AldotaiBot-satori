import re

from arclet.entari import Plugin, Session, Quote, Text, MessageChain
from arclet.entari.event import MessageCreatedEvent
from aldotaibot_satori.plugins import AUTHOR

from ..utils.setting import config
from satori import select, Author

plug = Plugin(author=AUTHOR, name=__name__)
disp_msg_request = plug.dispatch(MessageCreatedEvent)


@disp_msg_request.on()
async def _(event: MessageCreatedEvent, session: Session, msg: MessageChain):
    if event.quote and (authors := select(event.quote, Author)):
        if authors[0].id != event.account.self_id:
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
