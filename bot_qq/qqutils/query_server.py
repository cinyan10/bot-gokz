
from bot_dc.dc_utils.query_server import format_server_status_general_line

from utils.steam.server_rcon import rcon_servers_info


async def servers_status_text(show_empty_server=True, show_duration=False) -> str:
    status_datas = await rcon_servers_info()
    content = ''
    for data in status_datas:
        content += format_server_status_general_line(
            data,
            show_empty_server=show_empty_server,
            show_duration=show_duration
        )

    return content


if __name__ == '__main__':
    pass
