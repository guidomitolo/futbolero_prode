from datetime import datetime

from sqlalchemy.sql.expression import false, null

# from application.auth.models import User
# from application import db

# import json

# import plotly
# import plotly.express as px


def pending(all_matches, date=None):

    date = datetime.strptime(all_matches[-1]['date'], '%d-%m-%Y').date()

    pending = []
    for match in all_matches:
        if datetime.strptime(match['date'], '%d-%m-%Y').date() <= date :
            if match['score'][0] == None:
                pending.append(match)

    return pending
    

def up_rounds(all_matches):

    # get the current round
    rounds = [matches['round'] for matches in all_matches if datetime.strptime(matches['date'], '%d-%m-%Y').date() <= datetime.utcnow().date()]
    return max(rounds)


def score(bet_home, score_home, bet_away, score_away):

    bet_home = int(bet_home)
    score_home = int(score_home)
    bet_away = int(bet_away)
    score_away = int(score_away)

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


# def points_plot(all_matches):

#     ### CHEQUEAR Q NO SE PUEDA ELIMINAR USER

#     user_data = db.session.query(User).join(User.rank).group_by(User.id).all()

#     round_points = []
#     for user in user_data:
#         for data in user.rank.all():
#             for match in all_matches:
#                 if match['matchID'] == data.match_id:
#                     round_points.append({'name':user.username,
#                         'round':match['round'],
#                         'points':data.points})

#     weeks = set([match['round'] for match in round_points])
#     users = [user.username for user in user_data]

#     label=[]
#     y=[]
#     x=[]
#     for user in users:
#         for week in weeks:
#             total_points = 0
#             for row in round_points:
#                 if row['name'] == user:
#                     if row['round'] == week:
#                         total_points = total_points + row['points']
#             label.append(user)
#             x.append(week)
#             y.append(total_points)

#     dic = dict(zip(['usuario','semana','puntos'],[label, x, y]))

#     fig = px.line(dic, x="semana", y="puntos", color="usuario",
#                 line_group="usuario", hover_name="usuario")
#     fig.update_traces(mode='markers+lines')
#     fig.update_layout(font_family="Helvetica")

#     chart = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
#     return chart


def get_history(fixture, user_points, user_bets, season):

    historial = []
    for match in fixture:
        for score in user_points:
            for bet in user_bets:
                if match['score'][0] != None:
                    if match['matchID'] == int(str(score.match_id)) and match['matchID'] == int(str(bet.match_id)):
                        historial.append({
                            'round':match['round'],
                            'homeTeam': match['homeTeam'], 
                            'score_home':match['score'][0],
                            'bet_local':bet.score_home,
                            'awayTeam':match['awayTeam'],
                            'score_away':match['score'][1],
                            'bet_away':bet.score_away,
                            'points':score.points,
                            'season':season
                            }
                        )

    return historial
    


def notify(username, user_points, email):

    import smtplib

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

        smtp.sendmail(adm_mail, f"{email}", msg)