import requests

from utils.configs.steam import STEAMID


# def get_gokzcn_info(discord_id=None, mode='kzt', steamid=None):
#     player_data = None
#     if steamid is None:
#         steamid = discord_id_to_steamid(discord_id)
#     steamid64 = convert_steamid(steamid, 'steamid64')
#
#     gokzcn_url = f"http://gokz.cn/api/rankings?page_size=1&search_text={steamid64}&mode={mode}"
#
#     response = requests.get(gokzcn_url)
#
#     if response.status_code == 200:
#         try:
#             player_data = response.json()['data']['list'][0]  # Parse JSON data
#         except ValueError:
#             print("Failed to parse JSON")
#     else:
#         print(f"Failed to retrieve data: {response.status_code}")
#
#     bili_url = f"https://space.bilibili.com/{player_data['bili_id']}"
#     content = (
#         f'Mode: {mode.upper()}\n'
#         f'Rank: {player_data["ranking"]}\n'
#         f'Skill Score: {player_data["point_skill"]}\n'
#     )
#     try:
#          info_embed = Embed(title=f"bilibili: {player_data['bili_name']}", description=content, colour=dc_utils.Colour.green(), url=bili_url)
#         info_embed.set_author(name=player_data['name'], icon_url=player_data['avatar'], url=player_data['url'])
#     except KeyError as e:
#         info_embed = Embed(title=f"Error fetching: {e}", description=content, colour=dc_utils.Colour.red(), url=bili_url)
#         info_embed.set_author(name=player_data['name'], url=player_data['url'])
#
#     return {'embed': info_embed, 'player_data': player_data}


def fetch_playerdata(steamid64, mode='kzt'):
    try:
        url = f"http://gokz.cn/api/rankings?page_size=1&search_text={steamid64}&mode={mode}"
        response = requests.get(url)
        if response.status_code == 200:
            # Parse and return the JSON response
            try:
                return response.json()['data']['list'][0]
            except IndexError:
                print("Couldn't find this player")
                return None
        else:
            print(f"Request failed with status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None


def get_rank(skill_score, ranking):
    if ranking <= 10:
        return "Legend"
    elif skill_score >= 8.0:
        return "Master"
    elif skill_score >= 7.5:
        return "Professional"
    elif skill_score >= 7.0:
        return "Expert"
    elif skill_score >= 6.0:
        return "Skilled"
    elif skill_score >= 5.0:
        return "Intermediate"
    elif skill_score >= 4.0:
        return "Beginner"
    else:
        return "New"


if __name__ == "__main__":
    rs = fetch_playerdata(STEAMID)
    print(rs)
