class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    offerings = db.relationship('Offering', backref='location_detail', lazy=True)

    def __repr__(self):
        return f"<Location {self.name} in {self.city}>"
