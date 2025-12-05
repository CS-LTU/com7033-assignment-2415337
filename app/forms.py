from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    IntegerField,
    FloatField,
    SelectField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    NumberRange,
    Optional,
)


# ---------------- AUTH FORMS ---------------- #

class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=64)],
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6)],
    )


class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=64)],
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(), Length(max=120)],
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6)],
    )


# ---------------- PATIENT FORM ---------------- #

class PatientForm(FlaskForm):

    patient_id = IntegerField(
        "Patient ID",
        validators=[DataRequired()],
    )

    gender = SelectField(
        "Gender",
        choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],
        validators=[DataRequired()],
    )

    age = FloatField(
        "Age",
        validators=[DataRequired(), NumberRange(min=0, max=130)],
    )

    hypertension = SelectField(
        "Hypertension",
        choices=[(0, "No"), (1, "Yes")],
        coerce=int,
        validators=[NumberRange(min=0, max=1)],
    )

    heart_disease = SelectField(
        "Heart Disease",
        choices=[(0, "No"), (1, "Yes")],
        coerce=int,
        validators=[NumberRange(min=0, max=1)],
    )

    ever_married = SelectField(
        "Ever Married",
        choices=[("Yes", "Yes"), ("No", "No")],
        validators=[DataRequired()],
    )

    work_type = StringField(
        "Work Type",
        validators=[DataRequired(), Length(max=50)],
    )

    residence_type = SelectField(
        "Residence Type",
        choices=[("Urban", "Urban"), ("Rural", "Rural")],
        validators=[DataRequired()],
    )

    avg_glucose_level = FloatField(
        "Average Glucose Level",
        validators=[DataRequired(), NumberRange(min=0)],
    )

    bmi = FloatField(
        "BMI",
        validators=[Optional()],
    )

    smoking_status = StringField(
        "Smoking Status",
        validators=[Optional(), Length(max=50)],
    )

    stroke = SelectField(
        "Stroke",
        choices=[(0, "No"), (1, "Yes")],
        coerce=int,
        validators=[NumberRange(min=0, max=1)],
    )
