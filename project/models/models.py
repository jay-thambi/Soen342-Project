from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    bookings = db.relationship('Booking', backref='client', lazy=True)

    def __repr__(self):
        return f"<Client {self.name}, Email: {self.email}>"

class Instructor(db.Model):
    __tablename__ = 'instructors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)  # Added email field
    phone_number = db.Column(db.String(10), nullable=False)
    specialization = db.Column(db.String(50), nullable=False)
    available_cities = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False) 
    offerings = db.relationship('Offering', backref='instructor', lazy=True)

    def __repr__(self):
        return f"<Instructor {self.name}, Email: {self.email}, Specialization: {self.specialization}>"

class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Admin {self.name}, Email: {self.email}>"

class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    offerings = db.relationship('Offering', backref='location', lazy=True)

    def __repr__(self):
        return f"<Location {self.name} in {self.city}>"

class Offering(db.Model):
    __tablename__ = 'offerings'
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    time_slot = db.Column(db.String(50), nullable=False)
    specialization = db.Column(db.String(50), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'), nullable=True)
    bookings = db.relationship('Booking', backref='offering', lazy=True)

    def __repr__(self):
        # Check if the location exists to avoid errors in representation
        location_name = self.location.name if self.location else "Unknown Location"
        return f"<Offering {self.specialization} at {location_name}>"

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    offering_id = db.Column(db.Integer, db.ForeignKey('offerings.id'), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Booking for Offering {self.offering_id} by Client {self.client_id}>"
