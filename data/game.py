import sqlalchemy as sa
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Game(SqlAlchemyBase):
    __tablename__ = 'game'

    id = sa.Column(sa.String(36), primary_key=True)
    title = sa.Column(sa.String(100), nullable=False)
    description = sa.Column(sa.String(500))
    organizer_id = sa.Column(sa.String(36), sa.ForeignKey('account.id'))
    avatar = sa.Column(sa.BLOB)
    location = sa.Column(sa.String(50))
    difficulty = sa.Column(sa.String(30), default="Не указано")
    duration = sa.Column(sa.Integer)
    max_members = sa.Column(sa.Integer)
    mode = sa.Column(sa.String(20))
    genre = sa.Column(sa.String(50), sa.ForeignKey('genres.id'))
    is_active = sa.Column(sa.Boolean, default=True)
    start_datetime = sa.Column(sa.DateTime)
    end_datetime = sa.Column(sa.DateTime)

    account = orm.relationship("Account")
    genres = orm.relationship('Genres')