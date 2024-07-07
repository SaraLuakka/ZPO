from datetime import datetime

from flask_login import UserMixin
from . import db

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


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
    to_fix_comment = db.Column(db.String(200)) # Poprawka 2

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

class Chat(db.Model):
    entry_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ccid = db.Column(db.Integer, ForeignKey('chat_category.ccid'), nullable=False)
    uid = db.Column(db.Integer, ForeignKey('user.uid'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    category = relationship('ChatCategory', backref='chats')
    user = relationship('User', backref='messages')

class ChatCategory(db.Model):
    __tablename__ = 'chat_category'
    ccid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chat_category_name = db.Column(db.String(100), nullable=False, unique=True)

class ChatWithAdmin(db.Model):
    __tablename__ = 'chat_with_admin'
    entry_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic_uid = db.Column(db.Integer, ForeignKey('user.uid'), nullable=False)
    uid = db.Column(db.Integer, ForeignKey('user.uid'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=func.now())