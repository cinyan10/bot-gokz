from contextlib import closing

import mysql.connector

from config import DB_CONFIG


def get_conn(database: str = None) -> mysql.connector.connect:
    DB_CONFIG["database"] = database
    return mysql.connector.connect(**DB_CONFIG)


def query_data(sql) -> list[dict]:
    conn = get_conn()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        conn.close()


if __name__ == "__main__":

    pass
