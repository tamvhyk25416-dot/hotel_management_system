from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models.invoice import Invoice
from ..models.booking import Booking
from ..models.room import Room

invoice_bp = Blueprint("invoice_bp", __name__)

# =========================
# CREATE INVOICE
# =========================
@invoice_bp.route("/invoices/<int:booking_id>", methods=["POST"])
def create_invoice(booking_id):
    booking = Booking.query.get(booking_id)

    if not booking:
        return jsonify({"error": "Không tìm thấy booking"}), 404

    if booking.status != "Đã check-in":
        return jsonify({"error": "Chỉ tạo hóa đơn khi khách đang lưu trú"}), 400

    days = (booking.check_out - booking.check_in).days
    room_price = float(booking.room.price)

    room_charge = days * room_price

    data = request.get_json()
    service_fee = float(data.get("service_fee", 0))
    extra_fee = float(data.get("extra_fee", 0))

    total_amount = room_charge + service_fee + extra_fee

    invoice = Invoice(
        booking_id=booking.id,
        room_charge=room_charge,
        service_fee=service_fee,
        extra_fee=extra_fee,
        total_amount=total_amount
    )

    db.session.add(invoice)
    db.session.commit()

    return jsonify({
        "message": "Tạo hóa đơn thành công",
        "total_amount": total_amount
    })
@invoice_bp.route("/invoices/<int:id>/pay", methods=["PUT"])
def pay_invoice(id):
    invoice = Invoice.query.get(id)

    if not invoice:
        return jsonify({"error": "Không tìm thấy hóa đơn"}), 404

    booking = Booking.query.get(invoice.booking_id)
    room = Room.query.get(booking.room_id)

    invoice.payment_status = "Đã thanh toán"
    booking.status = "Đã check-out"
    room.status = "Đang dọn"

    db.session.commit()

    return jsonify({"message": "Thanh toán thành công"})