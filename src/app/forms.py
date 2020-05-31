from flask_wtf import FlaskForm
from wtforms.fields import BooleanField, PasswordField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField("Password", validators=[
        DataRequired(),
        Length(min=4)
    ])
    remember = BooleanField("Remember me (7 days)")
    # submit = SubmitField("Submit")


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[
        DataRequired()
    ])
    email = EmailField("Email", validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField("Password", validators=[
        DataRequired(),
        Length(min=4)
    ])
    # submit = SubmitField("Submit")
