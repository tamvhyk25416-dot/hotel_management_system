from ..extensions import db
from datetime import datetime
from sqlalchemy import Enum
from sqlalchemy.orm import validates


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customers.id"),
        nullable=False
    )

    room_id = db.Column(
        db.Integer,
        db.ForeignKey("rooms.id"),
        nullable=False
    )

    check_in = db.Column(db.Date, nullable=False)
    check_out = db.Column(db.Date, nullable=False)

    # Trạng thái theo SRS
    status = db.Column(
        Enum(
            "Chờ xác nhận",
            "Chờ check-in",
            "Đã check-in",
            "Đã check-out",
            "Đã hủy",
            name="booking_status"
        ),
        nullable=False,
        default="Chờ xác nhận"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # =========================
    # Validation
    # =========================

    @validates("check_out")
    def validate_dates(self, key, value):
        if self.check_in and value <= self.check_in:
            raise ValueError("Ngày check-out phải sau ngày check-in")
        return value

    def __repr__(self):
        return f"<Booking {self.id}>"