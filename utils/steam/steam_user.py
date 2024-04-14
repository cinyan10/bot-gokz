import os
from datetime import datetime, timedelta

import requests

from utils.file_operation.file_operation import check_last_modified_date
from config import STEAM_API_KEY, IMAGES_LOCAL_PATH


def check_steam_bans(steamid):
    """
    Check the ban status of a Steam user using their SteamID64.

    Returns:
        dict: A dictionary containing ban status information about the user.
            The dictionary structure is as follows:
            {
                'SteamId': str,
                'CommunityBanned': bool,
                'VACBanned': bool,
                'NumberOfVACBans': int,
                'DaysSinceLastBan': int,
                'NumberOfGameBans': int,
                'EconomyBan': str
            }
            Note: 'EconomyBan' can be 'none' or 'probation' indicating the economy ban status.
    """

    steamid64 = convert_steamid(steamid, 2)
    url = f'http://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key={STEAM_API_KEY}&steamids={steamid64}'
    response = requests.get(url)
    ban_data = response.json()

    return ban_data['players'][0]


def convert_steamid(source_id, target_type=0) -> str | None:
    """
    Converts between SteamID, SteamID32, and SteamID64.

    :param source_id: The source SteamID in any format.
    :param target_type: The target format type ('steamid', 'steamid32', 'steamid64').
    :return: The converted SteamID in the target format.
    """
    source_id = str(source_id).upper()

    def steamid_to_steamid64(steamid):
        parts = steamid.split(':')
        y = int(parts[1])
        z = int(parts[2])
        return z * 2 + y + 76561197960265728

    def steamid64_to_steamid(steamid64):
        steamid64_base = 76561197960265728
        z = (steamid64 - steamid64_base) // 2
        y = (steamid64 - steamid64_base) % 2
        return f"STEAM_1:{y}:{z}"

    def steamid32_to_steamid64(steamid32):
        return steamid32 + 76561197960265728

    def steamid64_to_steamid32(steamid64):
        return steamid64 - 76561197960265728

    # Format source SteamID if it starts with STEAM_0
    if source_id.startswith("STEAM_0"):
        source_id = "STEAM_1" + source_id[7:]

    # Detect source SteamID format
    if ':' in source_id:  # STEAM_X:Y:Z format
        source_format = 'steamid'
        steamid64 = steamid_to_steamid64(source_id)
    elif source_id.isdigit():
        if len(source_id) > 10:  # SteamID64 format
            source_format = 'steamid64'
            steamid64 = int(source_id)
        else:  # SteamID32 format
            source_format = 'steamid32'
            steamid64 = steamid32_to_steamid64(int(source_id))
    else:
        return None

    # Convert to target format
    if target_type == 'steamid' or target_type == 0:
        return steamid64_to_steamid(steamid64) if source_format != 'steamid' else source_id
    elif target_type == 'steamid32' or target_type == 1 or target_type == 32:
        return steamid64_to_steamid32(steamid64) if source_format != 'steamid32' else int(source_id)
    elif target_type == 'steamid64' or target_type == 2 or target_type == 64:
        return steamid64 if source_format != 'steamid64' else int(source_id)
    else:
        raise Exception("Invalid target SteamID format")


def get_steam_user_info(steamid64, convert_id=True):
    """
        Get information about a Steam user using their SteamID64.

        Args:
            steamid64 (str): The SteamID of the user, can be any type.
            convert_id: Whether to convert the SteamID to SteamID64 format.
        Returns:
            dict or None: A dictionary containing information about the user, or None if an error occurs.
                The dictionary structure is as follows:
                {
                    'steamid': str,
                    'communityvisibilitystate': int,
                    'profilestate': int,
                    'personaname': str,
                    'commentpermission': int,
                    'profileurl': str,
                    'avatar': str,
                    'avatarmedium': str,
                    'avatarfull': str,
                    'avatarhash': str,
                    'lastlogoff': int,
                    'personastate': int,
                    'primaryclanid': str,
                    'timecreated': int,
                    'personastateflags': int,
                    'loccountrycode': str,
                    'locstatecode': str,
                    'loccityid': int
                }
        """
    if convert_id:
        steamid64 = convert_steamid(steamid64, 2)
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={STEAM_API_KEY}&steamids={steamid64}"
    response = requests.get(url)
    data = response.json()
    try:
        player_data = data['response']['players'][0]
        return player_data
    except IndexError:
        print(f"Failed to get user info for SteamID: {steamid64}")
        return None


def get_steam_avatar_localfile_url(steamid):
    steamid = convert_steamid(steamid)

    image_url = f'avatars/{steamid}.jpg'

    # 如果有直接返回相对路径
    filepath = os.path.join(IMAGES_LOCAL_PATH, image_url)
    last_modified_date = check_last_modified_date(filepath)

    if last_modified_date and (datetime.now() - last_modified_date <= timedelta(days=1)):
        return image_url

    # 如果无则下载
    avatar_url = get_steam_avatar_url(steamid)

    response = requests.get(avatar_url)

    if response.status_code == 200:
        # 如果请求成功，则将图片内容写入本地文件
        with open(os.path.join(IMAGES_LOCAL_PATH, image_url), 'wb') as f:
            f.write(response.content)
        print(f'成功下载头像到{os.path.join(IMAGES_LOCAL_PATH, image_url)}')
        return image_url
    else:
        print('Failed to download image')
        return None


def get_steam_avatar_url(steamid):
    steamid64 = convert_steamid(steamid, 2)
    return get_steam_user_info(steamid64)['avatarfull']


def get_steam_user_name(steamid64):
    steamid64 = convert_steamid(steamid64, 2)
    return get_steam_user_info(steamid64)['personaname']
