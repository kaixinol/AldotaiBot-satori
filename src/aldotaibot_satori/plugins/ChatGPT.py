from arclet.entari import MessageCreatedEvent, Plugin, EntariCommands, At
from . import AUTHOR

plug = Plugin(author=AUTHOR, name=__name__)
disp_message = plug.dispatch(MessageCreatedEvent)

commands = EntariCommands.current()


@disp_message.on()
async def _(event: MessageCreatedEvent):
    if event.quote is not None or event.content.has(At) and event.content[At][-1].id == event.account.self_id:
        print(event.content.extract_plain_text().strip())
        print(event.user)
