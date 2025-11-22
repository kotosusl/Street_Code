from flask import Blueprint, request, jsonify
from sqlalchemy import select
from data.db_session import create_session
from data.game import Game
from data.registration import Registration
from data.team import Team
from uuid import uuid4

blueprint_post_registration = Blueprint('blueprint_post_registration', __name__)


@blueprint_post_registration.route('/api/post_registration', methods=['POST'])
def post_registration():
    jsn = request.get_json() or {}
    if not jsn:
        return jsonify({
            'error': 'Отсутствует тело запроса'
        }), 400

    if not (jsn.get('game_name', 0) and jsn.get('team_name', 0)):
        return jsonify({
            'error': 'Не хватает данных для добавления регистрации'
        }), 400

    db_sess = create_session()
    game = db_sess.execute(select(Game).select_from(Game).where(Game.title == jsn['game_name'])).first()
    team = db_sess.execute(select(Team).select_from(Team).where(Team.name == jsn['team_name'])).first()

    if not game:
        db_sess.close()
        return jsonify({
            'error': 'Квест не найден'
        }), 404

    if not team:
        db_sess.close()
        return jsonify({
            'error': 'Команда не найдена'
        }), 404

    game_registration = db_sess.execute(select(Registration).select_from(Registration).where(
        (Registration.game_id == game[0].id) & (Registration.team_id == team[0].id))).first()
    if game_registration and game_registration[0].status == 'active':
        db_sess.close()
        return jsonify({
            'error': 'Команда уже зарегистрирована'
        }), 304

    if game_registration:
        game_registration[0].status = 'active'
        db_sess.commit()
        db_sess.close()
        return jsonify({'status': 'OK'}), 200

    new_registration = Registration(
        id=str(uuid4()),
        game_id=game[0].id,
        team_id=team[0].id,
        status="active"
    )

    db_sess.add(new_registration)
    db_sess.commit()
    db_sess.close()
    return jsonify({'status': 'OK'}), 200


