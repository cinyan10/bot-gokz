from bot_qq.qqutils.database.users import get_user_info
from bot_qq.qqutils.ext import Command
from bot_qq.qqutils.general import check_params, send_img
from bot_qq.tool_scripts.screenshot import (
    kzgoeu_compare_screenshot,
    vnl_screenshot_async,
    kzgoeu_screenshot_async,
)


@Command("compare")
async def compare(message, params):
    params = await check_params(message, params)
    steamid2 = params["steamid"]
    kz_mode = params["kz_mode"]

    steamid1 = get_user_info(message.author.member_openid)["steamid"]

    url = kzgoeu_compare_screenshot(steamid1, steamid2, kz_mode)
    await send_img(message, url)


@Command("kzgo")
async def kzgo(message, params):
    rs = await check_params(message, params)
    steamid = rs["steamid"]
    kz_mode = rs["kz_mode"]
    print(steamid, kz_mode)
    if kz_mode == "kz_vanilla":
        url = await vnl_screenshot_async(steamid)
        print("正在生vnl.kz图片", steamid)
    else:
        print("正在生成kzgo.eu图片", steamid, kz_mode)
        url = await kzgoeu_screenshot_async(steamid, kz_mode)
    await send_img(message, url)
