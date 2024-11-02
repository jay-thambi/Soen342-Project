class Offering(db.Model):
    __tablename__ = 'offerings'

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    time_slot = db.Column(db.String(50), nullable=False)
    specialization = db.Column(db.String(50), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'), nullable=True)
    bookings = db.relationship('Booking', backref='offering', lazy=True)

    def __repr__(self):
        return f"<Offering {self.specialization} at {self.location}>"
