from app import db
from app.models import User, Bets, Points
from datetime import datetime

# lista = []
# lista2 = [1]

# if not lista and lista2:
#     print('hola')
# else:
#     print('yeah')

bet_matches = Bets.query.all()

last_orders = db.session.query(Bets.user_id, db.func.max(Bets.score_away).label('points_order')).group_by(Bets.user_id).all()

users = User.query.all()


ranking = []
for row in range(len(users)):
    if users[row].id == last_orders[row][0]:
        ranking.append({'usuario':users[row].username,'puntos':last_orders[row][1]})

users_points = db.session.query(Points.user_id, db.func.max(Points.points)).group_by(Points.user_id).all()

print(users_points)