import random
from datetime import datetime
from contextlib import closing
import mysql.connector

from bot_qq.qqutils.database.users import update_points
from config import DB_CONFIG


def insert_member(member_openid):
    with closing(mysql.connector.connect(**DB_CONFIG)) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(
                "INSERT INTO bot_qq.users (member_openid, steamid) VALUES (%s, %s)",
                (member_openid, ""),
            )
            conn.commit()


def check_member_exists(member_openid):
    with closing(mysql.connector.connect(**DB_CONFIG)) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(
                "SELECT member_openid FROM bot_qq.users WHERE member_openid = %s",
                (member_openid,),
            )
            result = cursor.fetchone()
            return bool(result)


def sign_in(member_openid):
    if not check_member_exists(member_openid):
        insert_member(member_openid)

    if check_sign_in(member_openid):
        return None

    points_earned = int(random.gauss(50, 15))
    points_earned = points_earned if points_earned > 0 else 0

    with closing(mysql.connector.connect(**DB_CONFIG)) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(
                "INSERT INTO bot_qq.sign_ins (member_openid, points_earned) VALUES (%s, %s)",
                (member_openid, points_earned),
            )
            conn.commit()

    update_points(member_openid, points_earned)

    return points_earned


def check_sign_in(member_openid):
    """查询今天是否已经签到过"""
    today_date = datetime.today().strftime("%Y-%m-%d")
    with closing(mysql.connector.connect(**DB_CONFIG)) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(
                "SELECT id FROM bot_qq.sign_ins WHERE member_openid = %s AND DATE(datetime_created) = %s",
                (member_openid, today_date),
            )
            existing_sign_in = cursor.fetchone()
            return bool(existing_sign_in)
