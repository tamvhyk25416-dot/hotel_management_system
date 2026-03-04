from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models.booking import Booking
from ..models.room import Room
from ..models.customer import Customer
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

booking_bp = Blueprint("booking_bp", __name__)


# =========================
# CREATE BOOKING
# =========================
@booking_bp.route("/bookings", methods=["POST"])
def create_booking():
    try:
        data = request.get_json()

        room = Room.query.get(data["room_id"])
        if not room:
            return jsonify({"error": "Phòng không tồn tại"}), 404

        customer = Customer.query.get(data["customer_id"])
        if not customer:
            return jsonify({"error": "Khách hàng không tồn tại"}), 404

        check_in_date = datetime.strptime(data["check_in"], "%Y-%m-%d").date()
        check_out_date = datetime.strptime(data["check_out"], "%Y-%m-%d").date()

        if check_out_date <= check_in_date:
            return jsonify({"error": "Check-out phải sau check-in"}), 400

        # NFR-02: Không đặt trùng
        conflict = Booking.query.filter(
            Booking.room_id == data["room_id"],
            Booking.status.in_(["Chờ xác nhận", "Chờ check-in", "Đã check-in"]),
            Booking.check_out > check_in_date,
            Booking.check_in < check_out_date
        ).first()

        if conflict:
            return jsonify({"error": "Phòng đã được đặt trong khoảng thời gian này"}), 400

        new_booking = Booking(
            check_in=check_in_date,
            check_out=check_out_date,
            room_id=data["room_id"],
            customer_id=data["customer_id"]
        )

        db.session.add(new_booking)
        db.session.commit()

        return jsonify({"message": "Tạo booking thành công"}), 201

    except (ValueError, SQLAlchemyError) as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


# =========================
# CONFIRM BOOKING
# =========================
@booking_bp.route("/bookings/<int:id>/confirm", methods=["PUT"])
def confirm_booking(id):
    booking = Booking.query.get(id)
    if not booking:
        return jsonify({"error": "Không tìm thấy booking"}), 404

    if booking.status != "Chờ xác nhận":
        return jsonify({"error": "Booking không hợp lệ để xác nhận"}), 400

    booking.status = "Chờ check-in"
    db.session.commit()

    return jsonify({"message": "Xác nhận thành công"})


# =========================
# CHECK-IN
# =========================
@booking_bp.route("/bookings/<int:id>/checkin", methods=["PUT"])
def check_in(id):
    booking = Booking.query.get(id)
    if not booking:
        return jsonify({"error": "Không tìm thấy booking"}), 404

    if booking.status != "Chờ check-in":
        return jsonify({"error": "Booking chưa sẵn sàng check-in"}), 400

    room = Room.query.get(booking.room_id)

    booking.status = "Đã check-in"
    room.status = "Đang ở"

    db.session.commit()

    return jsonify({"message": "Check-in thành công"})


# =========================
# CHECK-OUT
# =========================
@booking_bp.route("/bookings/<int:id>/checkout", methods=["PUT"])
def check_out(id):
    booking = Booking.query.get(id)
    if not booking:
        return jsonify({"error": "Không tìm thấy booking"}), 404

    if booking.status != "Đã check-in":
        return jsonify({"error": "Chỉ có thể check-out khi đã check-in"}), 400

    room = Room.query.get(booking.room_id)

    booking.status = "Đã check-out"
    room.status = "Đang dọn"

    db.session.commit()

    return jsonify({"message": "Check-out thành công"})


# =========================
# CANCEL BOOKING
# =========================
@booking_bp.route("/bookings/<int:id>/cancel", methods=["PUT"])
def cancel_booking(id):
    booking = Booking.query.get(id)
    if not booking:
        return jsonify({"error": "Không tìm thấy booking"}), 404

    if booking.status in ["Đã check-in", "Đã check-out"]:
        return jsonify({"error": "Không thể hủy booking này"}), 400

    booking.status = "Đã hủy"
    db.session.commit()

    return jsonify({"message": "Hủy booking thành công"})