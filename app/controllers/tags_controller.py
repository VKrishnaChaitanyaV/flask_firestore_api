from flask import Blueprint, request, jsonify
from app.services import tag_service
from pydantic import ValidationError

tags_bp = Blueprint("tags_bp", __name__)


@tags_bp.route("/", methods=["GET"])
def list_tagss():
    tags = tag_service.get_all_tags()
    return jsonify(tags)
