from flask import Flask, request, jsonify
from flask_restx import Api, Resource

from models import Movie, Director, Genre
from schemas import movie_schema, movies_schema, director_schema, directors_schema, genre_schema, genres_schema
from setup_db import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 3}

app.app_context().push()

db.init_app(app)

api = Api(app)
movies_ns = api.namespace('movies')
directors_ns = api.namespace('directors')
genres_ns = api.namespace('genre')


@movies_ns.route('/')
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


@movies_ns.route('/<int:mid>/')
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


@directors_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        directors = Director.query.all()
        return directors_schema.dump(directors), 200

    def post(self):
        data = request.json
        new_directors = Director(**data)
        with db.session.begin():
            db.session.add(new_directors)
        return 'Object appended', 201

    def delete(self):
        pass


@directors_ns.route('/<int:did>/')
class DirectorView(Resource):
    def get(self, did: int):
        director = Director.query.filter(Director.id == did).first()
        if director:
            return director_schema.dump(director), 200
        return 'Object not found', 404

    def path(self, did: int):
        director = Director.query.filter(Director.id == did).first()
        data = request.json
        if director:
            if 'name' in data:
                director.title = data['name']
            db.session.add(director)
            db.session.commit()
            return 'Object updated', 204
        return 'Object not found', 404

    def put(self, did: int):
        director = Director.query.filter(Director.id == did).first()
        data = request.json
        if director:
            director.name = data['name']
            db.session.add(director)
            db.session.commit()
            return 'Object updated', 204
        return 'Object not found', 404

    def delete(self, did: int):
        director = Director.query.filter(Director.id == did).first()
        if director:
            return 'Movie not found', 404
        db.session.delete(director)
        db.session.commit()
        return 'Object deleted', 204


@genres_ns.route('/')
class GenresView(Resource):
    def get(self):
        genres = Genre.query.all()
        return genres_schema.dump(genres), 200

    def post(self):
        data = request.json
        new_genres = Genre(**data)
        with db.session.begin():
            db.session.add(new_genres)
        return 'Object appended', 201

    def delete(self):
        pass


@genres_ns.route('/<int:gid>/')
class GenreView(Resource):
    def get(self, gid: int):
        genre = Genre.query.filter(Genre.id == gid).first()
        if genre:
            return genre_schema.dump(genre), 200
        return 'Object not found', 404

    def path(self, gid: int):
        genre = Genre.query.filter(Genre.id == gid).first()
        data = request.json
        if genre:
            if 'name' in data:
                genre.title = data['name']
            db.session.add(genre)
            db.session.commit()
            return 'Object updated', 204
        return 'Object not found', 404

    def put(self, gid: int):
        genre = Genre.query.filter(Genre.id == gid).first()
        data = request.json
        if genre:
            genre.name = data['name']
            db.session.add(genre)
            db.session.commit()
            return 'Object updated', 204
        return 'Object not found', 404

    def delete(self, gid: int):
        genre = Genre.query.filter(Genre.id == gid).first()
        if genre:
            return jsonify({'details': 'no such content'}), 404
        db.session.delete(genre)
        db.session.commit()
        return 'Object deleted', 204


if __name__ == '__main__':
    app.run(debug=True)
