from flask import render_template, flash, redirect, url_for
from app import app, api_connection
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Points, Bets
from app import db
from app.forms import RegistrationForm, EditProfileForm

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
    fixture = api_connection.fixture('PL',datetime.utcnow().strftime('%Y'),'1')
    tabla = api_connection.standings('PL',datetime.utcnow().strftime('%Y'))
    return render_template("index.html", title='Home Page', table=tabla, fixture=fixture)

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
                    logo=api_connection.logo('PL',user.fav_squad),
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

@app.route('/bet')
@login_required
# the @login_required decorator intercepts the request and responds with a redirect to /login, 
# adding a query string argument to the URL, making the complete redirect URL /login?next=/index.
# The next query string argument is set to the original URL, so the application can use 
# that to redirect back after login.
def bet():
    fixture = api_connection.fixture('PL','2019','1')
    return render_template("bet.html", title='Home Page', fixture=fixture)