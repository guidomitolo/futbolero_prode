import requests
import os
import pandas as pd
from datetime import datetime

api_key = os.environ.get("API_KEY")
api_header = os.environ.get("API_HEADER")

headers = { api_header: api_key }

def logo(league, team):

    # Contact API
    try:
        URL = f"http://api.football-data.org/v2/competitions/{league}/teams"
        response = requests.get(url = URL, headers = headers) 
        response.raise_for_status()
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


# get all rounds and then cut
def fixture(league, season):

    # Contact API
    try:
        URL = f"https://api.football-data.org/v2/competitions/{league}/matches?season={season}"
        response = requests.get(url = URL, headers = headers) 
        response.raise_for_status()
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
    try:
        URL = f"https://api.football-data.org/v2/competitions/{league}/standings?season={season}"
        response = requests.get(url = URL, headers = headers) 
        response.raise_for_status()
    except requests.RequestException:
        return None

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

# print(fixture('PL','2020')[0])