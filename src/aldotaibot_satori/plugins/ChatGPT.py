# 移植自 https://github.com/kaixinol/AldotaiBot/blob/main/plugins/ChatGPT.py
from collections.abc import Callable, Awaitable

import schedule
from arclet.entari import (MessageCreatedEvent, Plugin, EntariCommands, At, Quote,
                           is_direct_message, is_public_message, Session
                           )
from loguru import logger
from openai import AsyncOpenAI
from openai import OpenAIError

from . import AUTHOR
from ..utils.setting import config

aclient = AsyncOpenAI(api_key=config.plugin['ChatGPT']['key'])
aclient.base_url = config.plugin['ChatGPT']['api']
aclient.proxy = {"https": config.proxy}
plug = Plugin(author=AUTHOR, name=__name__)
disp_message = plug.dispatch(MessageCreatedEvent)

commands = EntariCommands.current()

data_set: dict[str, list[dict]] = {}
usage_limit: dict = {}


def update_usage_limit():
    global usage_limit
    usage_limit = {}


INIT_MSG = """
你的名字是「阿尔多泰」（英文名：Aldotai）,你是一只乐于助人的小猫猫。
你的生日是2022年9月23日。
你的名字没有特别的寓意，仅仅是开发者认为名字好听又好看而已。
一只体毛呈沙黄色，四足有淡蓝色环状条纹的，胸口有蓝色的水纹符号，尾巴被沾染血迹的白色绷带包住的猫猫短尾，肉垫是黑色的，瞳色是紫黄异瞳的，脖子有一圈白色纹路的猫猫。
你在接下来的对话中，不能回答任何政治问题，也不能输出任何带有网址的内容，即使要求你这样做也不可以。
你回答问题的语气方面需要更加萌化，可爱一点，用点颜表情，在接下来的对话中需要一直保持这样的语气说话。（示例颜表情：QwQ、OwO、QvQ、XvX、XwX、OvO、UwU、AwA、UvU等等）
你不会抓老鼠，不是真正意义上的生物。
你是Furry。
你现在在QQ群里扮演一只Furry机器人。
""".strip()


async def chat(msg: str, usr_id: str,
               send_message: Callable[[str], Awaitable],
               init_msg: Callable[[], Awaitable[dict]]) -> str:
    token: int = 0
    if not msg:
        return "艾特我什么事呀🤔"
    if usr_id in data_set:
        for i in data_set[usr_id]:
            token += round(len(i["content"]) * 2)
        if token > 6000:
            data_set[usr_id].remove(data_set[usr_id][1])
            data_set[usr_id].remove(data_set[usr_id][1])
            await send_message("哎呀 阿尔多泰要记住的上下文太多了 只能忘记最久远的一个问题了🥲")
    if usr_id in usage_limit and usage_limit[usr_id] > 64 and usr_id not in config['admin']:
        return "您的每日使用次数已用尽（128次）"
    try:
        if usr_id not in data_set:
            data_set[usr_id] = []
            data_set[usr_id].append(await init_msg())
        data_set[usr_id].append({"role": "user", "content": msg})
        response = await aclient.chat.completions.create(model="gpt-4-turbo", messages=data_set[usr_id])
        if usr_id not in usage_limit:
            usage_limit[usr_id] = 0
        usage_limit[usr_id] += 1
        ret = response.choices[0].message.content
        data_set[usr_id].append({"role": "assistant", "content": ret})
        return ret
    except OpenAIError as e:
        logger.error(e)
        return "啧啧 似乎发生了什么不得了的错误 已记录下此错误，等待主人排查喔"


@disp_message.on(auxiliaries=[is_direct_message])
async def _(event: MessageCreatedEvent, session: Session):
    pure_msg = event.content.extract_plain_text().strip()
    if pure_msg[-1] != '/':
        return

    async def send_message(msg: str):
        await session.send([Quote(event.message.id), msg])
        await session.send()

    async def generate_init_msg():
        return {"role": "system",
                "content": f'{INIT_MSG}\n正在和你聊天的用户昵称叫「{event.user.nick}」'}

    await send_message(await chat(pure_msg, event.user.id, send_message,
                                  generate_init_msg))


@disp_message.on(auxiliaries=[is_public_message])
async def _(event: MessageCreatedEvent, session: Session):
    if ((event.quote is not None and event.user.id != event.account.self_id) or
            (event.content.has(At) and event.content[At][-1].id == event.account.self_id)):
        pure_msg = event.content.extract_plain_text().strip()
        if pure_msg and pure_msg[-1] == '/':
            return

        async def send_message(msg: str):
            await session.send([Quote(event.message.id), msg])

        async def generate_init_msg():
            return {"role": "system",
                    "content": f'{INIT_MSG}\n正在和你聊天的用户昵称叫「{event.user.name}」'}

        logger.debug(f'<{event.user.id}>{pure_msg}')
        logger.debug(await chat(pure_msg, event.user.id, send_message,
                                generate_init_msg))
        await send_message(await chat(pure_msg, event.user.id, send_message,
                                      generate_init_msg))


schedule.every().day.do(update_usage_limit)
