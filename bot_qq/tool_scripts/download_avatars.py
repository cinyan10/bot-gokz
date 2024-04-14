import os
import requests
from tqdm import tqdm

from utils.database.firstjoin import get_all_players_steamid
from utils.steam.steam_user import get_steam_avatar_url

def download_steam_avatars(players_steamid, save_path): # NOQA
    total_players = len(players_steamid)
    with tqdm(total=total_players, desc='Downloading avatars') as pbar:
        for steam_id in players_steamid:
            avatar_url = get_steam_avatar_url(steam_id)
            if avatar_url:
                try:
                    response = requests.get(avatar_url, stream=True)
                    response.raise_for_status()  # 检查请求是否成功
                    if response.status_code == 200:
                        file_name = f'{steam_id}.jpg'
                        file_path = os.path.join(save_path, file_name)
                        with open(file_path, 'wb') as f:
                            for chunk in response.iter_content(chunk_size=1024):
                                if chunk:
                                    f.write(chunk)
                        pbar.update(1)  # 更新总体进度条
                    else:
                        print(f'Failed to download avatar for {steam_id}')
                except requests.exceptions.RequestException as e:
                    print(f'Error downloading avatar for {steam_id}: {e}')


if __name__ == '__main__':
    players_steamid = get_all_players_steamid()  # 请替换为您要下载头像的玩家 SteamID
    save_path = '/www/wwwroot/fastdl.axekz.com/images/avatars/'  # 请指定保存头像的路径

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    download_steam_avatars(players_steamid, save_path)
