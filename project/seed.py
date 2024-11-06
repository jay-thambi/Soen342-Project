from app import app
from models import db, LessonType

def seed_lesson_types():
    lesson_types = ['Swimming', 'Yoga', 'Karate', 'Dance', 'Art', 'Music']

    with app.app_context():
        for lt_name in lesson_types:
            existing_lt = LessonType.query.filter_by(name=lt_name).first()
            if not existing_lt:
                new_lt = LessonType(name=lt_name)
                db.session.add(new_lt)
        db.session.commit()
        print("Lesson types seeded successfully.")

if __name__ == '__main__':
    seed_lesson_types()
