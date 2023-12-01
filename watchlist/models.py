from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from watchlist import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class MovieInfo(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.String(10), unique=True, nullable=False, primary_key=True)
    movie_name = db.Column(db.String(20), nullable=False)
    release_date = db.Column(db.DateTime)
    country = db.Column(db.String(20))
    type = db.Column(db.String(10))
    year = db.Column(db.Integer, nullable=False)


class MovieBox(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.String(10), db.ForeignKey('movie_info.movie_id'), unique=True, nullable=False, primary_key=True)
    box = db.Column(db.Float)


class ActorInfo(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.String(10), unique=True, nullable=False, primary_key=True)
    actor_name = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(2), nullable=False)
    country = db.Column(db.String(20))


class MovieActorRelation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.String(10), db.ForeignKey('movie_info.movie_id'), nullable=False)
    actor_id = db.Column(db.String(10), db.ForeignKey('actor_info.actor_id'), nullable=False)
    relation_type = db.Column(db.String(20))
