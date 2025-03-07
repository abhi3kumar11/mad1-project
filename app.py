from flask import Flask, render_template, redirect, url_for, flash, request
from models import db, User, bcrypt,Subject
from forms import RegistrationForm, LoginForm,SubjectForm
from flask_login import login_user, logout_user, login_required

app = Flask(__name__)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(email=form.email.data, password=hashed_password, full_name="User Name")
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully!", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            flash("Login unsuccessful. Check email and password.", "danger")
    return render_template("login.html", form=form)

from flask_login import current_user, login_required

@app.route("/admin/dashboard")
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return redirect(url_for("dashboard"))
    return render_template("admin/dashboard.html")

@app.route("/admin/subjects", methods=["GET", "POST"])
@login_required
def manage_subjects():
    if not current_user.is_admin:
        return redirect(url_for("dashboard"))
    
    form = SubjectForm()
    if form.validate_on_submit():
        new_subject = Subject(name=form.name.data)
        db.session.add(new_subject)
        db.session.commit()
        flash("Subject added successfully!", "success")
        return redirect(url_for("manage_subjects"))
    
    subjects = Subject.query.all()
    return render_template("admin/subjects.html", subjects=subjects, form=form)

@app.route("/admin/subjects/delete/<int:subject_id>")
@login_required
def delete_subject(subject_id):
    if not current_user.is_admin:
        return redirect(url_for("dashboard"))
    
    subject = Subject.query.get_or_404(subject_id)
    db.session.delete(subject)
    db.session.commit()
    flash("Subject deleted successfully!", "danger")
    return redirect(url_for("manage_subjects"))
