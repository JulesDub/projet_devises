from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Devise(db.Model):
    __tablename__ = 'devises'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50))
    symbole = db.Column(db.String(10))

class Cours(db.Model):
    __tablename__ = 'cours'
    id = db.Column(db.Integer, primary_key=True)
    devise_id = db.Column(db.Integer, db.ForeignKey('devises.id'))
    valeur = db.Column(db.Numeric)
    date = db.Column(db.Date)
