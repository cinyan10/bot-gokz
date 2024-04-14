import asyncio
from contextlib import closing
from difflib import SequenceMatcher
from datetime import datetime
import mysql.connector
import random

from bot_qq.qqutils.database.users import update_points
from config import DB_CONFIG
from botpy.message import GroupMessage

from bot_qq.qqutils.general import send, send_img
from utils.configs.gokz import MAP_TIERS
from utils.globalapi.gokz import get_maps_in_tier_range


class GuessMap:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.recent_maps = []

        self.message: GroupMessage | None = None
        self.map_name = None
        self.map_tier = None
        self.map_prefix = None
        self.map_realm = None
        self.winner = None
        self.msg_seq = 1
        self.start_time = None

        self.hint_task = None
        self.end_task = None

    def reset(self):
        self.message = None
        self.map_name = None
        self.map_tier = None
        self.map_prefix = None
        self.map_realm = None
        self.winner = None
        self.msg_seq = 1
        self.start_time = None

        self.hint_task = None
        self.end_task = None

    async def send_game_rule(self):
        await send(
            self.message,
            "猜猜地图名是什么 回答格式:\n@我 <地图名>",
            msg_seq=self.msg_seq,
        )
        self.msg_seq += 1

    async def send_map_image(self):
        await send_img(self.message, f"maps/{self.map_name}.jpg", msg_seq=self.msg_seq)
        self.msg_seq += 1

    async def start(self, tier1, tier2):
        self.start_time = datetime.now()

        available_maps = list(
            set(get_maps_in_tier_range(tier1, tier2).keys()) - set(self.recent_maps)
        )
        self.map_name = random.choice(available_maps)
        self.recent_maps.append(self.map_name)
        self.recent_maps = self.recent_maps[-15:]
        print(f"开始猜图:", self.map_name)

        self.map_prefix = self.map_name.split("_")[0]
        self.map_realm = self.map_name.split("_", 1)[1]
        self.map_tier = MAP_TIERS[self.map_name]

        await self.send_game_rule()
        await self.send_map_image()

        self.hint_task = asyncio.ensure_future(self.hint(30))
        self.end_task = asyncio.ensure_future(self.end_if_nobody_guess_right(60))

    async def guess(self, message: GroupMessage, guess_map_name: str):
        if self.winner:
            await send(
                message,
                f"已经有人猜对了, 答案是{self.map_name}, 难度T{self.map_tier}",
            )
            return

        similarity = SequenceMatcher(None, guess_map_name, self.map_name).ratio()
        if similarity < 0.6:
            await send(
                message,
                f"差的有点远, 再试试看吧！",
            )
        elif 0.6 <= similarity < 0.8:
            await send(
                message,
                f"有几分相似了, 再试试看吧！",
            )
        elif 0.8 <= similarity < 1:
            await send(
                message,
                f"你猜的很接近了，再试试看吧！",
            )
        elif guess_map_name == self.map_name:
            self.winner = message.author.member_openid
            self.hint_task.cancel()
            self.end_task.cancel()

            await send(
                message,
                f"恭喜你答对了, 答案是{self.map_name}, 难度T{self.map_tier}",
            )
            pts = self.insert_into_guess_map()
            if pts == 0:
                await send(
                    message, "今天已经获得过三次积分了, 无法再获得积分了", msg_seq=2
                )
            else:
                await send(message, f"你获得了{pts}积分", msg_seq=2)
            self.reset()
        else:
            await send(
                message,
                f"不对噢, 请继续",
                msg_seq=1,
            )

    async def hint(self, timeout=30):
        await asyncio.sleep(timeout)
        prompt = ""
        for char in self.map_realm:
            if char.isalpha() or char.isdigit():
                prompt += "-"
            elif char == "_":
                prompt += "_"
        await send(
            self.message,
            f"30秒了还没有人猜出来噢, 给你们点提示吧\n{self.map_prefix}_{self.map_realm[0]}{prompt[1:]}, 难度T{self.map_tier}",
            msg_seq=self.msg_seq,
        )
        self.msg_seq += 1

    async def end_if_nobody_guess_right(self, timeout):
        await asyncio.sleep(timeout)
        if self.winner is None:
            await send(
                self.message,
                f"一分钟了没有人猜出来噢, 现在公布答案\n地图是: {self.map_name}, 难度T{self.map_tier}",
                msg_seq=self.msg_seq + 1,
            )
            self.reset()

    def insert_into_guess_map(self):
        points_earned = int(random.gauss(20, 2))

        with closing(mysql.connector.connect(**DB_CONFIG)) as connection:
            with closing(connection.cursor()) as cursor:
                # Check how many times the player has earned points today
                query = """
                        SELECT COUNT(*) FROM bot_qq.guess_map
                        WHERE DATE(created_time) = CURDATE() AND member_openid = %s
                        """
                cursor.execute(query, (self.winner,))
                count = cursor.fetchone()[0]

                # 检查今天是否获得过三次积分
                if count >= 3:
                    points_earned = 0

                # 更新积分
                query = """
                INSERT INTO bot_qq.guess_map (member_openid, points_earned)
                VALUES (%s, %s)
                """

                update_points(self.winner, points_earned)
                cursor.execute(query, (self.winner, points_earned))
                connection.commit()
                return points_earned


if __name__ == "__main__":
    pass
