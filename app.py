from flask import Flask
from flask_restx import Api

from config import Config
from setup_db import db
from views.directors import director_ns
from views.genres import genre_ns
from views.movies import movies_ns


def create_app(config: Config):
    application = Flask(__name__)
    application.config.from_object(config)
    register_extensions(application)
    return application


def register_extensions(app):
    db.init_app(app)
    api = Api(app)
    api.add_namespace(movies_ns)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    # create_data(app, db)


# def create_data(app, db):
#     with app.app_context():
#         db.create_all()
#
#         with db.session.begin():
#             db.session.add_all()


app = create_app(Config())
app.debug = True

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)
