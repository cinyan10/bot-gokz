import requests

from utils.configs.steam import STEAM_GROUP_ID
from utils.steam.steam_user import convert_steamid
from config import *


def get_steam_username(steamid64):
    api_url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steamid64}"

    try:
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            player_info = data["response"]["players"][0]

            username = player_info.get("personaname")
            return username

        else:
            print(f"Error: HTTP {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return None


# Function to get Steam user's profile picture by their SteamID64
def get_steam_pfp(steamid64):
    # Construct the API Request URL
    url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
    parameters = {
        'key': STEAM_API_KEY,  # Your Steam Web API key
        'steamids': steamid64  # The SteamID64 of the user
    }

    # Make the API Call
    response = requests.get(url, params=parameters)

    # Check if the response is successful
    if response.status_code == 200:
        data = response.json()
        # Parse the JSON Response for the profile picture URL
        players = data.get('response', {}).get('players', [])
        if players:
            return players[0].get('avatarfull', 'No avatar URL found')
        else:
            return 'No players data found'
    else:
        return f'Error: {response.status_code}'

def get_steam_profile_url(steamid64):
    """
    Constructs the URL to a Steam user's profile page using their SteamID64.

    :param steamid64: A SteamID64 of the user
    :return: The URL to the user's Steam profile page
    """
    convert_steamid(steamid64, 2)
    base_url = "https://steamcommunity.com/profiles/"
    return f"{base_url}{steamid64}"


def get_steam_user_country(steamid64):
    url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
    params = {
        'key': STEAM_API_KEY,
        'steamids': steamid64
    }

    response = requests.get(url, params=params)
    data = response.json()

    try:
        country = data['response']['players'][0]['loccountrycode']
        return country
    except (KeyError, IndexError):
        return "black"


def get_steam_avatar_small(steamid64):
    base_url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
    params = {
        "key": STEAM_API_KEY,
        "steamids": steamid64
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        players = data.get("response", {}).get("players", [])
        if players:
            return players[0].get("avatar")
        else:
            return None
    except requests.RequestException as e:
        print(f"Error fetching Steam avatar: {e}")
        return None


def get_steam_avatar_medium(steamid64):
    base_url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
    params = {
        "key": STEAM_API_KEY,
        "steamids": steamid64
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        players = data.get("response", {}).get("players", [])
        if players:
            return players[0].get("avatarmedium")  # Accessing the medium avatar
        else:
            return None
    except requests.RequestException as e:
        print(f"Error fetching Steam avatar: {e}")
        return None


def is_in_group(steamid64):
    # Replace 'YOUR_API_KEY' with your actual Steam API key
    api_key = STEAM_API_KEY

    # Make a request to get the user's group memberships
    url = f"https://api.steampowered.com/ISteamUser/GetUserGroupList/v1/?key={api_key}&steamid={steamid64}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if 'response' in data and 'groups' in data['response']:
            group_ids = [group['gid'] for group in data['response']['groups']]

            # Check if the desired group_id_64 is in the user's group memberships
            return STEAM_GROUP_ID in group_ids
        else:
            # User's group list not available or empty
            return False

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return False


if __name__ == '__main__':

    pass
