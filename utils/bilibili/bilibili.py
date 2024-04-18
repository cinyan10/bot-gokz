from bilibili_api import user
import asyncio

from bilibili_api.exceptions import ResponseCodeException

from bot_qq.qqutils.text import borders


def format_bili_info(data: dict) -> str:
    if data is None:
        return "用户不存在，请检查你输入的UID格式是否正确"

    content = f"""
昵称:  {data['name']}
UID:   {data['mid']}
性别:  {data['sex']}
等级:  {data['level']}
{data['sign']}
"""

    content = borders(content)

    return content


def format_bili_live_info(data: dict) -> str:
    if data is None:
        return "用户不存在，请检查你输入的UID格式是否正确"

    live = data['live_room']
    if live['roomStatus'] == 0:
        return "该用户当前未开通直播间"

    content = f"""
{live['title']}
{live['url']}
    """

    content = borders(content)

    return content


async def get_bili_user_info(uid: int) -> dict | None:
    bili_user = user.User(uid)
    try:
        data = await bili_user.get_user_info()
        return data
    except ResponseCodeException:
        return None


if __name__ == '__main__':
    data = asyncio.run(get_bili_user_info(295323770))
    print(format_bili_info(data))
    pass
