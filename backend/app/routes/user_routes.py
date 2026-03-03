from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models.user import User

user_bp = Blueprint("user_bp", __name__)
# =========================
# CREATE USER
# =========================
@user_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    # Kiểm tra username đã tồn tại chưa
    existing_user = User.query.filter_by(username=data["username"]).first()
    if existing_user:
        return jsonify({"error": "Username already exists"}), 400

    new_user = User(
        username=data["username"],
        password=data["password"],
        role=data["role"]
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

# =========================
# GET ALL USERS
# =========================
@user_bp.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()

    return jsonify([
        {
            "id": user.id,
            "username": user.username,
            "role": user.role
        }
        for user in users
    ])
# =========================
# GET USER BY ID
# =========================
@user_bp.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get_or_404(id)

    return jsonify({
        "id": user.id,
        "username": user.username,
        "role": user.role
    })


# =========================
# UPDATE USER
# =========================
@user_bp.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()

    user.username = data.get("username", user.username)
    user.password = data.get("password", user.password)
    user.role = data.get("role", user.role)

    db.session.commit()

    return jsonify({"message": "User updated successfully"})


# =========================
# DELETE USER
# =========================
@user_bp.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get_or_404(id)

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"})