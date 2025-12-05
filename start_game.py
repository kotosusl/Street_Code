from datetime import datetime
from uuid import uuid4

from flask import Blueprint, request, jsonify
from sqlalchemy import select

from data.db_session import create_session
from data.game_session import GameSession
from data.game import Game
from data.question import Question
from data.registration import Registration

blueprint_start_game = Blueprint('blueprint_start_game', __name__)


@blueprint_start_game.route('/api/start_game', methods=['POST'])
def start_game():
    jsn = request.get_json() or {}

    if not jsn:
        return jsonify({
            'success': False,
            'message': 'Отсутствует тело запроса'
        }), 400

    if not (jsn.get('registration_id', 0)):
        return jsonify({
            'success': False,
            'message': 'Не хватает данных для начала игры'
        }), 400

    db_sess = create_session()
    registration = db_sess.execute(
        select(Registration).select_from(Registration).where(Registration.id == jsn['registration_id'])).first()
    if not registration or registration[0].status != 'active':
        db_sess.close()
        return jsonify({
            'success': False,
            'message': 'Регистрация не существует или неактивна'
        }), 304

    questions_list = db_sess.execute(
        select(Question).select_from(Question).join(Game, Game.id == Question.game_id).where(
            Game.id == registration[0].game_id))

    new_game_session = GameSession(
        id=str(uuid4()),
        start_datetime=datetime.now(),
        score=0,
        hints=0,
        status='active',
        registration_id=jsn['registration_id']
    )
    db_sess.add(new_game_session)
    db_sess.commit()

    response_questions_list = {
        'success': True,
        'game_session': {
            'id': new_game_session.id,
            'start_datetime': new_game_session.start_datetime,
            'score': new_game_session.score,
            'hints': new_game_session.hints,
            'status': new_game_session.status,
            'registration_id': new_game_session.registration_id
        },
        'questions_id_list': [
            {
                'id': p[0].id,
                'game_id': p[0].game_id,
                'title': p[0].title,
                'description': p[0].description,
                'image_url': p[0].image_url,
                'score': p[0].score,
                'bool_hint': p[0].bool_hint,
                'hint': p[0].hint,
                'penalty': p[0].penalty
            }
            for p in questions_list
        ]
    }
    db_sess.close()
    return jsonify(response_questions_list), 200