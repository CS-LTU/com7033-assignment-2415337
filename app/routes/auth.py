from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.models import User
from app import db
from app.forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash
from flask_login import current_user, login_required
from app.decorators import admin_required
from sqlalchemy.exc import IntegrityError



auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Logged in successfully.", "success")
            return redirect(url_for("main.index"))
        else:
            flash("Invalid username or password", "danger")
    elif form.is_submitted():
        # form submitted but failed validation: show errors
        flash(f"Login form errors: {form.errors}", "danger")

    return render_template("auth/login.html", form=form)




@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_users = User.query.count()
        role = "admin" if existing_users == 0 else "staff"

        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            role=role,
        )
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Username or email already exists. Please use a different one.", "danger")
            return render_template("auth/register.html", form=form)

        flash(f"Registration successful. Assigned role: {role}. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)

@auth_bp.route("/users")
@login_required
@admin_required
def list_users():
    """Admin-only page: list all users and their roles."""
    users = User.query.order_by(User.id.asc()).all()
    return render_template("auth/users.html", users=users)


@auth_bp.route("/users/<int:user_id>/make-admin", methods=["POST"])
@login_required
@admin_required
def make_admin(user_id):
    user = User.query.get_or_404(user_id)
    if user.role != "admin":
        user.role = "admin"
        db.session.commit()
        flash(f"User {user.username} promoted to ADMIN.", "success")
    else:
        flash(f"User {user.username} is already admin.", "info")
    return redirect(url_for("auth.list_users"))


@auth_bp.route("/users/<int:user_id>/make-staff", methods=["POST"])
@login_required
@admin_required
def make_staff(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("You cannot downgrade your own account.", "warning")
        return redirect(url_for("auth.list_users"))

    if user.role != "staff":
        user.role = "staff"
        db.session.commit()
        flash(f"User {user.username} set to STAFF.", "success")
    else:
        flash(f"User {user.username} is already staff.", "info")
    return redirect(url_for("auth.list_users"))




@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.", "info")
    return redirect(url_for("main.index"))
