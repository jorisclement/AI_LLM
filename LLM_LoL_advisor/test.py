import requests
import json
from typing import Optional, Dict, List

class LoLGameChecker:
    """
    Application pour vérifier si un joueur LoL est en partie
    et récupérer les informations sur les autres joueurs
    """
    
    def __init__(self, api_key: str, region: str = "euw1"):
        """
        :param api_key: Votre clé API Riot Games
        :param region: Région du serveur (euw1, na1, kr, etc.)
        """
        self.api_key = api_key
        self.region = region
        self.base_url = f"https://{region}.api.riotgames.com"
        self.headers = {"X-Riot-Token": api_key}
    
    def get_summoner_by_name(self, summoner_name: str, tag_line: str = "EUW") -> Optional[Dict]:
        """
        Récupère les informations d'un invocateur par son nom
        Note: Riot utilise maintenant le système Riot ID (nom#tag)
        """
        # Nouvelle API RIOT ID
        region_mapping = {
            "euw1": "europe",
            "na1": "americas",
            "kr": "asia"
        }
        continent = region_mapping.get(self.region, "europe")
        
        url = f"https://{continent}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag_line}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code != 200:
            print(f"❌ Erreur: Impossible de trouver l'invocateur {summoner_name}#{tag_line}")
            print(f"Status code: {response.status_code}")
            return None
        
        account_data = response.json()
        puuid = account_data['puuid']
        game_name = account_data.get('gameName', summoner_name)
        tag = account_data.get('tagLine', tag_line)
        
        # Récupérer les infos du summoner
        summoner_url = f"{self.base_url}/lol/summoner/v4/summoners/by-puuid/{puuid}"
        summoner_response = requests.get(summoner_url, headers=self.headers)
        
        if summoner_response.status_code == 200:
            summoner_data = summoner_response.json()
            # Ajouter le nom de jeu à la réponse
            summoner_data['gameName'] = game_name
            summoner_data['tagLine'] = tag
            return summoner_data
        
        return None
    
    def get_active_game(self, puuid: str) -> Optional[Dict]:
        """
        Vérifie si l'invocateur est actuellement en partie
        Note: L'API v5 utilise maintenant le PUUID au lieu de l'encrypted summoner ID
        """
        url = f"{self.base_url}/lol/spectator/v5/active-games/by-summoner/{puuid}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 404:
            return None  # Pas en partie
        elif response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Erreur API: {response.status_code}")
            return None
    
    def format_game_info(self, game_data: Dict) -> str:
        """
        Formate les informations de la partie en cours
        """
        output = []
        output.append("\n" + "="*60)
        output.append("🎮 PARTIE EN COURS")
        output.append("="*60)
        
        game_mode = game_data.get('gameMode', 'Unknown')
        game_type = game_data.get('gameType', 'Unknown')
        game_length = game_data.get('gameLength', 0)
        
        output.append(f"\n📊 Mode: {game_mode} | Type: {game_type}")
        output.append(f"⏱️  Durée: {game_length // 60} min {game_length % 60} sec")
        
        # Séparer les équipes
        team_blue = []
        team_red = []
        
        for participant in game_data.get('participants', []):
            player_info = {
                'name': participant.get('riotId', participant.get('summonerName', 'Unknown')),
                'champion_id': participant.get('championId', 0),
                'summoner_id': participant.get('summonerId', ''),
            }
            
            if participant.get('teamId') == 100:
                team_blue.append(player_info)
            else:
                team_red.append(player_info)
        
        # Afficher équipe bleue
        output.append("\n🔵 ÉQUIPE BLEUE:")
        output.append("-" * 60)
        for i, player in enumerate(team_blue, 1):
            output.append(f"  {i}. {player['name']} (Champion ID: {player['champion_id']})")
        
        # Afficher équipe rouge
        output.append("\n🔴 ÉQUIPE ROUGE:")
        output.append("-" * 60)
        for i, player in enumerate(team_red, 1):
            output.append(f"  {i}. {player['name']} (Champion ID: {player['champion_id']})")
        
        output.append("\n" + "="*60)
        
        return "\n".join(output)
    
    def check_player(self, summoner_name: str, tag_line: str = "EUW"):
        """
        Fonction principale pour vérifier un joueur
        """
        print(f"\n🔍 Recherche de {summoner_name}#{tag_line}...")
        
        # Récupérer les infos du joueur
        summoner = self.get_summoner_by_name(summoner_name, tag_line)
        if not summoner:
            return
        
        display_name = f"{summoner.get('gameName', summoner_name)}#{summoner.get('tagLine', tag_line)}"
        print(f"✅ Joueur trouvé: {display_name} (Niveau {summoner['summonerLevel']})")
        
        # Vérifier s'il est en partie
        print(f"\n🔍 Vérification si le joueur est en partie...")
        game = self.get_active_game(summoner['puuid'])
        
        if game:
            print(self.format_game_info(game))
        else:
            print("\n❌ Le joueur n'est pas actuellement en partie.")


def main():
    """
    Exemple d'utilisation
    """
    # ⚠️ IMPORTANT: Remplacez par votre clé API Riot
    # Obtenez votre clé sur: https://developer.riotgames.com/
    API_KEY = "VOTRE_CLE_API_ICI"
    
    # Vérifiez que la clé API est configurée
    if API_KEY == "RGAPI-a8c85a1b-8962-453b-b512-d05878c4aa9a":
        print("❌ ERREUR: Vous devez configurer votre clé API Riot Games!")
        print("📝 Rendez-vous sur https://developer.riotgames.com/ pour obtenir une clé")
        print("💡 Puis remplacez 'VOTRE_CLE_API_ICI' dans le code")
        return
    
    # Créer l'instance du checker
    checker = LoLGameChecker(api_key=API_KEY, region="euw1")
    
    # Demander le nom du joueur
    print("\n" + "="*60)
    print("🎮 LOL LIVE GAME CHECKER")
    print("="*60)
    
    summoner_name = input("\n📝 Entrez le nom d'invocateur: ").strip()
    tag_line = input("📝 Entrez le tag (par défaut EUW): ").strip() or "EUW"
    
    # Vérifier le joueur
    checker.check_player(summoner_name, tag_line)


if __name__ == "__main__":
    main()