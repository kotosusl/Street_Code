import sqlalchemy as sa
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Account(SqlAlchemyBase):
    __tablename__ = 'account'

    id = sa.Column(sa.String(36), primary_key=True)
    email = sa.Column(sa.String(100), unique=True, nullable=False)
    password = sa.Column(sa.String(200), nullable=False)
    username = sa.Column(sa.String(50), unique=True, nullable=False)
    avatar = sa.Column(sa.BLOB)
    count_game = sa.Column(sa.Integer, default=0)
    count_winner = sa.Column(sa.Integer, default=0)
    total_score = sa.Column(sa.Integer, default=0)
    favorite_genre = sa.Column(sa.String(50), sa.ForeignKey('genres.id'))

    genres = orm.relationship('Genres')
