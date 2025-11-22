from flask import Blueprint, jsonify, request
from data.db_session import create_session
from data.game import Game
from data.locations import Locations
from data.genres import Genres
from data.account import Account
from sqlalchemy import select

blueprint_get_quests_filters = Blueprint('blueprint_get_quests_filters', __name__)


@blueprint_get_quests_filters.route('/api/get_quests', methods=['GET'])
def get_quests_filters():
    args = request.args
    title = args.get('title', '').lower()
    location = args.get('location', 0)
    difficulty = args.get('difficulty', 0)
    duration = args.get('duration', 0)
    mode = args.get('mode', 0)
    genre = args.get('genre', 0)

    db_sess = create_session()
    all_quests = select(Game).select_from(Game).join(Locations,
                                                     Game.location == Locations.id).join(Genres,
                                                                                         Genres.id == Game.genre)
    if location:
        all_quests = all_quests.where(Locations.name == location)

    if genre:
        all_quests = all_quests.where(Genres.name == genre)

    if difficulty:
        all_quests = all_quests.where(Game.difficulty == difficulty)

    if mode:
        all_quests = all_quests.where(Game.mode == mode)

    if duration:
        all_quests = all_quests.where(Game.duration <= int(duration))

    search_quests = db_sess.execute(all_quests)
    if title:
        title_filter = []
        for i in search_quests:
            if title in i[0].title.lower():
                title_filter.append(i)

        search_quests = title_filter.copy()

    if not search_quests:
        db_sess.close()
        return jsonify({
            'searching_quests': []
        }), 404

    response = {
        'searching_quests': [
            {
                'id': p[0].id,
                'title': p[0].title,
                'description': p[0].description,
                'organizer': db_sess.execute(
                    select(Account).select_from(Account).where(p[0].organizer_id == Account.id)).first()[0].username,
                'avatar': p[0].avatar,
                'location': db_sess.execute(
                    select(Locations).select_from(Locations).where(p[0].location == Locations.id)).first()[0].name,
                'difficulty': p[0].difficulty,
                'duration': p[0].duration,
                'max_members': p[0].max_members,
                'genre': db_sess.execute(select(Genres).select_from(Genres).where(p[0].genre == Genres.id)).first()[
                    0].name,
                'is_active': p[0].is_active,
                'start_datetime': p[0].start_datetime,
                'end_datetime': p[0].end_datetime
            }
            for p in search_quests
        ]
    }

    db_sess.close()
    return jsonify(response), 200
