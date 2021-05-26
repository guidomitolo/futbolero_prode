from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    fav_squad = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    # db relationship lets the user db be connected with the other dbs
    rank = db.relationship('Points', backref='user_points', lazy='dynamic')
    bet = db.relationship('Bets', lazy='dynamic')
    winner = db.relationship('Seasons', backref='user_winner', lazy='dynamic')

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



class Bets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    match_id = db.Column(db.Integer, nullable=False)
    score_home = db.Column(db.String(140))
    score_away = db.Column(db.String(140))
    league = db.Column(db.String(140))
    season = db.Column(db.Integer)

    def __repr__(self):
        return '{}'.format(self.match_id)
        

class Points(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    match_id = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    points = db.Column(db.Integer)
    hits = db.Column(db.Integer, default=0)
    league = db.Column(db.String(140))
    season = db.Column(db.Integer)

    def __repr__(self):
        return '{}'.format(self.match_id)


class Seasons(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    league = db.Column(db.String(140))
    season = db.Column(db.Integer)
    finished = db.Column(db.Boolean)
    winner = db.Column(db.Integer, db.ForeignKey('user.id'))
    total_points = db.Column(db.Integer)
    matches_hits = db.Column(db.Integer)

    def __repr__(self):
        return '{}'.format(self.season)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))