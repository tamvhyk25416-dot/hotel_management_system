from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models.booking import Booking
from datetime import datetime

booking_bp = Blueprint("booking_bp", __name__)

@booking_bp.route("/bookings", methods=["POST"])
def create_booking():
    data = request.get_json()

    # Kiểm tra format ngày
    try:
        check_in_date = datetime.strptime(data["check_in"], "%Y-%m-%d")
        check_out_date = datetime.strptime(data["check_out"], "%Y-%m-%d")
    except:
        return jsonify({"error": "Date must be YYYY-MM-DD"}), 400

    new_booking = Booking(
        check_in=check_in_date,
        check_out=check_out_date,
        room_id=data["room_id"],
        customer_id=data["customer_id"],
        status="Confirmed"
    )

    db.session.add(new_booking)
    db.session.commit()

    return jsonify({
        "message": "Booking created successfully",
        "booking_id": new_booking.id
    }), 201