from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    body = TextAreaField('Mensaje', validators=[DataRequired()])
    submit = SubmitField('Enviar')