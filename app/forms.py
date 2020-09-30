from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms import FormField, FieldList, IntegerField, Form
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, NumberRange, InputRequired
from app.models import User
from app import api_connection

class LoginForm(FlaskForm):

    # The four classes that represent the field types are imported directly 
    # from the WTForms package. For each field, an object is created as a 
    # class variable in the LoginForm class. Each field is 
    # given a description or label as a first argument.

    # The optional validators argument is 
    # used to attach validation behaviors to fields.
    # The DataRequired validator checks that the field is not submitted empty. 

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    fav_squad = SelectField('Fav\' Squad',choices=api_connection.team('PL'))
    submit = SubmitField('Submit')

    # constructor to check if the user is logged
    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):

    # This username is saved as an instance variable, and checked in the validate_username() method.
    # If the username entered in the form is the same as the original username, 
    # then there is no reason to check the database for duplicates.
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

class BetForm(Form):
    home = IntegerField()
    away = IntegerField()

class GamblingForm(FlaskForm):
    bet = FieldList(FormField(BetForm), min_entries=10, max_entries=10)
    
    def validate_bet(form, bet):
        for field in bet.data:
            if field['home'] == None or field['away'] == None:
                raise ValidationError('Completar los campos numéricos')
            elif field['home'] < 0 or field['away'] < 0:
                raise ValidationError('Por favor completar con números Positivos')