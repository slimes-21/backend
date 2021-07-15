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
    date_legend = {"Mon": 1, "Tue": 2, "Wed": 3, "Thu": 4, "Fri": 5}
    time_legend = {"8:00": 1, "8:30": 2, "9:00": 3, "9:30": 4, "10:00": 5, "10:30": 6, "11:00": 7, "11:30": 8,
                   "12:00": 9, "12:30": 10, "13:00": 11, "13:30": 12, "14:00": 13, "14:30": 14, "15:00": 15,
                   "15:30": 16, "16:00": 17, "16:30": 18, "17:00": 19, "17:30": 20, "18:00": 21, "18:30": 22,
                   "19:00": 23, "19:30": 24, "20:00": 25, "20:30": 26}
    time_rev_legend = dict((v, k) for k, v in time_legend.items())
    table = []
    for i in range(1, 27):
        row = []
        if i % 2 != 0:
            row.append(f"<td id=\"c1\">{time_rev_legend[i]}</td>")
        else:
            row.append("<td></td>")
        row += ["<td></td>"] * 5
        table.append(row)
    timetable = current_user.get_timetable()
    checked_friends = []
    if timetable is not None:
        friends_timetable = []
        friends = request.args.get("friends")
        if friends is not None:
            for friend in friends.split(","):
                friend_user = User.query.filter_by(username=friend).first()
                if friend_user:
                    friends_timetable.append((friend_user, friend_user.get_timetable()))
                    checked_friends.append(friend_user.username)
        for subject in timetable.subjects:
            row_index = time_legend[subject.time] - 1
            col_index = date_legend[subject.day]
            duration = int(float(subject.duration.split(" ")[0]) * 2)
            same_friends = []
            for friend_user, friend_timetable in friends_timetable:
                for friend_subject in friend_timetable.subjects:
                    if friend_subject == subject:
                        same_friends.append(friend_user.get_full_name())
                        break
            for i in range(row_index, row_index + duration):
                if same_friends:
                    table[i][
                        col_index] = f"<td><div class=\"haveclass\"><div class=\"friendhaveclasstoo\" friends=\"{','.join(same_friends)}\">{subject.get_neat_code()}</div></div></td>"
                else:
                    table[i][col_index] = f"<td><div class=\"haveclass\">{subject.get_neat_code()}</div></td>"
    return render_template('home.html', table=table, checked_friends=checked_friends)


@app.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user == current_user:
        return redirect(url_for('self_profile'))
    return render_template('otherprofile.html', user=user)


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
        output_csv = input_excel.to_csv(sep="!")
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
