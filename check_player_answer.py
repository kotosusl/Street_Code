from flask import Blueprint, request, jsonify
from sqlalchemy import select
from uuid import uuid4
from data.db_session import create_session
from data.game_session import GameSession
from data.player_answer import PlayerAnswer
from data.question import Question

blueprint_check_player_answer = Blueprint('blueprint_check_player_answer', __name__)


@blueprint_check_player_answer.route('/api/check_answer', methods=['POST'])
def check_answer():
    jsn = request.get_json() or {}
    if not jsn:
        return jsonify({
            'error': 'Отсутствует тело запроса'
        }), 400

    if not (jsn.get('answer', 0) and jsn.get('game_session_id', 0) and jsn.get('question_id', 0)) or jsn.get('hint',
                                                                                                             -1) == -1:
        return jsonify({
            'error': 'Не хватает данных для проверки ответа'
        }), 400

    db_sess = create_session()
    question = db_sess.execute(select(Question).select_from(Question).where(jsn['question_id'] == Question.id)).first()
    if not question:
        db_sess.close()
        return jsonify({
            'error': 'Вопрос не найден'
        }), 404

    game_session = db_sess.execute(
        select(GameSession).select_from(GameSession).where(jsn['game_session_id'] == GameSession.id)).first()
    if not game_session:
        db_sess.close()
        return jsonify({
            'error': 'Игровая сессия не найдена'
        }), 404

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
    else:
        new_player_answer.correct_answer = False
        new_player_answer.score = 0

    db_sess.add(new_player_answer)
    db_sess.commit()

    game_session[0].question_id = jsn['question_id']
    game_session[0].score += new_player_answer.score
    db_sess.commit()

    response = {
        'status': "OK",
        'correct': new_player_answer.correct_answer,
        'question_score': new_player_answer.score,
        'total_score': game_session[0].score
    }

    db_sess.close()
    return jsonify(response), 200
