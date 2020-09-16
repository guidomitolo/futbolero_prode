import requests
import os
import pandas as pd
from datetime import datetime

# export API_KEY=X-Auth-Token:e72e6080e092489abd8342d58b9b170e
# api_key = os.environ.get("API_KEY")

headers = { 'X-Auth-Token': 'e72e6080e092489abd8342d58b9b170e' }

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

def fixture(league, season, match_round):

    # Contact API
    try:
        URL = f"https://api.football-data.org/v2/competitions/{league}/matches?season={season}&matchday={match_round}"
        response = requests.get(url = URL, headers = headers) 
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        query = response.json()
        matches = []
        print(query['matches'])
        for match in query['matches']:
            matches.append({'season':f'{season}-{str(int(season)+1)}',
            'round':match_round,
            'date': str(match["utcDate"][0:10]),
            'homeTeam': match['homeTeam']['name'],
            'homeTeam_logo': logo(league, match['homeTeam']['name']),
            'awayTeam': match['awayTeam']['name'],
            'awayTeam_logo': logo(league, match['awayTeam']['name']),
            'score': [match['score']['fullTime']['homeTeam'],match['score']['fullTime']['awayTeam']]})
        return matches
    except (KeyError, TypeError, ValueError):
        return None

# print(datetime.utcnow().strftime('%Y'))
print(fixture('PL',datetime.utcnow().strftime('%Y'),'1'),'\n\n\n\n\n')

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
        return standings
    except (KeyError, TypeError, ValueError):
        return None

# print(pd.DataFrame(standings('PL',datetime.utcnow().strftime('%Y'))))
print(standings('PL',datetime.utcnow().strftime('%Y')))

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