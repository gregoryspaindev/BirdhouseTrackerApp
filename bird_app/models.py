from flask_login import UserMixin
from bird_app import db


# describe the birdhouse Schema
class Birdhouse(db.Model):
    birdhouse_id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100), unique=True)
    repair_flag = db.Column(db.Boolean)
    cowbird_flag = db.Column(db.Boolean)


# describe the user Schema
class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))

    # override the get_id function of the UserMixin since the id isn't just 'id'
    def get_id(self):
        return self.user_id


# describe the species Schema
class Species(db.Model):
    species_id = db.Column(db.Integer, primary_key=True)
    species_name = db.Column(db.String(100), unique=True)


# describe the visit Schema
class Visit(db.Model):
    visit_id = db.Column(db.Integer, primary_key=True)
    visit_date = db.Column(db.Date)
    birdhouse_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    species_id = db.Column(db.Integer)
    species_eggs_amount = db.Column(db.Integer)
    species_live_young_amount = db.Column(db.Integer)
    species_dead_young_amount = db.Column(db.Integer)
    cowbird_eggs_amount = db.Column(db.Integer)
    cowbird_live_young_amount = db.Column(db.Integer)
    cowbird_dead_young_amount = db.Column(db.Integer)
    needs_repair = db.Column(db.Boolean)
    comments = db.Column(db.Text(5000))
    
    