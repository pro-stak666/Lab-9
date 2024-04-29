import sqlalchemy
from .db_session import SqlAlchemyBase
import sqlalchemy.orm as orm
from sqlalchemy_serializer import SerializerMixin


class Author(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'author'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name_author = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    books = orm.relationship("Name")
