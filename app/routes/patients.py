from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    current_app,
    request,
)
from flask_login import login_required
from app import mongo
from bson.objectid import ObjectId
from app.forms import PatientForm
from pymongo.errors import ServerSelectionTimeoutError
import csv
import os
from app.decorators import admin_required


patients_bp = Blueprint("patients", __name__, url_prefix="/patients")


# ---------- LIST + SEARCH ----------
@patients_bp.route("/")
@login_required
def list_patients():
    """
    List patients, with optional search (?q=) and pagination (?page=)
    """
    dummy_patients = [
        {"_id": 1, "patient_id": 1001, "gender": "Male", "age": 45, "stroke": 0},
        {"_id": 2, "patient_id": 1002, "gender": "Female", "age": 60, "stroke": 1},
    ]

    q = request.args.get("q", "").strip()
    page = request.args.get("page", 1, type=int)
    per_page = 50  # patients per page

    query = {}
    if q:
        try:
            num = int(q)
            query["patient_id"] = num
        except ValueError:
            query["$or"] = [
                {"gender": {"$regex": q, "$options": "i"}},
                {"smoking_status": {"$regex": q, "$options": "i"}},
                {"work_type": {"$regex": q, "$options": "i"}},
            ]

    try:
        total = mongo.db.patients.count_documents(query)
        cursor = (
            mongo.db.patients.find(query)
            .skip((page - 1) * per_page)
            .limit(per_page)
        )
        patients = list(cursor)

        if total == 0 and not q:
            flash("MongoDB is connected but no patients are stored yet.", "info")
            patients = dummy_patients
            total = len(dummy_patients)
            per_page = len(dummy_patients)
            page = 1

    except ServerSelectionTimeoutError:
        flash("Could not connect to MongoDB. Showing dummy data instead.", "warning")
        patients = dummy_patients
        total = len(dummy_patients)
        per_page = len(dummy_patients)
        page = 1

    total_pages = max((total + per_page - 1) // per_page, 1)

    return render_template(
        "patients/list.html",
        patients=patients,
        count=total,
        q=q,
        page=page,
        total_pages=total_pages,
    )

# ---------- CREATE ----------
@patients_bp.route("/create", methods=["GET", "POST"])
@login_required
@admin_required
def create_patient():
    form = PatientForm()

    if form.validate_on_submit():
        data = {
            "patient_id": form.patient_id.data,
            "gender": form.gender.data,
            "age": form.age.data,
            "hypertension": form.hypertension.data,
            "heart_disease": form.heart_disease.data,
            "ever_married": form.ever_married.data,
            "work_type": form.work_type.data,
            "residence_type": form.residence_type.data,
            "avg_glucose_level": form.avg_glucose_level.data,
            "bmi": form.bmi.data,
            "smoking_status": form.smoking_status.data,
            "stroke": form.stroke.data,
        }
        mongo.db.patients.insert_one(data)
        flash("Patient created successfully.", "success")
        return redirect(url_for("patients.list_patients"))

    if form.is_submitted():
        flash(f"Form errors: {form.errors}", "danger")

    return render_template("patients/form.html", form=form,title="Add New Patient",submit_label="Create Patient",
    )


# ---------- READ / DETAIL ----------
@patients_bp.route("/detail/<patient_id>")
@login_required
def patient_detail(patient_id):
    try:
        patient = mongo.db.patients.find_one({"_id": ObjectId(patient_id)})
    except Exception:
        patient = None

    if not patient:
        flash("Patient not found (or MongoDB not available).", "warning")
        return redirect(url_for("patients.list_patients"))

    return render_template("patients/form.html",form=form,title="Edit Patient",submit_label="Save Changes",
    )


# ---------- UPDATE ----------
@patients_bp.route("/edit/<patient_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_patient(patient_id):
    try:
        patient = mongo.db.patients.find_one({"_id": ObjectId(patient_id)})
    except Exception:
        patient = None

    if not patient:
        flash("Patient not found.", "warning")
        return redirect(url_for("patients.list_patients"))

    form = PatientForm(obj=patient)

    # Pre-populate WTForms fields on GET
    if request.method == "GET":
        form.patient_id.data = patient.get("patient_id")
        form.gender.data = patient.get("gender")
        form.age.data = float(patient.get("age", 0))
        form.hypertension.data = int(patient.get("hypertension", 0))
        form.heart_disease.data = int(patient.get("heart_disease", 0))
        form.ever_married.data = patient.get("ever_married")
        form.work_type.data = patient.get("work_type")
        form.residence_type.data = patient.get("residence_type")
        form.avg_glucose_level.data = float(patient.get("avg_glucose_level", 0))
        form.bmi.data = patient.get("bmi")
        form.smoking_status.data = patient.get("smoking_status")
        form.stroke.data = int(patient.get("stroke", 0))

    if form.validate_on_submit():
        update = {
            "patient_id": form.patient_id.data,
            "gender": form.gender.data,
            "age": form.age.data,
            "hypertension": form.hypertension.data,
            "heart_disease": form.heart_disease.data,
            "ever_married": form.ever_married.data,
            "work_type": form.work_type.data,
            "residence_type": form.residence_type.data,
            "avg_glucose_level": form.avg_glucose_level.data,
            "bmi": form.bmi.data,
            "smoking_status": form.smoking_status.data,
            "stroke": form.stroke.data,
        }
        mongo.db.patients.update_one({"_id": patient["_id"]}, {"$set": update})
        flash("Patient updated successfully.", "success")
        return redirect(url_for("patients.patient_detail", patient_id=patient_id))

    if form.is_submitted():
        flash(f"Form errors: {form.errors}", "danger")

    return render_template("patients/form.html", form=form, mode="edit")


# ---------- DELETE ----------
@patients_bp.route("/delete/<patient_id>", methods=["POST"])
@login_required
@admin_required
def delete_patient(patient_id):
    try:
        mongo.db.patients.delete_one({"_id": ObjectId(patient_id)})
        flash("Patient deleted.", "info")
    except Exception:
        flash("Could not delete patient.", "danger")
    return redirect(url_for("patients.list_patients"))

@patients_bp.route("/dashboard")
@login_required
def dashboard():
    try:
        coll = mongo.db.patients

        # basic counts
        total = coll.count_documents({})
        stroke_yes = coll.count_documents({"stroke": 1})
        stroke_no = coll.count_documents({"stroke": 0})

        # stroke rate %
        if total > 0:
            stroke_rate = round((stroke_yes / total) * 100, 1)
        else:
            stroke_rate = 0.0

        # gender counts
        genders = ["Male", "Female", "Other"]
        gender_counts = [coll.count_documents({"gender": g}) for g in genders]

        # ---- if you already have these, keep your versions ----
        # averages
        avg_age = avg_glucose = avg_bmi = None
        pipeline = [
            {"$group": {
                "_id": None,
                "avg_age": {"$avg": "$age"},
                "avg_glucose": {"$avg": "$avg_glucose_level"},
                "avg_bmi": {"$avg": "$bmi"},
            }}
        ]
        agg = list(coll.aggregate(pipeline))
        if agg:
            avg_age = round(agg[0].get("avg_age", 0), 1)
            avg_glucose = round(agg[0].get("avg_glucose", 0), 1)
            avg_bmi = round(agg[0].get("avg_bmi", 0), 1)

        # age bands + high-risk etc...
        age_bands = ["0–20", "21–40", "41–60", "61–80", "81+"]
        age_band_counts = [
            coll.count_documents({"age": {"$gte": 0,  "$lte": 20}}),
            coll.count_documents({"age": {"$gt": 20, "$lte": 40}}),
            coll.count_documents({"age": {"$gt": 40, "$lte": 60}}),
            coll.count_documents({"age": {"$gt": 60, "$lte": 80}}),
            coll.count_documents({"age": {"$gt": 80}}),
        ]

        high_risk = list(
            coll.find({"stroke": 1})
                .sort([("avg_glucose_level", -1)])
                .limit(10)
        )

    except Exception:
        total = stroke_yes = stroke_no = 0
        stroke_rate = 0.0
        genders = []
        gender_counts = []
        avg_age = avg_glucose = avg_bmi = None
        age_bands = []
        age_band_counts = []
        high_risk = []

    return render_template(
        "dashboard.html",
        total=total,
        stroke_yes=stroke_yes,
        stroke_no=stroke_no,
        stroke_rate=stroke_rate,          # <-- important
        genders=genders,
        gender_counts=gender_counts,
        avg_age=avg_age,
        avg_glucose=avg_glucose,
        avg_bmi=avg_bmi,
        age_bands=age_bands,
        age_band_counts=age_band_counts,
        high_risk=high_risk,
    )


# ---------- IMPORT FROM CSV ----------
@patients_bp.route("/import")
@login_required
@admin_required
def import_patients():
    csv_path = os.path.join(current_app.root_path, "healthcare-dataset-stroke-data.csv")
    csv_path = os.path.abspath(csv_path)

    if not os.path.exists(csv_path):
        flash(f"CSV file not found at: {csv_path}", "danger")
        return redirect(url_for("patients.list_patients"))

    try:
        mongo.db.patients.delete_many({})
    except ServerSelectionTimeoutError:
        flash("Could not connect to MongoDB to import data.", "danger")
        return redirect(url_for("patients.list_patients"))

    inserted = 0
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                doc = {
                    "patient_id": int(row["id"]),
                    "gender": row["gender"],
                    "age": float(row["age"]),
                    "hypertension": int(row["hypertension"]),
                    "heart_disease": int(row["heart_disease"]),
                    "ever_married": row["ever_married"],
                    "work_type": row["work_type"],
                    "residence_type": row["Residence_type"],
                    "avg_glucose_level": float(row["avg_glucose_level"]),
                    "bmi": float(row["bmi"]) if row["bmi"] not in ("", "N/A") else None,
                    "smoking_status": row["smoking_status"],
                    "stroke": int(row["stroke"]),
                }
                mongo.db.patients.insert_one(doc)
                inserted += 1
            except Exception as e:
                print("Error importing row:", row, e)

    flash(f"Imported {inserted} patients into MongoDB.", "success")
    return redirect(url_for("patients.list_patients"))


# ---------- DEBUG COUNT ----------
@patients_bp.route("/debug-count")
@login_required
def debug_count():
    try:
        count = mongo.db.patients.count_documents({})
        flash(f"There are {count} patients in MongoDB.", "info")
    except ServerSelectionTimeoutError:
        flash("MongoDB is not available (cannot count patients).", "danger")
    return redirect(url_for("patients.list_patients"))
