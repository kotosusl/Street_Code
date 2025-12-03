import logging
from functools import wraps
from flask import request, jsonify, g
from models import User

# Настройка логирования
logger = logging.getLogger(__name__)

def token_required(f):
    """Декоратор для защиты эндпоинтов JWT токеном"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({
                'success': False,
                'message': 'Токен отсутствует'
            }), 401
        
        user = User.verify_auth_token(token)
        if not user:
            return jsonify({
                'success': False,
                'message': 'Невалидный или просроченный токен'
            }), 401
        
        g.current_user = user
        return f(*args, **kwargs)
    
    return decorated

def error_response(message, error_code, status_code=400):
    return jsonify({
        'success': False,
        'message': message,
        'error': error_code
    }), status_code