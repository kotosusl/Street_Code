import sqlalchemy as sa
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Registration(SqlAlchemyBase):
    __tablename__ = 'registration'

    id = sa.Column(sa.String(36), primary_key=True)
    team_id = sa.Column(sa.String(36), sa.ForeignKey('team.id'))
    game_id = sa.Column(sa.String(36), sa.ForeignKey('game.id'))
    status = sa.Column(sa.String(20))

    team = orm.relationship("Team")
    game = orm.relationship("Game")