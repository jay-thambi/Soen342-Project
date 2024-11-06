# from Soen342-Project directory -> python -m project.seed
from project.app import app
from project.models import City, db, LessonType

def seed_lesson_types():
    # Seed Cities
    with app.app_context():
        cities = ['Montreal', 'Toronto', 'Vancouver']
        for city_name in cities:
            if not City.query.filter_by(name=city_name).first():
                db.session.add(City(name=city_name))

        lesson_types = ['Swimming', 'Yoga', 'Karate', 'Dance', 'Art', 'Music']
        for lt_name in lesson_types:
            existing_lt = LessonType.query.filter_by(name=lt_name).first()
            if not existing_lt:
                new_lt = LessonType(name=lt_name)
                db.session.add(new_lt)
        db.session.commit()
        print("Db seeded successfully.")

if __name__ == '__main__':
    seed_lesson_types()
