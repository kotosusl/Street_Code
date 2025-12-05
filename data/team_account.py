import sqlalchemy as sa
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Team_Account(SqlAlchemyBase):
    __tablename__ = 'team_account'

    id = sa.Column(sa.String(36), primary_key=True)
    account_id = sa.Column(sa.String(36), sa.ForeignKey('account.id'))
    team_id = sa.Column(sa.String(36), sa.ForeignKey('team.id'))

    account = orm.relationship("Account")
    team = orm.relationship("Team")