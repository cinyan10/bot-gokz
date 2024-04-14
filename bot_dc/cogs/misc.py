from discord.ext import commands
from discord.ext.commands import Bot
import re
from utils.misc.python_execution import async_execute_python_code


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.hybrid_command()
    async def python(self, ctx):
        """Execute python code, must be enclosed with triple quotes"""
        content = ctx.message.content

        match = re.search(r'```(?:python)?\n?(.*?)```', content, re.DOTALL)

        if match:
            code = match.group(1)
            result = await async_execute_python_code(code)
            result = f'```\n{result}\n```'
            await ctx.reply(f'{result}')
        else:
            await ctx.reply('No valid code block found.')


async def setup(bot):
    await bot.add_cog(Misc(bot))
