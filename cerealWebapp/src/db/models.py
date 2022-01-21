from ... import db
from flask_login import UserMixin

class User(UserMixin,db.Model):
    __tablename__ = 'cerealuser'
    id = db.Column(db.Integer,primary_key=True)
    pwd = db.Column(db.String(128))
    name = db.Column(db.String(20))

class CerealPicture(db.Model):
    __tablename__ = 'cerealpictures'
    id = db.Column(db.Integer,primary_key=True)
    cerealid = db.Column(db.Integer,db.ForeignKey('cereal.id', ondelete='CASCADE'))
    picturepath = db.Column(db.String(50))

class Cereal(db.Model):
    __tablename__ = 'cereal'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    mfr = db.Column(db.String(50))
    type = db.Column(db.String(50))
    calories = db.Column(db.Integer)
    protein = db.Column(db.Integer)
    fat = db.Column(db.Integer)
    sodium = db.Column(db.Integer)
    fiber = db.Column(db.Float)
    carbo = db.Column(db.Float)
    sugars = db.Column(db.Integer)
    potass = db.Column(db.Integer)
    vitamins = db.Column(db.Integer)
    shelf = db.Column(db.Integer)
    weight = db.Column(db.Float)
    cups = db.Column(db.Float)
    rating = db.Column(db.Integer)
    child = db.relationship(CerealPicture,backref="parent",passive_deletes=True)





