from flask import Blueprint, request, jsonify
from app.services import user_service
from pydantic import ValidationError

user_bp = Blueprint("user_bp", __name__)

@user_bp.route("/", methods=["POST"])
def create_user():
    try:
        data = request.json
        user_service.create_user(data)
        return jsonify({"message": "User created"}), 201
    except ValidationError as e:
        raise e

@user_bp.route("/<userid>", methods=["GET"])
def get_user(userid):
    user = user_service.get_user(userid)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@user_bp.route("/<userid>", methods=["PUT"])
def update_user(userid):
    data = request.json
    result = user_service.update_user(userid, data)
    if result is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User updated"})

@user_bp.route("/<userid>", methods=["DELETE"])
def delete_user(userid):
    user_service.delete_user(userid)
    return jsonify({"message": "User deleted"})

@user_bp.route("/", methods=["GET"])
def list_users():
    phone = request.args.get("phone")
    if phone:
        user = user_service.get_user_by_phone(phone)
        if user:
            return jsonify(user)
        return jsonify({"error": "User not found"}), 404

    users = user_service.list_all_users()
    return jsonify(users)
