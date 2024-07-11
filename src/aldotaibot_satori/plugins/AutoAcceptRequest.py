from aldotaibot_satori.plugins import AUTHOR
from arclet.entari import Plugin, Session
from arclet.entari.event import GuildRequestEvent,FriendRequestEvent

plug = Plugin(author=AUTHOR, name=__name__)
disp_guild_request = plug.dispatch(GuildRequestEvent)
disp_friend_request = plug.dispatch(FriendRequestEvent)


@disp_guild_request.on()
async def _(session: Session):
    await session.guild_approve(approve=True, comment="")


@disp_friend_request.on()
async def _(session: Session):
    await session.friend_approve(approve=True, comment="")
