from app import db
from app.models import User, Bets, Points
from app import app, api_connection
from datetime import datetime

# fixture = api_connection.fixture('PL',datetime.utcnow().strftime('%Y'))

bet_matches = Bets.query.filter_by(user_id=User.query.filter_by(username='guido').first().id).all()

points_db = Points.query.filter_by(user_id=User.query.filter_by(username='guido').first().id).all()

points_recorded = [score.match_id for score in points_db]

def score(bet_home, score_home, bet_away, score_away):
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

#   QUE HACER CUANDO LA APUESTA YA ESTA HECHA Y EL PUNTAJE CARGADO????

# evaluate new bets
# for match in fixture:
#     for bet in bet_matches:
#         # primero chequear q se hizo la apuesta
#         # segundo chequear si la apuesta no fue evaluada previamente
#         if int(str(bet.match_id)) == match['matchID'] and match['matchID'] not in points_recorded:

#             # chequear q se haya jugado el partido al que se apostó
#             # si no se jugó, queda la evaluación pediente (pass)
#             if match['score'][0] != None:

#                 points_match = Points(user_id=User.query.filter_by(username=current_user.username).first().id, 
#                 match_id=match['matchID'],
#                 points= score(int(str(bet.score_home)), match['score'][0], int(str(bet.score_away)), match['score'][1]))
#                 db.session.add(points_match)
#                 db.session.commit()

# rounds = [matches['round'] for matches in fixture if datetime.strptime(matches['date'], '%d-%m-%Y').date() <= datetime.utcnow().date()]
# last_round_2 = [matches for matches in fixture if matches['round'] == max(rounds) - 1]

last_round = [{'season': '2020-2021', 'round': 2, 'date': '19-09-2020', 'matchID': 303772, 'homeTeamID': 62, 'homeTeam': 'Everton FC', 'awayTeamID': 74, 'awayTeam': 'West Bromwich Albion FC', 'score': [5, 2]}, {'season': '2020-2021', 'round': 2, 'date': '19-09-2020', 'matchID': 303775, 'homeTeamID': 341, 'homeTeam': 'Leeds United FC', 'awayTeamID': 63, 'awayTeam': 'Fulham FC', 'score': [4, 3]}, {'season': '2020-2021', 'round': 2, 'date': '19-09-2020', 'matchID': 303773, 'homeTeamID': 66, 'homeTeam': 'Manchester United FC', 'awayTeamID': 354, 'awayTeam': 'Crystal Palace FC', 'score': [1, 3]}, {'season': '2020-2021', 'round': 2, 'date': '19-09-2020', 'matchID': 303770, 'homeTeamID': 57, 'homeTeam': 'Arsenal FC', 'awayTeamID': 563, 'awayTeam': 'West Ham United FC', 'score': [2, 1]}, {'season': '2020-2021', 'round': 2, 'date': '20-09-2020', 'matchID': 303776, 'homeTeamID': 340, 'homeTeam': 'Southampton FC', 'awayTeamID': 73, 'awayTeam': 'Tottenham Hotspur FC', 'score': [2, 5]}, {'season': '2020-2021', 'round': 2, 'date': '20-09-2020', 'matchID': 303769, 'homeTeamID': 67, 'homeTeam': 'Newcastle United FC', 'awayTeamID': 397, 'awayTeam': 'Brighton & Hove Albion FC', 'score': [0, 3]}, {'season': '2020-2021', 'round': 2, 'date': '20-09-2020', 'matchID': 303771, 'homeTeamID': 61, 'homeTeam': 'Chelsea FC', 'awayTeamID': 64, 'awayTeam': 'Liverpool FC', 'score': [0, 2]}, {'season': '2020-2021', 'round': 2, 'date': '20-09-2020', 'matchID': 303774, 'homeTeamID': 338, 'homeTeam': 'Leicester City FC', 'awayTeamID': 328, 'awayTeam': 'Burnley FC', 'score': [4, 2]}, {'season': '2020-2021', 'round': 2, 'date': '21-09-2020', 'matchID': 303768, 'homeTeamID': 58, 'homeTeam': 'Aston Villa FC', 'awayTeamID': 356, 'awayTeam': 'Sheffield United FC', 'score': [1, 0]}, {'season': '2020-2021', 'round': 2, 'date': '21-09-2020', 'matchID': 303767, 'homeTeamID': 76, 'homeTeam': 'Wolverhampton Wanderers FC', 'awayTeamID': 65, 'awayTeam': 'Manchester City FC', 'score': [1, 3]}]


points = []

print(points_recorded)

print(len(last_round))
print(len(points_db))
print(len(bet_matches))

print(points_db)
print(bet_matches)

# show last points
# for match in last_round:
#     for score in points_db:
#         for bet in bet_matches:
#             # problema -> score = NOne
#             print(type(match['matchID']), type(score.match_id), type(bet.match_id))
            # if match['matchID'] == int(str(score.match_id)) and match['matchID'] == int(str(bet.match_id)):
            #     match['bet_local'] = bet.score_home
            #     match['bet_away'] = bet.score_away
            #     # si hay resultado
            #     if match['score'][0] != None:
            #         match['points'] = score.points
            #         points.append(score.points)
            #     # si no hay resultado, completar con None
            #     else:
            #         match['points'] = None
            #         points.append(None)

# # if there are not any bets
# print(points_recorded)
# if points_recorded[0] == None:
#     total = False
# else:
#     total = sum([num for num in points if isinstance(num,int)])

# print(last_round)
# print(total)