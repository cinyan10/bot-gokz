import os
import asyncio

import discord
from discord.ext import commands

from config import DISCORD_TOKEN

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
discord.utils.setup_logging(level=1)


async def load():
    for filename in os.listdir('bot_dc/cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'bot_dc.cogs.{filename[:-3]}')
            print(f'Loaded {filename[:-3]}')


async def main():
    await load()
    await bot.start(DISCORD_TOKEN)


if __name__ == '__main__':
    asyncio.run(main())
