import asyncio
import random

from botpy.message import GroupMessage

from bot_qq.games.guess_map import GuessMap
from bot_qq.qqutils.database.users import get_total_points
from bot_qq.games.duel import Duel, cancel_duel_after_timeout
from bot_qq.qqutils.ext import Command
from bot_qq.qqutils.general import send, send_voice

d = Duel()
gm = GuessMap()


@Command("ljpk")
async def lj_pk(message, params):
    opponent = params[0].replace("@", "")
    if opponent == "":
        opponent = "对手"
    distance1 = random.gauss(273, 5)
    distance2 = random.gauss(273, 5)
    content = f"正在与 {opponent} 比拼lj！\n"
    content += f"{'你'.center(6, '　')}跳出了{format(distance1, '.3f')}\n"
    content += f"|".ljust(int((distance1 - 240) / 2), "=") + "|"
    content += f"\n{opponent.center(6, '　')}跳出了{format(distance2, '.3f')}\n"
    content += f"|".ljust(int((distance2 - 240) / 2), "=") + "|" + "\n"

    if distance1 > distance2:
        content += f"你在此次比拼中胜出！🍾"
        await send(message, content=content)
        await send_voice(message, "tooeasy")

    elif distance1 < distance2:
        content += f"你在此次比拼中落败，{opponent}胜出"
        await send(message, content=content)
        await send_voice(message, "noob_practice_more")

    else:
        content += "居然打平了"
        await send(message, content=content)


@Command("duel", "决斗", "pk")
async def lj_duel(message: GroupMessage, params=None):
    global d
    try:
        if not params or not params[0]:
            bet_points = 5
        else:
            bet_points = int(params[0])
            if bet_points < 0:
                return await send(message, "赌注不能是负数")
    except ValueError:
        return await send(message, "赌注必须是整数")

    bet_points = d.bet_points if d.bet_points else bet_points

    pts = get_total_points(message.author.member_openid)
    pts = pts if pts else 0

    if pts < bet_points:
        return await send(message, f"积分不足, 无法决斗。当前积分: {pts}")

    if d.message1 is None:
        d.message1 = message
        d.bet_points = bet_points
        await send(
            message,
            f'决斗发起成功, 赌注: {bet_points} 积分\n等待对手中... @我输入 "!pk" 接受决斗',
        )
        asyncio.ensure_future(cancel_duel_after_timeout(d, 120))

    elif d.message1.author.member_openid == message.author.member_openid:
        await send(message, "你是影流之主吗, 自己和自己决斗")

    else:
        d.message2 = message
        await send(message, "接收决斗成功, 开始决斗")
        await d.start_duel()


@Command("猜地图", "猜图", "ct")
async def guess_mapp(message: GroupMessage, params=None):
    tier1, tier2 = 1, 7

    try:
        if len(params) in [1, 2]:
            tiers = list(map(int, params))
            if all(1 <= tier <= 7 for tier in tiers):
                tier1, tier2 = tiers[0], tiers[-1]
            else:
                await send(message, "你有病吗, 你家KZ有这个难度")
                return
    except ValueError:
        await send(message, "请输入整数难度")
        return

    if tier1 not in range(1, 8) or tier2 not in range(1, 8):
        return await send(message, "你有病吗, 你家KZ有这个难度")

    global gm
    if gm.message is None:
        gm.message = message
        await gm.start(tier1, tier2)
    else:
        await send(message, "已经有猜图游戏在运行了")
