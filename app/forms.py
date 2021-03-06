from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Length


class RegisterForm(FlaskForm):
    name = StringField('username', [InputRequired(), Length(min=5, max=25)])
    email = EmailField('email', validators=[InputRequired(), Length(min=5, max=150)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=5, max=150)])


class ChangepPassForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Length(min=5, max=150)])
    new_password = PasswordField('Новый пароль', validators=[InputRequired(), Length(min=5, max=150)])
