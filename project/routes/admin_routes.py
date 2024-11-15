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
                           admins_count=admins_count)

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

@admin_bp.route('/lesson_types', methods=['GET', 'POST'])
@login_required
def manage_lesson_types():
    form = LessonTypeForm()
    if form.validate_on_submit():
        new_lesson_type = LessonType(name=form.name.data)
        db.session.add(new_lesson_type)
        db.session.commit()
        flash('Lesson type added successfully.')
        return redirect(url_for('admin.manage_lesson_types'))
    lesson_types = LessonType.query.order_by('name').all()
    return render_template('admin/lesson_types.html', form=form, lesson_types=lesson_types)

@admin_bp.route('/cities', methods=['GET', 'POST'])
@login_required
def manage_cities():
    form = CityForm()
    if form.validate_on_submit():
        new_city = City(name=form.name.data)
        db.session.add(new_city)
        db.session.commit()
        flash('City added successfully.')
        return redirect(url_for('admin.manage_cities'))
    cities = City.query.order_by('name').all()
    return render_template('admin/cities.html', form=form, cities=cities)

@admin_bp.route('/locations', methods=['GET', 'POST'])
@login_required
def manage_locations():
    form = LocationForm()
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
    return render_template('admin/locations.html', form=form, locations=locations)

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