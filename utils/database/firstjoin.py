import mysql.connector

from config import DB_CONFIG
from utils.steam.steam_user import convert_steamid


def find_player(name):
    with mysql.connector.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            query = f"SELECT auth FROM firstjoin.firstjoin WHERE name LIKE '%{name}%'"
            cursor.execute(query)
            results = cursor.fetchall()

    if len(results) < 5:
        return [row[0] for row in results]
    else:
        return [row[0] for row in results[:5]]


def get_mostactive_data(steamid) -> dict:
    """
    The 'mostactive' table has the following columns:
    - playername: The name of the Steam user.
    - steamid: The SteamID of the user.
    - last_accountuse: The last time the user used their account.
    - timeCT: The total time the user has spent as a Counter-Terrorist.
    - timeTT: The total time the user has spent as a Terrorist.
    - timeSPE: The total time the user has spent as a Spectator.
    - total: The total time the user has spent in the game.
    """
    steamid = convert_steamid(steamid)
    with mysql.connector.connect(**DB_CONFIG) as conn:
        with conn.cursor(dictionary=True) as cursor:
            query = """SELECT * FROM firstjoin.mostactive WHERE steamid = %s"""
            cursor.execute(query, (steamid,))
            result = cursor.fetchone()
            return result or {}


def get_all_players_steamid():
    """return a list of steamID"""
    with mysql.connector.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            # Execute SQL query to retrieve Steam IDs with whitelist = 1
            cursor.execute("SELECT auth FROM firstjoin.firstjoin")

            whitelisted_players = cursor.fetchall()

            # Extract Steam IDs from the result and store them in a list
            steam_ids = [row[0] for row in whitelisted_players]
            return steam_ids


def get_firstjoin_data(steamid: str) -> dict:
    """
    Returns:
    dict: A dictionary containing the first join data for the user. If the user is not found, an empty dictionary is returned.
        - name: The name of the Steam user.
        - auth: The SteamID of the user.
        - ip: The IP address from which the user first joined.
        - joindate: The date when the user first joined.
        - lastseen: The date when the user was last seen.
        - timestamps: A list of timestamps representing the user's activity.
        - whitelist: A flag indicating whether the user is whitelisted.
    """
    steamid = convert_steamid(steamid)
    with mysql.connector.connect(**DB_CONFIG) as conn:
        with conn.cursor(dictionary=True) as cursor:
            query = """SELECT * FROM firstjoin.firstjoin WHERE auth = %s"""
            cursor.execute(query, (steamid,))
            result = cursor.fetchone()
            return result or {}


def get_recent_players(num: int = 50) -> list:
    """Returns a list of the most recent players who joined the server."""
    with mysql.connector.connect(**DB_CONFIG) as conn:
        with conn.cursor(dictionary=True) as cursor:
            query = f"""SELECT * FROM firstjoin.firstjoin ORDER BY lastseen DESC LIMIT {num}"""
            cursor.execute(query)
            results = cursor.fetchall()
            return results


if __name__ == "__main__":
    pass
