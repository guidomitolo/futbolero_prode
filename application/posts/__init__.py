from flask import Blueprint

bp = Blueprint('posts', __name__)

from application.posts import forms, models, routes