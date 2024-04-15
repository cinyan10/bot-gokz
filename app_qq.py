import botpy
from botpy import logging


from bot_qq.commands.casual import *
from bot_qq.commands.firstjoin import *
from bot_qq.commands.general import *
from bot_qq.commands.global_kz import *
from bot_qq.commands.gokz import *
from bot_qq.commands.kreedz import *
from bot_qq.commands.kztimer import *
from bot_qq.commands.screenshot import *
from bot_qq.commands.server import *

from config import APPID, SECRET
from bot_qq.qqutils.ext import Command

_log = logging.get_logger()

# 全角空格(　)


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_group_at_message_create(self, message: GroupMessage):  # NOQA
        for handler in Command.command_handlers:
            if await handler(message=message):
                return

        if message.content == " ":
            num = random.randint(1, 3)
            if num == 1:
                await send(message, random.choice(REPLIES))
            elif num == 2:
                await random_image(message, seq=1)
            else:
                await random_audio(message, seq=1)
            return
        if gm.message:
            if message.content.strip().startswith(
                ("kz", "bkz", "xc", "skz", "vnl", "kzpro")
            ):
                await gm.guess(message, message.content.strip().replace(" ", "_"))

    async def on_message_create(self, message: GroupMessage):  # NOQA
        await send(message, "Test")


if __name__ == "__main__":
    intents = botpy.Intents.all()
    intents.public_messages = True

    client = MyClient(intents=intents)
    client.run(appid=APPID, secret=SECRET)
