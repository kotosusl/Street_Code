from flask import Blueprint, jsonify, request
from data.db_session import create_session
from data.game import Game
from sqlalchemy import select

blueprint_get_quests_filters = Blueprint('blueprint_get_quests_filters', __name__)


@blueprint_get_quests_filters.route('/api/get_quests', methods=['GET'])
def get_quests_filters():
    args = request.args
    name = args.get('name', 0)
    location = args.get('location', 0)
    difficulty = args.get('difficulty', 0)
    duration = args.get('duration', 0)
    mode = args.get('mode', 0)
    genre = args.get('genre', 0)
    db_sess = create_session()
    all_quests = select(Game).select_from(Game)
    # TODO: фильтры

