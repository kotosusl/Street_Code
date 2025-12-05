from datetime import datetime, timedelta

from flask import Blueprint, request, jsonify
from sqlalchemy import select
from uuid import uuid4
from data.db_session import create_session
from data.game import Game
from data.game_session import GameSession
from data.player_answer import PlayerAnswer
from data.question import Question
from data.registration import Registration

blueprint_check_player_answer = Blueprint('blueprint_check_player_answer', __name__)


@blueprint_check_player_answer.route('/api/check_answer', methods=['POST'])
def check_answer():
    jsn = request.get_json() or {}
    if not jsn:
        return jsonify({
            'success': False,
            'message': 'Отсутствует тело запроса'
        }), 400

    if (not (jsn.get('answer', 0) and jsn.get('game_session_id', 0) and jsn.get('question_id', 0)) or
            jsn.get('end_question_bool', -1) == -1 or jsn.get('hint', -1) == -1):
        return jsonify({
            'success': False,
            'message': 'Не хватает данных для проверки ответа'
        }), 400

    db_sess = create_session()
    question = db_sess.execute(select(Question).select_from(Question).where(jsn['question_id'] == Question.id)).first()
    if not question:
        db_sess.close()
        return jsonify({
            'success': False,
            'message': 'Вопрос не найден'
        }), 404

    game_session = db_sess.execute(
        select(GameSession).select_from(GameSession).where(jsn['game_session_id'] == GameSession.id)).first()
    if not game_session:
        db_sess.close()
        return jsonify({
            'success': False,
            'message': 'Игровая сессия не найдена'
        }), 404

    game = db_sess.execute(
        select(Game).select_from(Game).join(Registration, Game.id == Registration.game_id).join(
            GameSession, GameSession.registration_id == Registration.id).where(
            GameSession.id == jsn['game_session_id'])).first()

    if (game_session[0].status == 'finished'
            or datetime.now() - game_session[0].start_datetime >= timedelta(minutes=game[0].duration)):
        if game_session[0].status != 'finished':
            game_session[0].end_datetime = game_session[0].start_datetime + timedelta(minutes=game[0].duration)
            game_session[0].status = 'finished'
            db_sess.commit()
        response = {
            'success': True,
            'game_status': "finished",
            'start_datetime': game_session[0].start_datetime,
            'end_datetime': game_session[0].end_datetime,
            'total_score': game_session[0].score,
            'hints': game_session[0].hints,
            'registration_id': game_session[0].registration_id
        }
        db_sess.close()
        return jsonify(response), 200

    new_player_answer = PlayerAnswer(
        id=str(uuid4()),
        game_session_id=jsn['game_session_id'],
        question_id=jsn['question_id'],
        text_answer=jsn['answer'],
        hint=bool(jsn['hint'])
    )

    if ' '.join(question[0].answer.lower().strip().split()) == ' '.join(jsn['answer'].lower().strip().split()):
        new_player_answer.correct_answer = True
        new_player_answer.score = question[0].score
        if jsn['hint']:
            new_player_answer.score -= question[0].penalty
            game_session[0].hints += 1
            db_sess.commit()
    else:
        new_player_answer.correct_answer = False
        new_player_answer.score = 0

    db_sess.add(new_player_answer)
    db_sess.commit()

    game_session[0].question_id = jsn['question_id']
    game_session[0].score += new_player_answer.score
    db_sess.commit()

    response = {
        'success': True,
        'game_status': 'active',
        'start_datetime': game_session[0].start_datetime,
        'correct': new_player_answer.correct_answer,
        'question_score': new_player_answer.score,
        'total_score': game_session[0].score,
        'hints': game_session[0].hints,
        'registration_id': game_session[0].registration_id
    }

    if jsn['end_question_bool']:
        response['game_status'] = 'finished'
        response['end_datetime'] = datetime.now()
        game_session[0].end_time = datetime.now()
        game_session[0].status = 'finished'
        db_sess.commit()

    db_sess.close()
    return jsonify(response), 200
