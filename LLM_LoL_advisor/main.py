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
    champion_data_map = {}

    def __init__(self, username, region):
        self.username = username
        self.region = region
        self.player_info = {
            "puuid": None,
            "ranked_flex_info": None,
            "ranked_solo_duo_info": None,
        }
        self.blue_team = []
        self.red_team = []
        self.red_compo = []
        self.blue_compo = []
        self._load_champ_id_to_name()

    def _load_champ_id_to_name(self):
        print("searching the latest patch of the game to load all champions informations")
        url = "https://ddragon.leagueoflegends.com/api/versions.json"
        r = requests.get(url)
        latest_version = r.json()[0]
        print("latest version is:" + str(latest_version))

        url = "http://ddragon.leagueoflegends.com/cdn/"+str(latest_version)+"/data/en_US/champion.json"
        r = requests.get(url)
        #print( str(r.json()["data"]))
        for champ in r.json()["data"].values():
            self.champion_data_map[champ["key"]] = champ["id"]
        print("Champion id map updated")
        return r.json()
    

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
        try:
            for player in r.json()["participants"]:
                if player["teamId"]==100:
                    self.blue_team.append(player)
                else:
                    self.red_team.append(player)
        except: print("Player not in game or in streamer mode")
        return r.json()
    
    def team_comp(self):

        for red_player in self.red_team:
            champ = self.champion_data_map[str(red_player["championId"])]
            self.red_compo.append(champ)

        for blue_player in self.blue_team:
            champ = self.champion_data_map[str(blue_player["championId"])]
            self.blue_compo.append(champ)
        print("############ Blue Team ############")
        print(self.blue_compo)
        print("############ Red Team ############")
        print(self.red_compo)
        return self.blue_compo,self.red_compo


joris = LoL_player("Nuclear Zeub","EUW")

print("=========== Player PUUID ===========")
summoner_puuid = joris.get_player_puuid()
# print(joris.player_info["puuid"])
print("=========== Player Infos ===========")
player_info=joris.get_player_info()
# print('ici')
# print(joris.player_info["ranked_solo_duo_info"])
print("=========== Live game infos ===========")
game_info = joris.is_in_game()
red,blue=joris.team_comp()

# player_info["player_puuid"] = summoner_puuid["puuid"]
# print(player_info["player_puuid"])
# player_info = get_player_info(player_info["player_puuid"])
# print(player_info)
# league_id=player_info[0]["leagueId"]
# game_status=is_in_game(league_id)
# print(game_status)

