import sqlalchemy as sa
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class PlayerAnswer(SqlAlchemyBase):
    __tablename__ = 'playerAnswer'

    id = sa.Column(sa.String(36), primary_key=True)
    game_session_id = sa.Column(sa.String(36), sa.ForeignKey('gameSession.id'))
    question_id = sa.Column(sa.String(36), sa.ForeignKey('question.id'))
    text_answer = sa.Column(sa.String(100))
    correct_answer = sa.Column(sa.Boolean, nullable=False)
    hint = sa.Column(sa.Boolean, default=False)
    score = sa.Column(sa.Integer, default=0)

    question = orm.relationship("Question")
    game_session = orm.relationship('GameSession')