from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length


class RegisterForm(FlaskForm):
    name = StringField('username', [InputRequired(), Length(min=5, max=25)])
    email = StringField('email', validators=[InputRequired(), Length(min=5, max=150)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=5, max=150)])
