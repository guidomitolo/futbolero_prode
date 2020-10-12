import requests
import os
from datetime import datetime

from app.models import User, Points, Bets
from app import db

import json

import plotly
import plotly.graph_objects as go
import plotly.express as px

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
    
    # Contact API
    try:
        URL = f"https://api.football-data.org/v2/competitions/{league}/standings?season={season}"
        response = requests.get(url = URL, headers = headers) 
        response.raise_for_status()
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

def season_end(all_matches):

    # if True, the season is ended
    all_played = [match['score'][0] for match in all_matches]
    return None not in all_played    

def up_rounds(all_matches):

    # get the current round
    rounds = [matches['round'] for matches in all_matches if datetime.strptime(matches['date'], '%d-%m-%Y').date() <= datetime.utcnow().date()]
    return max(rounds)

def score(bet_home, score_home, bet_away, score_away):

    # give points
    if bet_home == score_home and bet_away == score_away:
        return 6
    elif bet_home > bet_away and score_home > score_away:
        return 3
    elif bet_home < bet_away and score_home < score_away:
        return 3
    elif bet_home == bet_away and score_home == score_away:
        return 3
    else:
        return 0

def load(all_matches, all_bets):

    # load points in database
    points_db = Points.query.all()
    points_recorded = [(score.user_id,score.match_id)  for score in points_db]
    bets_recorded = [(score.user_id,score.match_id) for score in all_bets]

    for match in all_matches:
        for bet in all_bets:
            if int(str(bet.match_id)) == match['matchID']:
                if (bet.user_id, bet.match_id) not in points_recorded:
                    if match['score'][0] != None:
                        points_match = Points(user_id=bet.user_id, 
                        match_id=match['matchID'],
                        points= score(int(str(bet.score_home)), match['score'][0], int(str(bet.score_away)), match['score'][1]))
                        db.session.add(points_match)
                        db.session.commit()

def points_plot(all_matches):

    user_data = db.session.query(User).join(User.rank).group_by(User.id).all()

    round_points = []
    for user in user_data:
        for data in user.rank.all():
            for match in all_matches:
                if match['matchID'] == data.match_id:
                    round_points.append({'name':user.username,
                        'round':match['round'],
                        'points':data.points})

    weeks = set([match['round'] for match in round_points])
    users = [user.username for user in user_data]

    label=[]
    y=[]
    x=[]
    for user in users:
        for week in weeks:
            total_points = 0
            for row in round_points:
                if row['name'] == user:
                    if row['round'] == week:
                        total_points = total_points + row['points']
            label.append(user)
            x.append(week)
            y.append(total_points)

    dic = dict(zip(['usuario','semana','puntos'],[label, x, y]))

    fig = px.line(dic, x="semana", y="puntos", color="usuario",
                line_group="usuario", hover_name="usuario")
    fig.update_traces(mode='markers+lines')
    fig.update_layout(font_family="Helvetica")

    chart = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return chart

def notify(username, user_points):

    import smtplib
    import base64

    user = User.query.filter_by(username=username).first()

    adm_mail = os.environ.get("ADM_MAIL")
    adm_pass = os.environ.get("ADM_PASS")

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(adm_mail, adm_pass)

        subject='USUARIO CAMPEON - PERMIER LEAGUE 2020-2021 - FUTBOLERO'
        body = f'Estimado/a {username},\n\nHa ganado el campeonato de apuestas con {user_points} puntos. Nos estaremos comunicando a la brevedad para coordinar la entrega de un premio sorpresa.\n\nSaluda atte.\n\nFUTBOLERO - PRODE'
        msg = f'{subject}\n\n{body}'

        smtp.sendmail(adm_mail, f"{user.email}", msg)