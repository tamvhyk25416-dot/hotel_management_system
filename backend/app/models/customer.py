from ..extensions import db
from sqlalchemy.orm import validates
import re


class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(
        db.String(150),
        nullable=False
    )

    phone = db.Column(
        db.String(20),
        nullable=False,
        unique=True
    )

    email = db.Column(
        db.String(100),
        nullable=True
    )

    # 1 Customer -> nhiều Bookings
    bookings = db.relationship(
        "Booking",
        backref="customer",
        lazy=True,
        cascade="all, delete"
    )

    # =========================
    # Validation
    # =========================

    @validates("full_name")
    def validate_name(self, key, value):
        if not value or value.strip() == "":
            raise ValueError("Tên khách hàng không được để trống")
        return value.strip()

    @validates("phone")
    def validate_phone(self, key, value):
        if not value:
            raise ValueError("Số điện thoại không được để trống")

        # Regex đơn giản cho số điện thoại VN
        pattern = r"^(0|\+84)[0-9]{8,10}$"
        if not re.match(pattern, value):
            raise ValueError("Số điện thoại không hợp lệ")

        return value

    def __repr__(self):
        return f"<Customer {self.full_name}>"