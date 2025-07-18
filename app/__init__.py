import os
import json
from flask import Flask, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
from pydantic import ValidationError

db = None

def create_app():
    global db
    app = Flask(__name__)

    # Initialize Firebase using environment variable
    firebase_json = os.getenv("FIREBASE_CONFIG")
    if not firebase_json:
        raise RuntimeError("FIREBASE_CONFIG environment variable is missing")

    try:
        firebase_creds = json.loads(firebase_json)
    except json.JSONDecodeError:
        raise RuntimeError("Invalid JSON in FIREBASE_CONFIG")

    cred = credentials.Certificate(firebase_creds)
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    # Register Blueprints
    from app.controllers.user_controller import user_bp
    from app.controllers.jobs_controller import job_bp
    from app.controllers.tags_controller import tags_bp
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(job_bp, url_prefix='/api/jobs')
    app.register_blueprint(tags_bp, url_prefix='/api/tags')

    # Custom Pydantic validation error handler
    @app.errorhandler(ValidationError)
    def handle_pydantic_validation_error(e):
        simplified_errors = [
            {
                "field": ".".join(str(loc) for loc in err["loc"]),
                "message": err["msg"]
            }
            for err in e.errors()
        ]
        return jsonify(simplified_errors), 422

    return app
