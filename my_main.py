from flask import Flask, render_template, redirect, request
from data import db_session
from data.author import Author
from data.name import Name
from forms.add_book import AddBookForm
from sqlalchemy import text


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/', methods=['GET', 'POST', 'DELETE'])
def index():
    db_sess = db_session.create_session()
    lst = db_sess.query(Name.title, Author.name_author).filter(Author.id == Name.author_id).all()

    if request.method == 'POST':
        if 'author' not in request.form.keys():
            db_sess.execute(text('DELETE FROM author'))
            db_sess.execute(text('DELETE FROM name'))
            db_sess.commit()
            return redirect('/')

    form = AddBookForm()
    if form.validate_on_submit():
        if db_sess.query(Author).filter(Author.name_author == form.author.data).first():
            id_author = db_sess.query(Author).filter(Author.name_author == form.author.data).first().id
            book = db_sess.query(Name).filter(Name.title == form.book.data).first()
            if book:
                if book.author_id == id_author:
                    return render_template('index.html', title='главная', books=lst, count=len(lst), message='такая запись уже имеется', form=form)
                else:
                    new_book = Name()  # добавляем книгу с известным автором
                    new_book.title = form.book.data
                    new_book.author_id = id_author
                    db_sess.add(new_book)
                    db_sess.commit()

                return redirect('/')
        else:
            new_author = Author()  # добавляем новую книгу с новым автором
            new_author.name_author = form.author.data
            db_sess.add(new_author)
            new_book = Name()
            new_book.title = form.book.data
            new_book.author_id = db_sess.query(Author).filter(Author.name_author == form.author.data).first().id
            db_sess.add(new_book)
            db_sess.commit()

            return redirect('/')

    return render_template('index.html', title='главная', books=lst, count=len(lst), form=form)


def main():
    db_session.global_init("db/database.db")
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
