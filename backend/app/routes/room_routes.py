from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models.room import Room

room_bp = Blueprint("room_bp", __name__)

# =========================
# CREATE ROOM
# =========================
@room_bp.route("/rooms", methods=["POST"])
def create_room():
    data = request.json

    if not data:
        return jsonify({"error": "No input data provided"}), 400

    required_fields = ["room_number", "room_type", "price"]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    if not isinstance(data["price"], (int, float)):
        return jsonify({"error": "Price must be a number"}), 400

    new_room = Room(
        room_number=data["room_number"],
        room_type=data["room_type"],
        price=data["price"],
        status=data.get("status", "available")
    )

    db.session.add(new_room)
    db.session.commit()

    return jsonify({"message": "Room created successfully"}), 201


# =========================
# GET ALL ROOMS
# =========================
@room_bp.route("/rooms", methods=["GET"])
def get_rooms():
    rooms = Room.query.all()

    result = []
    for room in rooms:
        result.append({
            "id": room.id,
            "room_number": room.room_number,
            "room_type": room.room_type,
            "price": room.price,
            "status": room.status
        })

    return jsonify(result), 200


# =========================
# GET ROOM BY ID
# =========================
@room_bp.route("/rooms/<int:id>", methods=["GET"])
def get_room(id):
    room = Room.query.get_or_404(id)

    return jsonify({
        "id": room.id,
        "room_number": room.room_number,
        "room_type": room.room_type,
        "price": room.price,
        "status": room.status
    }), 200


# =========================
# UPDATE ROOM
# =========================
@room_bp.route("/rooms/<int:id>", methods=["PUT"])
def update_room(id):
    room = Room.query.get_or_404(id)
    data = request.json

    if not data:
        return jsonify({"error": "No input data provided"}), 400

    if "price" in data and not isinstance(data["price"], (int, float)):
        return jsonify({"error": "Price must be a number"}), 400

    room.room_number = data.get("room_number", room.room_number)
    room.room_type = data.get("room_type", room.room_type)
    room.price = data.get("price", room.price)
    room.status = data.get("status", room.status)

    db.session.commit()

    return jsonify({"message": "Room updated successfully"}), 200


# =========================
# DELETE ROOM
# =========================
@room_bp.route("/rooms/<int:id>", methods=["DELETE"])
def delete_room(id):
    room = Room.query.get_or_404(id)

    db.session.delete(room)
    db.session.commit()

    return jsonify({"message": "Room deleted successfully"}), 200