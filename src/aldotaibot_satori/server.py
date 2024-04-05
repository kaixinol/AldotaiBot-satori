from arclet.entari import ContextSession, Entari, EntariCommands, WebsocketsInfo

command = EntariCommands()


@command.on("add {a} {b}")
async def add(a: int, b: int, session: ContextSession):
    await session.send_message(f"{a + b =}")


app = Entari()
app.apply(WebsocketsInfo(port=5500, token='38be6838db388ba3f921457064850590bf2d65fadd5aeaa4288f41711e5b60ca'))

app.run()