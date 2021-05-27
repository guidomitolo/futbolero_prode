import requests
import os
from dotenv import load_dotenv

from datetime import datetime

# API VARS IN ENV
env_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(env_dir, '../.env'))
api_key = os.environ.get("API_KEY")

# API REQUEST
headers = { 'X-Auth-Token': api_key }
# URL = f"https://api.football-data.org/v2/competitions/PL/matches?season=2020"
# response = requests.get(url = URL, headers = headers)


def logo(league, team):
    # Contact API
    try:
        URL = f"http://api.football-data.org/v2/competitions/{league}/teams"
        response = requests.get(url = URL, headers = headers) 
        response.raise_for_status()
        print("LOGO", response)
    except requests.RequestException:
        return None

    # Parse response
    try:
        query = response.json()
        for squad in query['teams']:
            if squad['name'] == team:
                return squad["crestUrl"]
    except (KeyError, TypeError, ValueError):
        return None

def fixture(league, season):
    # Contact API
    try:
        URL = f"https://api.football-data.org/v2/competitions/{league}/matches?season={season}"
        response = requests.get(url = URL, headers = headers)
        response.raise_for_status()
        print("FIXTURE", response)
    except requests.RequestException:
        return None
    # Parse response
    try:
        query = response.json()
        matches = []
        for match in query['matches']:
            matches.append({'season':f'{season}-{str(int(season)+1)}',
            'round':match['matchday'],
            'date': datetime.strptime(match['utcDate'][0:10], '%Y-%m-%d').strftime('%d-%m-%Y'),
            'matchID': match['id'],
            'homeTeamID': match['homeTeam']['id'],
            'homeTeam': match['homeTeam']['name'],
            'awayTeamID': match['awayTeam']['id'],
            'awayTeam': match['awayTeam']['name'],
            'score': [match['score']['fullTime']['homeTeam'],match['score']['fullTime']['awayTeam']]})
        return matches
    except (KeyError, TypeError, ValueError):
        return None

def standings(league, season):
    # Contact API
    try:
        URL = f"https://api.football-data.org/v2/competitions/{league}/standings?season={season}"
        response = requests.get(url = URL, headers = headers) 
        response.raise_for_status()
        print("STANDINGS", response)
    except requests.RequestException:
        return None
    # Parse response
    try:
        query = response.json()
        standings = []
        logos = []
        for standing in query['standings'][0]['table']:
            standings.append({'season':f'{season}-{str(int(season)+1)}',
                    'standing': standing['position'],
                    'team': standing['team']['name'],
                    'teamlogo': standing['team']["crestUrl"],
                    'points': standing['points'],
                    'PG': standing["playedGames"],
                    'Wons': standing["won"],
                    'Draws': standing["draw"],
                    'Loses': standing["lost"],
                    'goals': standing["goalsFor"],
                    'goals_against': standing["goalsAgainst"],
                    'goals_diff': standing["goalDifference"]})
            logos.append({'team': standing['team']['name'],'teamlogo': standing['team']["crestUrl"]})
        return standings, logos
    except (KeyError, TypeError, ValueError):
        return None

def team(league):
    # Contact API
    try:
        URL = f"http://api.football-data.org/v2/competitions/{league}/teams"
        response = requests.get(url = URL, headers = headers) 
        response.raise_for_status()
        print("TEAM", response)
    except requests.RequestException:
        return None
    # Parse response
    try:
        query = response.json()
        teams = []
        for squad in query['teams']:
            teams.append(squad["name"])
        return teams
    except (KeyError, TypeError, ValueError):
        return None