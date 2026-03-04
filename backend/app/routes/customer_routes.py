from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models.customer import Customer
from sqlalchemy.exc import SQLAlchemyError

customer_bp = Blueprint("customer_bp", __name__)


# =========================
# CREATE CUSTOMER
# =========================
@customer_bp.route("/customers", methods=["POST"])
def create_customer():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Không có dữ liệu gửi lên"}), 400

        required_fields = ["full_name", "phone"]

        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Thiếu trường {field}"}), 400

        # Kiểm tra trùng số điện thoại
        existing_customer = Customer.query.filter_by(
            phone=data["phone"]
        ).first()

        if existing_customer:
            return jsonify({"error": "Số điện thoại đã tồn tại"}), 400

        new_customer = Customer(
            full_name=data["full_name"],
            phone=data["phone"],
            email=data.get("email")
        )

        db.session.add(new_customer)
        db.session.commit()

        return jsonify({"message": "Tạo khách hàng thành công"}), 201

    except (ValueError, SQLAlchemyError) as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


# =========================
# GET ALL CUSTOMERS
# =========================
@customer_bp.route("/customers", methods=["GET"])
def get_customers():
    customers = Customer.query.all()

    result = []
    for customer in customers:
        result.append({
            "id": customer.id,
            "full_name": customer.full_name,
            "phone": customer.phone,
            "email": customer.email
        })

    return jsonify(result), 200


# =========================
# GET CUSTOMER BY ID
# =========================
@customer_bp.route("/customers/<int:id>", methods=["GET"])
def get_customer(id):
    customer = Customer.query.get(id)

    if not customer:
        return jsonify({"error": "Không tìm thấy khách hàng"}), 404

    return jsonify({
        "id": customer.id,
        "full_name": customer.full_name,
        "phone": customer.phone,
        "email": customer.email
    }), 200


# =========================
# UPDATE CUSTOMER
# =========================
@customer_bp.route("/customers/<int:id>", methods=["PUT"])
def update_customer(id):
    try:
        customer = Customer.query.get(id)

        if not customer:
            return jsonify({"error": "Không tìm thấy khách hàng"}), 404

        data = request.get_json()

        if not data:
            return jsonify({"error": "Không có dữ liệu gửi lên"}), 400

        # Kiểm tra trùng số điện thoại nếu cập nhật
        if "phone" in data:
            existing_customer = Customer.query.filter_by(
                phone=data["phone"]
            ).first()

            if existing_customer and existing_customer.id != customer.id:
                return jsonify({"error": "Số điện thoại đã tồn tại"}), 400

        customer.full_name = data.get("full_name", customer.full_name)
        customer.phone = data.get("phone", customer.phone)
        customer.email = data.get("email", customer.email)

        db.session.commit()

        return jsonify({"message": "Cập nhật khách hàng thành công"}), 200

    except (ValueError, SQLAlchemyError) as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


# =========================
# DELETE CUSTOMER
# =========================
@customer_bp.route("/customers/<int:id>", methods=["DELETE"])
def delete_customer(id):
    customer = Customer.query.get(id)

    if not customer:
        return jsonify({"error": "Không tìm thấy khách hàng"}), 404

    # Không cho xóa nếu đã có booking
    if customer.bookings:
        return jsonify({
            "error": "Không thể xóa khách hàng đã có booking"
        }), 400

    db.session.delete(customer)
    db.session.commit()

    return jsonify({"message": "Xóa khách hàng thành công"}), 200


# =========================
# SEARCH CUSTOMER (FR15)
# =========================
@customer_bp.route("/customers/search", methods=["GET"])
def search_customer():
    keyword = request.args.get("q")

    if not keyword:
        return jsonify({"error": "Thiếu từ khóa tìm kiếm"}), 400

    customers = Customer.query.filter(
        (Customer.full_name.ilike(f"%{keyword}%")) |
        (Customer.phone.ilike(f"%{keyword}%"))
    ).all()

    result = []
    for customer in customers:
        result.append({
            "id": customer.id,
            "full_name": customer.full_name,
            "phone": customer.phone,
            "email": customer.email
        })

    return jsonify(result), 200