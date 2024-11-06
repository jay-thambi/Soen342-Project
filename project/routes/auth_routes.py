from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from ..models import db, User, Client, Instructor
from ..forms import ClientRegistrationForm, LoginForm, InstructorRegistrationForm, RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash

from ..models import City, LessonType

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if user already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered.')
            return redirect(url_for('auth.register'))

        # Create new user
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            password=hashed_password,
            phone_number=form.phone_number.data,
            role=form.role.data
        )
        db.session.add(new_user)
        db.session.commit()

        if form.role.data == 'client':
            # Create client profile
            client_profile = Client(
                user_id=new_user.id,
                name=form.name.data,  # Use the name provided
                date_of_birth=form.date_of_birth.data
            )
            db.session.add(client_profile)
            db.session.commit()
        elif form.role.data == 'instructor':
            # Create instructor profile
            instructor_profile = Instructor(user_id=new_user.id)
            db.session.add(instructor_profile)
            db.session.commit()

            # Add specializations and availability cities
            selected_specializations = form.specializations.data
            selected_cities = form.availability_cities.data

            for lt_id in selected_specializations:
                lesson_type = LessonType.query.get(lt_id)
                instructor_profile.specializations.append(lesson_type)

            for city_id in selected_cities:
                city = City.query.get(city_id)
                instructor_profile.availability_cities.append(city)

            db.session.commit()

        flash('Registration successful. Please log in.')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)

# @auth_bp.route('/register/client', methods=['GET', 'POST'])
# def register_client():
#     form = ClientRegistrationForm()
#     if form.validate_on_submit():
#         # Check if user already exists
#         existing_user = User.query.filter_by(email=form.email.data).first()
#         if existing_user:
#             flash('Email already registered.')
#             return redirect(url_for('auth.register_client'))

#         # Create new user
#         hashed_password = generate_password_hash(form.password.data)
#         new_user = User(
#             name=form.name.data,
#             email=form.email.data,
#             password=hashed_password,
#             phone_number=form.phone_number.data,
#             role='client'
#         )
#         db.session.add(new_user)
#         db.session.commit()

#         # Create client profile
#         client_profile = Client(
#             user_id=new_user.id,
#             date_of_birth=form.date_of_birth.data
#         )
#         db.session.add(client_profile)
#         db.session.commit()

#         flash('Registration successful. Please log in.')
#         return redirect(url_for('auth.login'))

#     return render_template('register_client.html', form=form)

# @auth_bp.route('/register/instructor', methods=['GET', 'POST'])
# def register_instructor():
#     form = InstructorRegistrationForm()
#     if form.validate_on_submit():
#         # Check if user already exists
#         existing_user = User.query.filter_by(email=form.email.data).first()
#         if existing_user:
#             flash('Email already registered.')
#             return redirect(url_for('auth.register_instructor'))

#         # Create new user
#         hashed_password = generate_password_hash(form.password.data)
#         new_user = User(
#             name=form.name.data,
#             email=form.email.data,
#             password=hashed_password,
#             phone_number=form.phone_number.data,
#             role='instructor'
#         )
#         db.session.add(new_user)
#         db.session.commit()

#         # Create instructor profile
#         instructor_profile = Instructor(user_id=new_user.id)
#         db.session.add(instructor_profile)
#         db.session.commit()

#         # Add specializations and availability cities
#         selected_specializations = form.specializations.data
#         selected_cities = form.availability_cities.data

#         for lt_id in selected_specializations:
#             lesson_type = LessonType.query.get(lt_id)
#             instructor_profile.specializations.append(lesson_type)

#         for city_id in selected_cities:
#             city = City.query.get(city_id)
#             instructor_profile.availability_cities.append(city)

#         db.session.commit()

#         flash('Registration successful. Please log in.')
#         return redirect(url_for('auth.login'))

#     return render_template('register_instructor.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Authenticate user
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully.')
            # Redirect based on role
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif user.role == 'client':
                return redirect(url_for('client.dashboard'))
            elif user.role == 'instructor':
                return redirect(url_for('instructor.dashboard'))
        else:
            flash('Invalid email or password.')
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('auth.login'))
