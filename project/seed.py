# from Soen342-Project directory -> python -m project.seed
from project.app import app
from project.models import City, Location, db, LessonType

def seed_lesson_types():
    with app.app_context():
        # Seed Cities
        cities = ['Montreal', 'Toronto', 'Vancouver']
        for city_name in cities:
            city = City.query.filter_by(name=city_name).first()
            if not city:
                city = City(name=city_name)
                db.session.add(city)
                db.session.commit()
            else:
                city = city

            # Seed Locations for each city
            location_name = f"Community Center {city_name}"
            if not Location.query.filter_by(name=location_name).first():
                location = Location(
                    name=location_name,
                    address=f"123 Main St, {city_name}",
                    city_id=city.id
                )
                db.session.add(location)
                db.session.commit()

        # Seed Lesson Types
        lesson_types = ['Swimming', 'Yoga', 'Karate']
        for lt_name in lesson_types:
            if not LessonType.query.filter_by(name=lt_name).first():
                db.session.add(LessonType(name=lt_name))
        db.session.commit()
        print("Database seeded successfully.")

if __name__ == '__main__':
    seed_lesson_types()
