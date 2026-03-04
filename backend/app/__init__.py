from flask import Flask
from .config import Config
from .extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = "hotel_management_secret_key"
    db.init_app(app)

    # Register blueprints
    from .routes.room_routes import room_bp
    from .routes.customer_routes import customer_bp
    from .routes.booking_routes import booking_bp
    from .routes.user_routes import user_bp
    from .routes.invoice_routes import invoice_bp

    app.register_blueprint(room_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(invoice_bp)


    # Import models BEFORE create_all
    from .models.room import Room
    from .models.customer import Customer
    from .models.booking import Booking
    from .models.user import User
    from .models.invoice import Invoice

    @app.route("/")
    def home():
        return {"message": "Hotel Management API is running"}

    with app.app_context():
        db.create_all()

    return app