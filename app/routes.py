from app import app, db
from flask import request, redirect, url_for, render_template, send_from_directory, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'GET':
        return render_template('sign_up.html')

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if first_name == '' or last_name == '' or email == '' or password == '' or confirm_password == '':
        return render_template('sign_up.html', error='Missing required fields')

    if password != confirm_password:
        return render_template('sign_up.html', error="Confirm password and password must match")

    existing_user = User.query.filter_by(email=email).first()
    if existing_user is not None:
        return render_template('sign_up.html', error="Email is already in use")

    user = User(first_name=first_name, last_name=last_name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'GET':
        return render_template('sign_in.html')

    email = request.form['email']
    password = request.form['password']

    if email == '' or password == '':
        return render_template('sign_in.html', error='Please enter both a email and a password')

    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        return render_template('sign_in.html', error='Invalid email or password')

    login_user(user)
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/home')
@login_required
def home():
    return render_template('home.html')


# @app.errorhandler(404)
# def not_found_error(error):
#     return render_template('404.html'), 404
#
#
# @app.errorhandler(500)
# def internal_error(error):
#     return render_template('500.html'), 500