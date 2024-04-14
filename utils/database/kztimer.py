import mysql.connector

from utils.steam.steam_user import convert_steamid
from config import DB_CONFIG


def get_top_players(limit=10):
    cursor = None
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT steamid, name, country, points, winratio, pointsratio, finishedmaps, multiplier, finishedmapstp, finishedmapspro, lastseen FROM kztimer.playerrank ORDER BY points DESC LIMIT %s",
            (limit,),
        )
        result = cursor.fetchall()
        for row in result:
            row["rank_name"] = get_rank_name(row["points"])

        return result

    except mysql.connector.Error as e:
        print(f"MySQL error: {e}")
        return None

    finally:
        cursor.close()
        conn.close()


def get_player_rank(steamid):
    steamid = convert_steamid(steamid)
    cursor = None
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT steamid, name, country, points, winratio, pointsratio, finishedmaps, multiplier, finishedmapstp, finishedmapspro, lastseen FROM kztimer.playerrank WHERE steamid = %s",
            (steamid,),
        )
        result = cursor.fetchone()

        # 如果查询结果不为空，则计算排名并添加到结果中
        if result:
            cursor.execute(
                "SELECT COUNT(*) AS player_rank FROM kztimer.playerrank WHERE points > %s",
                (result["points"],),
            )
            rank_result = cursor.fetchone()
            rank = rank_result["player_rank"] + 1  # 从1开始排名
            result["rank"] = rank
            result["rank_name"] = get_rank_name(result["points"])

            date_obj = result["lastseen"]
            result["lastseen"] = date_obj.strftime("%Y年%m月%d日")

        return result

    except mysql.connector.Error as e:
        print(f"MySQL error: {e}")
        return None

    finally:
        cursor.close()
        conn.close()


def get_rank_name(points):
    if points < 3784:
        return "新手入门"
    elif points < 21439:
        return "初学乍练"
    elif points < 42878:
        return "略有小成"
    elif points < 88277:
        return "注入佳境"
    elif points < 151332:
        return "炉火纯青"
    elif points < 201776:
        return "技冠群雄"
    elif points < 315275:
        return "登峰造极"
    elif points < 504440:
        return "出神入化"
    else:
        return "萌新"


if __name__ == "__main__":
    pass
