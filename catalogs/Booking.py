from models.models import db, Booking

# --- Booking Management Functions ---

def create_booking(client_id, offering_id, booking_date=None):
    """Creates a new booking for a client for a specific offering."""
    new_booking = Booking(
        client_id=client_id,
        offering_id=offering_id,
        booking_date=booking_date
    )
    db.session.add(new_booking)
    db.session.commit()
    return new_booking

def get_booking_by_id(booking_id):
    """Retrieves a booking by its ID."""
    return Booking.query.get(booking_id)

def get_bookings_by_client(client_id):
    """Retrieves all bookings made by a specific client."""
    return Booking.query.filter_by(client_id=client_id).all()

def get_bookings_by_offering(offering_id):
    """Retrieves all bookings for a specific offering."""
    return Booking.query.filter_by(offering_id=offering_id).all()

def delete_booking(booking_id):
    """Deletes a booking by its ID."""
    booking = Booking.query.get(booking_id)
    if booking:
        db.session.delete(booking)
        db.session.commit()
