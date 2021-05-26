from application import db
from datetime import datetime


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