import asyncio
import datetime

from discord import Embed

from utils.configs.web_urls import REDIR_URL
from utils.globalapi.kz_maps import get_map_tier
from utils.steam.server_a2s import aquery_server_status
from utils.steam.server_rcon import rcon_servers_info
from config import SERVER_LIST


async def query_server_markdown_line(address: tuple) -> str:
    info, players = await aquery_server_status(address)

    try:
        map_tier = get_map_tier(info.map_name)
    except Exception:
        return "🚫 **Timeout**\n"

    # server info
    server_str = (
        f"[**{info.server_name}**]({REDIR_URL}{address[0]}:{address[1]}) | "
        f"{info.player_count}/{info.max_players} | "
        f"*{info.map_name}* ({map_tier})\n"
    )

    # players
    players_str = ''
    if info.player_count > 0:
        for player in players:
            if player.name == '':
                players_str += '` ` '
            players_str += f"`{player.name.replace('`', '')}`  "
        players_str += '\n'

    return server_str + players_str


async def query_all_servers_markdown(servers: list[tuple]) -> str:
    tasks = [query_server_markdown_line(server) for server in servers]
    results = await asyncio.gather(*tasks)

    content = ''
    for result in results:
        content += result

    return content


async def get_servers_status_embed():
    content = await query_all_servers_markdown(SERVER_LIST)
    return Embed(
        title="SERVER LIST",
        description=content,
        color=0x58B9FF,
        timestamp=datetime.datetime.now(),
    )


def format_server_status_markdown_line(
    status_data: dict,
    show_player_profile_link=False,
    show_duration=False,
    redirect=True,
) -> str:

    if status_data is None:
        return "🚫 **Server Query Timeout**\n"

    info = status_data
    players = status_data['players']

    map_tier = get_map_tier(info['map'])

    if redirect:
        server_str = (
            f"[**{info['server_name']}**]({REDIR_URL}{info['address']}) | "
            f"{info['player_count']}/{info['max_players']} | "
            f"*{info['map']}* ({map_tier})\n"
        )
    else:
        server_str = (
            f"[**{info['server_name']}**](https://www.axekz.com/) | "
            f"{info['player_count']}/{info['max_players']} | "
            f"*{info['map']}* ({map_tier})\n"
        )

    # players
    players_str = ''
    if info['player_count'] > 0:
        players_str += '> '
        for player in players:
            if show_player_profile_link:
                if player['name'] == '':
                    players_str += '` ` '
                players_str += (
                    f"[{player['name']}](https://kzgo.eu/players/{player['steamid']}) "
                )

                if show_duration:
                    players_str += f"- `{player['duration']}`  "

            else:
                if player['name'] == '':
                    players_str += '` ` '
                if show_duration:
                    players_str += (
                        f"`{player['name'].replace('`', '')} - {player['duration']}`  "
                    )
                else:
                    players_str += f"`{player['name'].replace('`', '')}`  "

        players_str += '\n'

    return server_str + players_str


def format_server_status_general_line(
    status_data: dict, show_duration=False, show_empty_server=True
) -> str:

    if status_data is None:
        if show_empty_server:
            return "🚫 服务器查询失败\n"
        else:
            return ''

    info = status_data
    players = status_data['players']

    if not show_empty_server:
        if not info['player_count']:
            return ''

    map_tier = get_map_tier(info['map'])

    # server info
    server_str = f"{info['server_name']} ({info['player_count']}/{info['max_players']}) | {info['map']} ({map_tier})\n"

    # players
    players_str = ''
    if info['player_count'] > 0:
        for player in players:
            if player['name'] == '':
                players_str += '`-` '
            if show_duration:
                players_str += (
                    f"{player['name'].replace('`', '')} - {player['duration']}  "
                )
            else:
                players_str += f"{player['name'].replace('`', '')}  "

        players_str += '\n'

    return server_str + players_str


async def servers_status_embed(
    show_player_profile_link=False, show_duration=False, redirect=True
) -> Embed:
    status_datas = await rcon_servers_info()
    content = ''
    for data in status_datas:
        content += format_server_status_markdown_line(
            data,
            show_player_profile_link=show_player_profile_link,
            show_duration=show_duration,
            redirect=redirect,
        )

    return Embed(
        title="SERVER LIST",
        description=content,
        color=0x58B9FF,
        timestamp=datetime.datetime.now(),
    )


if __name__ == '__main__':
    status_datas = asyncio.run(rcon_servers_info())
    content = ''
    for data in status_datas:
        content += format_server_status_markdown_line(data)

    print(content)
    pass
