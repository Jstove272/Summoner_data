from lib2to3.pgen2.pgen import DFAState
import requests
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd




headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": "RGAPI-073522ca-0b9e-4866-896e-7664ac4de1c6"
}
summoner_name = "yapsuo"
match_count = 50
account_info = requests.get(f'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}', headers=headers)

account_puuid = account_info.json()["puuid"]

match_id_url = f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{account_puuid}/ids?start=0&count={match_count}'

match_ids = requests.get(match_id_url, headers=headers)

valid_games = pd.DataFrame(columns=["match_id","spell1Casts","spell2Casts","spell3Casts","spell4Casts","win","totalHeal"])

# test_match_url = f'https://americas.api.riotgames.com/lol/match/v5/matches/NA1_4391108464'

# test_match = requests.get(test_match_url, headers=headers)

for match_id in match_ids.json():
    print(f"Querying match: {match_id}")

    unique_match_url = f'https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}'

    unique_match = requests.get(unique_match_url, headers=headers)
    if  unique_match.ok:
        for participant in unique_match.json()["info"]["participants"]:
            if participant["summonerName"] == summoner_name and participant["championName"] == "Sylas": 
                valid_games = valid_games.append({
                    "match_id":unique_match.json()["metadata"]["matchId"],
                    "spell1Casts":participant["spell1Casts"],
                    "spell2Casts":participant["spell2Casts"],
                    "spell3Casts":participant["spell3Casts"],
                    "spell4Casts":participant["spell4Casts"],
                    "win":participant["win"],
                    "totalHeal":participant["totalHeal"]},
                    ignore_index=True)
    else:
        print(f"Error at {match_id}")
        print(unique_match.status_code)
print(valid_games)

