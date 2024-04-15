from botpy.message import GroupMessage

from bot_qq.qqutils.ext import Command
from bot_qq.qqutils.general import send
from bot_qq.qqutils.query_server import servers_status_text


@Command('s')
async def server_status_simple(message: GroupMessage, params=None):
    content = await servers_status_text(False, False)
    if content == '':
        content = '暂时没有人在服务器里玩噢'

    await send(message, content=content, st=True)


@Command('ls', 'list')
async def server_status_list(message: GroupMessage, params=None):
    content = await servers_status_text(True, True)
    await send(message, content=content, st=True)


@Command('yd')
async def nominate(message, param):
    return await send(message, '此指令暂不可用')

    # if param == '':
    #     await send(message, '你地图名都不给我，我怎么给你定图呢\n (ノ—_—)ノ~┴————┴')
    #     return
    #
    # map_name = search_map(param.split(';')[0])[0]
    #
    # for s in SERVER_LIST:
    #     if is_server_empty(s):
    #         server_name = query_server_name(s)
    #         try:
    #             sent_rcon(s, "changelevel " + map_name)
    #         except valve.rcon.RCONCommunicationError: # NOQA
    #             pass
    #         content = f'\n==={server_name}===\n'
    #         content += f'已为你更换地图 {map_name} T{MAP_TIERS[map_name]}\n'
    #
    #         is_map_shit = False
    #         for sp1 in SP1:
    #             if sp1 in map_name:
    #                 is_map_shit = True
    #                 break
    #         if is_map_shit:
    #             content += f'答辩图你也恰啊 (/ﾟДﾟ)/\n'
    #         else:
    #             content += f'Happy Kreedz! ヾ(*´▽‘*)ﾉ\n'
    #         await send(message, content=content)
    #         return
    #
    # await send(message, "暂时没有空服噢，定图失败")
