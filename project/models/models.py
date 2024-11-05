from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

#! ADMIN
# class Admin(db.Model):
#     __tablename__ = 'admins'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password = db.Column(db.String(100), nullable=False)

#     def __repr__(self):
#         return f"<Admin {self.name}, Email: {self.email}>"

#! BOOKING
class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 'active', 'cancelled'

    def __repr__(self):
        return f"<Booking for Offering {self.session_id} by Client {self.client_id}>"

#! CITY
class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    # Relationships
    locations = db.relationship('Location', backref='city', lazy=True)

#! CLIENT
class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # FK to User
    date_of_birth = db.Column(db.Date, nullable=False)
    # Relationships
    bookings = db.relationship('Booking', backref='client', lazy=True) # one-to-many

    def __repr__(self):
        return f"<Client {self.name}, DOB: {self.date_of_birth}>"

#! INSTRUCTOR
class Instructor(db.Model):
    __tablename__ = 'instructors'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Relationships
    specializations = db.relationship('LessonType', secondary='instructor_specializations', backref='instructors') # many-to-many
    availability_cities = db.relationship('City', secondary='instructor_cities', backref='instructors') # many-to-many
    offerings = db.relationship('Offering', backref='instructor', lazy=True) # one-to-many

    # specialization = db.Column(db.String(50), nullable=False)
    # available_cities = db.Column(db.String(100), nullable=False)
    # password = db.Column(db.String(100), nullable=False) 
    # offerings = db.relationship('Offering', backref='instructor', lazy=True)

    def __repr__(self):
        return f"<Instructor {self.user.name}>"

#! LESSON TYPE
class LessonType(db.Model):
    __tablename__ = 'lesson_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

#! LOCATION
class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    # Relationships
    offerings = db.relationship('Offering', backref='location', lazy=True) # one-to-many

    def __repr__(self):
        city_name = self.city.name if self.city else "Unknown City"
        return f"<Location {self.name} in {city_name}>"

#! OFFERING
class Offering(db.Model):
    __tablename__ = 'offerings'
    id = db.Column(db.Integer, primary_key=True)
    lesson_type_id = db.Column(db.Integer, db.ForeignKey('lesson_types.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    mode = db.Column(db.String(20), nullable=False)  # 'group' or 'private'
    capacity = db.Column(db.Integer, nullable=False, default=1)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'), nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    day_of_week = db.Column(db.String(10), nullable=False)  # e.g., 'Sunday'
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 'pending_instructor', 'available', 'closed'
    # Relationships
    sessions = db.relationship('Session', backref='offering', lazy=True)

    def __repr__(self):
        # Check if the location exists to avoid errors in representation
        lesson_type_name = self.lesson_type.name if self.lesson_type else "Unknown Lesson Type"
        location_name = self.location.name if self.location else "Unknown Location"
        return f"<Offering {lesson_type_name} at {location_name}>"

#! SESSION
class Session(db.Model):
    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True)
    offering_id = db.Column(db.Integer, db.ForeignKey('offerings.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    # Relationships
    bookings = db.relationship('Booking', backref='session', lazy=True)

#! USER
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin', 'client', 'instructor'
    phone_number = db.Column(db.String(20), nullable=False)
    # Relationships
    clients = db.relationship('Client', backref='user', lazy=True)
    instructor_profile = db.relationship('Instructor', uselist=False, backref='user', lazy=True)

#! ASSOCIATION TABLES
instructor_specializations = db.Table('instructor_specializations',
    db.Column('instructor_id', db.Integer, db.ForeignKey('instructors.id'), primary_key=True),
    db.Column('lesson_type_id', db.Integer, db.ForeignKey('lesson_types.id'), primary_key=True)
)

instructor_cities = db.Table('instructor_cities',
    db.Column('instructor_id', db.Integer, db.ForeignKey('instructors.id'), primary_key=True),
    db.Column('city_id', db.Integer, db.ForeignKey('cities.id'), primary_key=True)
)