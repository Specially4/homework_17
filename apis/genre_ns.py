from flask import request
from flask_restx import Namespace, Resource

from setup_db import db
from models import Genre
from schemas import genre_schema, genres_schema

genres_ns = Namespace('genres')


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


@genres_ns.route('/<int:gid>')
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
            return 'Object not found', 404
        db.session.delete(genre)
        db.session.commit()
        return 'Object deleted', 204
