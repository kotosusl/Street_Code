import sqlalchemy as sa
from .db_session import SqlAlchemyBase


class Genres(SqlAlchemyBase):
    __tablename__ = 'genres'

    id = sa.Column(sa.String(36), primary_key=True)
    name = sa.Column(sa.String(50), unique=True)
