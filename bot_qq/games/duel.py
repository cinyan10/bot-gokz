import random
import asyncio
from datetime import datetime

import mysql.connector
from mysql.connector import Error
from botpy.message import GroupMessage

from bot_qq.qqutils.database.users import get_total_points, update_points
from bot_qq.qqutils.general import send
from config import DB_CONFIG


class Duel:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.message1: GroupMessage | None = None
        self.message2: GroupMessage | None = None
        self.bet_points: int = 0

        self.dist1 = random.gauss(273, 5)
        self.dist2 = random.gauss(273, 5)
        self.content1 = (
            f"{'你'.center(6, '　')}跳出了{format(self.dist1, '.3f')}\n"
            + f"|".ljust(int((self.dist1 - 240) / 2), "=")
            + "|"
        )
        self.content2 = (
            f"{'你'.center(6, '　')}跳出了{format(self.dist2, '.3f')}\n"
            + f"|".ljust(int((self.dist2 - 240) / 2), "=")
            + "|"
        )

        self.winner = None

    def reset(self):
        self.message1 = None
        self.message2 = None
        self.bet_points = 0

        self.dist1 = random.gauss(273, 5)
        self.dist2 = random.gauss(273, 5)

        self.content1 = (
            f"{'你'.center(6, '　')}跳出了{format(self.dist1, '.3f')}\n"
            + f"|".ljust(int((self.dist1 - 240) / 2), "=")
            + "|"
        )
        self.content2 = (
            f"{'你'.center(6, '　')}跳出了{format(self.dist2, '.3f')}\n"
            + f"|".ljust(int((self.dist1 - 240) / 2), "=")
            + "|"
        )

        self.winner = None

    def record_result(self):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            sql_insert_query = """ INSERT INTO bot_qq.ljpk (player1_openid, player2_openid, player1_distance, player2_distance, bet_points)
                                   VALUES (%s, %s, %s, %s, %s) """
            insert_tuple = (
                self.message1.author.member_openid,
                self.message2.author.member_openid,
                self.dist1,
                self.dist2,
                self.bet_points,
            )
            cursor.execute(sql_insert_query, insert_tuple)
            conn.commit()

            winner_openid = (
                self.message1.author.member_openid
                if self.dist1 > self.dist2
                else self.message2.author.member_openid
            )
            loser_openid = (
                self.message1.author.member_openid
                if self.dist1 < self.dist2
                else self.message2.author.member_openid
            )

            update_points(winner_openid, self.bet_points)
            update_points(loser_openid, -self.bet_points)

            cursor.close()
            conn.close()
        except Error as e:
            print(e)

    async def start_duel(self):
        if self.message1 and self.message2:
            self.winner = self.message1 if self.dist1 > self.dist2 else self.message2

            await send(self.message1, self.content1, msg_seq=2, st=True)
            await send(self.message2, self.content2, msg_seq=2, st=True)

            self.record_result()

            winner_points = get_total_points(self.winner.author.member_openid)
            await send(
                self.winner,
                f"🎉恭喜你在此次比拼中胜出！🎉\n获得 {self.bet_points} 积分. 当前积分 {winner_points} ",
                msg_seq=3,
                st=True,
            )

        self.reset()


async def cancel_duel_after_timeout(duel: Duel, timeout):
    await asyncio.sleep(timeout)
    if duel.message1 is not None:
        await send(duel.message1, "由于长时间无人接受，决斗已被自动取消", msg_seq=4)
        duel.message1 = None


if __name__ == "__main__":

    pass
