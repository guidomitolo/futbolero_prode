from app import db
from app.models import User, Bets


user = User.query.filter_by(username='guido').first().id
print(user)