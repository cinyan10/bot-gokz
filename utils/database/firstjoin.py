import mysql.connector

from config import DB_CONFIG

DB_CONFIG["database"] = "firstjoin"


def get_player_name(steamid):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    try:
        # Define the SQL query to retrieve the values
        query = """SELECT name FROM firstjoin.firstjoin WHERE auth = %s"""
        cursor.execute(query, (steamid,))
        # Fetch the result (assuming only one row)
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return "你未来服务器游玩过噢, 无法查到昵称"

    except mysql.connector.Error as err:
        print("Error:", err)

    finally:
        cursor.close()
        conn.close()


def find_player(name):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    query = f"SELECT auth FROM firstjoin.firstjoin WHERE name LIKE '%{name}%'"
    cursor.execute(query)

    results = cursor.fetchall()

    conn.close()

    if len(results) < 5:
        return [row[0] for row in results]  # Extract and return the 'auth' values
    else:
        return []  # Return an empty list if there are more than or equal to 5 results


def update_whitelist_status(steamid):
    conn = mysql.connector.connect(**DB_CONFIG)
    try:
        # Update the whitelist status in the database
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE firstjoin.firstjoin SET whitelist = %s WHERE auth = %s",
            (1, steamid),
        )
        conn.commit()
        cursor.close()
        return True

    except mysql.connector.Error as e:
        print(f"MySQL error: {e}")
        return False

    except Exception as e:
        print(f"Error updating whitelist status: {e}")
        return False

    finally:
        conn.close()


def get_whitelisted_players() -> list:
    """return a list of steamID"""
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if not conn.is_connected():
            print("Database connection failed.")
            return []
        cursor = conn.cursor()
        # Execute SQL query to retrieve Steam IDs with whitelist = 1
        cursor.execute("SELECT auth FROM firstjoin.firstjoin WHERE whitelist = 1")

        whitelisted_players = cursor.fetchall()

        # Extract Steam IDs from the result and store them in a list
        steam_ids = [row[0] for row in whitelisted_players]
        return steam_ids
    except mysql.connector.Error as e:
        print(f"MySQL error: {e}")
        return []
    except Exception as e:
        print(f"Error fetching whitelisted players: {e}")
        return []
    finally:
        if "cursor" in locals() and cursor is not None:
            cursor.close()
        if conn.is_connected():
            conn.close()
            print("Database connection closed")


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
    with mysql.connector.connect(**DB_CONFIG) as conn:
        with conn.cursor(dictionary=True) as cursor:
            query = """SELECT * FROM firstjoin.mostactive WHERE steamid = %s"""
            cursor.execute(query, (steamid,))
            result = cursor.fetchone()
            return result or {}


def check_wl(steamid):
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = "SELECT whitelist FROM firstjoin.firstjoin WHERE auth = %s"

        cursor.execute(query, (steamid,))

        result = cursor.fetchone()

        if result is not None:
            whitelist_status = result[0]
            return whitelist_status
        else:
            return None

    except mysql.connector.Error as err:
        print("Error:", err)
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_all_players_steamid():
    """return a list of steamID"""
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if not conn.is_connected():
            print("Database connection failed.")
            return []
        cursor = conn.cursor()
        # Execute SQL query to retrieve Steam IDs with whitelist = 1
        cursor.execute("SELECT auth FROM firstjoin.firstjoin")

        whitelisted_players = cursor.fetchall()

        # Extract Steam IDs from the result and store them in a list
        steam_ids = [row[0] for row in whitelisted_players]
        return steam_ids
    except mysql.connector.Error as e:
        print(f"MySQL error: {e}")
        return []
    except Exception as e:
        print(f"Error fetching whitelisted players: {e}")
        return []
    finally:
        if "cursor" in locals() and cursor is not None:
            cursor.close()
        if conn.is_connected():
            conn.close()
            print("Database connection closed")


def get_firstjoin_data(auth: str) -> dict:
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
    with mysql.connector.connect(**DB_CONFIG) as conn:
        with conn.cursor(dictionary=True) as cursor:
            query = """SELECT * FROM firstjoin.firstjoin WHERE auth = %s"""
            cursor.execute(query, (auth,))
            result = cursor.fetchone()
            return result or {}


def get_recent_players(num: int = 50) -> list:
    """
    Returns a list of the most recent players who joined the server.
    """
    with mysql.connector.connect(**DB_CONFIG) as conn:
        with conn.cursor(dictionary=True) as cursor:
            query = f"""SELECT * FROM firstjoin.firstjoin ORDER BY lastseen DESC LIMIT {num}"""
            cursor.execute(query)
            results = cursor.fetchall()
            return results


if __name__ == "__main__":
    pass
