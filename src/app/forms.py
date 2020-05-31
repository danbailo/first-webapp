from flask_wtf import FlaskForm
from wtforms.fields import BooleanField, PasswordField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[
        DataRequired("This field is necessary!"),
        Email()
    ])
    password = PasswordField("Password", validators=[
        DataRequired("This field is necessary!")
    ])
    remember = BooleanField("Remember me (7 days)")
    # submit = SubmitField("Submit")


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[
        DataRequired("This field is necessary!")
    ])
    email = EmailField("Email", validators=[
        DataRequired("This field is necessary!"),
        Email()
    ])
    password = PasswordField("Password", validators=[
        DataRequired("This field is necessary!"),
        Length(min=4)
    ])
    # submit = SubmitField("Submit")
