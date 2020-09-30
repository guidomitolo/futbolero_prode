from app import db
from app.models import User, Bets, Points
from app import app, api_connection
from datetime import datetime

# lista = []
# lista2 = [1]

# if not lista and lista2:
#     print('hola')
# else:
#     print('yeah')

bet_matches = Bets.query.filter_by(user_id=User.query.filter_by(username='guido').first().id).all()

print(not bet_matches)