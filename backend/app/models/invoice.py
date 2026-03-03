from ..extensions import db
from datetime import datetime

class Invoice(db.Model):
    __tablename__ = "invoices"

    id = db.Column(db.Integer, primary_key=True)

    booking_id = db.Column(
        db.Integer,
        db.ForeignKey("bookings.id"),
        nullable=False
    )

    room_charge = db.Column(db.Float, nullable=False)
    service_fee = db.Column(db.Float, default=0)
    extra_fee = db.Column(db.Float, default=0)
    total_amount = db.Column(db.Float, nullable=False)

    payment_status = db.Column(db.String(50), default="unpaid")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    booking = db.relationship("Booking", backref="invoice", uselist=False)