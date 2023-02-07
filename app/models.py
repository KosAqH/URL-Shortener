from app import db

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique = True)
    original_link = db.Column(db.String(1000))
    hash = db.Column(db.String(100), unique=True)