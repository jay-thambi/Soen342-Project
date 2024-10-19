from models.models import db, Offering

def create_offering(location, time_slot, specialization):
    new_offering = Offering(location=location, time_slot=time_slot, specialization=specialization)
    db.session.add(new_offering)
    db.session.commit()
    return new_offering

def get_offering_by_id(offering_id):
    return Offering.query.get(offering_id)

def get_all_offerings():
    return Offering.query.all()

def delete_offering(offering_id):
    offering = Offering.query.get(offering_id)
    if offering:
        db.session.delete(offering)
        db.session.commit()
