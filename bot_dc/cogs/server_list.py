from discord.ext import commands, tasks
from bot_dc.config import SERVER_LIST_CHANNEL_ID
from bot_dc.dc_utils.general import get_or_create_message
from bot_dc.dc_utils.query_server import servers_status_embed


class ServerList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.server_list_loop.start()

    @tasks.loop(seconds=60)
    async def server_list_loop(self):
        await self.bot.wait_until_ready()

        channel = self.bot.get_channel(SERVER_LIST_CHANNEL_ID)
        message = await get_or_create_message(channel, self.bot)

        embed = await servers_status_embed(
            show_player_profile_link=True, show_duration=True, redirect=False
        )
        await message.edit(embed=embed)

    @commands.hybrid_command()
    async def ls(self, ctx):
        """Show the server list"""
        embed = await servers_status_embed(show_player_profile_link=True)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ServerList(bot))
