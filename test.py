from app import db
from app.models import Points, User
from sqlalchemy import desc


users = User.query.all()

# users_points = db.session.query(Points.user_id, db.func.max(Points.points)).group_by(Points.user_id).all()
users_points = db.session.query(Points.user_id, db.func.max(Points.points).label('max')).group_by(Points.user_id).order_by(desc('max')).all()
print(users_points)
print(users)

ranking = []
if users_points:
    print('ok')
    for row in range(len(users_points)):
        for user in users:
            if user.id == users_points[row][0]:
                print(users_points[row], user.id)
                ranking.append({'name':user.username,'points':users_points[row][1]})
else:
    ranking = False
print(ranking)