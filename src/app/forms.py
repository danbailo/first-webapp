from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField
from wtforms.fields import BooleanField, PasswordField, SubmitField


class LoginForm(FlaskForm):
    email = EmailField("Email")
    password = PasswordField("Password")
    remember = BooleanField("Stay Connected")
    submit = SubmitField('Submit')
