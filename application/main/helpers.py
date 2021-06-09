import os
from datetime import datetime
from PIL import Image
from application import current_app as app
import secrets


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


def save_picture(form_picture):

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn