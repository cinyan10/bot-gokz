from botpy.message import GroupMessage

from utils.database.kztimer import get_player_rank, get_top_players
from bot_qq.qqutils.ext import Command
from bot_qq.qqutils.general import check_params, send


@Command('kztrank')
async def kztrank(message: GroupMessage, params):
    rs = await check_params(message, params)
    if not rs:
        return

    steamid = rs['steamid']

    player = get_player_rank(steamid)
    if player is None:
        await send(message, '未查询到该玩家')
        return

    content = f'''╔══Kztimer服务器排名══
║ 玩家:　　　{player['name']}
║ 排名:　　　{player['rank']}
║ 分数:　　　{'{:,}'.format(player['points'])} pts
║ 段位:　　　{player['rank_name']}
║ 地图数:　　{player['finishedmaps']}
║ 存点:　　　{player['finishedmapstp']}
║ 裸跳:　　　{player['finishedmapspro']}
╚ 上次在线:　{player['lastseen']}'''

    await send(message, content)


@Command('kzttop')
async def kzttop(message: GroupMessage, params=None):
    top_datas = get_top_players(limit=10)
    content = '\n' + 'kztimer排行榜'.center(25, '=')
    rank = 0
    for data in top_datas:
        rank += 1
        content += f"""
{str(rank).ljust(22, '-')}
{data['name']} | {data['rank_name']} | {"{:,}".format(data['points'])}pts 
{data['steamid']}"""

    await send(message, content, st=False)
