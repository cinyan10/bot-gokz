from textwrap import dedent

from botpy.message import GroupMessage
from aiohttp.client_exceptions import ClientResponseError

from utils.configs.gokz import MAP_TIERS
from utils.database.firstjoin import get_mostactive_data
from utils.database.gokz import get_ljpb
from bot_qq.qqutils.database.users import get_user_info
from utils.globalapi.gokzcn import fetch_playerdata
from utils.globalapi.kz_global_stats import (
    fetch_personal_purity,
    fetch_world_record,
    fetch_personal_recent,
    fetch_personal_best,
    KzGlobalStats,
)
from utils.globalapi.kz_mode import format_kzmode, globalapi_check, format_kzmode_simple
from utils.misc.aiohttp import aiohttp_get
from utils.misc.misc import format_seconds_to_time, record_format_time, seconds_to_hms
from utils.steam.steam import convert_steamid
from utils.steam.steam_user import get_steam_avatar_localfile_url
from bot_qq.qqutils.ext import Command
from bot_qq.qqutils.general import (
    check_params,
    send,
    search_map,
    send_img,
    send_voice,
    send_chart,
)
from botpy import logger


BASE_URL = 'http://47.238.188.6:8000'


@Command('stats')
async def personal_stats(message, params):
    rs = await check_params(message, params)
    steamid = rs["steamid"]
    query_url = f"{BASE_URL}/statistics/?steamid={steamid}"
    data = await aiohttp_get(query_url)

    content = dedent(
        f"""
        玩家名: {data['oldest_record']['player_name']}
        SteamID: {data['oldest_record']['steam_id']}
        =======================
        总记录数: {data['total_records']}
        总时间: {format_seconds_to_time(data['total_time'])}
        总TP数: {data['total_teleports']}
        总地图数: {data['total_maps']}
        平均时间: {format_seconds_to_time(data['avg_time'])}
        =======================
        游玩次数最多的地图: {data['most_played_map']} ({data['most_played_map_times']}次)
        游玩最长时间的地图: {data['most_played_time_map']} ({format_seconds_to_time(data['most_played_time_map_time'])})
        最长磨图时间: {format_seconds_to_time(data['max_map_time'])}
        =====最常玩的服务器=====: 
        {data['most_played_server']} {data['most_played_server_times']} 次，占比 {data['most_played_server_percentage']:.2f}%
        =====入坑时间=====
        地图名: {data['oldest_record']['map_name']}
        时间: {format_seconds_to_time(data['oldest_record']['time'])}
        传送次数: {data['oldest_record']['teleports']}
        服务器名: {data['oldest_record']['server_name']}
        创建时间: {data['oldest_record']['created_on']}
        """
    )

    await send(message, content)


@Command('calendar', '日历图')
async def player_heatmap(message, params):
    rs = await check_params(message, params)
    steamid = rs["steamid"]
    query_url = f"http://47.238.188.6:8000/charts/url/{steamid}/calendar"

    try:
        await send_chart(message, query_url)
    except Exception as e:
        await send(message, repr(e))


@Command('radar', '雷达')
async def player_radar_pie_chart(message, params):
    rs = await check_params(message, params)
    steamid = rs["steamid"]
    query_url = f"http://47.238.188.6:8000/charts/url/{steamid}/radar"

    try:
        await send_chart(message, query_url)
    except ClientResponseError as e:
        await send(message, "gokz.cn未找到该玩家")


@Command('cdt')
async def player_purity_graph(message, params):
    rs = await check_params(message, params)
    steamid = rs["steamid"]
    query_url = f"http://47.238.188.6:8000/charts/url/{steamid}/purity"
    await send_chart(message, query_url)


@Command('pd')
async def player_data(message, params):
    rs = await check_params(message, params)
    steamid = rs["steamid"]
    kz_mode = rs["kz_mode"]
    query_url = f"http://47.238.188.6:8000/charts/url/{steamid}/points?mode={kz_mode}"
    await send_chart(message, query_url)


@Command('td')
async def player_time_graph(message, params):
    rs = await check_params(message, params)
    steamid = rs["steamid"]
    query_url = f"http://47.238.188.6:8000/charts/url/{steamid}/playtime"
    await send_chart(message, query_url)


@Command('纯度', 'purity')
async def purity(message, params):
    rs = await check_params(message, params)
    steamid = rs["steamid"]
    kz_mode = rs["kz_mode"]
    logger.info(f"纯度查询: {steamid} {kz_mode}")

    data1 = fetch_personal_purity(steamid, kz_mode, exclusive=False)
    data2 = fetch_personal_purity(steamid, kz_mode, exclusive=True)
    try:
        playtime = get_mostactive_data(steamid)["total"]
        hours, minutes, seconds = seconds_to_hms(playtime)
    except KeyError:
        hours, minutes, seconds = 0, 0, 0

    content = f"""
=======纯度测试=======
ID: {steamid}
玩家名称:   {data1["name"]}
游戏模式:   {kz_mode}
游玩时间:   {hours}h {minutes}m {seconds}s
-----仅 AXE GOKZ API-----
总地图数:   {data1["total"]}
本服完成:   {data1["count"]}
百分比:   　{"{:.2%}".format(data1["percentage"])}
------包含以前的API------
总地图数:   {data2["total"]}
本服完成:   {data2["count"]}
百分比:　   {"{:.2%}".format(data2["percentage"])}
"""

    if (
        data2["percentage"] >= 0.3
        and data2['total'] >= 50
        or data2["count"] >= 200
        or hours >= 100
    ):
        content += '✅满足条件, 私信群主获取广州服IP'

    await send(message, content)


@Command("提纯")
async def ti_purity(message, params=None):
    rs = await check_params(message, params)
    steamid = rs["steamid"]
    kz_mode = rs["kz_mode"]

    limit = 20

    maps = fetch_personal_purity(steamid, kz_mode, exclusive=False)['maps']

    content = "可提纯地图:\n"
    content += "\n".join(maps[:limit])
    await send(message, content)


@Command("wr")
async def wr(message: GroupMessage, params=None):
    if len(params) == 0:
        await send(message, "你地图名都不给我，我查什么WR\n (ノ—_—)ノ~┴————┴")
        return

    kz_mode = format_kzmode(params[1])
    if kz_mode is None:
        kz_mode = get_user_info(message.author.member_openid)["kz_mode"]

    map_name = search_map(params[0])[0]

    content = f"""╔ 地图:　{map_name}
║ 难度:　T{MAP_TIERS[map_name]}
║ 模式:　{kz_mode}
╠═════存点记录═════"""

    try:
        data = fetch_world_record(map_name, mode=kz_mode, has_tp=True)
        content += f"""
║ {data['steam_id']}
║ 昵称:　　{data['player_name']}
║ 用时:　　{format_seconds_to_time(data['time'])}
║ 存点数:　{data['teleports']}
║ 分数:　　{data['points']}
║ 服务器:　{data['server_name']}
║ {record_format_time(data['created_on'])}"""

    except:
        content += f"\n╠ 未发现存点记录:"

    content += f"\n╠═════裸跳记录═════"
    try:
        pro = fetch_world_record(map_name, mode=kz_mode, has_tp=False)
        content += f"""
║ {pro['steam_id']}
║ 昵称:　　{pro['player_name']}
║ 用时:　　{format_seconds_to_time(pro['time'])}
║ 分数:　　{pro['points']}
║ 服务器:　{pro['server_name']}
╚ {record_format_time(pro['created_on'])}  ═══"""

    except:
        content += f"\n未发现裸跳记录:"

    try:
        await send_img(message, url="maps/" + map_name + ".jpg", msg_seq=1)
    except:
        pass
    await send(message, content, msg_seq=2)
    if "fafnir" in map_name:
        await send_voice(message, "fafnir", msg_seq=3)


@Command("pr")
async def pr(message: GroupMessage, params):
    rs = await check_params(message, params)
    logger.info(f"pr: {rs}")
    if not rs:
        return

    steamid = rs["steamid"]
    kz_mode = rs["kz_mode"]

    data = fetch_personal_recent(steamid, kz_mode)

    content = dedent(
        f"""
        ╔ 地图:　　{data['map_name']}
        ║ 难度:　　T{MAP_TIERS[data['map_name']]}
        ║ 模式:　　{kz_mode}
        ║ 玩家:　　{data['player_name']} 
        ║ 用时:　　{format_seconds_to_time(data['time'])}
        ║ 存点数:　{data['teleports']}
        ║ 分数:　　{data['points']}
        ║ 服务器:　{data['server_name']}
        ╚ {record_format_time(data['created_on'])} ═══”"""
    )

    await send(message, content)
    try:
        await send_img(message, url="maps/" + data["map_name"] + ".jpg")
    except Exception as e:
        logger.info(repr(e))


@Command('pb')
async def pb(message, params):
    rs = await check_params(message, params)
    if not rs:
        return

    steamid = rs["steamid"]
    kz_mode = rs["kz_mode"]
    try:
        map_name = rs["others"][0]
    except IndexError:
        return await send(message, "(￣^￣) 你地图名都不给我，我查什么PB")

    map_name = search_map(map_name)[0]

    content = f"""
╔ 地图:　{map_name}
║ 难度:　T{MAP_TIERS[map_name]}
║ 模式:　{kz_mode}
╠═════存点记录═════"""
    try:
        data = fetch_personal_best(steamid, map_name, kz_mode)
        content += f"""
║ 玩家:　　{data['player_name']}
║ 用时:　　{format_seconds_to_time(data['time'])}
║ 存点:　　{data['teleports']}
║ 分数:　　{data['points']}
║ 服务器:　{data['server_name']}
║ {record_format_time(data['created_on'])} """
    except Exception as e:
        content += f"\n║ 未发现存点记录"

    content += f"\n╠═════裸跳记录═════"
    try:
        pro = fetch_personal_best(steamid, map_name, kz_mode, has_tp=False)
        content += f"""
║ 玩家:　　{pro['player_name']}
║ 用时:　　{format_seconds_to_time(pro['time'])}
║ 分数:　　{pro['points']}
║ 服务器:　{pro['server_name']}
╚ {record_format_time(pro['created_on'])} ═══"""

    except Exception as e:
        content += f"\n╚ 未发现裸跳记录"

    try:
        await send_img(message, url="maps/" + map_name + ".jpg", msg_seq=1)
    except:
        pass

    await send(message, content, msg_seq=2)
    if "fafnir" in map_name:
        await send_voice(message, "fafnir", msg_seq=3)


@Command("api")
async def api_check(message, params=None):
    rs = globalapi_check()
    if rs:
        await send(message, content="✅GlobalAPI 正常")
    else:
        await send(message, content="❌GlobalAPI 寄了")


@Command("kztext")
async def kz_text(message: GroupMessage, params):
    rs = await check_params(message, params)
    steamid = rs["steamid"]
    kz_mode = format_kzmode_simple(rs["kz_mode"])

    if steamid is None:
        await send(message, "请先绑定steamid")
        return False
    steamid = convert_steamid(steamid, "steamid")
    steamid64 = convert_steamid(steamid, "steamid64")
    steamid32 = convert_steamid(steamid, "steamid32")
    stats = KzGlobalStats(steamid64=steamid64, kzmode=kz_mode)
    content = stats.text_stats()

    # gokz.cn 排名
    try:
        cn_data = fetch_playerdata(steamid, kz_mode)
        content += f"cn排名：{cn_data['ranking']} 技术得分：{cn_data['point_skill']}\n"
    except Exception as e:  # NOQA
        content += f"获取cn数据失败\n"

    # 服务器内时间
    try:
        seconds = get_mostactive_data(steamid)["total"]
        h, m, s = seconds_to_hms(seconds)
        content += f"服务器内游玩时间：{h} 时 {m}分 {s}秒\n"
    except:
        content += "获取服务器内游玩时间失败"

    # LJPB
    try:
        ljpb_data = get_ljpb(steamid32, kz_mode, 0, 0)
        content += f"LJPB : {ljpb_data['Distance']}"
    except:
        content += "获取LJPB数据失败"

    await send_img(message, get_steam_avatar_localfile_url(steamid), msg_seq=1)
    await send(message, content=content, msg_seq=2)
