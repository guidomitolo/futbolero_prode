from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5

# the data to be stored in the database will be represented by 
# a collection of classes (called database models) that inherit
# db.Model, a base class for all models from Flask-SQLAlchemy, 
# defines several fields as class variables. 

class User(UserMixin, db.Model):

    # fields are created as instances of the db.Column class, 
    # which takes the field type as an argument

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    fav_squad = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # db relationship lets the user db be connected with the other dbs
    rank = db.relationship('Points', backref='user_points', lazy='dynamic')

    bet = db.relationship('Bets', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Points(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    match_id = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    points = db.Column(db.Integer)

    def __repr__(self):
        return '{}'.format(self.match_id)

class Bets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    match_id = db.Column(db.Integer, nullable=False)
    score_home = db.Column(db.String(140))
    score_away = db.Column(db.String(140))

    def __repr__(self):
        return '{}'.format(self.match_id)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))