from flask import Flask, jsonify
from models import db
from auth import auth_bp
from utils import token_required, error_response
import logging
import os

def create_app():
    app = Flask(__name__)
    
    # Конфигурация
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600
    
    # Инициализация базы данных
    db.init_app(app)
    
    # Регистрация блюпринтов
    app.register_blueprint(auth_bp)
    
    # Глобальная обработка ошибок
    @app.errorhandler(404)
    def not_found_error(error):
        return error_response('Ресурс не найден', 'not_found', 404)
    
    @app.errorhandler(500)
    def internal_error(error):
        return error_response('Внутренняя ошибка сервера', 'internal_server_error', 500)
    
    # Эндпоинт для проверки здоровья
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'healthy'}), 200
    
    # Защищенный эндпоинт для примера
    @app.route('/api/protected', methods=['GET'])
    @token_required
    def protected_endpoint():
        from flask import g
        return jsonify({
            'success': True,
            'message': f'Доступ разрешен для {g.current_user.email}',
            'role': g.current_user.role
        })
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    # Настройка логирования
    logging.basicConfig(level=logging.INFO)
    
    # Создание таблиц в базе данных
    with app.app_context():
        db.create_all()
        print("✅ База данных создана/проверена")
    
    print("🚀 Сервер запущен: http://127.0.0.1:5000")
    print("📌 Доступные эндпоинты:")
    print("   GET  /health                    - Проверка здоровья")
    print("   POST /api/auth/register         - Регистрация")
    print("   POST /api/auth/login            - Вход")
    print("   POST /api/auth/logout           - Выход")
    print("   POST /api/auth/refresh          - Обновление токена")
    print("   GET  /api/auth/me               - Информация о пользователе")
    print("   GET  /api/protected             - Пример защищенного эндпоинта")
    
    app.run(debug=True, host='0.0.0.0', port=5000)