from flask import render_template, flash, redirect, url_for
from app import app, helpers
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Points, Bets
from app import db
from app.forms import RegistrationForm, EditProfileForm, GamblingForm

from flask import request
from werkzeug.urls import url_parse

from datetime import datetime

@app.route('/')
@app.route('/index')
@login_required
# the @login_required decorator intercepts the request and responds with a redirect to /login, 
# adding a query string argument to the URL, making the complete redirect URL /login?next=/index.
# The next query string argument is set to the original URL, so the application can use 
# that to redirect back after login.

def index():

    # api requests
    fixture = helpers.fixture('PL',datetime.utcnow().strftime('%Y'))
    tabla = helpers.standings('PL',datetime.utcnow().strftime('%Y'))

    # get all rounds until now
    rounds = [matches['round'] for matches in fixture if datetime.strptime(matches['date'], '%d-%m-%Y').date() <= datetime.utcnow().date()]
    # get matches of current round
    current_round = [matches for matches in fixture if matches['round'] == max(rounds)]
    
    # add logo for each team in fixture
    for team in fixture:
        for logo in tabla[1]:
            if team['homeTeam'] == logo['team']:
                team['homelogo'] = logo['teamlogo']
            if team['awayTeam'] == logo['team']:
                team['awaylogo'] = logo['teamlogo']
    
    return render_template("index.html", title='Home Page', table=tabla[0], fixture=current_round)

@app.route('/login', methods=['GET', 'POST'])
def login():

    # current_user can be used to obtain the user object that 
    # represents the client of the request
    # is_authenticated property is True if the user has valid credentials
    if current_user.is_authenticated:
    # if already logged in users goes to index page        
        return redirect(url_for('index'))

    # form object instantiated from the LoginForm class
    form = LoginForm()

    # when the browser sends the POST request, form.validate_on_submit() 
    # will gather all the data and run all the validators attached to fields,    
    # else (if the the browser sends the GET request 
    # or if at least one field fails validation) will return False

    if form.validate_on_submit():

        # query the database to find the user with the filter_by().
        # instead of all(), first() returns one result only
        user = User.query.filter_by(username=form.username.data).first() 
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        
        # this contains all the information that the client sent with the request
        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    
    return render_template('login.html', title='Sign In', form=form)

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

        # register the user
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        # give cero points to the new user
        user_points = Points(user_id=User.query.filter_by(username=form.username.data).first().id,
                        timestamp = datetime.utcnow(),
                        points = 0)
        db.session.add(user_points)
        db.session.commit()
    
        user.set_password(form.password.data)

        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    users = User.query.all()
    
    user_list = [{'nombre':user.username,'puntos': user.rank.first().points} for user in users]
    ranking = sorted(user_list, key=lambda diccionario: diccionario['puntos'], reverse=True)

    return render_template('user.html',
                    user=user, 
                    logo=helpers.logo('PL',user.fav_squad),
                    ranking=enumerate(ranking))

# @before_request decorator from Flask register the decorated function to be executed right before the view function
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
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.fav_squad.data = current_user.fav_squad
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/bet', methods=['GET', 'POST'])
@login_required
# the @login_required decorator intercepts the request and responds with a redirect to /login, 
# adding a query string argument to the URL, making the complete redirect URL /login?next=/index.
# The next query string argument is set to the original URL, so the application can use 
# that to redirect back after login.
def bet():
    # api request for matches/fixture
    fixture = helpers.fixture('PL',datetime.utcnow().strftime('%Y'))
    # get current round
    rounds = [matches['round'] for matches in fixture if datetime.strptime(matches['date'], '%d-%m-%Y').date() <= datetime.utcnow().date()]
    # get matches of next round

    ####### OJO OJO OJO OJO
    next_round = [matches for matches in fixture if matches['round'] == max(rounds) -1]

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

    fixture = helpers.fixture('PL',datetime.utcnow().strftime('%Y'))
    bet_matches = Bets.query.filter_by(user_id=User.query.filter_by(username=current_user.username).first().id).all()

    # evaluate bets of the played matchets
    helpers.load(fixture, bet_matches, current_user.username)

    show_points = Points.query.filter_by(user_id=User.query.filter_by(username=current_user.username).first().id).all()

    rounds = [matches['round'] for matches in fixture if datetime.strptime(matches['date'], '%d-%m-%Y').date() <= datetime.utcnow().date()]

    last_round = [matches for matches in fixture if matches['round'] == max(rounds) - 1]

    points = []

    # add corresponding data in dictionary to show on template
    for match in last_round:
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

        # load all the data if it is not a new user who has bets
    if not bet_matches:
        total = False
    else:
        total = sum([num for num in points if isinstance(num,int)])
    print(points)
    print(total)

    return render_template("results.html", title='Home Page', table=last_round, total=total)