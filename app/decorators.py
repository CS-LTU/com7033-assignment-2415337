# app/decorators.py

from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user


def admin_required(f):
    """Allow only users with role == 'admin'."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Not logged in: send to login page
        if not current_user.is_authenticated:
            flash("Please log in first.", "warning")
            return redirect(url_for("auth.login"))

        # Logged in but not admin
        if getattr(current_user, "role", None) != "admin":
            flash("You do not have permission to perform this action.", "danger")
            return redirect(url_for("patients.list_patients"))

        # OK: user is admin
        return f(*args, **kwargs)

    return wrapper
