from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime as dt
from flask import current_app

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    token_version = db.Column(db.Integer, default=0)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
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
        self.token_version += 1
        db.session.commit()
    
    @staticmethod
    def verify_auth_token(token):
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
            user = User.query.get(payload['user_id'])
            
            if user and user.is_active and user.token_version == payload.get('token_version', 0):
                return user
            return None
        except:
            return None
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'role': self.role
        }