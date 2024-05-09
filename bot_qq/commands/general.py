import random

import steam.steamid
from botpy.message import GroupMessage
from botpy.types.inline import Button, RenderData, Action, Permission, KeyboardRow, Keyboard
from botpy.types.message import MessageMarkdownParams, MarkdownPayload, Ark, ArkKv, KeyboardPayload, Embed, EmbedField

from config import RESOURCE_URL
from bot_qq.configs.text import HELP_DOCS, REPLIES
from bot_qq.qqutils.database.users import update_steamid, set_kzmode, reset_steamid, bind_bili_uid
from utils.bilibili.bilibili import get_bili_user_info, format_bili_info
from utils.globalapi.gokz import lj_color
from utils.globalapi.kz_mode import format_kzmode
from bot_qq.qqutils.ext import Command
from bot_qq.qqutils.general import send, user_info_text, send_img
from utils.steam.steam_user import get_steam_user_info, convert_steamid


@Command('help')
async def send_help_info(message: GroupMessage, params=None):
    await send(message, HELP_DOCS)


@Command("test", split_command=False)
async def test(message: GroupMessage, params):
    """
    param st: 是否在消息前加换行符
    """
    await send_img(message, 'blob:http://47.238.188.6:8000/abd8f98b-5123-46d0-b5e2-beeea642e53d', use_fastdl=False)


def build_a_demo_keyboard() -> Keyboard:
    """
    创建一个只有一行且该行只有一个 button 的键盘
    """
    button1 = Button(
        id="1",
        render_data=RenderData(label="button", visited_label="BUTTON", style=0),
        action=Action(
            type=2,
            permission=Permission(type=2, specify_role_ids=["1"], specify_user_ids=["1"]),
            click_limit=10,
            data="/搜索",
            at_bot_show_channel_list=True,
        ),
    )

    row1 = KeyboardRow(buttons=[button1])
    return Keyboard(rows=[row1])


@Command('绑定', 'bind')
async def bind(message, params):

    if params[0] in ['bili', 'bilibili', '哔哩哔哩']:
        uid = params[1]
        data = await get_bili_user_info(uid)
        if data is None:
            await send(message, '无法获取到用户信息, 请检查你的UID格式是否正确')
            return
        # 更新数据库
        if bind_bili_uid(message.author.member_openid, uid):
            await send(message, f"绑定成功\n{format_bili_info(data)}")
            await send_img(message, data['face'], use_fastdl=False)
        else:
            await send(message, "绑定失败")

        return

    if not params:
        await send(message, '请输入steamid或主页链接噢')
        return

    param = params[0]

    if param.startswith('http'):
        steamid = convert_steamid(steam.steamid.from_url(param))
    else:
        steamid = convert_steamid(param)

        # 校验steamid是否合格
        try:
            steamid = get_steam_user_info(steamid)['steamid']
        except TypeError:
            await send(message, '无法获取到用户信息, 请检查你的steamid格式是否正确')
            return

    update_steamid(message.author.member_openid, steamid)

    rs = user_info_text(steamid)
    await send(message, f"绑定成功\n{rs}")


@Command('lj')
async def lj(message: GroupMessage, params=None):
    binds = params
    mid = 273
    sigma = 6
    bind_names = ''
    if binds:
        if '脚本' in binds:
            mid = 290
            sigma = 3
        else:
            if 'null' in binds:
                mid = mid + 2
                sigma = sigma + 0.5
                bind_names += 'null '
            if '-w' in binds:
                mid = mid + 1
                sigma = sigma - 0.5
                bind_names += '-w '
            if 'onekey' in binds:
                mid = mid + 3
                sigma = sigma + 1
                bind_names += 'onekey '
            if 'mouseslap' in binds:
                mid = mid + 2
                sigma = sigma - 0.5

    distance = random.gauss(mid, sigma)
    color = lj_color(distance)

    content = f"你LJ跳出了 {format(distance, ".3f")}!"
    if bind_names:
        content += f"\n但是你开了{bind_names}, 你这个binder!"
    if '脚本' in binds:
        content += f"\n但是你开了脚本, 喜提{random.choice(['ban0', "E神的认可👍", "荣誉序章"])}"

    await message._api.post_group_message(group_openid=message.group_openid,
                                          msg_id=message.id,
                                          msg_seq=1,  # NOQA
                                          content=content)

    file_url = RESOURCE_URL + 'audio/' + color + ".silk" # 这里需要填写上传的资源Url
    upload_media = await message._api.post_group_file(
        group_openid=message.group_openid,
        file_type=3,
        url=file_url
    )

    # 资源上传后，会得到Media，用于发送消息
    await message._api.post_group_message(
        group_openid=message.group_openid,
        msg_type=7,
        msg_id=message.id,
        msg_seq=2,
        media=upload_media
    )


@Command('mode')
async def set_kz_mode(message, params):
    kz_mode = format_kzmode(params[0])
    if kz_mode is None:
        await send(message, "请输入正确的kz模式", st=False)
        return

    rs = set_kzmode(message.author.member_openid, kz_mode)
    if rs:
        await send(message, "成功将你的模式设置为 " + kz_mode)
    elif rs is False:
        await send(message, f"你的默认模式已经是{kz_mode}")


@Command('unbind', '解绑')
async def unbind_steamid(message, params=None):
    if reset_steamid(message.author.member_openid):
        await send(message, "解绑成功", st=False)
    else:
        await send(message, "解绑失败", st=False)


@Command('ping')
async def ping(message, params=None):
    await send(message, random.choice(REPLIES), st=False)

