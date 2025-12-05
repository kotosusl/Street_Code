from flask import Blueprint, request, jsonify
from sqlalchemy import select

from data.game import Game
from data.account import Account
from data.locations import Locations
from data.db_session import create_session
from data.genres import Genres

blueprint_get_one_game = Blueprint('blueprint_get_one_game', __name__)


@blueprint_get_one_game.route('/api/get_one_game', methods=['POST'])
def get_one_game():
    jsn = request.get_json() or {}
    if not jsn:
        return jsonify({
            'error': 'Отсутствует тело запроса'
        }), 400

    if not jsn.get('game_id', 0):
        return jsonify({
            'error': 'Не указан id игры'
        }), 400

    db_sess = create_session()
    game = db_sess.execute(select(Game).select_from(Game).where(Game.id == jsn['game_id'])).first()
    if not game:
        db_sess.close()
        return jsonify({
            'error': 'Квест не найден'
        }), 404

    response = {
        'game_id': game[0].id,
        'title': game[0].title,
        'description': game[0].description,
        'organizer': db_sess.execute(
                select(Account).select_from(Account).where(game[0].organizer_id == Account.id)).first()[0].username,
        'avatar': game[0].avatar,
        'location': db_sess.execute(
                select(Locations).select_from(Locations).where(game[0].location == Locations.id)).first()[0].name,
        'difficulty': game[0].difficulty,
        'duration': game[0].duration,
        'max_members': game[0].max_members,
        'genre': db_sess.execute(select(Genres).select_from(Genres).where(game[0].genre == Genres.id)).first()[
            0].name,
        'is_active': game[0].is_active,
        'start_datetime': game[0].start_datetime,
        'end_datetime': game[0].end_datetime
    }
    db_sess.close()
    return jsonify(response), 200
