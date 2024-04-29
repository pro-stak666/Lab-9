from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class AddBookForm(FlaskForm):
    book = StringField('название книги')
    author = StringField('имя автора')
    submit = SubmitField("добавить")
