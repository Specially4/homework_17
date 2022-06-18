# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from logger import new_logger

app = Flask(__name__)

api = Api(app)
movies_ns = api.namespace('movies')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class MovieSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String()
    description = fields.String()
    trailer = fields.String()
    year = fields.Integer()
    rating = fields.Float()
    genre_id = fields.Integer()
    director_id = fields.Integer()


class DirectorSchema(Schema):
    __tablename__ = 'director'
    id = fields.Integer()
    name = fields.String()


class GenreSchema(Schema):
    __tablename__ = 'genre'
    id = fields.Integer()
    name = fields.String()


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@movies_ns.route('/')
class MoviesView(Resource):
    @property
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        if director_id is not None or genre_id is not None:
            if director_id is not None and genre_id is not None:
                try:
                    movies = Movie.query.filter(Movie.director_id == director_id, Movie.genre_id == genre_id)
                    return movies_schema.dump(movies), 200
                except Exception as e:
                    return '', 404
            elif director_id is not None:
                try:
                    movies = Movie.query.filter(Movie.director_id == director_id)
                    return movies_schema.dump(movies), 200
                except Exception as e:
                    return '', 404
            elif genre_id is not None:
                try:
                    movies = Movie.query.filter(Movie.genre_id == genre_id)
                    return movies_schema.dump(movies), 200
                except Exception as e:
                    return '', 404
        movies = Movie.query.limit(10).offset(0).all()
        return movies_schema.dump(movies), 200

    def post(self):
        pass

    def delete(self):
        pass


@movies_ns.route('/<int:mid>/')
class MovieView(Resource):
    def get(self, mid: int):
        try:
            movie = Movie.query.filter(Movie.id == mid).first()
        except Exception as e:
            new_logger.warning(message=e.args)
            return '', 404
        else:
            return movie_schema.dump(movie), 200

    def post(self):
        pass

    def delete(self):
        pass


if __name__ == '__main__':
    app.run(debug=True)
