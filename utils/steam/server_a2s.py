import asyncio

import a2s

from config import CS2_SERVER


def query_server_status(address: tuple):
    try:
        info = query_server_info(address)
        players = query_server_players(address)
        return info, players
    except asyncio.exceptions.TimeoutError as e:
        print(f"Error: {e}")


def query_server_players(address: tuple):
    """
    "index": 0,
    "name": "Mamth",
    "score": 0,
    "duration": 58281.17578125
    """
    try:
        players = a2s.players(address)
        return players
    except asyncio.exceptions.TimeoutError as e:
        print(f"Error: {e}")
        return


def query_server_info(address: tuple):
    """
    "protocol": 17,
    "server_name": "AXE Kztimer 北京 #5",
    "map_name": "kz_cdr_slash_final",
    "folder": "csgo",
    "game": "Counter-Strike: Global Offensive",
    "app_id": 730,
    "player_count": 4,
    "max_players": 1,
    "bot_count": 1,
    "server_type": "d",
    "platform": "l",
    "password_protected": false,
    "vac_enabled": true,
    "version": "1.38.8.1",
    "edf": 161,
    "port": 10005,
    "steam_id": null,
    "stv_port": null,
    "stv_name": null,
    "keywords": "KZTimer,KZTimer 1.106,Tickrate 128,hidden,secure",
    "game_id": 730,
    "ping": 0.05771624999943015
    """
    try:
        info = a2s.info(address)
        return info
    except asyncio.exceptions.TimeoutError as e:
        print(f"Error: {e}")
        return


async def aquery_server_info(address: tuple):
    try:
        info = await a2s.ainfo(address)
        return info
    except asyncio.exceptions.TimeoutError as e:
        print(f"Error: {e}")
        return


async def aquery_server_players(address: tuple):
    try:
        players = await a2s.aplayers(address)
        return players
    except asyncio.exceptions.TimeoutError as e:
        print(f"Error: {e}")
        return


async def aquery_server_status(address: tuple):
    try:
        info_task = a2s.ainfo(address)
        players_task = a2s.aplayers(address)
        info, players = await asyncio.gather(info_task, players_task)
        return info, players
    except asyncio.exceptions.TimeoutError:
        print(f"timeout connect to {address}")
        return None, None


async def aquery_all_servers(servers: list[tuple]):
    tasks = [query_server_info(server) for server in servers]
    return await asyncio.gather(*tasks)


if __name__ == "__main__":
    info = a2s.info(CS2_SERVER[0])
    print(info)
