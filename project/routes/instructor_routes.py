from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import Session, db, Offering, Instructor
# from project.forms import AcceptOfferingForm  # You'll need to create this form

instructor_bp = Blueprint('instructor', __name__)

@instructor_bp.before_request
@login_required
def require_instructor():
    if current_user.role != 'instructor':
        flash('You do not have access to this page.')
        return redirect(url_for('auth.login'))

@instructor_bp.route('/dashboard')
def dashboard():
    instructor = Instructor.query.filter_by(user_id=current_user.id).first()
    if not instructor:
        flash('Instructor profile not found.')
        return redirect(url_for('auth.login'))
    offerings = Offering.query.filter_by(instructor_id=instructor.id).all()
    return render_template('instructor/dashboard.html', offerings=offerings)

@instructor_bp.route('/available_offerings')
def available_offerings():
    instructor = Instructor.query.filter_by(user_id=current_user.id).first()
    # Get offerings matching instructor's specializations and cities
    matching_offerings = Offering.query.filter(
        Offering.status == 'pending_instructor',
        Offering.lesson_type_id.in_([lt.id for lt in instructor.specializations]),
        Offering.location.has(city_id.in_([city.id for city in instructor.availability_cities]))
    ).all()
    return render_template('instructor/available_offerings.html', offerings=matching_offerings)

@instructor_bp.route('/accept_offering/<int:offering_id>', methods=['POST'])
def accept_offering(offering_id):
    offering = Offering.query.get_or_404(offering_id)
    instructor = Instructor.query.filter_by(user_id=current_user.id).first()
    # Assign offering to instructor
    offering.instructor_id = instructor.id
    offering.status = 'available'
    db.session.commit()
    # Generate sessions
    generate_sessions(offering)
    flash('Offering accepted and sessions generated.')
    return redirect(url_for('instructor.dashboard'))

def generate_sessions(offering):
    # Logic to generate sessions based on offering details
    from datetime import timedelta
    import datetime

    day_of_week = offering.day_of_week  # e.g., 'Sunday'
    current_date = offering.start_date
    end_date = offering.end_date
    while current_date <= end_date:
        if current_date.strftime('%A') == day_of_week:
            new_session = Session(
                offering_id=offering.id,
                date=current_date,
                start_time=offering.start_time,
                end_time=offering.end_time,
                capacity=offering.capacity
            )
            db.session.add(new_session)
        current_date += timedelta(days=1)
    db.session.commit()

# Additional instructor routes for managing profiles, offerings, etc.
