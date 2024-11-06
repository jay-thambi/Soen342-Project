from models.models import db, Location

# --- Location Management Functions ---

def create_location(name, city, address):
    """Creates a new location."""
    new_location = Location(
        name=name,
        city=city,
        address=address
    )
    db.session.add(new_location)
    db.session.commit()
    return new_location

def get_location_by_id(location_id):
    """Retrieves a location by its ID."""
    return Location.query.get(location_id)

def get_all_locations():
    """Retrieves all locations."""
    return Location.query.all()

def update_location(location_id, name=None, city=None, address=None):
    """Updates a location's details."""
    location = Location.query.get(location_id)
    if location:
        if name:
            location.name = name
        if city:
            location.city = city
        if address:
            location.address = address
        db.session.commit()
        return location
    return None

def delete_location(location_id):
    """Deletes a location by its ID."""
    location = Location.query.get(location_id)
    if location:
        db.session.delete(location)
        db.session.commit()
