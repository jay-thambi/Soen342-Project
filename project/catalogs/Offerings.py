from code.models.models import db, Offering

# --- Offering Management Functions ---

def create_offering(location, time_slot, specialization, instructor_id=None):
    """Creates a new offering with an optional instructor assignment."""
    new_offering = Offering(
        location=location,
        time_slot=time_slot,
        specialization=specialization,
        instructor_id=instructor_id
    )
    db.session.add(new_offering)
    db.session.commit()
    return new_offering

def get_offering_by_id(offering_id):
    """Retrieves an offering by its ID."""
    return Offering.query.get(offering_id)

def get_all_offerings():
    """Retrieves all offerings."""
    return Offering.query.all()

def update_offering(offering_id, location=None, time_slot=None, specialization=None, instructor_id=None):
    """Updates an offering's details."""
    offering = Offering.query.get(offering_id)
    if offering:
        if location:
            offering.location = location
        if time_slot:
            offering.time_slot = time_slot
        if specialization:
            offering.specialization = specialization
        if instructor_id is not None:
            offering.instructor_id = instructor_id
        db.session.commit()
        return offering
    return None

def delete_offering(offering_id):
    """Deletes an offering by its ID."""
    offering = Offering.query.get(offering_id)
    if offering:
        db.session.delete(offering)
        db.session.commit()
