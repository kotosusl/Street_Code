from flask import Blueprint, request, jsonify, current_app, g
from sqlalchemy import select
from uuid import uuid4

from sqlalchemy.testing import db_spec

from data.account import Account
from data.db_session import create_session
from utils import token_required, error_response
import re

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


@auth_bp.route('/register', methods=['POST'])
def register():
    db_sess = create_session()
    try:
        data = request.get_json()
        
        if not data:
            return error_response('Нет данных', 'no_data', 400)
        
        # Валидация
        email = data.get('email', '').strip()
        password = data.get('password', '')
        confirm_password = data.get('confirm_password', '')
        name = data.get('name', '').strip()
        
        # Проверка email
        if not email or not validate_email(email):
            return error_response('Некорректный email', 'invalid_email', 400)
        
        # Проверка пароля
        if len(password) < 8:
            return error_response('Пароль должен быть минимум 8 символов', 'password_too_short', 400)
        
        if password != confirm_password:
            return error_response('Пароли не совпадают', 'passwords_mismatch', 400)
        
        # Проверка имени
        if len(name) < 2 or len(name) > 80:
            return error_response('Имя должно быть от 2 до 80 символов', 'invalid_name', 400)
        
        # Проверка существования пользователя

        if db_sess.execute(select(Account).select_from(Account).where(Account.email == email)).first():
            return error_response('Пользователь уже существует', 'user_exists', 409)
        
        # Создание пользователя
        user = Account(email=email, username=name, id=str(uuid4()))
        user.set_password(password)

        db_sess.add(user)
        db_sess.commit()
        
        # Генерация токенов
        access_token = user.generate_auth_token()
        refresh_token = user.generate_refresh_token()

        db_sess.close()
        return jsonify({
            'success': True,
            'message': 'Регистрация успешна',
            'data': {
                'user': user.to_dict(),
                'tokens': {
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'expires_in': 3600
                }
            }
        }), 201
        
    except Exception as e:
        db_sess.close()
        return error_response(f'Ошибка сервера: {str(e)}', 'server_error', 500)


@auth_bp.route('/login', methods=['POST'])
def login():
    db_sess = create_session()
    try:
        data = request.get_json()
        
        if not data:
            return error_response('Нет данных', 'no_data', 400)
        
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not email or not password:
            return error_response('Email и пароль обязательны', 'missing_credentials', 400)
        
        user = db_sess.execute(select(Account).select_from(Account).where(Account.email == email)).first()
        
        if not user or not user[0].check_password(password):
            return error_response('Неверный email или пароль', 'invalid_credentials', 401)
        
        if not user[0].is_active:
            return error_response('Аккаунт деактивирован', 'account_inactive', 403)
        
        # Генерация токенов
        access_token = user[0].generate_auth_token()
        refresh_token = user[0].generate_refresh_token()
        db_sess.close()
        return jsonify({
            'success': True,
            'message': 'Вход выполнен успешно',
            'data': {
                'user': user[0].to_dict(),
                'tokens': {
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'expires_in': 3600
                }
            }
        })
        
    except Exception as e:
        db_sess.close()
        return error_response(f'Ошибка сервера: {str(e)}', 'server_error', 500)


@auth_bp.route('/refresh', methods=['POST'])
def refresh_token():
    db_sess = create_session()
    try:
        data = request.get_json()
        
        if not data or 'refresh_token' not in data:
            return error_response('Refresh токен обязателен', 'missing_token', 400)
        
        import jwt
        from datetime import datetime

        try:
            payload = jwt.decode(
                data['refresh_token'],
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
            
            if payload.get('type') != 'refresh':
                raise jwt.InvalidTokenError
            
            user = db_sess.execute(select(Account).select_from(Account).where(payload['user_id'] == Account.id)).first()
            
            if not user or not user[0].is_active:
                raise jwt.InvalidTokenError
            
            if user[0].token_version != payload.get('token_version', 0):
                raise jwt.InvalidTokenError
            
            access_token = user[0].generate_auth_token()
            db_sess.close()
            return jsonify({
                'success': True,
                'message': 'Токен обновлен',
                'data': {
                    'access_token': access_token,
                    'expires_in': 3600
                }
            })
            
        except:
            db_sess.close()
            return error_response('Невалидный refresh токен', 'invalid_token', 401)
            
    except Exception as e:
        db_sess.close()
        return error_response(f'Ошибка сервера: {str(e)}', 'server_error', 500)


@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout():
    try:
        g.current_user.invalidate_tokens()
        
        return jsonify({
            'success': True,
            'message': 'Выход выполнен успешно'
        })
        
    except Exception as e:
        return error_response(f'Ошибка сервера: {str(e)}', 'server_error', 500)


@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user():
    return jsonify({
        'success': True,
        'data': {
            'user': g.current_user.to_dict()
        }
    })