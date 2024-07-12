from aldotaibot_satori.plugins import AUTHOR
from arclet.entari import PluginMetadata, Session
from arclet.entari.event import GuildRequestEvent,FriendRequestEvent
__plugin_metadata__ = PluginMetadata(author=AUTHOR, name=__name__)


@GuildRequestEvent.dispatch().on()
async def _(session: Session):
    await session.guild_approve(approve=True, comment="")


@FriendRequestEvent.dispatch().on()
async def _(session: Session):
    await session.friend_approve(approve=True, comment="")
