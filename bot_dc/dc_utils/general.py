from discord import Embed


async def get_or_create_message(channel, bot):
    async for message in channel.history(limit=1):
        if message.author == bot.user:
            return message

    return await channel.send(embed=Embed(title="Loading..."))


