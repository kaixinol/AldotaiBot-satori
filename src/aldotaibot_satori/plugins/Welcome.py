from arclet.entari import Plugin, At, Session
from arclet.entari.event import GuildMemberAddedEvent

from aldotaibot_satori.plugins import AUTHOR
from ..utils.setting import config
plug = Plugin(author=AUTHOR, name=__name__)
disp_new_member_request = plug.dispatch(GuildMemberAddedEvent)


@disp_new_member_request.on()
async def _(event: GuildMemberAddedEvent,session: Session):
    await session.send([At(event.user.id), f'欢迎~bot方法\t【腾讯文档】AldotaiBot(satori) 使用指南'
                                           f'{config.plugin["Welcome"]["doc"]}'])
