from contextlib import closing

import mysql.connector

from config import DB_CONFIG
from utils.steam.steam_user import convert_steamid


def get_user_info(member_openid):
    """
    Returns:
        dict: A dictionary containing the user's information. The keys in the dictionary are:
            - member_openid: The openid of the member.
            - qq_number: The QQ number of the member.
            - user_name: The name of the user.
            - steamid: The Steam ID of the user.
            - kz_mode: The KZ mode of the user.
            - bili_uid: The BiliBili UID of the user.
            - points: The points of the user.
            - date_created: The date when the user was created.
    """
    with mysql.connector.connect(**DB_CONFIG) as conn:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                "SELECT * FROM bot_qq.users WHERE member_openid = %s",
                (member_openid,),
            )
            result = cursor.fetchone()
            return result


def reset_steamid(member_openid):
    with mysql.connector.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE bot_qq.users SET steamid = NULL WHERE member_openid = %s",
                (member_openid,),
            )
            conn.commit()
            return cursor.rowcount > 0


def set_kzmode(member_openid, kzmode: str) -> bool:
    with mysql.connector.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE bot_qq.users SET kz_mode = %s WHERE member_openid = %s",
                (kzmode, member_openid),
            )
            conn.commit()
            return cursor.rowcount > 0


def update_steamid(member_openid, steamid, kz_mode="kz_timer"):
    steamid = convert_steamid(steamid)

    with mysql.connector.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO bot_qq.users (member_openid, steamid, kz_mode) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE steamid = %s",
                (member_openid, steamid, kz_mode, steamid),
            )
            conn.commit()
            return cursor.rowcount > 0


def update_points(member_openid, points_earned):
    with closing(mysql.connector.connect(**DB_CONFIG)) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(
                "UPDATE bot_qq.users SET points = points + %s WHERE member_openid = %s",
                (points_earned, member_openid),
            )
            conn.commit()


def get_total_points(member_openid):
    rs = get_user_info(member_openid)
    if rs:
        return rs["points"]
    return 0
