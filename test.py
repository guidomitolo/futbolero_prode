from app import db
from app.models import Points, User, Bets
from app.helpers import up_rounds, fixture
from sqlalchemy import desc, func
from datetime import datetime
import pandas as pd

fixture = [{'season': '2020-2021', 'round': 1, 'date': '13-09-2020', 'matchID': 303757, 'homeTeamID': 65, 'homeTeam': 'Manchester City FC', 'awayTeamID': 58, 'awayTeam': 'Aston Villa FC', 'score': [None, None]}, {'season': '2020-2021', 'round': 1, 'date': '13-09-2020', 'matchID': 303758, 'homeTeamID': 328, 'homeTeam': 'Burnley FC', 'awayTeamID': 66, 'awayTeam': 'Manchester United FC', 'score': [None, None]}, {'season': '2020-2021', 'round': 1, 'date': '12-09-2020', 'matchID': 303759, 'homeTeamID': 63, 'homeTeam': 'Fulham FC', 'awayTeamID': 57, 'awayTeam': 'Arsenal FC', 'score': [0, 3]}, {'season': '2020-2021', 'round': 1, 'date': '12-09-2020', 'matchID': 303764, 'homeTeamID': 354, 'homeTeam': 'Crystal Palace FC', 'awayTeamID': 340, 'awayTeam': 'Southampton FC', 'score': [1, 0]}, {'season': '2020-2021', 'round': 1, 'date': '12-09-2020', 'matchID': 303760, 'homeTeamID': 64, 'homeTeam': 'Liverpool FC', 'awayTeamID': 341, 'awayTeam': 'Leeds United FC', 'score': [4, 3]}, {'season': '2020-2021', 'round': 1, 'date': '12-09-2020', 'matchID': 303763, 'homeTeamID': 563, 'homeTeam': 'West Ham United FC', 'awayTeamID': 67, 'awayTeam': 'Newcastle United FC', 'score': [0, 2]}, {'season': '2020-2021', 'round': 1, 'date': '13-09-2020', 'matchID': 303762, 'homeTeamID': 74, 'homeTeam': 'West Bromwich Albion FC', 'awayTeamID': 338, 'awayTeam': 'Leicester City FC', 'score': [0, 3]}, {'season': '2020-2021', 'round': 1, 'date': '13-09-2020', 'matchID': 303761, 'homeTeamID': 73, 'homeTeam': 'Tottenham Hotspur FC', 'awayTeamID': 62, 'awayTeam': 'Everton FC', 'score': [0, 1]}, {'season': '2020-2021', 'round': 1, 'date': '14-09-2020', 'matchID': 303765, 'homeTeamID': 356, 'homeTeam': 'Sheffield United FC', 'awayTeamID': 76, 'awayTeam': 'Wolverhampton Wanderers FC', 'score': [0, 2]}, {'season': '2020-2021', 'round': 1, 'date': '14-09-2020', 'matchID': 303766, 'homeTeamID': 397, 'homeTeam': 'Brighton & Hove Albion FC', 'awayTeamID': 61, 'awayTeam': 'Chelsea FC', 'score': [1, 3]}, {'season': '2020-2021', 'round': 2, 'date': '19-09-2020', 'matchID': 303772, 'homeTeamID': 62, 'homeTeam': 'Everton FC', 'awayTeamID': 74, 'awayTeam': 'West Bromwich Albion FC', 'score': [5, 2]}, {'season': '2020-2021', 'round': 2, 'date': '19-09-2020', 'matchID': 303775, 'homeTeamID': 341, 'homeTeam': 'Leeds United FC', 'awayTeamID': 63, 'awayTeam': 'Fulham FC', 'score': [4, 3]}, {'season': '2020-2021', 'round': 2, 'date': '19-09-2020', 'matchID': 303773, 'homeTeamID': 66, 'homeTeam': 'Manchester United FC', 'awayTeamID': 354, 'awayTeam': 'Crystal Palace FC', 'score': [1, 3]}, {'season': '2020-2021', 'round': 2, 'date': '19-09-2020', 'matchID': 303770, 'homeTeamID': 57, 'homeTeam': 'Arsenal FC', 'awayTeamID': 563, 'awayTeam': 'West Ham United FC', 'score': [2, 1]}, {'season': '2020-2021', 'round': 2, 'date': '20-09-2020', 'matchID': 303776, 'homeTeamID': 340, 'homeTeam': 'Southampton FC', 'awayTeamID': 73, 'awayTeam': 'Tottenham Hotspur FC', 'score': [2, 5]}, {'season': '2020-2021', 'round': 2, 'date': '20-09-2020', 'matchID': 303769, 'homeTeamID': 67, 'homeTeam': 'Newcastle United FC', 'awayTeamID': 397, 'awayTeam': 'Brighton & Hove Albion FC', 'score': [0, 3]}, {'season': '2020-2021', 'round': 2, 'date': '20-09-2020', 'matchID': 303771, 'homeTeamID': 61, 'homeTeam': 'Chelsea FC', 'awayTeamID': 64, 'awayTeam': 'Liverpool FC', 'score': [0, 2]}, {'season': '2020-2021', 'round': 2, 'date': '20-09-2020', 'matchID': 303774, 'homeTeamID': 338, 'homeTeam': 'Leicester City FC', 'awayTeamID': 328, 'awayTeam': 'Burnley FC', 'score': [4, 2]}, {'season': '2020-2021', 'round': 2, 'date': '21-09-2020', 'matchID': 303768, 'homeTeamID': 58, 'homeTeam': 'Aston Villa FC', 'awayTeamID': 356, 'awayTeam': 'Sheffield United FC', 'score': [1, 0]}, {'season': '2020-2021', 'round': 2, 'date': '21-09-2020', 'matchID': 303767, 'homeTeamID': 76, 'homeTeam': 'Wolverhampton Wanderers FC', 'awayTeamID': 65, 'awayTeam': 'Manchester City FC', 'score': [1, 3]}, {'season': '2020-2021', 'round': 3, 'date': '26-09-2020', 'matchID': 303786, 'homeTeamID': 397, 'homeTeam': 'Brighton & Hove Albion FC', 'awayTeamID': 66, 'awayTeam': 'Manchester United FC', 'score': [2, 3]}, {'season': '2020-2021', 'round': 3, 'date': '26-09-2020', 'matchID': 303785, 'homeTeamID': 354, 'homeTeam': 'Crystal Palace FC', 'awayTeamID': 62, 'awayTeam': 'Everton FC', 'score': [1, 2]}, {'season': '2020-2021', 'round': 3, 'date': '26-09-2020', 'matchID': 303781, 'homeTeamID': 74, 'homeTeam': 'West Bromwich Albion FC', 'awayTeamID': 61, 'awayTeam': 'Chelsea FC', 'score': [3, 3]}, {'season': '2020-2021', 'round': 3, 'date': '26-09-2020', 'matchID': 303783, 'homeTeamID': 328, 'homeTeam': 'Burnley FC', 'awayTeamID': 340, 'awayTeam': 'Southampton FC', 'score': [0, 1]}, {'season': '2020-2021', 'round': 3, 'date': '27-09-2020', 'matchID': 303782, 'homeTeamID': 356, 'homeTeam': 'Sheffield United FC', 'awayTeamID': 341, 'awayTeam': 'Leeds United FC', 'score': [0, 1]}, {'season': '2020-2021', 'round': 3, 'date': '27-09-2020', 'matchID': 303780, 'homeTeamID': 73, 'homeTeam': 'Tottenham Hotspur FC', 'awayTeamID': 67, 'awayTeam': 'Newcastle United FC', 'score': [1, 1]}, {'season': '2020-2021', 'round': 3, 'date': '27-09-2020', 'matchID': 303779, 'homeTeamID': 65, 'homeTeam': 'Manchester City FC', 'awayTeamID': 338, 'awayTeam': 'Leicester City FC', 'score': [2, 5]}, {'season': '2020-2021', 'round': 3, 'date': '27-09-2020', 'matchID': 303784, 'homeTeamID': 563, 'homeTeam': 'West Ham United FC', 'awayTeamID': 76, 'awayTeam': 'Wolverhampton Wanderers FC', 'score': [4, 0]}, {'season': '2020-2021', 'round': 3, 'date': '28-09-2020', 'matchID': 303777, 'homeTeamID': 63, 'homeTeam': 'Fulham FC', 'awayTeamID': 58, 'awayTeam': 'Aston Villa FC', 'score': [0, 3]}, {'season': '2020-2021', 'round': 3, 'date': '28-09-2020', 'matchID': 303778, 'homeTeamID': 64, 'homeTeam': 'Liverpool FC', 'awayTeamID': 57, 'awayTeam': 'Arsenal FC', 'score': [3, 1]}, {'season': '2020-2021', 'round': 4, 'date': '03-10-2020', 'matchID': 303791, 'homeTeamID': 61, 'homeTeam': 'Chelsea FC', 'awayTeamID': 354, 'awayTeam': 'Crystal Palace FC', 'score': [4, 0]}, {'season': '2020-2021', 'round': 4, 'date': '03-10-2020', 'matchID': 303792, 'homeTeamID': 62, 'homeTeam': 'Everton FC', 'awayTeamID': 397, 'awayTeam': 'Brighton & Hove Albion FC', 'score': [4, 2]}, {'season': '2020-2021', 'round': 4, 'date': '03-10-2020', 'matchID': 303795, 'homeTeamID': 341, 'homeTeam': 'Leeds United FC', 'awayTeamID': 65, 'awayTeam': 'Manchester City FC', 'score': [1, 1]}, {'season': '2020-2021', 'round': 4, 'date': '03-10-2020', 'matchID': 303789, 'homeTeamID': 67, 'homeTeam': 'Newcastle United FC', 'awayTeamID': 328, 'awayTeam': 'Burnley FC', 'score': [3, 1]}, {'season': '2020-2021', 'round': 4, 'date': '04-10-2020', 'matchID': 303794, 'homeTeamID': 338, 'homeTeam': 'Leicester City FC', 'awayTeamID': 563, 'awayTeam': 'West Ham United FC', 'score': [0, 3]}, {'season': '2020-2021', 'round': 4, 'date': '04-10-2020', 'matchID': 303796, 'homeTeamID': 340, 'homeTeam': 'Southampton FC', 'awayTeamID': 74, 'awayTeam': 'West Bromwich Albion FC', 'score': [2, 0]}, {'season': '2020-2021', 'round': 4, 'date': '04-10-2020', 'matchID': 303787, 'homeTeamID': 76, 'homeTeam': 'Wolverhampton Wanderers FC', 'awayTeamID': 63, 'awayTeam': 'Fulham FC', 'score': [1, 0]}, {'season': '2020-2021', 'round': 4, 'date': '04-10-2020', 'matchID': 303790, 'homeTeamID': 57, 'homeTeam': 'Arsenal FC', 'awayTeamID': 356, 'awayTeam': 'Sheffield United FC', 'score': [2, 1]}, {'season': '2020-2021', 'round': 4, 'date': '04-10-2020', 'matchID': 303793, 'homeTeamID': 66, 'homeTeam': 'Manchester United FC', 'awayTeamID': 73, 'awayTeam': 'Tottenham Hotspur FC', 'score': [1, 2]}, {'season': '2020-2021', 'round': 4, 'date': '04-10-2020', 'matchID': 303788, 'homeTeamID': 58, 'homeTeam': 'Aston Villa FC', 'awayTeamID': 64, 'awayTeam': 'Liverpool FC', 'score': [None, None]}, {'season': '2020-2021', 'round': 5, 'date': '17-10-2020', 'matchID': 303801, 'homeTeamID': 62, 'homeTeam': 'Everton FC', 'awayTeamID': 64, 'awayTeam': 'Liverpool FC', 'score': [None, None]}, {'season': '2020-2021', 'round': 5, 'date': '17-10-2020', 'matchID': 303798, 'homeTeamID': 67, 'homeTeam': 'Newcastle United FC', 'awayTeamID': 66, 'awayTeam': 'Manchester United FC', 'score': [None, None]}, {'season': '2020-2021', 'round': 5, 'date': '17-10-2020', 'matchID': 303799, 'homeTeamID': 61, 'homeTeam': 'Chelsea FC', 'awayTeamID': 340, 'awayTeam': 'Southampton FC', 'score': [None, None]}, {'season': '2020-2021', 'round': 5, 'date': '17-10-2020', 'matchID': 303802, 'homeTeamID': 74, 'homeTeam': 'West Bromwich Albion FC', 'awayTeamID': 328, 'awayTeam': 'Burnley FC', 'score': [None, None]}, {'season': '2020-2021', 'round': 5, 'date': '17-10-2020', 'matchID': 303803, 'homeTeamID': 356, 'homeTeam': 'Sheffield United FC', 'awayTeamID': 63, 'awayTeam': 'Fulham FC', 'score': [None, None]}, {'season': '2020-2021', 'round': 5, 'date': '17-10-2020', 'matchID': 303804, 'homeTeamID': 338, 'homeTeam': 'Leicester City FC', 'awayTeamID': 58, 'awayTeam': 'Aston Villa FC', 'score': [None, None]}, {'season': '2020-2021', 'round': 5, 'date': '17-10-2020', 'matchID': 303797, 'homeTeamID': 65, 'homeTeam': 'Manchester City FC', 'awayTeamID': 57, 'awayTeam': 'Arsenal FC', 'score': [None, None]}, {'season': '2020-2021', 'round': 5, 'date': '18-10-2020', 'matchID': 303806, 'homeTeamID': 354, 'homeTeam': 'Crystal Palace FC', 'awayTeamID': 397, 'awayTeam': 'Brighton & Hove Albion FC', 'score': [None, None]}, {'season': '2020-2021', 'round': 5, 'date': '18-10-2020', 'matchID': 303800, 'homeTeamID': 73, 'homeTeam': 'Tottenham Hotspur FC', 'awayTeamID': 563, 'awayTeam': 'West Ham United FC', 'score': [None, None]}, {'season': '2020-2021', 'round': 5, 'date': '19-10-2020', 'matchID': 303805, 'homeTeamID': 341, 'homeTeam': 'Leeds United FC', 'awayTeamID': 76, 'awayTeam': 'Wolverhampton Wanderers FC', 'score': [None, None]}]
# points_db = Points.query.filter_by(user_id=User.query.filter_by(username='paula').first().id).all()
# users = User.query.all()

# users_points = db.session.query(User.rank, db.func.sum(User.rank.points).label('sum')).group_by(User.id).order_by(desc('sum')).all()

# print(users[0].rank.all())

# for points in users[0].rank.all():
#     print(points.points)


# session.query(func.count(User.id))

q = db.session.query(User).join(User.rank).group_by(User.id).all()

round_points = []
for user in q:
    for data in user.rank.all():
        for match in fixture:
            if match['matchID'] == data.match_id:
                round_points.append({'name':user.username,
                    'round':match['round'],
                    'points':data.points})


weeks = set([matches['round'] for matches in fixture])
users = [user.username for user in q]


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
        # print('ususario',user,'total',total_points,'round',week)


print(label)
print(x)
print(y)

dic = dict(zip(['usuario','semana','puntos'],[label, x, y]))

import plotly.express as px

fig = px.line(dic, x="semana", y="puntos", color="usuario",
              line_group="usuario", hover_name="usuario")
fig.update_traces(mode='markers+lines')
fig.update_layout(title="Puntaje por semana según usuario")
import plotly.offline
plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')
print(plotly.offline.plot(fig, include_plotlyjs=False, output_type='div'))