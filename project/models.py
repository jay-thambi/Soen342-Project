from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

#! BOOKING
class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id', on_delete='CASCADE', name='fk_booking_session'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id', name='fk_booking_client'), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 'active', 'cancelled'

    # Relationships
    session = db.relationship('Session', back_populates='bookings')  # many-to-one
    client = db.relationship('Client', backref='bookings')  # many-to-one

    def __repr__(self):
        return f"<Booking for Session {self.session_id} by Client {self.client_id}>"

#! CITY
class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    # Relationships
    locations = db.relationship('Location', backref='city', lazy=True) # many-to-one (Location -> City) because FK is in Location

#! CLIENT
class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # FK to User
    name = db.Column(db.String(120), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    # Relationships
    # bookings = db.relationship('Booking', back_populates='client')

    def __repr__(self):
        return f"<Client {self.name}, DOB: {self.date_of_birth}>"

#! INSTRUCTOR
class Instructor(db.Model):
    __tablename__ = 'instructors'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Relationships
    specializations = db.relationship('LessonType', secondary='instructor_specializations', backref='instructors')  # many-to-many
    availability_cities = db.relationship('City', secondary='instructor_cities', backref='instructors')  # many-to-many
    lessons = db.relationship('Lesson', back_populates='assigned_instructor', lazy=True)  # one-to-many

    def __repr__(self):
        return f"<Instructor {self.user.name}>"

#! LESSON
class Lesson(db.Model):
    __tablename__ = 'lessons'
    id = db.Column(db.Integer, primary_key=True)
    lesson_type_id = db.Column(db.Integer, db.ForeignKey('lesson_types.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    mode = db.Column(db.String(20), nullable=False)  # 'group' or 'private'
    capacity = db.Column(db.Integer, nullable=False, default=1)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    day_of_week = db.Column(db.String(10), nullable=False)  # e.g., 'Sunday'
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='pending_instructor')  # 'pending_instructor', 'active', 'archived'

    # Relationships
    sessions = db.relationship('Session', back_populates='lesson', lazy=True, cascade='all, delete-orphan')
    lesson_type = db.relationship('LessonType', back_populates='lessons', lazy=True)
    location = db.relationship('Location', back_populates='lessons', lazy=True)
    assigned_instructor = db.relationship('Instructor', back_populates='lessons', lazy=True)

    def __repr__(self):
        return f"<Lesson {self.lesson_type.name} at {self.location.name}>"

#! LESSON TYPE
class LessonType(db.Model):
    __tablename__ = 'lesson_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    # Relationships
    lessons = db.relationship('Lesson', back_populates='lesson_type', lazy=True)  # one-to-many

#! LOCATION
class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    # Relationships
    lessons = db.relationship('Lesson', back_populates='location', lazy=True)  # one-to-many

    def __repr__(self):
        city_name = self.city.name if self.city else "Unknown City"
        return f"<Location {self.name} in {city_name}>"

#! SESSION
class Session(db.Model):
    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id', on_delete='CASCADE', name='fk_session_lesson'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    # Relationships
    bookings = db.relationship('Booking', back_populates='session', lazy=True, cascade='all, delete-orphan')
    lesson = db.relationship('Lesson', back_populates='sessions', lazy=True)

#! USER
class User(db.Model, UserMixin):
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