from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models.customer import Customer

customer_bp = Blueprint("customer_bp", __name__)

@customer_bp.route("/customers", methods=["POST"])
def create_customer():
    data = request.get_json()

    new_customer = Customer(
        full_name=data["full_name"],
        phone=data["phone"],
        email=data.get("email")
    )

    db.session.add(new_customer)
    db.session.commit()

    return jsonify({
        "message": "Customer created successfully",
        "customer_id": new_customer.id
    }), 201