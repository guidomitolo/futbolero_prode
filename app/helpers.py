from datetime import datetime

import app
from app.models import User, Points
from app import db

import json

import plotly
import plotly.express as px


def season_end(all_matches):
    # check if all matches have any scores. If any score missing, return False
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

    # adm_mail = os.environ.get("ADM_MAIL")
    # adm_pass = os.environ.get("ADM_PASS")
    adm_mail = app.config("ADM_MAIL")
    adm_pass = app.config("ADM_PASS")

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(adm_mail, adm_pass)

        subject='USUARIO CAMPEON - PERMIER LEAGUE 2020-2021 - FUTBOLERO'
        body = f'Estimado/a {username},\n\nHa ganado el campeonato de apuestas con {user_points} puntos. Nos estaremos comunicando a la brevedad para coordinar la entrega de un premio sorpresa.\n\nSaluda atte.\n\nFUTBOLERO - PRODE'
        msg = f'{subject}\n\n{body}'

        smtp.sendmail(adm_mail, f"{user.email}", msg)