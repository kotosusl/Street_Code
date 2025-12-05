import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.testing.config import db_url

from .db_session import SqlAlchemyBase, create_session
from sqlalchemy import orm, select
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime
import datetime as dt
from flask import current_app

db = SQLAlchemy()


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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    token_version = db.Column(db.Integer, default=0)
    role = db.Column(db.String(20), default='user')

    genres = orm.relationship('Genres')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def generate_auth_token(self, expires_in=3600):
        payload = {
            'user_id': self.id,
            'email': self.email,
            'role': self.role,
            'token_version': self.token_version,
            'exp': datetime.utcnow() + dt.timedelta(seconds=expires_in),
            'iat': datetime.utcnow()
        }
        return jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

    def generate_refresh_token(self):
        payload = {
            'user_id': self.id,
            'type': 'refresh',
            'token_version': self.token_version,
            'exp': datetime.utcnow() + dt.timedelta(days=7),
            'iat': datetime.utcnow()
        }
        return jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

    def invalidate_tokens(self):
        db_sess = create_session()
        self.token_version += 1
        db_sess.commit()
        db_sess.close()

    @staticmethod
    def verify_auth_token(token):
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
            db_sess = create_session()
            user = db_sess.execute(select(Account).select_from(Account).where(payload['user_id'] == Account.id)).first()
            db_sess.close()
            if user and user[0].is_active and user[0].token_version == payload.get('token_version', 0):
                return user[0]
            return None
        except:
            return None

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'role': self.role
        }