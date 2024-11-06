from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..models import db, Offering, Booking, Session, Client
from ..forms import BookingForm  # You'll need to create this form

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

@client_bp.route('/offerings')
def view_offerings():
    offerings = Offering.query.filter_by(status='available').all()
    return render_template('client/offerings.html', offerings=offerings)

@client_bp.route('/book/<int:session_id>', methods=['GET', 'POST'])
def book_session(session_id):
    form = BookingForm()
    session = Session.query.get_or_404(session_id)
    if form.validate_on_submit():
        # Check capacity
        if len(session.bookings) >= session.capacity:
            flash('This session is fully booked.')
            return redirect(url_for('client.view_offerings'))

        # Create booking
        client = Client.query.filter_by(user_id=current_user.id).first()
        new_booking = Booking(
            session_id=session.id,
            client_id=client.id,
            status='active'
        )
        db.session.add(new_booking)
        db.session.commit()
        flash('Booking successful.')
        return redirect(url_for('client.dashboard'))
    return render_template('client/book_session.html', form=form, session=session)

# Additional client routes for managing bookings, profiles, etc.
