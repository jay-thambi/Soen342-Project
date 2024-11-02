from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Instructor(db.Model):
    __tablename__ = 'instructors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=True)  # Optional email field
    phone_number = db.Column(db.String(10), nullable=False)
    specialization = db.Column(db.String(50), nullable=False)
    available_cities = db.Column(db.String(100), nullable=False)  # Comma-separated cities
    offerings = db.relationship('Offering', backref='instructor', lazy=True)

    def __repr__(self):
        return f"<Instructor {self.name}, Specialization: {self.specialization}>"
