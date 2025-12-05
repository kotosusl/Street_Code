import sqlalchemy as sa
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Question(SqlAlchemyBase):
    __tablename__ = 'question'

    id = sa.Column(sa.String(36), primary_key=True)
    game_id = sa.Column(sa.String(36), sa.ForeignKey('game.id'))
    title = sa.Column(sa.String(500), nullable=False)
    description = sa.Column(sa.String(500))
    image_url = sa.Column(sa.String(200))
    answer = sa.Column(sa.String(100))
    score = sa.Column(sa.Integer, nullable=False)
    bool_hint = sa.Column(sa.Boolean, default=False)
    hint = sa.Column(sa.String(200))
    penalty = sa.Column(sa.Integer, default=0)

    game = orm.relationship("Game")