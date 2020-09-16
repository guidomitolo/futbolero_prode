import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():

    "standard configuration of the flask app according to flask ad-hoc objects"

    # The SECRET_KEY configuration variable is used as a 
    # cryptographic key to generate signatures or tokens 
    # and to protect web forms against a nasty attack called Cross-Site Request Forgery
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
