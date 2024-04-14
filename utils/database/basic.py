
import mysql.connector

from config import DB_CONFIG


class Database:
    def __init__(self, database_name : str):
        self.conn = get_conn(database_name)

    def query(self, sql):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            self.conn.close()


def get_conn(database_name: str = None) -> mysql.connector.connect:
    DB_CONFIG['database'] = database_name
    return mysql.connector.connect(**DB_CONFIG)


def query_data(conn, sql) -> list[dict]:
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def write_data(conn, sql) -> None:
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    finally:
        conn.close()


if __name__ == '__main__':
    db = Database('firstjoin')
    pass
