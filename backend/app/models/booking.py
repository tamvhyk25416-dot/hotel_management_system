from ..extensions import db
from datetime import datetime

class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)

    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"), nullable=False)

    check_in = db.Column(db.Date, nullable=False)
    check_out = db.Column(db.Date, nullable=False)

    status = db.Column(db.String(50), default="Pending")  # Pending, Confirmed, Checked-in, Checked-out, Cancelled

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Booking {self.id}>"