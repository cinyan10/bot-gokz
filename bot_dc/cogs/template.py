from discord.ext import commands
from discord.ext.commands import Bot


class Template(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.hybrid_command()
    async def template(self, ctx):

        pass


async def setup(bot):
    await bot.add_cog(Template(bot))
