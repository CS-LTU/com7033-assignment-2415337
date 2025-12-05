from flask import render_template
from flask_login import login_required
from app import create_app, mongo   # <- mongo comes from app/__init__.py

app = create_app()


# ---------- DASHBOARD ROUTE ----------
@app.route("/dashboard")
@login_required
def dashboard():
    """
    Analytics dashboard at /dashboard.
    Uses MongoDB 'patients' collection.
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
# -------------------------------------


if __name__ == "__main__":
    app.run(debug=True)
