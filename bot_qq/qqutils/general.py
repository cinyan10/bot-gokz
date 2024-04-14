import steam.steamid
from botpy.message import GroupMessage
import difflib

from utils.database.firstjoin import get_mostactive_data, get_firstjoin_data
from bot_qq.qqutils.database.users import get_user_info
from utils.globalapi.kz_mode import format_kzmode
from utils.misc.misc import format_string_to_datetime, seconds_to_hms
from utils.steam.steam import convert_steamid
from config import RESOURCE_URL
from utils.configs.gokz import MAP_TIERS


def my_format(
    str, width, align, sep=" "
):  # 定义函数接受三个参数：要输出的字符串(str)、总占用宽度（int）、对齐方式（str:l、r、c对应左右中）
    sigle = 0
    double = 0
    for i in str:  # 统计单字宽和双字宽的数目
        if len(i.encode("gb2312")) == 1:
            sigle += 1
        elif len(i.encode("gb2312")) == 2:
            double += 1
    if align == "l":
        return str + (width * 2 - sigle - double * 2) * sep
    elif align == "r":
        return (width * 2 - sigle - double * 2) * sep + str
    elif align == "c":
        return (
            int((width * 2 - sigle - double * 2) // 2) * sep
            + str
            + int(
                (width * 2 - sigle - double * 2) - (width * 2 - sigle - double * 2) // 2
            )
            * sep
        )


def print_format(
    string, width, fill="=", way="^", ed=""
):  # 格式输出函数,默认格式填充用单空格,不换行。
    try:
        count = 0  # 长宽度中文字符数量
        for word in string:  # 检测长宽度中文字符
            if (word >= "\u4e00" and word <= "\u9fa5") or word in [
                "；",
                "：",
                "，",
                "（",
                "）",
                "！",
                "？",
                "——",
                "……",
                "、",
                "》",
                "《",
            ]:
                count += 1
        width = width - count if width >= count else 0
        print("{0:{1}{2}{3}}".format(string, fill, way, width), end=ed, flush=True)
    except:
        print("print_format函数参数输入错误！")


def command(message: GroupMessage, cmd: str) -> list | None:
    if message.content.strip().startswith(cmd):
        return message.content.split(cmd)[1].strip().split(" ")
    else:
        return None


def search_map(map_name, threshold=0.2) -> list:
    matches = difflib.get_close_matches(
        map_name, MAP_TIERS.keys(), n=5, cutoff=threshold
    )
    return matches


def user_info_text(steamid) -> str:
    steamid = convert_steamid(steamid, 0)
    steamid64 = convert_steamid(steamid, 64)

    content = f"╔ {steamid}\n║ {steamid64}"

    firstjoin_data = get_firstjoin_data(steamid)
    if not firstjoin_data:
        return "玩家未加入过服务器, 无法获取信息"

    joindate = format_string_to_datetime(firstjoin_data["joindate"]).strftime(
        "%Y-%m-%d %H:%M"
    )
    lastseen = format_string_to_datetime(firstjoin_data["lastseen"]).strftime(
        "%Y-%m-%d %H:%M"
    )

    try:
        playtime = get_mostactive_data(steamid)["total"]
        hours, minutes, seconds = seconds_to_hms(playtime)
    except KeyError:
        hours, minutes, seconds = 0, 0, 0

    name = firstjoin_data["name"]

    content += f"""
║ 玩家名称:      {name}
║ 加入时间: {joindate}
║ 上次在线: {lastseen}
╚ 游玩时间: {hours}h {minutes}m {seconds}s
"""
    return content


async def check_params(message: GroupMessage, params: str | list):
    if type(params) is str:
        params = params.split()

    rs = {"steamid": None, "kz_mode": None, "others": None}

    for param in params:
        if param.startswith("http"):
            rs["steamid"] = convert_steamid(steam.steamid.from_url(param), 0)
            params.remove(param)
        elif convert_steamid(param, 0):
            rs["steamid"] = convert_steamid(param, 0)
            params.remove(param)
        elif format_kzmode(param):
            rs["kz_mode"] = format_kzmode(param)
            params.remove(param)

    rs["others"] = params

    if rs["steamid"] is None:
        user_data = get_user_info(message.author.member_openid)
        if user_data:
            rs["steamid"] = user_data["steamid"]
        else:
            await send(
                message,
                '请先 "/bind <steamid | url>", 支持 SteamID, SteamID64 及 Steam主页链接',
                st=False,
            )
            return False

    if rs["kz_mode"] is None:
        rs["kz_mode"] = format_kzmode(
            get_user_info(message.author.member_openid)["kz_mode"]
        )

    return rs


async def steamid_getter(message: GroupMessage, steamid):
    if steamid == "":
        try:
            steamid = get_user_info(message.author.member_openid)["steamid"]
            return steamid
        except:  # NOQA
            await send(message, "未绑定steamid")
            return None
    else:
        try:
            steamid = convert_steamid(steamid, 0)
            return steamid
        except:  # NOQA
            await send(message, "输入的teamID不正确")
            return None


async def send(
    message: GroupMessage, content: str, msg_seq=1, msg_type=0, st: bool = False
) -> None:
    """
    param st: 是否在消息前加换行符
    """
    if st:
        content = "\n" + content

    await message._api.post_group_message(  # NOQA
        group_openid=message.group_openid,
        msg_type=msg_type,
        msg_id=message.id,
        msg_seq=msg_seq,  # NOQA
        content=content,
    )


async def send_img(
    message: GroupMessage, url: str, msg_seq=2, fastdl=True, debug=False
) -> None:
    if fastdl:
        file_url = RESOURCE_URL + "images/" + url  # 这里需要填写上传的资源Url
    else:
        file_url = url

    if debug:
        print(file_url)

    uploadMedia = await message._api.post_group_file(  # NOQA
        group_openid=message.group_openid,
        file_type=1,  # 文件类型要对应上，具体支持的类型见方法说明
        url=file_url,  # 文件Url
    )

    # 资源上传后，会得到Media，用于发送消息
    await message._api.post_group_message(  # NOQA
        group_openid=message.group_openid,
        msg_type=7,  # 7表示富媒体类型
        msg_id=message.id,
        msg_seq=msg_seq,
        media=uploadMedia,
    )


async def send_voice(
    message: GroupMessage, filename: str, msg_seq=2, add_ed=True, debug=False
) -> None:
    if add_ed:
        file_url = RESOURCE_URL + "audio/" + filename + ".silk"
    else:
        file_url = RESOURCE_URL + "audio/" + filename

    if debug:
        print(file_url)

    uploadMedia = await message._api.post_group_file(  # NOQA
        group_openid=message.group_openid, file_type=3, url=file_url
    )

    # 资源上传后，会得到Media，用于发送消息
    await message._api.post_group_message(  # NOQA
        group_openid=message.group_openid,
        msg_type=7,  # 7表示富媒体类型
        msg_id=message.id,
        msg_seq=msg_seq,
        media=uploadMedia,
    )


if __name__ == "__main__":
    pass
