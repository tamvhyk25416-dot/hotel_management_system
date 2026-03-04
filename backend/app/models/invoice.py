from ..extensions import db
from datetime import datetime

class Invoice(db.Model):
    __tablename__ = "invoices"

    id = db.Column(db.Integer, primary_key=True)

    booking_id = db.Column(
        db.Integer,
        db.ForeignKey("bookings.id"),
        nullable=False,
        unique=True
    )

    room_charge = db.Column(db.Float, nullable=False)
    service_fee = db.Column(db.Float, default=0)
    extra_fee = db.Column(db.Float, default=0)

    total_amount = db.Column(db.Float, nullable=False)

    # unpaid | paid → đổi sang tiếng Việt
    payment_status = db.Column(db.String(20), default="Chưa thanh toán")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    booking = db.relationship("Booking", backref="invoice", uselist=False)

    def __repr__(self):
        return f"<Invoice {self.id}>"