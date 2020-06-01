from flask_wtf import FlaskForm
from markupsafe import Markup
from wtforms.fields import (BooleanField, Field, PasswordField, StringField,
                            SubmitField, SelectField)
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, Length
from wtforms.widgets.core import HTMLString, escape, html_params
from app.models import Book


class InlineButtonWidget(object):
    def __init__(self, class_=None):
        self.class_ = class_

    def __call__(self, field, **kwargs):
        kwargs.setdefault('type', 'submit')
        kwargs["class"] = self.class_
        title = kwargs.pop('title', field.description or '')
        params = html_params(title=title, **kwargs)

        html = '<button %s>%s</button>'
        return HTMLString(html % (params, escape(field.label.text)))


class InlineButton(Field):
    widget = InlineButtonWidget()

    def __init__(self, label=None, validators=None, text='Save', **kwargs):
        super(InlineButton, self).__init__(label, validators, **kwargs)
        self.text = text

    def _value(self):
        if self.data:
            return u''.join(self.data)
        else:
            return u''


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField("Password", validators=[
        DataRequired()
    ])
    remember = BooleanField("Remember me (7 days)")
    text = Markup('<i class="fas fa-sign-in-alt"></i> Submit')
    submit = SubmitField(text, widget=InlineButtonWidget(class_="btn btn-info"))


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
        Length(min=4, message="At least 4 characters are required!")
    ])
    text = Markup('<i class="fas fa-user-plus"></i> Submit')
    submit = SubmitField(text, widget=InlineButtonWidget(class_="btn btn-success"))    


class BookForm(FlaskForm):
    name = StringField("Name", validators=[
        DataRequired()
    ])
    text = Markup('<i class="fas fa-plus"></i> Add')
    submit = SubmitField(text, widget=InlineButtonWidget(class_="btn btn-success"))

class UserBookForm(FlaskForm):
    books = Book()
    book = SelectField("Book",
        coerce=int,
    )
    text = Markup('<i class="fas fa-plus"></i> Add')
    submit = SubmitField(text, widget=InlineButtonWidget(class_="btn btn-success"))    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.book.choices = [
            (book.id_book, book.book) for book in Book().query.all()
        ]