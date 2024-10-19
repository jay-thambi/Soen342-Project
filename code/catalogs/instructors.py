from models.models import db, Instructor

def create_instructor(name, specialization):
    new_instructor = Instructor(name=name, specialization=specialization)
    db.session.add(new_instructor)
    db.session.commit()
    return new_instructor

def get_instructor_by_id(instructor_id):
    return Instructor.query.get(instructor_id)

def get_all_instructors():
    return Instructor.query.all()

def delete_instructor(instructor_id):
    instructor = Instructor.query.get(instructor_id)
    if instructor:
        db.session.delete(instructor)
        db.session.commit()
