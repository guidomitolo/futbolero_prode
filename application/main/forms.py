from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import FormField, FieldList, IntegerField, Form
from wtforms.validators import ValidationError, DataRequired
from flask_wtf.file import FileField, FileAllowed
from application.auth.models import User


class EditProfileForm(FlaskForm):

    # constructor to check if the user is logged
    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    username = StringField('Nombre de usuario', validators=[DataRequired()])
    user_pic = FileField('Foto Carné', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Guardar')

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Por favor usar otro nombre de usuario')


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