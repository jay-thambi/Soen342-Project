from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Instructor(db.Model):
    __tablename__ = 'instructors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)
    specialization = db.Column(db.String(50), nullable=False)
    available_cities = db.Column(db.String(100), nullable=False)  # Stores comma-separated cities
    offerings = db.relationship('Offering', backref='instructor', lazy=True)

    def __repr__(self):
        return f"<Instructor {self.name}>"

class Offering(db.Model):
    __tablename__ = 'offerings'
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    time_slot = db.Column(db.String(50), nullable=False)
    specialization = db.Column(db.String(50), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'), nullable=True)

    def __repr__(self):
        return f"<Offering {self.specialization} at {self.location}>"
