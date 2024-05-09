import difflib
import os
import random
from datetime import time, datetime

from botpy.message import GroupMessage

from bot_qq.qqutils.database.sign_ins import sign_in
from bot_qq.qqutils.database.users import get_total_points, update_points
from bot_qq.qqutils.ext import Command
from bot_qq.qqutils.general import send, send_voice, send_img
from bot_qq.qqutils.misc import execute_python_code
from config import LOCAL_PATH, LOCAL_AUDIO_PATH
from utils.database.firstjoin import get_recent_players
from utils.file_operation.file_operation import list_files


@Command('gn', '晚安')
async def good_night(message: GroupMessage, params=None):
    start_time = time(20, 0, 0)
    end_time = time(6, 0, 0)
    current_time = datetime.now().time()

    if start_time <= current_time <= end_time:
        await send(message, "晚安!😴💤⭐️🌙", )
        await send_voice(message, 'goodnight')
    else:
        await send(message, "这才几点, 你就要睡觉了?")


@Command('早上好', '早安', 'gm')
async def good_morning(message: GroupMessage, params=None):
    start_time = time(5, 0, 0)
    end_time = time(12, 0, 0)
    current_time = datetime.now().time()
    if start_time <= current_time <= end_time:
        await send(message, "早安!(๑╹ω╹๑ )☀️", )
        await send_voice(message, 'goodmorning')
    else:
        await send(message, f"都已经{datetime.now().strftime("%H")}点了, 还在早安呢")


@Command('yuyu', '玉玉')
async def yuyu(message: GroupMessage, params=None):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg']

    image_files = []

    for file_name in os.listdir(LOCAL_PATH + 'depression'):
        _, extension = os.path.splitext(file_name)
        if extension.lower() in image_extensions:
            image_files.append(file_name)

    await send_img(message, 'depression/' + random.choice(image_files))


@Command('anime', '二次元')
async def anime(message: GroupMessage, params=None):
    await random_image(message)


@Command('python', 'py', split_command=False)
async def python(message: GroupMessage, params=None):
    rs = execute_python_code(params)
    await send(message, rs)


@Command('签到', 'qd')
async def qian_dao(message: GroupMessage, params=None):
    points_earned = sign_in(message.author.member_openid)
    total = get_total_points(message.author.member_openid)

    if points_earned:
        await send(message, f"签到成功! 获得 {points_earned} 积分\n当前总积分: {total}")
    else:
        await send(message, f"今天已经签到过了, 明天再来吧\n当前总积分: {total}")


@Command("积分", "jf")
async def ji_fen(message: GroupMessage, params=None):
    total = get_total_points(message.author.member_openid)
    await send(message, f"当前总积分: {total}")


@Command('a', '音效', split_command=False)
async def audio(message: GroupMessage, params=None):
    silk_files = list_files(LOCAL_AUDIO_PATH, endswith='.silk')

    if params:
        file_dict = {}
        for file_name in silk_files:
            if '/' in file_name:
                file_dict[file_name.split('/')[1][:-5]] = file_name
            else:
                file_dict[file_name[:-5]] = file_name

        match = difflib.get_close_matches(params, file_dict.keys(), n=5, cutoff=0.2)[0]
        await send_voice(message, file_dict[match], add_ed=False)
    else:
        choice = random.choice(silk_files)
        await send_voice(message, choice, add_ed=False)


@Command("抽老婆", "clp")
async def roll_wife(message: GroupMessage, params=None):
    costs = 10
    total = get_total_points(message.author.member_openid)
    if total < costs:
        return await send(message, f"积分不足, 需要 {costs} 积分")

    update_points(message.author.member_openid, -costs)
    players = get_recent_players()
    wife = random.choice(players)
    await send(message, f"恭喜你抽到了 {wife['name']} | {wife['auth']}\n花费 {costs} 积分, 剩余 {total - costs}")
    await send_img(message, f"avatars/{wife['auth']}.jpg")


async def random_audio(message: GroupMessage, seq=2):
    silk_files = list_files(LOCAL_AUDIO_PATH, endswith='.silk', except_folder='qz')
    choice = random.choice(silk_files)
    await send_voice(message, choice, add_ed=False, msg_seq=seq)


async def random_image(message: GroupMessage, seq=2):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg']

    image_files = []

    for file_name in os.listdir(LOCAL_PATH + 'anime/'):
        _, extension = os.path.splitext(file_name)
        if extension.lower() in image_extensions:
            image_files.append(file_name)

    await send_img(message, 'anime/' + random.choice(image_files), msg_seq=seq)
