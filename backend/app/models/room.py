from ..extensions import db
from sqlalchemy import Enum
from sqlalchemy.orm import validates


class Room(db.Model):
    __tablename__ = "rooms"

    id = db.Column(db.Integer, primary_key=True)

    room_number = db.Column(
        db.String(10),
        unique=True,
        nullable=False
    )

    room_type = db.Column(
        db.String(50),
        nullable=False
    )

    # Giá tiền phòng
    price = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    # Trạng thái theo SRS:
    # Trống | Đang ở | Đang dọn | Bảo trì
    status = db.Column(
        Enum("Trống", "Đang ở", "Đang dọn", "Bảo trì", name="room_status"),
        nullable=False,
        default="Trống"
    )

    # Quan hệ 1 Room -> nhiều Bookings
    bookings = db.relationship(
        "Booking",
        backref="room",
        lazy=True,
        cascade="all, delete"
    )

    # =========================
    # Validation
    # =========================

    @validates("price")
    def validate_price(self, key, value):
        if value <= 0:
            raise ValueError("Giá phòng phải lớn hơn 0")
        return value

    def __repr__(self):
        return f"<Room {self.room_number}>"