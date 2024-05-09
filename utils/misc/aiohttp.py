import aiohttp
from aiohttp import ClientTimeout


async def aiohttp_get(url, params=None, timeout=15):
    async with aiohttp.ClientSession(timeout=ClientTimeout(total=timeout)) as session:
        async with session.get(url, params=params) as response:
            return await response.json()
