import sqlalchemy as sa
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class GameSession(SqlAlchemyBase):
    __tablename__ = 'gameSession'

    id = sa.Column(sa.String(36), primary_key=True)
    question_id = sa.Column(sa.String(36), sa.ForeignKey('question.id'))
    start_datetime = sa.Column(sa.DateTime)
    end_datetime = sa.Column(sa.DateTime)
    score = sa.Column(sa.Integer, default=0)
    hints = sa.Column(sa.Integer, default=0)
    status = sa.Column(sa.String(20))
    registration_id = sa.Column(sa.String(36), sa.ForeignKey('registration.id'))

    registration = orm.relationship("Registration")
    question = orm.relationship("Question")