from datetime import date
from flask_wtf import FlaskForm
from wtforms import RadioField, SelectMultipleField, StringField, PasswordField, SubmitField, SelectField, DateField, TimeField, IntegerField
from wtforms.validators import DataRequired, Email, Length, Optional

from .models import City, LessonType, Location

#! AUTH FORMS
class RegistrationForm(FlaskForm):
    # Common Fields
    role = RadioField('Role', choices=[('client', 'Client'), ('instructor', 'Instructor'), ('admin', 'Administrator')], validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired(), Length(1, 120)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 100)])
    # password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])

    # Client-Specific Fields
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d', validators=[Optional()])

    # Instructor-Specific Fields
    specializations = SelectMultipleField('Specializations', coerce=int, validators=[Optional()])
    availability_cities = SelectMultipleField('Available Cities', coerce=int, validators=[Optional()])

    submit = SubmitField('Register')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        # Populate choices for specializations and cities
        self.specializations.choices = [(lt.id, lt.name) for lt in LessonType.query.all()]
        self.availability_cities.choices = [(city.id, city.name) for city in City.query.all()]

    def validate(self, **kwargs):
        rv = super(RegistrationForm, self).validate(**kwargs)
        if not rv:
            return False

        # Conditional validation based on role
        if self.role.data == 'client':
            if not self.date_of_birth.data:
                self.date_of_birth.errors.append('Date of Birth is required for clients.')
                return False
            else:
                # Check that the client is over 18
                today = date.today()
                dob = self.date_of_birth.data
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                if age < 18:
                    self.date_of_birth.errors.append('You must be at least 18 years old to register as a client.')
                    return False

        elif self.role.data == 'instructor':
            if not self.specializations.data:
                self.specializations.errors.append('At least one specialization is required.')
                return False
            if not self.availability_cities.data:
                self.availability_cities.errors.append('At least one available city is required.')
                return False
        elif self.role.data == 'admin':
            pass
        else:
            self.role.errors.append('Invalid role selected.')
            return False

        return True

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

#! CLIENT FORMS
class BookingForm(FlaskForm):
    client_id = SelectField('Select Client', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Book Session')

class DependentForm(FlaskForm):
    name = StringField('Dependent Name', validators=[DataRequired(), Length(1, 120)])
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Add Dependent')

#! INSTUCTOR FORMS
class TakeLessonForm(FlaskForm):
    submit = SubmitField('Take on this Lesson')

#! ADMIN FORMS
class LessonTypeForm(FlaskForm):
    name = StringField('Lesson Type Name', validators=[DataRequired(), Length(max=120)])
    submit = SubmitField('Add Lesson Type')

class CityForm(FlaskForm):
    name = StringField('City Name', validators=[DataRequired(), Length(max=120)])
    submit = SubmitField('Add City')

class LocationForm(FlaskForm):
    name = StringField('Location Name', validators=[DataRequired(), Length(max=100)])
    address = StringField('Address', validators=[DataRequired(), Length(max=150)])
    city = SelectField('City', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Location')

    def __init__(self, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        self.city.choices = [(city.id, city.name) for city in City.query.order_by('name').all()]

class LessonForm(FlaskForm):
    lesson_type = SelectField('Lesson Type', coerce=int, validators=[DataRequired()])
    location = SelectField('Location', coerce=int, validators=[DataRequired()])
    mode = SelectField('Mode', choices=[('group', 'Group'), ('private', 'Private')], validators=[DataRequired()])
    capacity = IntegerField('Capacity', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    day_of_week = SelectField('Day of Week', choices=[
        ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')
    ], validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    submit = SubmitField('Create Lesson')

    def __init__(self, *args, **kwargs):
        super(LessonForm, self).__init__(*args, **kwargs)
        self.lesson_type.choices = [(lt.id, lt.name) for lt in LessonType.query.all()]
        self.location.choices = [(loc.id, f"{loc.name} ({loc.city.name})") for loc in Location.query.all()]

