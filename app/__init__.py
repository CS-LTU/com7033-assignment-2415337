from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pymongo import PyMongo
from flask_wtf.csrf import CSRFProtect
from config import Config

# ---- global extension objects (NO imports from app here) ----
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
mongo = PyMongo()
csrf = CSRFProtect()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # init extensions
    db.init_app(app)
    login_manager.init_app(app)
    mongo.init_app(app)
    csrf.init_app(app)

    # register blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.patients import patients_bp

    app.register_blueprint(main_bp)                     # "/" and "/dashboard"
    app.register_blueprint(auth_bp, url_prefix="/auth") # "/auth/..."
    app.register_blueprint(patients_bp, url_prefix="/patients")

    with app.app_context():
        from app import models
        db.create_all()

    return app
