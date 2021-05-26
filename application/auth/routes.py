# flask core libs
from flask import render_template, flash, redirect, url_for, session
from flask_login import current_user, login_user, logout_user
from flask import request
from sqlalchemy.sql.expression import null

# app modules
from application.auth.models import User
from application.auth.forms import LoginForm, RegistrationForm
from application.auth import bp

from application import db

# external libs
from werkzeug.urls import url_parse
from datetime import datetime


@bp.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first() 
        if user is None or not user.check_password(form.password.data):
            flash('Usuario o Password Inválidos')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember_me.data)
        
        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')

        return redirect(next_page)
    
    return render_template('auth/login.html', title='Ingresar', form=form)


@bp.route('/logout')
def logout():
    session.pop('fixture', default=None)
    session.pop('logos', default=None)
    session.pop('tabla', default=None)
    session.pop('season', default=None)
    session.pop('league', default=None)

    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register_fbs', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()

    # check submitted form
    if form.validate_on_submit():

        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        user.set_password(form.password.data)

        flash('Felicitaciones, usted se ha registrado exitosamente!')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', title='Registrarse', form=form)


@bp.before_request
def before_request():

    # current_user reference -> Flask-Login will invoke the user loader callback function, 
    # which will run a database query that will put the target user in the database session
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow() 
        db.session.commit()