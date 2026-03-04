from flask import Blueprint, request, jsonify, session
from ..extensions import db
from ..models.user import User

user_bp = Blueprint("user_bp", __name__)

# ========================================
# HELPER: CHECK LOGIN
# ========================================

def is_logged_in():
    return "user_id" in session


def is_admin():
    return session.get("role") == "Admin"


# ========================================
# FR1 – LOGIN
# ========================================

@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if not user or user.password != password:
        return jsonify({"message": "Sai tài khoản hoặc mật khẩu"}), 401

    if not user.is_active:
        return jsonify({"message": "Tài khoản đã bị vô hiệu hóa"}), 403

    session["user_id"] = user.id
    session["role"] = user.role

    return jsonify({
        "message": "Đăng nhập thành công",
        "role": user.role
    })


# ========================================
# FR3 – LOGOUT
# ========================================

@user_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Đăng xuất thành công"})


# ========================================
# FR4 – ADMIN TẠO TÀI KHOẢN LỄ TÂN
# ========================================

@user_bp.route("/users", methods=["POST"])
def create_user():
    if not is_logged_in() or not is_admin():
        return jsonify({"message": "Không có quyền truy cập"}), 403

    data = request.get_json()

    new_user = User(
        username=data["username"],
        password=data["password"],
        role=data["role"],  # Admin hoặc Lễ tân
        is_active=True
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Tạo tài khoản thành công"}), 201


# ========================================
# ADMIN XEM DANH SÁCH USER
# ========================================

@user_bp.route("/users", methods=["GET"])
def get_users():
    if not is_logged_in() or not is_admin():
        return jsonify({"message": "Không có quyền truy cập"}), 403

    users = User.query.all()

    result = []
    for user in users:
        result.append({
            "id": user.id,
            "username": user.username,
            "role": user.role,
            "is_active": user.is_active
        })

    return jsonify(result)


# ========================================
# ADMIN CẬP NHẬT USER
# ========================================

@user_bp.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    if not is_logged_in() or not is_admin():
        return jsonify({"message": "Không có quyền truy cập"}), 403

    user = User.query.get_or_404(id)
    data = request.get_json()

    user.username = data.get("username", user.username)
    user.password = data.get("password", user.password)
    user.role = data.get("role", user.role)

    db.session.commit()

    return jsonify({"message": "Cập nhật thành công"})


# ========================================
# FR4 – VÔ HIỆU HÓA TÀI KHOẢN (KHÔNG XÓA CỨNG)
# ========================================

@user_bp.route("/users/<int:id>", methods=["DELETE"])
def disable_user(id):
    if not is_logged_in() or not is_admin():
        return jsonify({"message": "Không có quyền truy cập"}), 403

    user = User.query.get_or_404(id)

    user.is_active = False
    db.session.commit()

    return jsonify({"message": "Tài khoản đã bị vô hiệu hóa"})