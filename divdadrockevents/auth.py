from flask import Blueprint, flash, render_template, request, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from .forms import LoginForm, RegisterForm
from . import db

# Create a blueprint - make sure all BPs have unique names
auth_bp = Blueprint('auth', __name__)

# login function
@auth_bp.route('/login', methods=['GET', 'POST'])
# view function
def login():
    login_form = LoginForm()
    error = None
    if login_form.validate_on_submit():
        user_email = login_form.email.data
        password = login_form.password.data
        user = db.session.scalar(db.select(User).where(User.email == user_email))
        if user is None or not check_password_hash(user.password, password): # takes the hash and cleartext password:
            error = 'Incorrect email address or password'
        if error is None:
            login_user(user)
            nextp = request.args.get('next')
            if not nextp or not nextp.startswith('/'):
                return redirect(url_for('main.index'))
            return redirect(nextp)
        else:
            flash(error)
    return render_template('user.html', form=login_form, heading='Login')                         

# Register new user account                   
@auth_bp.route('/register', methods=['GET', 'POST']) 
def register():
    form = RegisterForm()
    error = None
    if form.validate_on_submit():
        fname = form.firstname.data
        lname = form.lastname.data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        phonenumber = form.phonenumber.data
        streetaddress = form.streetaddress.data
        existing = db.session.scalar(db.select(User).where((User.username == username) | (User.email == email)))
        if existing:
            error = 'Username or email already taken'
        if error is None:
            hashed = generate_password_hash(password)
            user = User(fullname= f"{fname} {lname}", username=username, email=email, password=hashed, phone=phonenumber, streetaddress=streetaddress)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful. Please log in.')
            return redirect(url_for('auth.login'))
        else:
            flash(error)
    return render_template('user.html', form=form, heading='Register')

# Log out function. Redirects to the homepage
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))  