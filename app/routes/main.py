from flask import Blueprint, render_template
from flask_login import login_required
from app import mongo

# Blueprint name MUST be "main" so endpoints are "main.index", "main.dashboard"
main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    # Home page
    return render_template("index.html")


@main_bp.route("/dashboard")
@login_required
def dashboard():
    """
    Analytics dashboard at URL: /dashboard
    Endpoint: main.dashboard
    """
    try:
        coll = mongo.db.patients
        total = coll.count_documents({})
        stroke_yes = coll.count_documents({"stroke": 1})
        stroke_no = coll.count_documents({"stroke": 0})

        genders = ["Male", "Female", "Other"]
        gender_counts = [coll.count_documents({"gender": g}) for g in genders]
    except Exception:
        total = stroke_yes = stroke_no = 0
        genders = []
        gender_counts = []

    return render_template(
        "dashboard.html",
        total=total,
        stroke_yes=stroke_yes,
        stroke_no=stroke_no,
        genders=genders,
        gender_counts=gender_counts,
    )
