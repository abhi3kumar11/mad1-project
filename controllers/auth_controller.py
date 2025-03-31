from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from .forms import LoginForm, RegistrationForm, ForgotPasswordForm, ResetPasswordForm
from .models import db, User
from datetime import datetime
import secrets

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        if session.get('is_admin'):
            return redirect(url_for('admin.admin_dashboard'))
        return redirect(url_for('quiz.user_dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            if not user.is_admin:  # Only allow non-admin users
                session['user_id'] = user.id
                session['username'] = user.username
                session['is_admin'] = False
                flash('Logged in successfully!', 'success')
                return redirect(url_for('quiz.user_dashboard'))
            else:
                flash('Please use admin login for administrator access.', 'danger')
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if session.get('user_id') and session.get('is_admin'):
        return redirect(url_for('admin.admin_dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            if user.is_admin:  # Only allow admin users
                session['user_id'] = user.id
                session['username'] = user.username
                session['is_admin'] = True
                flash('Logged in as administrator!', 'success')
                return redirect(url_for('admin.admin_dashboard'))
            else:
                flash('Access denied. Admin privileges required.', 'danger')
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('auth/admin_login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('user_id'):
        if session.get('is_admin'):
            return redirect(url_for('admin.admin_dashboard'))
        return redirect(url_for('quiz.user_dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered.', 'danger')
            return render_template('auth/register.html', form=form)
        
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already taken.', 'danger')
            return render_template('auth/register.html', form=form)
        
        user = User(
            username=form.username.data,
            email=form.email.data,
            full_name=form.full_name.data,
            qualification=form.qualification.data,
            dob=form.dob.data,
            is_admin=False  # Ensure new registrations are not admin
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # In a real application, you would send an email with a reset link
            # For this demo, we'll just show a message
            flash('If that email exists in our system, a password reset link has been sent.', 'info')
        else:
            # Don't reveal if the email exists or not (security best practice)
            flash('If that email exists in our system, a password reset link has been sent.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/forgot_password.html', form=form)

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))
