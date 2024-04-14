import random
from datetime import datetime

import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Bot

from bot_dc.config import DEBUG_CHANNEL_ID

RESPONSES = ["meow~", "Itami~ >.<", "What's the matter, gosyujinnsama?", "pong~", "UwU", "don't poke me, plz T^T"]


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user.name} (ID: {self.bot.user.id})')
        await self.bot.tree.sync()

        embed = Embed(
            title="I'm successfully started!!",
            colour=discord.Colour.green(),
            timestamp=datetime.now())
        await self.bot.get_channel(DEBUG_CHANNEL_ID).send(embed=embed)

    @commands.hybrid_command()
    async def ping(self, ctx):
        """Pings the dc_bot"""
        result = random.choice(RESPONSES)
        await ctx.send(f'{result}')

    @commands.hybrid_command()
    async def test(self, ctx):
        """Test command"""
        content = ctx.message.content
        await ctx.send(f'You said:\n {content}')


async def setup(bot):
    await bot.add_cog(Basic(bot))
