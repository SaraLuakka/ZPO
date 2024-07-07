from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint('main', __name__)


@bp.route('/')
def home():
    return render_template("home.html")

@bp.route('/restricted')
@login_required
def restricted():
    return render_template("home.html")