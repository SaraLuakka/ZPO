from flask_login import UserMixin
from . import db

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class User(UserMixin, db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(300))
    role = db.Column(db.String(100))

    # Foreign keys
    achievements = relationship('Achievement', back_populates='user')
    tasks = relationship('Task', back_populates='user')

    def get_id(self):
        return str(self.uid)

class Category(db.Model):
    cid = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), unique=True, nullable=False)

    # Foreign keys
    achievements = relationship('Achievement', back_populates='category')
    tasks = relationship('Task', back_populates='category')

class Hashtags(db.Model):
    hid = db.Column(db.Integer, primary_key=True)
    hashtag_name = db.Column(db.String(100), unique=True, nullable=False)

    # Foreign keys
    achievements = relationship('Achievement', back_populates='hashtags')

class Achievement(db.Model):
    aid = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer, ForeignKey('category.cid'))
    title = db.Column(db.String(100))
    description = db.Column(db.String(400))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    hid = db.Column(db.Integer, ForeignKey('hashtags.hid'))
    rating = db.Column(db.Float)
    uid = db.Column(db.Integer, ForeignKey('user.uid'))
    status = db.Column(db.String(100))

    # Foreign keys
    category = relationship('Category', back_populates='achievements')
    hashtags = relationship('Hashtags', back_populates='achievements')
    user = relationship('User', back_populates='achievements')

class Task(db.Model):
    tid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(400))
    cid = db.Column(db.Integer, ForeignKey('category.cid'))
    uid = db.Column(db.Integer, ForeignKey('user.uid'))

    # Foreign keys
    category = relationship('Category', back_populates='tasks')
    user = relationship('User', back_populates='tasks')