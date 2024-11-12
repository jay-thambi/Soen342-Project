from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from ..forms import OfferingForm
from ..models import Lesson, Session, db, Offering, Instructor
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

# @instructor_bp.route('/available_offerings')
# def available_offerings():
#     instructor = Instructor.query.filter_by(user_id=current_user.id).first()
#     # Get offerings matching instructor's specializations and cities
#     matching_offerings = Offering.query.filter(
#         Offering.status == 'pending_instructor',
#         Offering.lesson_type_id.in_([lt.id for lt in instructor.specializations]),
#         Offering.location.has(Location.city_id.in_([city.id for city in instructor.availability_cities]))
#     ).all()
#     return render_template('instructor/available_offerings.html', offerings=matching_offerings)

# @instructor_bp.route('/accept_offering/<int:offering_id>', methods=['POST'])
# def accept_offering(offering_id):
#     offering = Offering.query.get_or_404(offering_id)
#     instructor = Instructor.query.filter_by(user_id=current_user.id).first()
#     # Assign offering to instructor
#     offering.instructor_id = instructor.id
#     offering.status = 'available'
#     db.session.commit()
#     # Generate sessions
#     generate_sessions(offering)
#     flash('Offering accepted and sessions generated.')
#     return redirect(url_for('instructor.dashboard'))

@instructor_bp.route('/available_lessons')
def available_lessons():
    instructor = Instructor.query.filter_by(user_id=current_user.id).first()
    # Get lessons matching instructor's specializations
    matching_lessons = Lesson.query.filter(
        Lesson.status == 'pending_instructor',
        Lesson.lesson_type_id.in_([lt.id for lt in instructor.specializations])
    ).all()
    return render_template('instructor/available_lessons.html', lessons=matching_lessons)

@instructor_bp.route('/create_offering/<int:lesson_id>', methods=['GET', 'POST'])
def create_offering(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    form = OfferingForm()
    if form.validate_on_submit():
        instructor = Instructor.query.filter_by(user_id=current_user.id).first()
        new_offering = Offering(
            lesson_id=lesson.id,
            instructor_id=instructor.id,
            location_id=form.location.data,
            mode=form.mode.data,
            capacity=form.capacity.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            day_of_week=form.day_of_week.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            status='active'
        )
        db.session.add(new_offering)
        # Update the lesson status
        lesson.status = 'active'
        db.session.commit()
        # Generate sessions
        generate_sessions(new_offering)
        flash('Offering created successfully.')
        return redirect(url_for('instructor.dashboard'))
    return render_template('instructor/create_offering.html', form=form, lesson=lesson)

def generate_sessions(offering):
    # Logic to generate sessions based on offering details
    from datetime import timedelta

    day_of_week = offering.day_of_week  # e.g., 'Sunday'
    current_date = offering.start_date
    end_date = offering.end_date

    # Map day names to numbers (Monday=0, Sunday=6)
    day_numbers = {
        'Monday': 0, 'Tuesday': 1, 'Wednesday': 2,
        'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6
    }
    target_day = day_numbers[day_of_week]

    # Find the first occurrence of the target day
    while current_date.weekday() != target_day:
        current_date += timedelta(days=1)

    while current_date <= end_date:
        new_session = Session(
            offering_id=offering.id,
            date=current_date,
            start_time=offering.start_time,
            end_time=offering.end_time,
            capacity=offering.capacity
        )
        db.session.add(new_session)
        current_date += timedelta(days=7)  # Move to the next week

    db.session.commit()