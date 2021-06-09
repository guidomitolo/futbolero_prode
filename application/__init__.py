import os
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, current_app

from config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from flask_session import Session

db = SQLAlchemy()
migrate = Migrate()

login = LoginManager()
login.login_view = 'auth.login'
login.login_message = u"Por favor ingresar para acceder al sitio."

moment = Moment()

server_session = Session()

def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(config_class)

    with app.app_context():

        # init modules
        db.init_app(app)
        migrate.init_app(app, db)
        login.init_app(app)
        moment.init_app(app)
        server_session.init_app(app)

        # register bluprints
        from application.auth import bp as auth_bp
        app.register_blueprint(auth_bp)
        from application.main import bp as main_bp
        app.register_blueprint(main_bp)
        from application.posts import bp as posts_bp
        app.register_blueprint(posts_bp)

        from application import errors
        
        from application.auth.models import User
        from application.posts.models import Post
        from application.main.models import Bets, Points, Seasons

        @app.shell_context_processor
        def make_shell_context():
            return {'db': db, 'User': User, 'Bets': Bets, 'Points': Points, 'Seasons': Seasons, 'Post': Post}

        @login.user_loader
        def load_user(id):
            return User.query.get(int(id))

        # create the database on deployment
        db.create_all()
        db.session.commit()

        if not app.debug:

            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler(
                'logs/futbolero.log', 
                maxBytes=10240,
                backupCount=10
            )
            file_handler.setFormatter(
                logging.Formatter(
                    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
                    )
                )
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

            app.logger.setLevel(logging.INFO)
            app.logger.info('Arranque de Futbolero')

        return app

