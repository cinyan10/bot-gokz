from utils.database.firstjoin import get_firstjoin_data
from utils.database.gokz import get_ljpb_stats
from bot_qq.qqutils.ext import Command
from bot_qq.qqutils.general import check_params, send
from bot_qq.qqutils.text import borders


@Command("ljpb")
async def ljpb(message, params):
    params = await check_params(message, params)
    steamid = params['steamid']
    kz_mode = params['kz_mode']

    data = get_ljpb_stats(steamid, kz_mode)
    name = get_firstjoin_data(steamid)['name']
    content = f"""ID: {steamid}
昵称:　　 {name}
类型:　　 {data['JumpType']}
模式:　　 {data['Mode']}
距离:　　 {data['Distance']}
板子:　　 {data['Block']}
加速:　　 {data['Strafes']}
同步:　　 {data['Sync']}
地速:　　 {data['Pre']}
空速:　　 {data['Max']}
滞空: 　　{data['Airtime']} 秒
{data['Created'].strftime('%Y年%m月%d日 %H:%M:%S')}"""

    content = borders(content)

    await send(message, '\n' + content)
