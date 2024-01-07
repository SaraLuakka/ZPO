from functools import wraps

from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, db
from app.helpers import *

auth = Blueprint('auth', __name__)

# https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login

def admin_required(f):
   @wraps(f)
   def decorated_function(*args, **kwargs):
       if not current_user.is_authenticated or current_user.role != 'admin':
           abort(403)
       return f(*args, **kwargs)
   return decorated_function

@auth.route('/login')
def login():
    return render_template("login.html")

@auth.route('/login', methods=['POST'])
def login_post():
    login = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(login=login).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password):
        flash_bootstrap_danger('Błędne dane logowania')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user)
    return redirect(url_for('main.restricted'))


@auth.route('/signup')
def signup():
    return render_template("signup.html")

@auth.route('/signup', methods=['POST'])
def signup_post():

    login = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(login=login).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash_bootstrap_danger('Taki użytkownik już istnieje')
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    try:
        new_user = User(login=login, role="user", password=generate_password_hash(password, method='pbkdf2:sha256'))

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        flash_bootstrap_danger(e)
        return redirect(url_for('auth.signup'))

    flash_bootstrap_success("Dodano użytkownika pomyślnie")
    return redirect(url_for('main.home'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))