from flask import Flask

from check_player_answer import blueprint_check_player_answer
from data import db_session
from flask_sqlalchemy import SQLAlchemy

from get_one_game import blueprint_get_one_game
from get_quests_filters import blueprint_get_quests_filters
from post_registration import blueprint_post_registration
from start_game import blueprint_start_game

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/street_code_database.db'
db = SQLAlchemy(app)
app.register_blueprint(blueprint_get_quests_filters)
app.register_blueprint(blueprint_post_registration)
app.register_blueprint(blueprint_check_player_answer)
app.register_blueprint(blueprint_start_game)
app.register_blueprint(blueprint_get_one_game)


@app.route("/")
def hello_world():
    return "Привет, мир!"


if __name__ == "__main__":
    db_session.global_init('instance/street_code_database.db')
    db_session = db_session.create_session()
    db_session.commit()
    app.run(host='127.0.0.1', port=8080)