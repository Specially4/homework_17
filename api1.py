from flask import Blueprint
from flask_restx import Api

from apis.movie_ns import api as movies_ns
from apis.director_ns import directors_ns
from apis.genre_ns import genres_ns

blueprint = Blueprint('api', __name__)
api = Api(blueprint)

api.add_namespace(movies_ns)
api.add_namespace(directors_ns)
api.add_namespace(genres_ns)
