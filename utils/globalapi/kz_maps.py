import json
import requests

from utils.configs.gokz import MAP_TIERS


def map_id_to_tier(map_id):
    maps_data = fetching_maps()
    for kz_map in maps_data:
        if kz_map["id"] == map_id:
            return kz_map["difficulty"]
    return None


def get_map_tier(map_name=None, from_local=True, map_id=None) -> str:
    if from_local:
        try:
            map_tier = MAP_TIERS[map_name]
            return "T" + str(map_tier)
        except KeyError:
            return "Unknown"
    else:
        try:
            map_tier = fetch_map_tier(map_name)
            return "T" + str(map_tier)
        except KeyError:
            return "Unknown"


def fetching_maps(use_local=True):
    if use_local:
        with open("utils/globalapi/maps.json", "r", encoding="utf-8") as json_file:
            maps_data = json.load(json_file)
    else:
        api_url = "https://kztimerglobal.com/api/v2.0/maps?is_validated=true&limit=2000"
        response = requests.get(api_url)
        response.raise_for_status()
        maps_data = response.json()
        with open("utils/globalapi/maps.json", "w", encoding="utf-8") as json_file:
            json.dump(maps_data, json_file)

    return maps_data


def fetch_map_tier(map_name: str):
    try:
        response = requests.get(
            "https://kztimerglobal.com/api/v2.0/maps/name/" + map_name
        )

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the response as JSON (assuming the API returns JSON)
            data = response.json()
            return data["difficulty"]
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None
