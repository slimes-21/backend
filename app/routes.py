import os
from app import app, db
from flask import request, redirect, url_for, render_template
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
import pandas as pd


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
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if first_name == '' or last_name == '' or username == '' or password == '' or confirm_password == '':
        return render_template('sign_up.html', error='Missing required fields')

    if password != confirm_password:
        return render_template('sign_up.html', error="Confirm password and password must match")

    existing_user = User.query.filter_by(username=username).first()
    if existing_user is not None:
        return render_template('sign_up.html', error="Username is already in use")

    user = User(first_name=first_name, last_name=last_name, username=username)
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

    username = request.form['username']
    password = request.form['password']

    if username == '' or password == '':
        return render_template('sign_in.html', error='Please enter both a email and a password')

    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return render_template('sign_in.html', error='Invalid username or password')

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


@app.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user == current_user:
        return redirect(url_for('self_profile'))
    return render_template('other_profile.html', user=user)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def self_profile():
    if request.method == 'GET':
        return render_template('profile.html', friend_requests=current_user.get_pending_requests())
    bio = request.form['bio']

    timetable = request.files.get('timetable', None)
    if timetable:
        _, file_ext = os.path.splitext(timetable.filename)
        if file_ext not in ['.xls']:
            return render_template('profile.html', error='Please upload a valid xls file',
                                   friend_requests=current_user.get_pending_requests())
        input_excel = pd.read_excel(timetable.read(), dtype=str)
        output_csv = input_excel.to_csv()
        current_user.timetable = output_csv

    current_user.bio = bio
    db.session.commit()
    return redirect(url_for('self_profile'))


@app.route('/request/<username>')
@login_required
def request_friend(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user == current_user:
        return redirect(url_for('self_profile'))
    current_user.request_user(user)
    return redirect(url_for('self_profile'))


@app.route('/accept/<username>')
@login_required
def accept_friend(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user == current_user:
        return redirect(url_for('self_profile'))
    current_user.accept_request(user)
    return redirect(url_for('self_profile'))


@app.route('/reject/<username>')
@login_required
def reject_friend(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user == current_user:
        return redirect(url_for('self_profile'))
    current_user.reject_request(user)
    return redirect(url_for('self_profile'))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
