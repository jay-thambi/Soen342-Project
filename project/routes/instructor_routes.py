from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from ..forms import TakeLessonForm
from ..models import Lesson, Location, Session, db, Instructor

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
    offerings = Lesson.query.filter_by(instructor_id=instructor.id).all()
    return render_template('instructor/dashboard.html', offerings=offerings, instructor=instructor)

@instructor_bp.route('/available_lessons')
@login_required
def available_lessons():
    # Filter lessons matching instructor's specializations and availability
    lessons = Lesson.query.filter(
        Lesson.status == 'pending_instructor',
        Lesson.lesson_type_id.in_([lt.id for lt in current_user.instructor_profile.specializations]),
        Lesson.location.has(Location.city_id.in_([city.id for city in current_user.instructor_profile.availability_cities]))
    ).all()
    # Create a form instance for each lesson
    forms = {lesson.id: TakeLessonForm() for lesson in lessons}
    return render_template('instructor/available_lessons.html', lessons=lessons, forms=forms)

@instructor_bp.route('/take_lesson/<int:lesson_id>', methods=['POST'])
@login_required
def take_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    if lesson.status != 'pending_instructor':
        flash('Lesson is not available.')
        return redirect(url_for('instructor.available_lessons'))

    lesson.instructor_id = current_user.instructor_profile.id
    lesson.status = 'active'
    db.session.commit()
    flash('You have successfully taken on the lesson.')
    return redirect(url_for('instructor.available_lessons'))

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