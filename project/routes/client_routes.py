from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..models import Lesson, db, Booking, Session, Client
from ..forms import BookingForm, DependentForm

client_bp = Blueprint('client', __name__)

@client_bp.before_request
@login_required
def require_client():
    if current_user.role != 'client':
        flash('You do not have access to this page.')
        return redirect(url_for('auth.login'))

@client_bp.route('/dashboard')
def dashboard():
    client_profiles = Client.query.filter_by(user_id=current_user.id).all()
    if not client_profiles:
        flash('No client profiles found.')
        return redirect(url_for('auth.login'))
    bookings = []
    for client in client_profiles:
        bookings.extend(Booking.query.filter_by(client_id=client.id).all())
    return render_template('client/dashboard.html', bookings=bookings, clients=client_profiles)

@client_bp.route('/lessons')
@login_required
def view_lessons():
    lessons = Lesson.query.filter_by(status='active').all()
    return render_template('client/lessons.html', lessons=lessons)

@client_bp.route('/book_lesson/<int:lesson_id>', methods=['GET', 'POST'])
@login_required
def book_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    form = BookingForm()
    if form.validate_on_submit():
        new_booking = Booking(
            lesson_id=lesson.id,
            client_id=current_user.client_profile.id,
            status='active'
        )
        db.session.add(new_booking)
        db.session.commit()
        flash('You have successfully booked the lesson.')
        return redirect(url_for('client.view_lessons'))
    return render_template('client/book_lesson.html', form=form, lesson=lesson)

# @client_bp.route('/offerings')
# def view_offerings():
#     offerings = Offering.query.filter_by(status='available').all()
#     return render_template('client/offerings.html', offerings=offerings)

# @client_bp.route('/book/<int:offering_id>', methods=['GET', 'POST'])
# def book_offering(offering_id):
#     offering = Offering.query.get_or_404(offering_id)
#     client = Client.query.filter_by(user_id=current_user.id).first()
#     # Check if already booked
#     existing_booking = Booking.query.filter_by(client_id=client.id, offering_id=offering.id).first()
#     if existing_booking:
#         flash('You have already booked this offering.')
#         return redirect(url_for('client.dashboard'))
#     # Create booking
#     new_booking = Booking(
#         client_id=client.id,
#         offering_id=offering.id,
#         status='active'
#     )
#     db.session.add(new_booking)
#     db.session.commit()
#     flash('Booking successful.')
#     return redirect(url_for('client.dashboard'))

@client_bp.route('/book/<int:session_id>', methods=['GET', 'POST'])
def book_session(session_id):
    form = BookingForm()
    session = Session.query.get_or_404(session_id)
    if form.validate_on_submit():
        # Check capacity
        if len(session.bookings) >= session.capacity:
            flash('This session is fully booked.')
            return redirect(url_for('client.view_offerings'))

        # Select client profile (if multiple exist)
        client_id = form.client_id.data
        new_booking = Booking(
            session_id=session.id,
            client_id=client_id,
            status='active'
        )
        db.session.add(new_booking)
        db.session.commit()
        flash('Booking successful.')
        return redirect(url_for('client.dashboard'))
    else:
        # Populate client choices
        client_profiles = Client.query.filter_by(user_id=current_user.id).all()
        form.client_id.choices = [(client.id, client.name) for client in client_profiles]
    return render_template('client/book_session.html', form=form, session=session)

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
