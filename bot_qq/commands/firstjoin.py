from botpy.message import GroupMessage

from bot_qq.qqutils.database.users import get_user_info
from bot_qq.qqutils.ext import Command
from bot_qq.qqutils.general import check_params, send, user_info_text, send_img
from bot_qq.qqutils.ip import query_ip_location
from bot_qq.qqutils.text import borders
from utils.database.firstjoin import get_firstjoin_data, find_player
from utils.steam.server_rcon import rcon_all_servers
from utils.steam.steam_user import get_steam_avatar_localfile_url


@Command("开河")
async def kaihe(message, params):
    params = await check_params(message, params)
    if not params:
        return

    steamid = params["steamid"]

    data = get_firstjoin_data(steamid)
    ip_data = None
    try:
        ip_data = query_ip_location(data["ip"])
    except Exception:
        await send(message, "没在服务器玩过开不了")

    content = f"""
{steamid}
玩家名:   {data['name']}
IP地址:   {ip_data['ip']}
国家:      {ip_data['country']}
省份:      {ip_data['region']}
城市:      {ip_data['city']}
ISP:        {ip_data['isp']}
邮编:      {ip_data['postal_code']}
地区码:   {ip_data['area_code']}
    """
    content = borders(content)

    await send(message, content)


@Command("find")
async def find(message, params):
    steamids = find_player(params[0])
    content = ""
    if steamids:
        for steamid in steamids:
            content += "===================\n"
            content += user_info_text(steamid)
        await send(message, content=content)
    else:
        await send(message, "未找到该玩家")


@Command("wl", "白名单")
async def whitelist(message: GroupMessage, params=None):
    steamid = get_user_info(message.author.member_openid)["steamid"]

    if not steamid:
        await send(
            message,
            '请先 "/bind <steamid | url>", 支持 SteamID, SteamID64 及 Steam主页链接',
            st=False,
        )
        return

    rs = await rcon_all_servers("sm_whitelist_add", f'"{steamid}"')
    for r in rs:
        if r:
            if "successfully added to" in r:
                await send(message, "✅ 白名单添加成功")
                await rcon_all_servers("sm_whitelist_reload")
                return
            else:
                await send(message, "❌ 白名单添加失败")


@Command("info")
async def info(message: GroupMessage, params):
    rs = await check_params(message, params)
    if not rs:
        return
    steamid = rs["steamid"]

    content = user_info_text(steamid)

    try:
        await send_img(message, get_steam_avatar_localfile_url(steamid), msg_seq=1)
    finally:
        await send(message, content, msg_seq=2)
