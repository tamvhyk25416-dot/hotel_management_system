from flask import Flask
from .config import Config
from .extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from .routes.room_routes import room_bp
    app.register_blueprint(room_bp)

    @app.route("/")
    def home():
        return {"message": "Hotel Management API is running"}

    with app.app_context():
        db.create_all()

    return app