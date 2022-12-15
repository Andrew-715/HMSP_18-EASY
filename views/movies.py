# здесь контроллеры/хендлеры/представления для обработки запросов (flask ручки). сюда импортируются сервисы из пакета service

# Пример
# from flask_restx import Resource, Namespace
#
# book_ns = Namespace('books')
#
#
# @book_ns.route('/')
# class BooksView(Resource):
#     def get(self):
#         return "", 200
#
#     def post(self):
#         return "", 201
from flask_restx import Resource, Namespace
from flask import request

from models import Movie, MovieSchema
from setup_db import db

movies_ns = Namespace('movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

@movies_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director = request.args.get('director_id')
        genre = request.args.get('genre_id')
        year = request.args.get('year')

        if director is not None:
            movies = Movie.query.filter(Movie.director_id == director)
            return movies_schema.dump(movies), 200
        elif genre is not None:
            movies = Movie.query.filter(Movie.genre_id == genre)
            return movies_schema.dump(movies), 200
        elif year is not None:
            movies = Movie.query.filter(Movie.year == year)
            return movies_schema.dump(movies), 200
        else:
            movies = db.session.query(Movie).all()
            return movies_schema.dump(movies), 200

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)
        db.session.add(new_movie)
        return 'Movie added', 201

@movies_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid:int):
        try:
            movie = Movie.query.get(mid)
            return movie_schema.dump(movie), 200

        except Exception as e:
            return str(e), 404

    def put(self, mid:int):
        movie = Movie.query.get(mid)
        req_json = request.json

        movie.title = req_json.get('title')
        movie.description = req_json.get('description')
        movie.trailer = req_json.get('trailer')
        movie.year = req_json.get('year')
        movie.rating = req_json.get('rating')
        movie.genre_id = req_json.get('genre_id')
        movie.director_id = req_json.get('director_id')

        db.session.add(movie)
        db.session.commit()
        return 'Movie updated', 204

    def delete(self, mid:int):
        movie = Movie.query.get(mid)
        db.session.delete(movie)
        db.session.commit()
        return 'Movie deleted', 204

