"""
Authentication routes — login, register, logout.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from app import db
from app.models.user import User
from app.utils.validators import validate_username, validate_email, validate_password

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            flash('Welcome back, operator.', 'success')
            return redirect(next_page or url_for('dashboard.index'))
        else:
            flash('Invalid credentials. Access denied.', 'error')

    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Validate inputs
        valid, msg = validate_username(username)
        if not valid:
            flash(msg, 'error')
            return render_template('login.html', register=True)

        valid, msg = validate_email(email)
        if not valid:
            flash(msg, 'error')
            return render_template('login.html', register=True)

        valid, msg = validate_password(password)
        if not valid:
            flash(msg, 'error')
            return render_template('login.html', register=True)

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('login.html', register=True)

        # Check uniqueness
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return render_template('login.html', register=True)

        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return render_template('login.html', register=True)

        # Create user
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash('Account created. Welcome to OTMindset.', 'success')
        return redirect(url_for('dashboard.index'))

    return render_template('login.html', register=True)


@auth_bp.route('/logout')
@login_required
def logout():
    """Handle user logout."""
    logout_user()
    flash('Session terminated.', 'info')
    return redirect(url_for('auth.login'))
