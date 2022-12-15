from flask_restx import Resource, Namespace

from models import GenreSchema, Genre
from setup_db import db


genre_ns = Namespace('genres')

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        genres = db.session.query(Genre)
        return genres_schema.dump(genres), 200

@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    def get(self, gid:int):
        try:
            genre = Genre.query.get(gid)
            return genre_schema.dump(genre), 200

        except Exception as e:
            return str(e), 404
