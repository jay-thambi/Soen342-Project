from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import Booking, Client, Instructor, Lesson, User, db, LessonType, Location, City
from ..forms import CityForm, LessonForm, LessonTypeForm, LocationForm
from flask_wtf.csrf import generate_csrf

admin_bp = Blueprint('admin', __name__)

@admin_bp.before_request
@login_required
def require_admin():
    if current_user.role != 'admin':
        flash('You do not have access to this page.')
        return redirect(url_for('auth.login'))

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    csrf_token = generate_csrf() 
    pending_lessons = Lesson.query.filter_by(status='pending_instructor').order_by('start_date').all()
    active_lessons = Lesson.query.filter_by(status='active').order_by('start_date').all()
    users_count = User.query.count()
    instructors_count = Instructor.query.count()
    clients_count = Client.query.count()
    admins_count = User.query.filter_by(role='admin').count()
    return render_template('admin/dashboard.html',
                           pending_lessons=pending_lessons,
                           active_lessons=active_lessons,
                           users_count=users_count,
                           instructors_count=instructors_count,
                           clients_count=clients_count,
                           admins_count=admins_count,
                           csrf_token=csrf_token)

@admin_bp.route('/create_lesson', methods=['GET', 'POST'])
@login_required
def create_lesson():
    form = LessonForm()
    if form.validate_on_submit():
        new_lesson = Lesson(
            lesson_type_id=form.lesson_type.data,
            location_id=form.location.data,
            mode=form.mode.data,
            capacity=form.capacity.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            day_of_week=form.day_of_week.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            status='pending_instructor'  # Lesson is pending instructor assignment
        )
        db.session.add(new_lesson)
        db.session.commit()
        flash('Lesson created successfully.')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/create_lesson.html', form=form)

@admin_bp.route('/delete_lesson/<int:lesson_id>', methods=['POST'])
@login_required
def delete_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    
    # Delete associated sessions and bookings
    for session in lesson.sessions:
        # Delete bookings for each session
        Booking.query.filter_by(session_id=session.id).delete()
        db.session.delete(session)
    
    db.session.delete(lesson)
    db.session.commit()
    flash('Lesson and associated sessions and bookings deleted successfully.')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/lesson_types', methods=['GET', 'POST'])
@login_required
def manage_lesson_types():
    form = LessonTypeForm()
    csrf_token = generate_csrf() 
    if form.validate_on_submit():
        new_lesson_type = LessonType(name=form.name.data)
        db.session.add(new_lesson_type)
        db.session.commit()
        flash('Lesson type added successfully.')
        return redirect(url_for('admin.manage_lesson_types'))
    lesson_types = LessonType.query.order_by('name').all()
    return render_template('admin/lesson_types.html', form=form, lesson_types=lesson_types, csrf_token=csrf_token)

@admin_bp.route('/delete_lesson_type/<int:lesson_type_id>', methods=['POST'])
@login_required
def delete_lesson_type(lesson_type_id):
    lesson_type = LessonType.query.get_or_404(lesson_type_id)

    # Check for associated lessons
    if lesson_type.lessons:
        flash('Cannot delete lesson type with associated lessons.')
        return redirect(url_for('admin.manage_lesson_types'))

    # Remove associations with instructors
    instructors = lesson_type.instructors
    for instructor in instructors:
        instructor.specializations.remove(lesson_type)

    db.session.delete(lesson_type)
    db.session.commit()
    flash('Lesson type deleted successfully.')
    return redirect(url_for('admin.manage_lesson_types'))

@admin_bp.route('/cities', methods=['GET', 'POST'])
@login_required
def manage_cities():
    form = CityForm()
    csrf_token = generate_csrf() 
    if form.validate_on_submit():
        new_city = City(name=form.name.data)
        db.session.add(new_city)
        db.session.commit()
        flash('City added successfully.')
        return redirect(url_for('admin.manage_cities'))
    cities = City.query.order_by('name').all()
    return render_template('admin/cities.html', form=form, cities=cities, csrf_token=csrf_token)

@admin_bp.route('/delete_city/<int:city_id>', methods=['POST'])
@login_required
def delete_city(city_id):
    city = City.query.get_or_404(city_id)

    # Check for associated locations
    if city.locations:
        flash('Cannot delete city with associated locations.')
        return redirect(url_for('admin.manage_cities'))

    # Remove associations with instructors
    instructors = city.instructors
    for instructor in instructors:
        instructor.availability_cities.remove(city)

    db.session.delete(city)
    db.session.commit()
    flash('City deleted successfully.')
    return redirect(url_for('admin.manage_cities'))

@admin_bp.route('/locations', methods=['GET', 'POST'])
@login_required
def manage_locations():
    form = LocationForm()
    csrf_token = generate_csrf() 
    if form.validate_on_submit():
        new_location = Location(
            name=form.name.data,
            address=form.address.data,
            city_id=form.city.data
        )
        db.session.add(new_location)
        db.session.commit()
        flash('Location added successfully.')
        return redirect(url_for('admin.manage_locations'))
    locations = Location.query.order_by('name').all()
    return render_template('admin/locations.html', form=form, locations=locations, csrf_token=csrf_token)

@admin_bp.route('/delete_location/<int:location_id>', methods=['POST'])
@login_required
def delete_location(location_id):
    location = Location.query.get_or_404(location_id)

    # Check for associated lessons
    if location.lessons:
        flash('Cannot delete location with associated lessons.')
        return redirect(url_for('admin.manage_locations'))

    db.session.delete(location)
    db.session.commit()
    flash('Location deleted successfully.')
    return redirect(url_for('admin.manage_locations'))

@admin_bp.route('/users')
@login_required
def manage_users():
    users = User.query.order_by('name').all()
    csrf_token = generate_csrf() 
    return render_template('admin/users.html', users=users, csrf_token=csrf_token)

@admin_bp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

        # Delete associated Client or Instructor
    if user.role == 'client':
        client = Client.query.filter_by(user_id=user_id).first()
        if client:
            db.session.delete(client)
    elif user.role == 'instructor':
        instructor = Instructor.query.filter_by(user_id=user_id).first()
        if instructor:
            db.session.delete(instructor)

    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully.')
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/bookings')
@login_required
def manage_bookings():
    bookings = Booking.query.order_by(Booking.id.desc()).all()
    csrf_token = generate_csrf() 
    return render_template('admin/bookings.html', bookings=bookings, csrf_token=csrf_token)

@admin_bp.route('/delete_booking/<int:booking_id>', methods=['POST'])
@login_required
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    flash('Booking deleted successfully.')
    return redirect(url_for('admin.manage_bookings'))