from models.models import db, Client, Instructor, Admin, Offering, Booking, Location
from app import app

# Create the database tables within the application context
with app.app_context():
    db.create_all()
    print("All tables have been created successfully.")
