from flask import Blueprint, jsonify
from flask_login import login_required
from sqlalchemy import func, cast, Numeric, Float

from app import db
from app.models import User, Achievement, Category

rating = Blueprint('rating', __name__)


@rating.route('/return_best_rated_user_for_category/<int:cid>')
@login_required
def return_best_rated_user_for_category(cid):
    subquery = db.session.query(
        User.uid,
        User.login,
        func.avg(Achievement.rating).label('average_rating')
    ).join(Achievement, User.uid == Achievement.uid) \
        .join(Category, Achievement.cid == Category.cid) \
        .filter(Achievement.status == 'APPROVED', Category.cid == cid) \
        .group_by(User.uid, User.login).subquery()

    top_users = db.session.query(
        subquery.c.uid,
        subquery.c.login,
        subquery.c.average_rating
    ).order_by(subquery.c.average_rating.desc()).limit(3).all()

    return jsonify([{'uid': user.uid, 'login': user.login, 'average_rating': round(user.average_rating, 2)} for user in top_users])