from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import User, db, Offering, LessonType, Location, City
from ..forms import LessonTypeForm, OfferingForm  # You'll need to create this form

admin_bp = Blueprint('admin', __name__)

@admin_bp.before_request
@login_required
def require_admin():
    if current_user.role != 'admin':
        flash('You do not have access to this page.')
        return redirect(url_for('auth.login'))

@admin_bp.route('/dashboard')
def dashboard():
    offerings = Offering.query.all()
    users = User.query.all()
    return render_template('admin/dashboard.html', offerings=offerings, users=users)

@admin_bp.route('/create_lesson', methods=['GET', 'POST'])
def create_lesson():
    form = LessonForm()
    if form.validate_on_submit():
        new_lesson = Lesson(
            lesson_type_id=form.lesson_type.data,
            description=form.description.data,
            status='pending_instructor'
        )
        db.session.add(new_lesson)
        db.session.commit()
        flash('Lesson created successfully.')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/create_lesson.html', form=form)

@admin_bp.route('/create_offering', methods=['GET', 'POST'])
def create_offering():
    form = OfferingForm()
    if form.validate_on_submit():
        # Create new offering
        new_offering = Offering(
            lesson_type_id=form.lesson_type.data,
            location_id=form.location.data,
            mode=form.mode.data,
            capacity=form.capacity.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            day_of_week=form.day_of_week.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            status='pending_instructor'
        )
        db.session.add(new_offering)
        db.session.commit()
        flash('Offering created successfully.')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/create_offering.html', form=form)

@admin_bp.route('/lesson_types', methods=['GET', 'POST'])
def manage_lesson_types():
    form = LessonTypeForm()
    if form.validate_on_submit():
        new_lt = LessonType(name=form.name.data)
        db.session.add(new_lt)
        db.session.commit()
        flash('Lesson type added.')
        return redirect(url_for('admin.manage_lesson_types'))
    lesson_types = LessonType.query.all()
    return render_template('admin/lesson_types.html', form=form, lesson_types=lesson_types)

