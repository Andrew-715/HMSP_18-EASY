from flask_restx import Resource, Namespace

from models import DirectorSchema, Director
from setup_db import db


director_ns = Namespace('directors')

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        directors = db.session.query(Director)
        return directors_schema.dump(directors), 200

@director_ns.route('/<int:did>')
class DirectorView(Resource):
    def get(self, did:int):
        try:
            director = Director.query.get(did)
            return director_schema.dump(director), 200

        except Exception as e:
            return str(e), 404
