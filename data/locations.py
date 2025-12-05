import sqlalchemy as sa
from .db_session import SqlAlchemyBase


class Locations(SqlAlchemyBase):
    __tablename__ = 'locations'

    id = sa.Column(sa.String(36), primary_key=True)
    name = sa.Column(sa.String(100), unique=True)
