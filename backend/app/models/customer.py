from ..extensions import db

class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))

    bookings = db.relationship("Booking", backref="customer", lazy=True)

    def __repr__(self):
        return f"<Customer {self.full_name}>"
