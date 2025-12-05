import sqlalchemy as sa
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Team(SqlAlchemyBase):
    __tablename__ = 'team'

    id = sa.Column(sa.String(36), primary_key=True)
    name = sa.Column(sa.String(50), nullable=False)
    captain_id = sa.Column(sa.String(36), sa.ForeignKey('account.id'))

    captain = orm.relationship("Account")