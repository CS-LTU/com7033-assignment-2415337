import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///app.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MONGO_URI = os.environ.get(
        "MONGO_URI",
        "mongodb://localhost:27017/patient_app"
    )

    # CSRF should be enabled in production / for your assignment
    WTF_CSRF_ENABLED = True
