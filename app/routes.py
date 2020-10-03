from flask import render_template, flash, redirect, url_for
from app import app, helpers
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Points, Bets
from sqlalchemy import desc
from app import db
from app.forms import RegistrationForm, EditProfileForm, GamblingForm

from flask import request
from werkzeug.urls import url_parse

from datetime import datetime

@app.route('/')
@app.route('/index')
@login_required
def index():
    
    # # call API once, each time index is rendered
    global fixture
    fixture = helpers.fixture('PL',datetime.utcnow().strftime('%Y'))

    global tabla
    tabla = helpers.standings('PL',datetime.utcnow().strftime('%Y'))

    # add logo for each team in fixture
    for team in fixture:
        for logo in tabla[1]:
            if team['homeTeam'] == logo['team']:
                team['homelogo'] = logo['teamlogo']
            if team['awayTeam'] == logo['team']:
                team['awaylogo'] = logo['teamlogo']

    # get matches of current round
    current_round = [matches for matches in fixture if matches['round'] == helpers.up_rounds(fixture)]
        
    return render_template("index.html", title='Bienvenido', table=tabla[0], fixture=current_round)

@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first() 
        if user is None or not user.check_password(form.password.data):
            flash('Usuario o Password Inválidos')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        
        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    
    return render_template('login.html', title='Ingresar', form=form)

@app.route('/logout')
def logout():
    
    logout_user()
    return redirect(url_for('index'))

@app.route('/register_fbs', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():

        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        user.set_password(form.password.data)

        flash('Felicitaciones, usted se ha registrado exitosamente!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):

    current_user = User.query.filter_by(username=username).first_or_404()
    users = User.query.all()

    users_points = db.session.query(Points.user_id, db.func.max(Points.points).label('max')).group_by(Points.user_id).order_by(desc('max')).all()

    ranking = []
    if users_points:
        for row in range(len(users_points)):
            for user in users:
                if user.id == users_points[row][0]:
                    ranking.append({'name':user.username,'points':users_points[row][1]})
    else:
        ranking = False

    return render_template('user.html',
                    user=current_user, 
                    logo=helpers.logo('PL',user.fav_squad),
                    ranking=ranking)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow() 
        # when you reference current_user, Flask-Login will invoke the user loader callback function, 
        # which will run a database query that will put the target user in the database session
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.fav_squad = form.fav_squad.data
        db.session.commit()
        flash('Los cambios han sido guardados')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.fav_squad.data = current_user.fav_squad
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/bet', methods=['GET', 'POST'])
@login_required
def bet():

    # get matches of next round
    next_round = [matches for matches in fixture if matches['round'] == helpers.up_rounds(fixture) + 1]
    # access to Bets database
    bet_matches = Bets.query.filter_by(user_id=User.query.filter_by(username=current_user.username).first().id).all()
    # make list of matches in bets
    bet_list = [int(str(bet)) for bet in bet_matches]
    # if one matchID exists, all other matches of the same round exist as well. 
    # then, make a list to pass as value of each form
    score_list = []
    for match in next_round:
        if match['matchID'] in bet_list:
            for bet in bet_matches:
                if int(str(bet.match_id)) == match['matchID']:
                    score_list.append({'home':int(str(bet.score_home)),'away':int(str(bet.score_home))})

    if not score_list:
        last = False
    else:
        last = score_list

    # close the bets if access to the bet form is equal to the first date of the coming round
    if datetime.utcnow().date() == datetime.strptime(next_round[0]['date'], '%d-%m-%Y').date():
        form = False
    else:
        # get bet fields
        form = GamblingForm()

        if form.validate_on_submit():
            # first check if the bet is already done to overwrite the scores
            for value, match in zip(form.bet.data, next_round):
                # check if the user has not place any bet and add a new user and a new bet
                if len(bet_matches) == 0:
                    new_user_bets = Bets(user_id=User.query.filter_by(username=current_user.username).first().id,
                        match_id=match['matchID'],
                        timestamp = datetime.utcnow(),
                        score_home = value['home'],
                        score_away = value['away'])
                    db.session.add(new_user_bets)
                    db.session.commit()
                # check if the already existing user has already place a bet in the database
                else:
                    if match['matchID'] in bet_list:
                        for bet in bet_matches:
                            if int(str(bet.match_id)) == match['matchID']:
                                bet.timestamp = datetime.utcnow()
                                bet.score_home = value['home']
                                bet.score_away = value['away']
                                db.session.commit()
                    else:
                        new_bet = Bets(user_id=User.query.filter_by(username=current_user.username).first().id,
                        match_id=match['matchID'],
                        timestamp = datetime.utcnow(),
                        score_home = value['home'],
                        score_away = value['away'])
                        db.session.add(new_bet)
                        db.session.commit()
            flash('Has enviado una apuesta')

    return render_template("bet.html", title='Home Page', table=next_round, form=form, value=last)

@app.route('/results', methods=['GET', 'POST'])
@login_required
def results():

    bet_matches = Bets.query.all()
    # evaluate bets of the played matchets
    helpers.load(fixture, bet_matches)

    show_points = Points.query.filter_by(user_id=User.query.filter_by(username=current_user.username).first().id).all()

    points = []

    # get matches of current and next round
    current_round = [matches for matches in fixture if matches['round'] == helpers.up_rounds(fixture)]
    next_round = [matches for matches in fixture if matches['round'] == helpers.up_rounds(fixture) + 1]

    # show matches of when "next round" becomes "current round"
    if not bet_matches:
        total = 'no_bets'
    elif datetime.utcnow().date() != datetime.strptime(next_round[0]['date'], '%d-%m-%Y').date():
        for match in current_round:
            for score in show_points:
                for bet in bet_matches:
                    # add match
                    if match['matchID'] == int(str(score.match_id)) and match['matchID'] == int(str(bet.match_id)):
                        match['bet_local'] = bet.score_home
                        match['bet_away'] = bet.score_away
                        # add points
                        if match['score'][0] != None:
                            match['points'] = score.points
                            points.append(score.points)
                        # add none if the match was not played
                        else:
                            match['points'] = None
                            points.append(None)
        total = sum([num for num in points if isinstance(num,int)])
    else:
        total = 'closed'

    return render_template("results.html", title='Home Page', table=current_round, total=total)