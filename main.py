from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
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
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()


class DirectorsSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class GenreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)
director_schema = DirectorsSchema()
directors_schema = DirectorsSchema(many=True)
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)

api = Api(app)
movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
gener_ns = api.namespace('genres')


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        all_movies = Movie.query.all()
        return movies_schema.dump(all_movies), 200

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_movie)
            db.session.commit()
        return "", 201


@movie_ns.route('/<int:u_id>')
class MovieView(Resource):
    def get(self, u_id):
        try:
            movie = Movie.query.get(u_id)
            return movie_schema.dump(movie), 200
        except Exception as e:
            return "", 404

    def put(self, u_id):
        movie = Movie.query.get(u_id)
        req_json = request.json
        movie.title = req_json.get("title")
        movie.description = req_json.get("description")
        movie.trailer = req_json.get("trailer")
        movie.year = req_json.get("year")
        movie.rating = req_json.get("rating")
        movie.genre_id = req_json.get("genre_id")
        movie.genre = req_json.get("genre")
        movie.director_id = req_json.get("director_id")
        movie.director = req_json.get("director")

        db.session.add(movie)
        db.session.commit()
        return "", 204

    def delete(self, u_id: int):
        movie = Movie.query.get(u_id)
        db.session.delete(movie)
        db.session.commit()
        return "", 204


@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        all_directors = Director.query.all()
        return directors_schema.dump(all_directors), 200


@director_ns.route('/<int:u_id>')
class DirectorView(Resource):
    def get(self, u_id):
        try:
            director = Director.query.get(u_id)
            return director_schema.dump(director), 200
        except Exception as e:
            return "", 404


@gener_ns.route('/')
class GenresView(Resource):
    def get(self):
        all_genrs = Genre.query.all()
        return genres_schema.dump(all_genrs), 200


@gener_ns.route('/<int:u_id>')
class GenreView(Resource):
    def get(self, u_id):
        try:
            gener = Genre.query.get(u_id)
            return director_schema.dump(gener), 200
        except Exception as e:
            return "", 404


if __name__ == '__main__':
    app.run(debug=True)

