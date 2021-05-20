# flask core libs
from flask import render_template, flash, redirect, url_for, session
from flask_login import current_user, login_user, logout_user, login_required
from flask import request

# app modules
from app.forms import LoginForm, RegistrationForm
from app.models import User, Points, Bets
from app import db
from app.forms import RegistrationForm, EditProfileForm, GamblingForm
from app import app, connect, helpers

# external libs
from sqlalchemy import desc
from werkzeug.urls import url_parse
from datetime import datetime

import json

@app.route('/')
@app.route('/index')
@login_required
def index():
    
    # # call API once, each time index is rendered
    # global fixture
    # fixture = connect.fixture('PL')

    # global tabla
    # tabla = connect.standings('PL')
    print(session.keys())
    # if not session.get('fixture'):

    with open(f'fixture.json', 'r') as file:
        data = json.load(file)
        session['fixture'] = data['fixture']
        file.close()

    with open(f'standings.json', 'r') as file:
        data = json.load(file)
        session['tabla'] = data
        file.close()

    with open(f'logos.json', 'r') as file:
        data = json.load(file)
        session['logos'] = data
        file.close()
    # else:
    #     print('there is sth in sessions')

    fixture = session['fixture']
    tabla = session['tabla']
    logos = session['logos']

    # add logo for each team in fixture
    for team in fixture:
        for logo in logos:
            if team['homeTeam'] == logo['team']:
                team['homelogo'] = logo['teamlogo']
            if team['awayTeam'] == logo['team']:
                team['awaylogo'] = logo['teamlogo']


    # get matches of current round if season is on track
    if helpers.season_end(fixture) == True:
        current_round = False
    else:
        current_round = [matches for matches in fixture if matches['round'] == helpers.up_rounds(fixture)]
        
    return render_template("index.html", 
        title='Bienvenido', 
        # table=tabla[0], 
        table=tabla, 
        fixture=current_round
    )

@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    # check submitted form
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
    session.pop('fixture', default=None)
    session.pop('logos', default=None)
    session.pop('tabla', default=None)

    logout_user()
    return redirect(url_for('index'))


@app.route('/register_fbs', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()

    # check submitted form
    if form.validate_on_submit():

        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        user.set_password(form.password.data)

        flash('Felicitaciones, usted se ha registrado exitosamente!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Registrarse', form=form)


@app.route('/user/<username>')
@login_required
def user(username):

    current_user = User.query.filter_by(username=username).first_or_404()
    users = User.query.all()
    users_points = db.session.query(Points.user_id, db.func.sum(Points.points).label('sum')).group_by(Points.user_id).order_by(desc('sum')).all()

    # prepare ranking
    ranking = []
    if users_points:
        for row in range(len(users_points)):
            for user in users:
                if user.id == users_points[row][0]:
                    ranking.append({'name':user.username,'points':users_points[row][1]})
    else:
        ranking = False

    if ranking:
        if username == ranking[0]['name']:
            flash('Felicitaciones, vas ganando!')

    # make a line chart with the users points of each round
    # line_chart=helpers.points_plot(fixture)
    line_chart = None

    return render_template('user.html',
                    user=current_user, 
                    logo=connect.logo('PL', current_user.fav_squad),
                    ranking=ranking,
                    plot=line_chart)

@app.route('/history/<username>')
@login_required
def history(username):

    fixture = session['fixture']

    # make table with all the data available (matches, points, bets)
    points_db = Points.query.filter_by(user_id=current_user.id).all()
    bet_matches = Bets.query.filter_by(user_id=current_user.id).all()

    historial = []
    for match in fixture:
        for score in points_db:
            for bet in bet_matches:
                if match['score'][0] != None:
                    if match['matchID'] == int(str(score.match_id)) and match['matchID'] == int(str(bet.match_id)):
                        historial.append({'round':match['round'],
                            'homeTeam': match['homeTeam'], 
                            'score_home':match['score'][0],
                            'bet_local':bet.score_home,
                            'awayTeam':match['awayTeam'],
                            'score_away':match['score'][1],
                            'bet_away':bet.score_away,
                            'points':score.points})
    
    return render_template('history.html', user=username, history=historial)

@app.before_request
def before_request():

    # current_user reference -> Flask-Login will invoke the user loader callback function, 
    # which will run a database query that will put the target user in the database session
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow() 
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():

    # let the user change username and choose squad
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
    return render_template('edit_profile.html', title='Editar Perfil', form=form)

@app.route('/bet', methods=['GET', 'POST'])
@login_required
def bet():

    fixture = session['fixture']
    # get matches of next round
    next_round_matches = [matches for matches in fixture if matches['round'] == helpers.up_rounds(fixture) + 1]
    # make list of matches in bets
    bet_matches = Bets.query.filter_by(user_id=current_user.id).all()
    bet_list = [int(str(bet)) for bet in bet_matches]

    # get matches of next round if season is active
    if helpers.season_end(fixture) == True:
        next_round_matches = False
    else:
        # then make a list to pass as value attribute of each field
        score_list = []
        for match in next_round_matches:
            if match['matchID'] in bet_list:
                for bet in bet_matches:
                    if int(str(bet.match_id)) == match['matchID']:
                        score_list.append({'home':int(str(bet.score_home)),'away':int(str(bet.score_home))})
        # if not list, no value attribute
        if not score_list:
             attribute = False
        else:
             attribute = score_list

        # QUE PASA CON EL CAMBIO DE TEMPORADA

        form = GamblingForm()

        if form.validate_on_submit():
            # first check if the bet is already done to overwrite the scores
            for value, match in zip(form.bet.data, next_round_matches):
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
                        new_bet = Bets(user_id=current_user.id,
                        match_id=match['matchID'],
                        timestamp = datetime.utcnow(),
                        score_home = value['home'],
                        score_away = value['away'])
                        db.session.add(new_bet)
                        db.session.commit()
            flash('Has enviado una apuesta')
            return redirect(url_for('bet'))

    return render_template("bet.html", 
        title='Apostar', 
        table=next_round_matches, 
        form=form, 
        value= attribute
    )

@app.route('/results', methods=['GET', 'POST'])
@login_required
def results():

    # load bets and compare with matches scores
    fixture = session['fixture']
    helpers.load(fixture, Bets.query.all())

    ### qué pasa cuando hay cambio de temporada

    # check if the tournament is over and send email to winner
    # else, load bets and points to show to the user
    if helpers.season_end(fixture) == True:
        current_round_matches = False
        users_points = db.session.query(Points.user_id, db.func.sum(Points.points).label('sum')).group_by(Points.user_id).order_by(desc('sum')).all()
        users = User.query.all()

        ranking = []
        if users_points:
            for row in range(len(users_points)):
                for user in users:
                    if user.id == users_points[row][0]:
                        ranking.append({'name':user.username,'points':users_points[row][1]})

        helpers.notify(ranking[0]['name'], ranking[0]['points'])
    
    else:
        show_points = Points.query.filter_by(user_id=current_user.id).all()

        # get matches of current and next round
        current_round_matches = [matches for matches in fixture if matches['round'] == helpers.up_rounds(fixture)]
        next_round_matches = [matches for matches in fixture if matches['round'] == helpers.up_rounds(fixture) + 1]

        # get last round last date and next round first date
        current_round_date = datetime.strptime(current_round_matches[-1]['date'], '%d-%m-%Y').date()
        next_round_date = datetime.strptime(next_round_matches[0]['date'], '%d-%m-%Y').date()

        # check bets are placed before current round
        user_bets = Bets.query.filter(Bets.user_id == 1, Bets.timestamp <= current_round_date).all()
        
        # if user has no bets for last round, nothing will be loaded
        # once the round is over, the next round will be loaded
        total = 0
        if not user_bets:
            total = 'no_bets'
        # show last/past round scores and bets (available until next round)
        elif datetime.utcnow().date() != next_round_date:
            print('loading')
            for match in current_round_matches:
                for score in show_points:
                    for bet in user_bets:
                        if match['matchID'] == int(str(score.match_id)) and match['matchID'] == int(str(bet.match_id)):
                            match['bet_local'] = bet.score_home
                            match['bet_away'] = bet.score_away
                            if match['score'][0] != None:
                                match['points'] = score.points
                                total = total + score.points
                            else:
                                match['points'] = None
        else:
            total = 'closed'
        
    return render_template("results.html",
        title='Puntos',
        table=current_round_matches,
        total=total
    )