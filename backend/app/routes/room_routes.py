from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models.room import Room
from sqlalchemy.exc import SQLAlchemyError

room_bp = Blueprint("room_bp", __name__)

VALID_ROOM_STATUS = ["Trống", "Đang ở", "Đang dọn", "Bảo trì"]


# =========================
# CREATE ROOM
# =========================
@room_bp.route("/rooms", methods=["POST"])
def create_room():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Không có dữ liệu gửi lên"}), 400

        required_fields = ["room_number", "room_type", "price"]

        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Thiếu trường {field}"}), 400

        if not isinstance(data["price"], (int, float)):
            return jsonify({"error": "Giá phòng phải là số"}), 400

        if data["price"] <= 0:
            return jsonify({"error": "Giá phòng phải lớn hơn 0"}), 400

        existing_room = Room.query.filter_by(
            room_number=data["room_number"]
        ).first()

        if existing_room:
            return jsonify({"error": "Số phòng đã tồn tại"}), 400

        status = data.get("status", "Trống")

        if status not in VALID_ROOM_STATUS:
            return jsonify({"error": "Trạng thái phòng không hợp lệ"}), 400

        new_room = Room(
            room_number=data["room_number"],
            room_type=data["room_type"],
            price=data["price"],
            status=status
        )

        db.session.add(new_room)
        db.session.commit()

        return jsonify({"message": "Tạo phòng thành công"}), 201

    except (ValueError, SQLAlchemyError) as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


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
            "price": float(room.price),
            "status": room.status
        })

    return jsonify(result), 200


# =========================
# GET ROOM BY ID
# =========================
@room_bp.route("/rooms/<int:id>", methods=["GET"])
def get_room(id):
    room = Room.query.get(id)

    if not room:
        return jsonify({"error": "Không tìm thấy phòng"}), 404

    return jsonify({
        "id": room.id,
        "room_number": room.room_number,
        "room_type": room.room_type,
        "price": float(room.price),
        "status": room.status
    }), 200


# =========================
# UPDATE ROOM
# =========================
@room_bp.route("/rooms/<int:id>", methods=["PUT"])
def update_room(id):
    try:
        room = Room.query.get(id)

        if not room:
            return jsonify({"error": "Không tìm thấy phòng"}), 404

        data = request.get_json()

        if not data:
            return jsonify({"error": "Không có dữ liệu gửi lên"}), 400

        if "price" in data:
            if not isinstance(data["price"], (int, float)):
                return jsonify({"error": "Giá phòng phải là số"}), 400
            if data["price"] <= 0:
                return jsonify({"error": "Giá phòng phải lớn hơn 0"}), 400

        if "status" in data:
            if data["status"] not in VALID_ROOM_STATUS:
                return jsonify({"error": "Trạng thái phòng không hợp lệ"}), 400

        if "room_number" in data:
            existing_room = Room.query.filter_by(
                room_number=data["room_number"]
            ).first()

            if existing_room and existing_room.id != room.id:
                return jsonify({"error": "Số phòng đã tồn tại"}), 400

        room.room_number = data.get("room_number", room.room_number)
        room.room_type = data.get("room_type", room.room_type)
        room.price = data.get("price", room.price)
        room.status = data.get("status", room.status)

        db.session.commit()

        return jsonify({"message": "Cập nhật phòng thành công"}), 200

    except (ValueError, SQLAlchemyError) as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


# =========================
# DELETE ROOM
# =========================
@room_bp.route("/rooms/<int:id>", methods=["DELETE"])
def delete_room(id):
    room = Room.query.get(id)

    if not room:
        return jsonify({"error": "Không tìm thấy phòng"}), 404

    # Không cho xóa nếu đang có khách
    if room.status == "Đang ở":
        return jsonify({
            "error": "Không thể xóa phòng đang có khách"
        }), 400

    db.session.delete(room)
    db.session.commit()

    return jsonify({"message": "Xóa phòng thành công"}), 200