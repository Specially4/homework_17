from flask import request
from flask_restx import Namespace, Resource

from setup_db import db
from models import Director
from schemas import director_schema, directors_schema

directors_ns = Namespace('directors')


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


@directors_ns.route('/<int:did>')
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
