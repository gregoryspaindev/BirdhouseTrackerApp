from flask_login import UserMixin
from bird_app import db


class Birdhouse(db.Model):
    birdhouse_id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100), unique=True)
    repair_flag = db.Column(db.Boolean)


class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))


    def get_id(self):
        return self.user_id

