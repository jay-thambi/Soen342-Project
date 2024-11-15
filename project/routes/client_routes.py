from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..models import Lesson, db, Booking, Session, Client
from ..forms import BookingForm, DependentForm
from flask_wtf.csrf import generate_csrf

client_bp = Blueprint('client', __name__)

@client_bp.before_request
@login_required
def require_client():
    if current_user.role != 'client':
        flash('You do not have access to this page.')
        return redirect(url_for('auth.login'))

@client_bp.route('/dashboard')
@login_required
def dashboard():
    csrf_token = generate_csrf() 
    client_profiles = Client.query.filter_by(user_id=current_user.id).all()
    if not client_profiles:
        flash('No client profiles found.')
        return redirect(url_for('auth.login'))
    bookings = []
    for client in client_profiles:
        client_bookings = Booking.query.filter_by(client_id=client.id).all()
        bookings.extend(client_bookings)
    return render_template('client/dashboard.html', bookings=bookings, clients=client_profiles, csrf_token=csrf_token)

@client_bp.route('/book_lesson/<int:lesson_id>', methods=['GET', 'POST'])
@login_required
def book_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    form = BookingForm()
    if form.validate_on_submit():
        new_booking = Booking(
            lesson_id=lesson.id,
            client_id=current_user.id,
            status='active'
        )
        db.session.add(new_booking)
        db.session.commit()
        flash('You have successfully booked the lesson.')
        return redirect(url_for('client.view_lessons'))
    return render_template('client/book_lesson.html', form=form, lesson=lesson)

@client_bp.route('/book/<int:session_id>', methods=['GET', 'POST'])
@login_required
def book_session(session_id):
    session_obj = Session.query.get_or_404(session_id)
    form = BookingForm()

    # Fetch client profiles and populate choices
    client_profiles = Client.query.filter_by(user_id=current_user.id).all()
    form.client_id.choices = [(client.id, client.name) for client in client_profiles]

    if form.validate_on_submit():
        # Check capacity
        if len(session_obj.bookings) >= session_obj.capacity:
            flash('This session is fully booked.')
            return redirect(url_for('client.view_sessions', lesson_id=session_obj.lesson_id))

        # Check if the selected client profile exists
        client_id = form.client_id.data
        if client_id not in [client.id for client in client_profiles]:
            flash('Invalid client selected.')
            return redirect(url_for('client.view_sessions', lesson_id=session_obj.lesson_id))

        # Create the booking
        new_booking = Booking(
            session_id=session_obj.id,
            client_id=client_id,
            status='active'
        )
        db.session.add(new_booking)
        db.session.commit()
        flash('Booking successful.')
        return redirect(url_for('client.dashboard'))
    return render_template('client/book_session.html', form=form, session=session_obj)

@client_bp.route('/delete_booking/<int:booking_id>', methods=['POST'])
@login_required
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)

    # Ensure the booking belongs to the current user
    client_ids = [client.id for client in Client.query.filter_by(user_id=current_user.id).all()]
    if booking.client_id not in client_ids:
        flash('You do not have permission to delete this booking.')
        return redirect(url_for('client.dashboard'))

    db.session.delete(booking)
    db.session.commit()
    flash('Your booking has been cancelled.')
    return redirect(url_for('client.dashboard'))

@client_bp.route('/lessons')
@login_required
def view_lessons():
    lessons = Lesson.query.filter_by(status='active').all()
    return render_template('client/lessons.html', lessons=lessons)

@client_bp.route('/lessons/<int:lesson_id>/sessions')
@login_required
def view_sessions(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    sessions = Session.query.filter_by(lesson_id=lesson_id).order_by('date').all()
    return render_template('client/sessions.html', lesson=lesson, sessions=sessions)

@client_bp.route('/add_dependent', methods=['GET', 'POST'])
def add_dependent():
    form = DependentForm()
    if form.validate_on_submit():
        # Create new client profile for the dependent
        dependent = Client(
            user_id=current_user.id,
            name=form.name.data,
            date_of_birth=form.date_of_birth.data
        )
        db.session.add(dependent)
        db.session.commit()
        flash('Dependent added successfully.')
        return redirect(url_for('client.dashboard'))
    return render_template('client/add_dependent.html', form=form)