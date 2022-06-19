from flask import request
from flask_restx import Namespace, Resource

from setup_db import db
from models import Movie
from schemas import movie_schema, movies_schema

api = Namespace('movies')


@api.route('/')
class MoviesView(Resource):
    def get(self):
        movies = Movie.query.limit(10).offset(0).all()
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        if director_id and genre_id:
            movies = Movie.query.filter(Movie.director_id == director_id, Movie.genre_id == genre_id)
        elif director_id:
            movies = Movie.query.filter(Movie.director_id == director_id)
        elif genre_id:
            movies = Movie.query.filter(Movie.genre_id == genre_id)
        all_movies = movies
        return movies_schema.dump(all_movies), 200

    def post(self):
        data = request.json
        new_movie = Movie(**data)
        with db.session.begin():
            db.session.add(new_movie)
        return 'Movie appended', 201

    def delete(self):
        pass


@api.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid: int):
        movie = Movie.query.filter(Movie.id == mid).first()
        if movie:
            return movie_schema.dump(movie), 200
        return 'Movie not found', 404

    def path(self, mid: int):
        movie = Movie.query.filter(Movie.id == mid).first()
        data = request.json
        if movie:
            if 'title' in data:
                movie.title = data['title']
            if 'description' in data:
                movie.description = data['description']
            if 'trailer' in data:
                movie.trailer = data['trailer']
            if 'year' in data:
                movie.year = data['year']
            if 'rating' in data:
                movie.rating = data['rating']
            if 'genre_id' in data:
                movie.genre_id = data['genre_id']
            if 'director_id' in data:
                movie.director_id = data['director_id']
            db.session.add(movie)
            db.session.commit()
            return 'Movie updated', 204
        return 'Movie not found', 404

    def put(self, mid: int):
        movie = Movie.query.filter(Movie.id == mid).first()
        data = request.json
        if movie:
            movie.title = data['title']
            movie.description = data['description']
            movie.trailer = data['trailer']
            movie.year = data['year']
            movie.rating = data['rating']
            movie.genre_id = data['genre_id']
            movie.director_id = data['director_id']
            db.session.add(movie)
            db.session.commit()
            return 'Movie updated', 204
        return 'Movie not found', 404

    def delete(self, mid: int):
        movie = Movie.query.filter(Movie.id == mid).first()
        if movie:
            return 'Movie not found', 404
        db.session.delete(movie)
        db.session.commit()
        return 'Movie deleted', 204
