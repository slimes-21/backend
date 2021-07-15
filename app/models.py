from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from app.entities.timetable import Timetable
from sqlalchemy import or_, and_


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(64), index=True, nullable=False)
    last_name = db.Column(db.String(64), index=True, nullable=False)
    bio = db.Column(db.String(255), nullable=True, default=None)
    timetable = db.Column(db.TEXT, nullable=True, default=None)
    password_hash = db.Column(db.String(128))

    def get_timetable(self):
        if self.timetable is None:
            return None
        return Timetable(self.timetable)

    def request_user(self, user):
        friendship = Friendship(sender_id=self.id, receiver_id=user.id)
        db.session.add(friendship)
        db.session.commit()
        return friendship

    def accept_request(self, user):
        friendship = Friendship.query.filter(
            and_(Friendship.sender_id == user.id, Friendship.receiver_id == self.id)).one()
        friendship.status = True
        db.session.commit()
        return friendship

    def get_friends(self):
        return Friendship.query.filter(
            or_(Friendship.sender_id == self.id, Friendship.receiver_id == self.id)).filter_by(
            status=True).all()

    def reject_request(self, user):
        self.unfriend_user(user)

    def get_pending_requests(self):
        return Friendship.query.filter_by(receiver_id=self.id).filter_by(status=False).all()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_formatted_name(self):
        return f"{self.first_name} {self.last_name[0]}"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.get_full_name()} ({self.email})>"


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Friendship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, index=True, nullable=False)
    receiver_id = db.Column(db.Integer, index=True, nullable=False)
    status = db.Column(db.Boolean, default=False)

    def get_sender(self):
        return User.query.get(self.sender_id)

    def get_receiver(self):
        return User.query.get(self.receiver_id)

    def __repr__(self):
        return f'<Friendship ({self.sender_id}, {self.receiver_id})>'
