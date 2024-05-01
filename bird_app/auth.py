from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User

auth = Blueprint('auth', __name__)


# route to display login page
@auth.route('/login')
def login():
    return render_template('login.html')


# route to handle logging in
@auth.route('/login', methods=["POST"])
def login_post():
    # get form data
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # query for existing user by email, return first instance
    user = User.query.filter_by(email=email).first()

    # handle bad input
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    # log in user, redirect to the user page
    login_user(user, remember=remember)
    return redirect(url_for('main.user'))


# route to handle logging user out
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
