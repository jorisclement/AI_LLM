import requests, json

# Load API key

with open('./credential.json', 'r') as f:
    credential = json.load(f)

# Récupérer la clé API
API_KEY = credential['RIOT_API']                                                                                                                    
API_KEY_BASE = "?api_key="+API_KEY
REGION = "euw1"
BASE = "https://europe.api.riotgames.com/"
BASE2 = "https://"+str(REGION)+".api.riotgames.com/"

class LoL_player:


    def __init__(self, username, region):
        self.username = username
        self.region = region
        self.player_info = {
            "puuid": None,
            "ranked_flex_info": None,
            "ranked_solo_duo_info": None,
        }

    def get_player_puuid(self):
        url =str(BASE)+"riot/account/v1/accounts/by-riot-id/"+str(self.username)+"/"+str(self.region)
        r = requests.get(url+API_KEY_BASE)
        print(r.json())
        self.player_info["puuid"] = r.json()["puuid"]
        return r.json()

    def get_player_info(self):
        url = str(BASE2)+"/lol/league/v4/entries/by-puuid/"+str(self.player_info["puuid"])
        r = requests.get(url+API_KEY_BASE)
        print(r.json())
        try:
            self.player_info["ranked_solo_duo_info"]=r.json()[0]
        except:
            self.player_info["ranked_solo_duo_info"]="Not Ranked Solo/Duo"
        try:    
            self.player_info["ranked_flex_info"]=r.json()[1]
        except:
            self.player_info["ranked_flex_info"]="Not Ranked Solo/Duo"
        return r.json()

    def is_in_game(self):
        url = str(BASE2)+"lol/spectator/v5/active-games/by-summoner/" + str(self.player_info["puuid"])
        r = requests.get(url+API_KEY_BASE)
        print(r.json())
        return r.json()



joris = LoL_player("Trayton","LOLX")
summoner_puuid = joris.get_player_puuid()
print(joris.player_info["puuid"])

player_info=joris.get_player_info()
print('ici')
print(joris.player_info["ranked_solo_duo_info"])
game_info = joris.is_in_game()
print(game_info)

# player_info["player_puuid"] = summoner_puuid["puuid"]
# print(player_info["player_puuid"])
# player_info = get_player_info(player_info["player_puuid"])
# print(player_info)
# league_id=player_info[0]["leagueId"]
# game_status=is_in_game(league_id)
# print(game_status)

