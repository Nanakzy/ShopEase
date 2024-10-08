from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config


db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    from app.routes.main_routes import main_routes
    from app.routes.user import user_routes
    from app.routes.checkout import checkout_routes

    app.register_blueprint(main_routes)
    app.register_blueprint(user_routes)
    app.register_blueprint(checkout_routes)

    return app
